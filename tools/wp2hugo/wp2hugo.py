"""Convert a WordPress WXR export into Hugo page bundles for the Blowfish theme.

Usage (from the repo root):
    tools/.venv/Scripts/python.exe tools/wp2hugo/wp2hugo.py --list
    tools/.venv/Scripts/python.exe tools/wp2hugo/wp2hugo.py --ids 844,2156 --zip uploads.zip
    tools/.venv/Scripts/python.exe tools/wp2hugo/wp2hugo.py --all --zip uploads.zip --force

Each post becomes content/posts/<slug>/index.md plus the images it uses.
Old WordPress URLs are kept alive through `aliases`. A report of anything that
could not be converted is written to wp-import/import-report.md (git-ignored).
"""
import argparse
import io
import json
import posixpath
import re
import sys
import zipfile
from pathlib import Path
from urllib.parse import unquote
import xml.etree.ElementTree as ET

from bs4 import BeautifulSoup, Comment
from markdownify import MarkdownConverter

NS = {
    "wp": "http://wordpress.org/export/1.2/",
    "content": "http://purl.org/rss/1.0/modules/content/",
    "excerpt": "http://wordpress.org/export/1.2/excerpt/",
}
OLD_PREFIX = "/wps"
# Posts re-published during the 2026-10 recovery carry this date; the real one is in _wp_old_date.
RECOVERY_DAY = "2026-10-23"
DROP_TAGS = {"recover"}
# Posts injected during the 2026-10-11 compromise (script-generated "test-post-<uuid>" slugs,
# backdated to 2026-09-11). Never import these.
ALWAYS_SKIP = {"3128", "3134"}
IMAGE_MAGIC = (b"\x89PNG", b"\xff\xd8\xff", b"GIF8", b"RIFF")
INTERNAL_POST = re.compile(
    r"^https?://(?:www\.|blog\.)?samarthya\.me/wps/(\d{4})/(\d{2})/(\d{2})/([^/?#]+)/?(#[^\s]*)?$")
UPLOAD_KEY = re.compile(r"wp-content/uploads/(\d{4}/\d{2})/([^/?#]+)$")
# Kubernetes service-account tokens and other JWTs pasted into posts.
JWT = re.compile(r"eyJ[A-Za-z0-9_-]{10,}\.eyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}")
# A whole private-key block is never documentation, so it is redacted like a JWT.
PRIVATE_KEY = re.compile(r"-----BEGIN ([A-Z ]*)PRIVATE KEY(?: BLOCK)?-----.*?-----END \1PRIVATE KEY(?: BLOCK)?-----", re.S)
# Everything else credential-shaped is only *reported* for manual review, using the same detectors and
# allowlist as the publish-time check (tools/privacy/check.py); auto-redacting it would mangle real examples.
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "privacy"))
import check as privacy_check  # noqa: E402
# The site is published under a screen name; old posts used the real name as sample data
# (LDAP dc=..., index names, Go structs). The mapping is kept out of git in pseudonym.local.txt
# ("<regex> => <replacement>" per line, applied in order), so the public repo doesn't spell it out.
PSEUDONYM_FILE = Path(__file__).with_name("pseudonym.local.txt")
PSEUDONYM = [
    (re.compile(pat.strip()), repl.strip())
    for pat, repl in (line.split("=>", 1) for line in
                      (PSEUDONYM_FILE.read_text(encoding="utf-8").splitlines() if PSEUDONYM_FILE.exists() else [])
                      if "=>" in line and not line.lstrip().startswith("#"))
]
# EXIF tags that name a person or place: Artist, Copyright, CameraOwnerName, BodySerialNumber, GPS IFD.
PERSONAL_EXIF = {0x013B, 0x8298, 0xA430, 0xA431, 0x8825}


def guess_language(code: str) -> str:
    """Return a Chroma language name (go, bash, yaml, json, java, ...) for a code block.

    WordPress stored no language for any of the 782 code blocks, so without a guess
    every block renders as unhighlighted text.
    """
    # TODO(Samarthya): implement the detection heuristic (see notes in the chat).
    return "text"


# ---------------------------------------------------------------- images

