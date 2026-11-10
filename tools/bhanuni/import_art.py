"""Import drawings for Bhanuni's Studio (/bhanuni/).

    tools/bhanuni/.venv/Scripts/python -I tools/bhanuni/import_art.py <folder with drawings> [--dry-run]

(see tools/bhanuni/STUDIO.md for the whole publishing routine)

For every image (jpg/jpeg/png/webp) in the folder that has not been imported before:
  * gives it a random 6-character id (e.g. "k7f2qa"), so file names say nothing about the picture
  * fixes its rotation, puts transparent areas on white, scales the long edge to at most 1800 px
  * saves it as content/bhanuni/art/<id>.jpg with NO metadata (EXIF, GPS, camera, dates are all dropped)
  * appends an entry to data/bhanuni.yaml (title, date, medium, ... to be filled in by hand)

Re-running is safe: a source file is recognised by its SHA-256, kept with its original name in
tools/bhanuni/ids.local.csv (git-ignored, so the original names never reach the public repo).
The source folder is only read, never changed.
"""
import csv, datetime as dt, hashlib, pathlib, secrets, sys

from PIL import Image, ImageOps

ROOT = pathlib.Path(__file__).resolve().parents[2]
ART = ROOT / "content/bhanuni/art"
DATA = ROOT / "data/bhanuni.yaml"
IDS = ROOT / "tools/bhanuni/ids.local.csv"
MAX_EDGE, QUALITY = 1800, 85
ALPHABET = "abcdefghjkmnpqrstuvwxyz23456789"  # no 0/o, 1/l/i: easy to read aloud
EXTS = {".jpg", ".jpeg", ".png", ".webp"}


def new_id(taken):
    while True:
        i = "".join(secrets.choice(ALPHABET) for _ in range(6))
        if i not in taken:
            return i


def taken_date(im, path):
    """When it was drawn, as best we know: the EXIF capture date, else the file's modified time."""
    exif = im.getexif()
    raw = (exif.get_ifd(0x8769).get(36867) or exif.get(306)) if exif else None
    if raw:
        try:
            return dt.datetime.strptime(str(raw)[:10], "%Y:%m:%d").date()
        except ValueError:
            pass
    return dt.date.fromtimestamp(path.stat().st_mtime)


def clean(im):
    im = ImageOps.exif_transpose(im)
    if im.mode in ("RGBA", "LA", "P"):
        im = im.convert("RGBA")
        bg = Image.new("RGB", im.size, "white")
        bg.paste(im, mask=im.getchannel("A"))
        im = bg
    else:
        im = im.convert("RGB")
    im.thumbnail((MAX_EDGE, MAX_EDGE), Image.LANCZOS)
    return im


def yaml_entry(i, d):
    """One gallery entry; the field meanings are documented once at the top of data/bhanuni.yaml."""
    return (f"\n- id: {i}\n"
            f"  title: \"\"\n"
            f"  date: {d.isoformat()}\n"
            f"  medium: digital\n"
            f"  kind: original\n"
            f"  inspired_by: \"\"\n"
            f"  series: \"\"\n"
            f"  words: \"\"\n"
            f"  about: \"\"\n"
            f"  featured: false\n"
            f"  publish: false\n")


def main():
    src = pathlib.Path(sys.argv[1]); dry = "--dry-run" in sys.argv
    known = {}
    if IDS.exists():
        with IDS.open(newline="", encoding="utf-8") as f:
            known = {r["sha256"]: r for r in csv.DictReader(f)}
    taken = {r["id"] for r in known.values()}
    rows, entries = [], []
    for p in sorted(x for x in src.iterdir() if x.suffix.lower() in EXTS):
        h = hashlib.sha256(p.read_bytes()).hexdigest()
        if h in known:
            print(f"skip  {p.name} (already {known[h]['id']})")
            continue
        with Image.open(p) as im:
            d = taken_date(im, p)
            out = clean(im)
        i = new_id(taken); taken.add(i)
        print(f"new   {p.name} -> {i}.jpg  {out.size[0]}x{out.size[1]}  {d}")
        if not dry:
            ART.mkdir(parents=True, exist_ok=True)
            out.save(ART / f"{i}.jpg", "JPEG", quality=QUALITY, optimize=True, progressive=True)
        rows.append({"id": i, "sha256": h, "original": p.name, "imported": dt.date.today().isoformat()})
        entries.append((d, i))
    if dry or not rows:
        print("nothing written" if dry else "nothing new")
        return
    if not DATA.exists():
        DATA.write_text("# Bhanuni's Studio: one entry per drawing; images in content/bhanuni/art/<id>.jpg\n"
                        "# Only entries with publish: true appear on the site.\n", encoding="utf-8")
    with DATA.open("a", encoding="utf-8") as f:
        for d, i in sorted(entries):
            f.write(yaml_entry(i, d))
    new_file = not IDS.exists()
    with IDS.open("a", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["id", "sha256", "original", "imported"])
        if new_file:
            w.writeheader()
        w.writerows(rows)
    print(f"{len(rows)} imported")


if __name__ == "__main__":
    main()
