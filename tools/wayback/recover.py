"""Recover old blog posts that are missing from the WordPress export, from the Internet Archive.

    tools\\.venv\\Scripts\\python.exe -I tools\\wayback\\recover.py --paths tools\\wayback\\paths.txt ^
        --cache "D:\\WebBackup\\samarthya.me-migration-2026-10\\import\\wayback" ^
        --zip "D:\\WebBackup\\samarthya.me-migration-2026-10\\raw-exports\\content-uploads.zip" ^
        --images "D:\\WebBackup\\samarthya.me-migration-2026-10\\import\\wp-uploads" --out content/posts

paths.txt lists old addresses, one per line (/wps/YYYY/MM/DD/slug/). For each one the newest archived copy is
downloaded once into --cache (re-runs read the cache), the post body is cut out of the page, and it goes
through the same converter as the WordPress import (wp2hugo.py): shortcodes, image lookup, links, secret
redaction, pseudonym rules, overrides.yaml and media/. Images come from the uploads archive first and from
the Internet Archive otherwise. A report lists what each post got and what's missing.
"""
import argparse
import json
import re
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path
from urllib.parse import quote, unquote

from bs4 import BeautifulSoup

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "wp2hugo"))
import wp2hugo as w  # noqa: E402

WAYBACK = "https://web.archive.org"
HOST = "blog.samarthya.me"
UA = {"User-Agent": "samarthya.me post recovery (owner); contact via https://samarthya.me/contact/"}
# Parts of the old theme around the post body (the body itself sits directly in #page).
CHROME = {"header", "footer", "script", "style", "noscript", "nav", "aside"}
CHROME_CLASS = re.compile(r"skip-link|preloader|mobile-menu|comments|post-navigation|related|sharedaddy|widget")
# Topic tags for data/covers.yaml, picked from words in the title and text.
TAG_WORDS = {
    "ai": r"\b(?:AI|artificial intelligence|GenAI|generative|speech[- ]to[- ]text|speech recognition)\b", "llm": r"\b(?:LLMs?|language models?)\b",
    "ml": r"\b(?:machine learning|ML|model selection|k-nearest|KNN|TF-IDF|classifier)\b",
    "langchain": r"\bLangChain\b", "ollama": r"\bOllama\b", "rag": r"\b(?:RAG|retrieval[- ]augmented)\b",
    "python": r"\bPython\b", "spark": r"\b(?:Spark|PySpark)\b", "pandas": r"\bpandas\b",
    "data-analytics": r"\b(?:analytics|forecast\w*|regression|correlation|covariance|segmentation|Monte Carlo|linear programming)\b",
    "data": r"\b(?:data mining|dataframe|Parquet|Arrow|dataset)\b", "gpu": r"\bGPUs?\b",
    "transformers": r"\btransformers?\b", "vertex": r"\bVertex\b",
    "ansible": r"\bAnsible\b", "kafka": r"\bKafka\b", "docker": r"\b(?:Docker|Podman|Buildah)\b",
    "kubernetes": r"\b(?:Kubernetes|K8S)\b", "security": r"\b(?:TLS|PKI|X\.?509|PCI|DAST|XXE|keystore|truststore)\b",
    "linux": r"\b(?:Linux|bash|umask|kernel|sed)\b", "golang": r"\bGolang\b",
}


def get(url, tries=4):
    for n in range(tries):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=90) as r:
                return r.read()
        except urllib.error.HTTPError as e:
            if e.code == 404:
                return None
            err = e
        except Exception as e:  # noqa: BLE001 - network hiccups: retry with backoff
            err = e
        time.sleep(3 * (n + 1))
    raise RuntimeError(f"{url}: {err}")


def snapshot(path, cache):
    """Newest 200 capture of the old page -> (timestamp, html bytes); cached on disk."""
    slug = path.rstrip("/").rsplit("/", 1)[-1]
    meta, page = cache / f"{slug}.json", cache / f"{slug}.html"
    if meta.exists() and page.exists():
        return json.loads(meta.read_text())["ts"], page.read_bytes()
    url = f"{HOST}{path}"
    rows = get(f"{WAYBACK}/cdx/search/cdx?url={quote(url)}&fl=timestamp&filter=statuscode:200&output=json")
    rows = json.loads(rows or b"[]")[1:]
    if not rows:
        return None, None
    ts = rows[-1][0]
    html = get(f"{WAYBACK}/web/{ts}id_/https://{url}")
    time.sleep(1.5)  # be gentle with the archive
    if not html:
        return None, None
    page.write_bytes(html)
    meta.write_text(json.dumps({"ts": ts, "path": path}))
    return ts, html