def upload_key(path):
    """'.../uploads/2021/11/Foo-1024x103@2x.png' -> ('2021/11', 'foo').

    Size variants collapse to one stem, and macOS names ('Screenshot 2020-08-02 at
    8.53.17 PM.png') match WordPress' hyphenated ones. Month is None for files
    dropped without YYYY/MM folders.
    """
    p = unquote(path).replace("\\", "/")
    m = UPLOAD_KEY.search(p) or re.search(r"(\d{4}/\d{2})/([^/]+)$", p)
    month, name = (m.group(1), m.group(2)) if m else (None, posixpath.basename(p))
    stem = posixpath.splitext(name)[0].lower()
    stem = re.sub(r"[\s  ]+", "-", stem).replace("@2x", "")
    stem = re.sub(r"-\d+x\d+$", "", stem)
    stem = re.sub(r"-scaled$", "", stem)
    return month, stem


def loose(stem):
    """WordPress renames duplicates 'foo-1.png'; compare without that and punctuation."""
    return re.sub(r"[^a-z0-9]", "", re.sub(r"-\d$", "", stem))


def distinctive(stem):
    """Names safe to match without a month folder (timestamps, camera names), unlike 'image-3'."""
    return bool(re.search(r"\d{4}-?\d{2}-?\d{2}|img[-_]\d{3,}|vid[-_]\d", stem))


class ImageSource:
    """Finds the best verified copy of an upload in uploads.zip and/or extra folders.

    Preference: a non-cropped copy over a 150x150 crop, then the largest file, so an
    original dropped into wp-uploads/ always beats a resized leftover.
    """

    def __init__(self, zip_path=None, extra_dirs=()):
        self.best = {}  # lookup key -> (rank, reader, ext, cropped)
        if zip_path:
            self.zip = zipfile.ZipFile(zip_path)
            for info in self.zip.infolist():
                if not info.is_dir():
                    self._offer(info.filename, info.file_size, lambda i=info: self.zip.read(i))
        for d in extra_dirs:
            for f in Path(d).rglob("*"):
                if f.is_file():
                    self._offer(f.relative_to(d).as_posix(), f.stat().st_size, f.read_bytes)

    def _offer(self, name, size, reader):
        ext = posixpath.splitext(name)[1].lower()
        if ext not in (".png", ".jpg", ".jpeg", ".gif", ".webp") or size < 100:
            return  # skips PHP/backdoors, logs, and empty/truncated files
        month, stem = upload_key(name)
        cropped = bool(re.search(r"-150x150(@2x)?\.\w+$", name, re.I))
        entry = ((not cropped, size), reader, ext, cropped)
        keys = [("any", stem)] if distinctive(stem) else []
        if month:
            keys += [(month, stem), (month, "~" + loose(stem))]
        for k in keys:
            if entry[0] > self.best.get(k, ((False, 0),))[0]:
                self.best[k] = entry

    def fetch(self, url):
        """-> (bundle filename, bytes, cropped) or (None, None, False)."""
        month, stem = upload_key(url or "")
        for k in ((month, stem), (month, "~" + loose(stem)), ("any", stem)):
            hit = self.best.get(k)
            if hit:
                data = hit[1]()
                if data.startswith(IMAGE_MAGIC):
                    return stem + (".jpg" if hit[2] == ".jpeg" else hit[2]), data, hit[3]
        return None, None, False


# ---------------------------------------------------------------- conversion

BLOCK_TAGS = (r"(?:table|thead|tfoot|caption|tbody|tr|td|th|div|dl|dd|dt|ul|ol|li|pre|blockquote|"
              r"p|h[1-6]|hr|section|figure|figcaption)")


def wpautop(text):
    """Rough port of WordPress' wpautop(): classic-editor posts have no <p>, only blank lines."""
    parts = re.split(r"(<pre[\s>].*?</pre>)", text, flags=re.S | re.I)
    out = []
    for i, part in enumerate(parts):
        if i % 2:
            out.append(part)
            continue
        part = re.sub(rf"(</?{BLOCK_TAGS}\b[^>]*>)", r"\n\n\1\n\n", part, flags=re.I)
        for chunk in re.split(r"\n\s*\n", part):
            c = chunk.strip()
            if not c:
                continue
            if re.match(rf"</?{BLOCK_TAGS}\b", c, re.I):
                out.append(c)
            else:
                out.append("<p>" + c.replace("\n", "<br>\n") + "</p>")
    return "\n".join(out)


def fence(code, lang):
    ticks = "~~~~" if "```" in code else "```"
    return f"{ticks}{lang}\n{code.rstrip()}\n{ticks}"


class Post:
    """Per-post conversion state: images written, problems found."""

    def __init__(self, bundle, images, known_slugs):
        self.bundle, self.images, self.known_slugs = bundle, images, known_slugs
        self.files = {}  # filename -> bytes
        self.missing, self.notes, self.langs = [], [], []
        self.privacy = {"jwt": 0, "private-key": 0, "pseudonym": 0}  # counts, filled in by convert()
        self.review = []  # privacy_check.Finding items left for a human to look at
        self.stash = []

    def token(self, md):
        self.stash.append(md)
        return f"WPHUGOBLOCK{len(self.stash) - 1}X"

    def image_md(self, url, alt="", caption=""):
        if not url:
            self.notes.append("dropped an <img> with no src (reference wiped in WordPress)")
            return ""
        name, data, cropped = self.images.fetch(url)
        alt = (alt or caption or "").replace("]", "").strip()
        if cropped:
            caption = (caption + " " if caption else "") + "(thumbnail only — original image lost)"
            self.notes.append(f"cropped thumbnail used for {posixpath.basename(unquote(url))}")
        title = f' "{caption.replace(chr(34), chr(39))}"' if caption else ""
        if name:
            self.files[name] = data
            return f"![{alt}]({name}{title})"
        if url and "wp-content/uploads/" not in url:
            return f"![{alt}]({url}{title})"  # external image (e.g. spinnaker.io): keep hotlink
        self.missing.append(url)
        label = posixpath.basename(unquote(url or "?"))
        return f"*[image unavailable: {label}{' — ' + caption if caption else ''}]*"

    def rewrite_href(self, href):
        m = INTERNAL_POST.match(href or "")
        if m:
            slug = unquote(m.group(4))
            return '{{< relref "/posts/%s" >}}%s' % (slug, m.group(5) or "")
        if "wp-content/uploads/" in (href or ""):
            name, data, _ = self.images.fetch(href)
            if name:
                self.files[name] = data
                return name
            return None  # link to a lost file: keep the text, drop the link
        if "attachment_id=" in (href or "") or not href:
            return None
        return href


class Converter(MarkdownConverter):
    def __init__(self, post, **kw):
        self.post = post
        # WordPress tables often have no <thead>; use the first row as header instead of an empty one.
        super().__init__(heading_style="ATX", bullets="-", code_language="", table_infer_header=True, **kw)

    def convert_img(self, el, text, parent_tags):
        return self.post.image_md(el.get("data-full-url") or el.get("src"), el.get("alt", ""))

    def convert_a(self, el, text, parent_tags):
        href = self.post.rewrite_href(el.get("href", ""))
        if href is None:
            return text
        el["href"] = href
        return super().convert_a(el, text, parent_tags)


def own(container, selector, owner_class):
    """Descendants matching selector whose nearest owner_class ancestor is container (skip nested blocks)."""
    return [e for e in container.select(selector) if e.find_parent(class_=owner_class) is container]