def take_maths(root):
    """Swap each MathML formula for a placeholder; return the TeX for each, as $$…$$ (block) or \\(…\\) (inline).
    The placeholders survive Markdown conversion untouched (which would escape the TeX's backslashes)."""
    maths = []
    for m in root.find_all("math"):
        ann = m.find("annotation", encoding="application/x-tex")
        if not ann:
            continue
        tex = ann.get_text().strip()
        block = m.get("display") == "block"
        maths.append(f"$$\n{tex}\n$$" if block else f"\\({tex}\\)")
        token = f"WPMATH{len(maths) - 1}X"
        if block:
            holder = root.new_tag("p")
            holder.string = token
        else:
            holder = root.new_string(token)
        (m.find_parent("div", class_="wp-block-math") or m).replace_with(holder)
    return maths


def tidy(root):
    """Undo what the old site's front end did to the markup, so the converter sees plain WordPress HTML."""
    for ns in root.find_all("noscript"):  # lazy-load fallbacks duplicate every image
        ns.decompose()
    for img in root.find_all("img"):  # lazy loading: the real address is in data-src
        for attr in ("src", "srcset"):
            if img.get(f"data-{attr}"):
                img[attr] = img[f"data-{attr}"]
    for code in root.find_all("code"):  # <code><a>x</a></code> would lose the link: make it <a><code>x</code></a>
        kids = [k for k in code.contents if str(k).strip()]
        if len(kids) == 1 and getattr(kids[0], "name", None) == "a":
            a = kids[0].extract()
            code.string = a.get_text()
            code.wrap(a)
    return root


def body_html(soup):
    """The post body: .entry-content when the theme had one, else the blocks directly inside #page."""
    ec = soup.select_one(".entry-content")
    if ec:
        return tidy(ec).decode_contents()
    page = tidy(soup.select_one("#page") or soup.body)
    keep = []
    for el in page.find_all(recursive=False):
        cls = " ".join(el.get("class") or [])
        if el.name in CHROME or CHROME_CLASS.search(cls):
            continue
        keep.append(str(el))
    return "\n".join(keep)


def first_paragraph(md, limit=200):
    """A card description from the opening prose: whole sentences up to `limit` characters."""
    for line in md.split("\n\n"):
        line = line.strip()
        if not line or line[0] in "!#-*>|`<{0123456789" or line.startswith("WPHUGO"):
            continue
        text = re.sub(r"!\[[^\]]*\]\([^)]*\)|\[([^\]]*)\]\([^)]*\)", r"\1", line)
        text = re.sub(r"[`*_]", "", text).replace("\n", " ").strip()
        if len(text) < 40:
            continue
        out = ""
        for s in re.split(r"(?<=[.!?])\s+", text):
            if len(out) + len(s) > limit:
                break
            out = (out + " " + s).strip()
        return out or text[:limit].rsplit(" ", 1)[0] + "…"
    return ""


class ArchiveImages:
    """Uploads archive first (via wp2hugo.ImageSource), then the Internet Archive's copy of the image."""

    def __init__(self, local, ts):
        self.local, self.ts, self.fetched = local, ts, 0

    def fetch(self, url):
        hit = self.local.fetch(url)
        if (hit[0] and not hit[2]) or not url or "wp-content/uploads/" not in url:
            return hit  # a full-size local copy (or not an upload at all)
        orig = re.sub(r"^https?://[^/]+/web/\d+\w*_/", "", url)
        data = get(f"{WAYBACK}/web/{self.ts}im_/{orig}")
        time.sleep(1)
        if data and data.startswith(w.IMAGE_MAGIC):
            self.fetched += 1
            month, stem = w.upload_key(orig)
            ext = Path(unquote(orig).split("?")[0]).suffix.lower().replace(".jpeg", ".jpg") or ".png"
            return stem + ext, data, False
        return hit  # the local thumbnail, if there was one, beats nothing


def clean_slug(raw):
    """Old addresses may hold emoji or other non-ASCII ('...-choosing-right-%F0%9F%90%8D'): keep a-z, 0-9 and -."""
    return re.sub(r"[^a-z0-9-]+", "-", unquote(raw).lower()).strip("-") or raw


def tags_for(title, text):
    tags = [t for t, rx in TAG_WORDS.items() if re.search(rx, title, re.I) or len(re.findall(rx, text, re.I)) >= 3]
    return tags[:6]