def html_to_md(html, post):
    soup = BeautifulSoup(html, "html.parser")
    for c in soup.find_all(string=lambda s: isinstance(s, Comment)):
        c.extract()

    def put(el, md):
        p = soup.new_tag("p")
        p.string = post.token(md)
        el.replace_with(p)

    # Snow Monkey tabs -> Blowfish tabs
    for tabs in soup.select("div.smb-tabs"):
        labels = {b.get("aria-controls"): b.get_text(" ", strip=True) for b in tabs.select("button.smb-tabs__tab")}
        out = ["{{< tabs >}}"]
        for panel in own(tabs, "div.smb-tab-panel", "smb-tabs"):
            body = panel.select_one(".smb-tab-panel__body") or panel
            label = labels.get(panel.get("id"), "Tab").replace('"', "'")
            out += [f'{{{{< tab label="{label}" >}}}}', html_to_md(body.decode_contents(), post), "{{< /tab >}}"]
        out.append("{{< /tabs >}}")
        put(tabs, "\n\n".join(out))

    # Snow Monkey accordion -> Blowfish accordion
    for acc in soup.select("div.smb-accordion"):
        out = ["{{< accordion >}}"]
        for it in own(acc, "div.smb-accordion__item", "smb-accordion"):
            title = it.select_one(".smb-accordion__item__title__label")
            body = it.select_one(".smb-accordion__item__body")
            label = (title.get_text(" ", strip=True) if title else "Details").replace('"', "'")
            out += [f'{{{{< accordionItem title="{label}" >}}}}',
                    html_to_md(body.decode_contents() if body else "", post), "{{< /accordionItem >}}"]
        out.append("{{< /accordion >}}")
        put(acc, "\n\n".join(out))

    # Snow Monkey step -> Blowfish steps
    for st in soup.select("div.smb-step"):
        out = ["{{< steps >}}"]
        for it in own(st, "div.smb-step__item", "smb-step"):
            title = it.select_one(".smb-step__item__title")
            body = it.select_one(".smb-step__item__body")
            label = (title.get_text(" ", strip=True) if title else "").replace('"', "'")
            out += [f'{{{{< step title="{label}" >}}}}',
                    html_to_md(body.decode_contents() if body else "", post), "{{< /step >}}"]
        out.append("{{< /steps >}}")
        put(st, "\n\n".join(out))

    # Snow Monkey speech balloon -> blockquote
    for b in soup.select("div.smb-balloon"):
        body = b.select_one(".smb-balloon__body") or b
        put(b, "\n".join("> " + line for line in ("💬 " + html_to_md(body.decode_contents(), post)).splitlines()))

    for pq in soup.select("figure.wp-block-pullquote"):
        cite = pq.find("cite")
        if cite:
            cite.extract()
        inner = html_to_md((pq.find("blockquote") or pq).decode_contents(), post)
        put(pq, "{{< lead >}}\n" + inner + (f"\n— {cite.get_text(strip=True)}" if cite else "") + "\n{{< /lead >}}")

    for g in soup.select("figure.wp-block-gallery"):
        imgs = g.find_all("img")
        cols = int((re.search(r"columns-(\d)", " ".join(g.get("class", []))) or [0, 3])[1])
        width = {1: "grid-w100", 2: "grid-w50"}.get(min(cols, len(imgs)), "grid-w33")
        rows = []
        for img in imgs:
            md = post.image_md(img.get("data-full-url") or img.get("src"), img.get("alt", ""))
            m = re.match(r"!\[(.*?)\]\(([^ )]+)", md)
            rows.append(f'  <img src="{m[2]}" alt="{m[1]}" class="{width}" />' if m else md)
        put(g, "{{< gallery >}}\n" + "\n".join(rows) + "\n{{< /gallery >}}" if len(imgs) > 1 else "\n".join(rows).strip())

    for fig in soup.select("figure.wp-block-image, div.wp-block-image figure"):
        img = fig.find("img")
        if not img:
            continue
        cap = fig.find("figcaption")
        put(fig, post.image_md(img.get("data-full-url") or img.get("src"), img.get("alt", ""),
                               cap.get_text(" ", strip=True) if cap else ""))

    # Cover = background photo with text on top -> the photo, then the text.
    for cov in soup.select("div.wp-block-cover"):
        img = cov.select_one("img.wp-block-cover__image-background, img")
        inner = cov.select_one(".wp-block-cover__inner-container")
        parts = [post.image_md(img.get("src"), img.get("alt", "")) if img else "",
                 html_to_md(inner.decode_contents(), post) if inner else ""]
        put(cov, "\n\n".join(p for p in parts if p))

    # File download (PDFs etc.): files weren't in the backup, so name it without a dead link.
    for fb in soup.select("div.wp-block-file"):
        a = fb.find("a", href=True)
        href = a["href"] if a else ""
        name = posixpath.basename(unquote(href)) or "file"
        post.missing.append(href)
        put(fb, f"📄 **{name}** *(download no longer available)*")

    for v in soup.select("figure.wp-block-video"):
        src = (v.find("video") or {}).get("src", "")
        post.missing.append(src)
        put(v, f"*[video unavailable: {posixpath.basename(src)}]*")

    for btns in soup.select("div.wp-block-buttons"):
        links = []
        for a in btns.find_all("a"):
            href = post.rewrite_href(a.get("href", ""))
            links.append(f"[{a.get_text(strip=True)}]({href})" if href else a.get_text(strip=True))
        put(btns, " · ".join(links))

    for pre in soup.find_all("pre"):
        for br in pre.find_all("br"):
            br.replace_with("\n")
        classes = " ".join(pre.get("class", []))
        if "wp-block-verse" in classes:
            text = Converter(post).convert(pre.decode_contents().replace("\n", "<br>"))
            put(pre, "{{< alert \"circle-info\" >}}\n" + text.strip() + "\n{{< /alert >}}")
            continue
        code = pre.get_text()
        m = re.search(r"\blang-(\w+)", classes)
        lang = m[1] if m else ("text" if "wp-block-preformatted" in classes else guess_language(code))
        post.langs.append(lang)
        put(pre, fence(code, lang))

    md = Converter(post).convert(str(soup))
    for i, block in enumerate(post.stash):
        md = md.replace(f"WPHUGOBLOCK{i}X", block)
    # Wrappers markdownify flattens fine; anything else with a block class needs a look.
    harmless = re.compile(r"wp-block-(group|quote|table|image|list|heading|columns?|separator|media-text)(\b|__)"
                          r"|smb-(tab|accordion|step)")
    leftovers = set(re.findall(r'class="([^"]*(?:wp-block|smb-)[^"]*)"', str(soup)))
    post.notes += [f"unconverted element class: {c}" for c in sorted(leftovers) if not harmless.search(c)]
    return re.sub(r"\n{3,}", "\n\n", md).strip()


# ---------------------------------------------------------------- posts

def meta(item, key):
    vals = [m.findtext("wp:meta_value", namespaces=NS) for m in item.findall("wp:postmeta", namespaces=NS)
            if m.findtext("wp:meta_key", namespaces=NS) == key]
    return sorted(v for v in vals if v)


def post_dates(item):
    """(date for front matter, list of old URL date paths)."""
    posted = item.findtext("wp:post_date", namespaces=NS)
    gmt = item.findtext("wp:post_date_gmt", namespaces=NS)
    url_dates = {posted[:10]}
    old = meta(item, "_wp_old_date")
    if posted.startswith(RECOVERY_DAY) and old:
        url_dates.update(old)
        return old[0], sorted(url_dates)
    stamp = (gmt if gmt and not gmt.startswith("0000") else posted).replace(" ", "T")
    return stamp + "Z", sorted(url_dates)


def taxonomy(item):
    cats, tags = [], []
    for c in item.findall("category"):
        name = (c.text or "").strip().lower()
        if not name:
            continue
        target = cats if c.get("domain") == "category" else tags
        if name not in target:
            target.append(name)
    # A tag that just repeats a category ("technical") adds nothing.
    tags = [t for t in tags if t not in DROP_TAGS and t not in cats]
    return cats, tags


def slug_of(item):
    slug = unquote(item.findtext("wp:post_name", namespaces=NS) or "").strip()
    if not slug:
        slug = re.sub(r"[^a-z0-9]+", "-", (item.findtext("title") or "untitled").lower()).strip("-")
    return slug


def escape_shortcodes(text):
    """Literal '{{< x >}}' in old posts (Hugo/Helm snippets) must not run as shortcodes."""
    return re.sub(r"\{\{([<%])(.*?)([>%])\}\}", r"{{\1/*\2*/\3}}", text, flags=re.S)


def pseudonymise(text):
    """Apply the pseudonym rules; return (text, number of replacements)."""
    total = 0
    for pattern, repl in PSEUDONYM:
        text, n = pattern.subn(repl, text)
        total += n
    return text, total