def recover(path, ts, html, out_root, local_images, known, slug_map):
    soup = BeautifulSoup(html, "html.parser")
    og = {m.get("property"): m.get("content", "") for m in soup.select("meta[property]")}
    m = re.match(r"/wps/(\d{4})/(\d{2})/(\d{2})/([^/]+)/$", path)
    y, mo, d, raw_slug = m.groups()
    slug = clean_slug(raw_slug)
    title = (og.get("og:title") or (soup.title.string if soup.title else slug)).split(" – ")[0].strip()
    images = ArchiveImages(local_images, ts)
    post = w.Post(out_root / slug, images, known)
    maths = take_maths(soup)
    body = w.html_to_md(w.escape_shortcodes(body_html(soup)), post)
    for raw, clean in slug_map.items():  # links between recovered posts use the original (uncleaned) slug
        body = body.replace(f'"/posts/{raw}"', f'"/posts/{clean}"')
    for i, tex in enumerate(maths):
        body = body.replace(f"WPMATH{i}X", tex)
    if maths:  # Blowfish loads KaTeX only on pages that use the katex shortcode
        body = "{{< katex >}}\n\n" + body
    body, jwts = w.JWT.subn("<REDACTED-TOKEN>", body)
    body, keys = w.PRIVATE_KEY.subn("<REDACTED-PRIVATE-KEY>", body)
    text = BeautifulSoup(body, "html.parser").get_text(" ")
    desc = first_paragraph(body)  # the archive's og:description is cut off mid-sentence
    fields = {
        "title": title,
        "date": f"{y}-{mo}-{d}T12:00:00Z",  # the archive keeps the day, not the time
        "slug": slug,
        "description": desc,
        "categories": ["technical"],
        "tags": tags_for(title, text),
        "aliases": sorted({path, f"/wps/{y}/{mo}/{d}/{unquote(raw_slug)}/"}),
        "recovered": f"Internet Archive snapshot {ts[:4]}-{ts[4:6]}-{ts[6:8]}",
    }
    body, unmatched = w.apply_overrides(slug, body, fields, w.OVERRIDES.get(slug) or {})
    media = w.MEDIA_DIR / slug
    for f in sorted(media.glob("*")) if media.is_dir() else []:
        post.files[f.name] = f.read_bytes()
    post.files = {n: data for n, data in post.files.items() if n in body}
    out, pseud = w.pseudonymise(w.front_matter(fields) + "\n" + body.strip() + "\n")
    allowed = w.privacy_check.load_allowlist(w.privacy_check.ALLOWLIST)
    review = [f for f in w.privacy_check.scan_text(out, f"{slug}/index.md") if (f.rule, f.fingerprint) not in allowed]
    return slug, out, post, {"jwt": jwts, "keys": keys, "pseudonym": pseud, "review": review,
                              "unmatched": unmatched, "from_archive": images.fetched, "chars": len(text)}


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--paths", required=True, help="file with old paths, one per line (/wps/YYYY/MM/DD/slug/)")
    ap.add_argument("--cache", required=True, help="folder for downloaded archive pages (kept for re-runs)")
    ap.add_argument("--zip", help="uploads archive (zip of wp-content/uploads)")
    ap.add_argument("--images", action="append", default=[], help="extra image folder laid out YYYY/MM/file")
    ap.add_argument("--out", default="content/posts")
    ap.add_argument("--report", required=True)
    ap.add_argument("--force", action="store_true", help="overwrite bundles that already exist")
    args = ap.parse_args()
    if not w.PSEUDONYM:
        sys.exit(f"error: no pseudonym rules loaded ({w.PSEUDONYM_FILE} is missing or empty)")
    w.OVERRIDES.update(w.load_overrides())
    paths = [p.strip() for p in Path(args.paths).read_text(encoding="utf-8").splitlines()
             if p.strip() and not p.startswith("#")]
    cache, out_root = Path(args.cache), Path(args.out)
    cache.mkdir(parents=True, exist_ok=True)
    local = w.ImageSource(args.zip, args.images)
    raws = [unquote(p.rstrip("/").rsplit("/", 1)[-1]) for p in paths]
    slug_map = {r: clean_slug(r) for r in raws if clean_slug(r) != r}
    known = {p.name for p in out_root.iterdir() if p.is_dir()} | set(raws)
    report = ["# Recovered from the Internet Archive", ""]
    for path in paths:
        ts, html = snapshot(path, cache)
        if not html:
            print(f"none   {path}")
            report.append(f"- **not archived**: `{path}`")
            continue
        slug, text, post, info = recover(path, ts, html, out_root, local, known, slug_map)
        bundle = out_root / slug
        if (bundle / "index.md").exists() and not args.force:
            print(f"skip   {slug} (exists; use --force)")
            continue
        bundle.mkdir(parents=True, exist_ok=True)
        (bundle / "index.md").write_text(text, encoding="utf-8")
        for name, data in post.files.items():
            (bundle / name).write_bytes(w.scrub_photo(data))
        print(f"wrote  {slug}: {info['chars']} chars, {len(post.files)} images "
              f"({info['from_archive']} from the archive), {len(post.missing)} missing"
              + (f", {len(info['review'])} for privacy review" if info["review"] else ""))
        report += [f"## {slug}  (snapshot {ts})", f"- text: {info['chars']} characters; images: {len(post.files)}, "
                   f"missing {len(post.missing)}", *[f"  - missing: `{u}`" for u in post.missing],
                   f"- privacy: {info['jwt']} JWT, {info['keys']} key, {info['pseudonym']} pseudonym replacements",
                   *[f"- review: {f}" for f in info["review"]], *[f"- override not matched: {u}" for u in info["unmatched"]],
                   *[f"- note: {n}" for n in post.notes], ""]
    Path(args.report).write_text("\n".join(report), encoding="utf-8")
    print("report ->", args.report)


if __name__ == "__main__":
    main()