def scrub_photo(data):
    """Drop EXIF from JPEGs that carry personal tags (owner name, GPS...). Re-encodes only those files,
    after applying the EXIF rotation so iPhone photos keep their orientation."""
    if not data.startswith(b"\xff\xd8"):
        return data
    from PIL import Image, ImageOps  # only needed for the few photos that carry personal tags
    img = Image.open(io.BytesIO(data))
    exif = img.getexif()
    if not (PERSONAL_EXIF & set(exif) or PERSONAL_EXIF & set(exif.get_ifd(0x8769))):
        return data
    out = io.BytesIO()
    ImageOps.exif_transpose(img).save(out, "JPEG", quality=92, optimize=True)
    return out.getvalue()


def front_matter(fields):
    lines = ["---"]
    for k, v in fields.items():
        if v in (None, "", []):
            continue
        lines.append(f"{k}: {json.dumps(v, ensure_ascii=False)}")
    return "\n".join(lines + ["---", ""])


def convert(item, out_root, images, known_slugs):
    slug = slug_of(item)
    bundle = out_root / slug
    date, url_dates = post_dates(item)
    cats, tags = taxonomy(item)
    status = item.findtext("wp:status", namespaces=NS)
    post = Post(bundle, images, known_slugs)

    html = escape_shortcodes(item.findtext("content:encoded", namespaces=NS) or "")
    if "<!-- wp:" not in html:
        html = wpautop(html)
    body = html_to_md(html, post)

    body, jwts = JWT.subn("<REDACTED-TOKEN>", body)
    body, keys = PRIVATE_KEY.subn("<REDACTED-PRIVATE-KEY>", body)
    post.privacy = {"jwt": jwts, "private-key": keys}
    if jwts:
        post.notes.append(f"redacted {jwts} JWT/service-account token(s)")
    if keys:
        post.notes.append(f"redacted {keys} private-key block(s)")

    fm = front_matter({
        "title": (item.findtext("title") or slug).strip(),
        "date": date,
        "slug": slug,
        "description": (item.findtext("excerpt:encoded", namespaces=NS) or "").strip(),
        "categories": cats,
        "tags": tags,
        "aliases": [f"{OLD_PREFIX}/{d[:4]}/{d[5:7]}/{d[8:10]}/{slug}/" for d in url_dates],
        "draft": True if status != "publish" else None,
        "wp_id": int(item.findtext("wp:post_id", namespaces=NS)),
    })
    text, post.privacy["pseudonym"] = pseudonymise(fm + "\n" + body + "\n")
    allowed = privacy_check.load_allowlist(privacy_check.ALLOWLIST)
    post.review = [f for f in privacy_check.scan_text(text, f"{slug}/index.md")
                   if (f.rule, f.fingerprint) not in allowed]
    return slug, bundle, text, post


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--xml", default="samarthya.WordPress.2026-10-23.xml")
    ap.add_argument("--zip", help="uploads.zip from wp-content/uploads")
    ap.add_argument("--images", action="append", default=[], help="extra folder laid out YYYY/MM/file")
    ap.add_argument("--out", default="content/posts")
    ap.add_argument("--report", default="wp-import/import-report.md")
    sel = ap.add_mutually_exclusive_group(required=True)
    sel.add_argument("--ids", help="comma-separated WordPress post IDs or slugs")
    sel.add_argument("--all", action="store_true")
    sel.add_argument("--list", action="store_true", help="list posts and exit")
    ap.add_argument("--skip", default="", help="comma-separated post IDs or slugs to leave out")
    ap.add_argument("--drafts", action="store_true", help="also import drafts (as draft: true)")
    ap.add_argument("--force", action="store_true", help="overwrite bundles that already exist")
    ap.add_argument("--allow-unredacted", action="store_true",
                    help=f"convert even if {PSEUDONYM_FILE.name} is missing (real names stay in the output)")
    args = ap.parse_args()

    channel = ET.parse(args.xml).getroot().find("channel")
    items = [i for i in channel.findall("item") if i.findtext("wp:post_type", namespaces=NS) == "post"]
    allowed = {"publish", "draft"} if args.drafts else {"publish"}
    items = [i for i in items if i.findtext("wp:status", namespaces=NS) in allowed]

    if args.list:
        for i in items:
            d, _ = post_dates(i)
            print(f"{i.findtext('wp:post_id', namespaces=NS):>5}  {d[:10]}  {slug_of(i):45.45s}  {i.findtext('title')}")
        return

    if args.ids:
        wanted = {w.strip() for w in args.ids.split(",")}
        items = [i for i in items if i.findtext("wp:post_id", namespaces=NS) in wanted or slug_of(i) in wanted]

    skip = ALWAYS_SKIP | {s.strip() for s in args.skip.split(",") if s.strip()}
    items = [i for i in items if i.findtext("wp:post_id", namespaces=NS) not in skip and slug_of(i) not in skip]
    slugs = [slug_of(i) for i in items]
    dupes = sorted({s for s in slugs if slugs.count(s) > 1})
    if dupes:
        sys.exit(f"duplicate slugs would overwrite each other: {dupes}; use --skip")

    if not PSEUDONYM and not args.allow_unredacted:
        sys.exit(f"error: no pseudonym rules loaded ({PSEUDONYM_FILE} is missing or empty), so real names in old "
                 f"posts would be published. Create it, or pass --allow-unredacted to convert anyway.")
    images = ImageSource(args.zip, args.images)
    known = {slug_of(i) for i in items}
    out_root = Path(args.out)
    report, totals, review = [], {"jwt": 0, "private-key": 0, "pseudonym": 0}, []
    for item in items:
        slug, bundle, text, post = convert(item, out_root, images, known)
        target = bundle / "index.md"
        if target.exists() and not args.force:
            print(f"skip   {slug} (exists; use --force)")
            continue
        bundle.mkdir(parents=True, exist_ok=True)
        target.write_text(text, encoding="utf-8")
        for name, data in post.files.items():
            (bundle / name).write_bytes(scrub_photo(data))
        langs = {l: post.langs.count(l) for l in sorted(set(post.langs))}
        for k in totals:
            totals[k] += post.privacy[k]
        review += post.review
        print(f"wrote  {slug}: {len(post.files)} images, {len(post.missing)} missing, code {langs}"
              + (f", {len(post.review)} for privacy review" if post.review else ""))
        report += [f"## {item.findtext('title')}  (`{slug}`, wp #{item.findtext('wp:post_id', namespaces=NS)})",
                   f"- images copied: {len(post.files)}; missing: {len(post.missing)}",
                   *[f"  - missing: `{u}`" for u in post.missing],
                   f"- code blocks by language: {langs}",
                   *[f"- note: {n}" for n in post.notes],
                   *[f"- privacy review: line {f.line} [{f.rule}] {f.detail} (fp {f.fingerprint})" for f in post.review],
                   ""]

    skipped = sorted(skip)
    summary = ["# WordPress import report", "", "## Privacy summary", "",
               (f"- Pseudonym rules: **{len(PSEUDONYM)} loaded**, {totals['pseudonym']} replacement(s) made"
                if PSEUDONYM else "- Pseudonym rules: **NONE loaded (--allow-unredacted): real names were NOT replaced**"),
               f"- Redacted automatically: {totals['jwt']} JWT(s), {totals['private-key']} private-key block(s)",
               f"- Left for manual review (credential-shaped, not in tools/privacy/allowlist.txt): **{len(review)}**",
               *[f"  - {f}" for f in review],
               f"- Skipped posts (ALWAYS_SKIP + --skip): {', '.join(skipped) if skipped else 'none'}",
               "- Images: JPEGs with personal EXIF (owner, GPS, serial) were re-encoded without it", ""]
    Path(args.report).parent.mkdir(parents=True, exist_ok=True)
    Path(args.report).write_text("\n".join(summary + report), encoding="utf-8")
    print(f"privacy: {totals['jwt']} JWT + {totals['private-key']} key redactions, "
          f"{totals['pseudonym']} pseudonym replacements, {len(review)} item(s) for manual review")
    print(f"report -> {args.report}")


if __name__ == "__main__":
    sys.exit(main())
