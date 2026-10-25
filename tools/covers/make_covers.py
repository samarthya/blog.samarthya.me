"""Generate card covers (assets/img/covers/*.svg), favicons (static/) and the header badge for the blog.

Covers are driven by data/covers.yaml, the same file the feature-image partial reads,
so adding a topic there and re-running this script is all it takes.

    tools\\.venv\\Scripts\\python.exe -I tools\\covers\\make_covers.py
"""
import json
import random
from html import escape
from pathlib import Path

import yaml
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[2]
COVERS = ROOT / "assets" / "img" / "covers"
STATIC = ROOT / "static"
W, H = 1200, 800  # Blowfish's default thumbnailAspectRatio is 1.5
FAVICON_FROM, FAVICON_TO = "#f97316", "#9a3412"  # "fire" scheme primary
FONT = Path("C:/Windows/Fonts/segoeuib.ttf")
LOGO = ROOT / "assets" / "img" / "logo.png"


def cover_svg(t: dict) -> str:
    # Seeded per topic so re-running the script doesn't churn the files in git.
    rng = random.Random(t["name"])
    dots = "".join(
        f'<circle cx="{rng.randint(0, W)}" cy="{rng.randint(0, H)}" r="{rng.randint(30, 170)}" '
        f'fill="#fff" fill-opacity="{rng.uniform(0.03, 0.10):.3f}"/>'
        for _ in range(9)
    )
    grid = "".join(
        f'<path d="M{x} 0V{H}" stroke="#fff" stroke-opacity=".05"/>' for x in range(0, W, 60)
    ) + "".join(f'<path d="M0 {y}H{W}" stroke="#fff" stroke-opacity=".05"/>' for y in range(0, H, 60))
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">
<defs>
<linearGradient id="g" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{t['from']}"/><stop offset="1" stop-color="{t['to']}"/></linearGradient>
<radialGradient id="r" cx=".85" cy=".15" r=".7"><stop offset="0" stop-color="#fff" stop-opacity=".28"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></radialGradient>
</defs>
<rect width="{W}" height="{H}" fill="url(#g)"/>{grid}{dots}<rect width="{W}" height="{H}" fill="url(#r)"/>
<text x="{W - 90}" y="{H // 2 + 40}" text-anchor="end" font-family="Segoe UI Symbol, Segoe UI, Noto Sans Symbols, DejaVu Sans, sans-serif" font-weight="700" font-size="360" fill="#fff" fill-opacity=".22">{escape(t['glyph'])}</text>
<text x="90" y="{H - 110}" font-family="Segoe UI, Roboto, Helvetica, Arial, sans-serif" font-weight="800" font-size="110" fill="#fff" letter-spacing="-2">{escape(t['label'])}</text>
<rect x="94" y="{H - 82}" width="140" height="10" rx="5" fill="#fff" fill-opacity=".75"/>
</svg>
"""


def gradient_square(size: int) -> Image.Image:
    a = tuple(int(FAVICON_FROM[i:i + 2], 16) for i in (1, 3, 5))
    b = tuple(int(FAVICON_TO[i:i + 2], 16) for i in (1, 3, 5))
    img = Image.new("RGBA", (size, size))
    px = img.load()
    for y in range(size):
        for x in range(size):
            k = (x + y) / (2 * (size - 1))
            px[x, y] = tuple(round(a[i] + (b[i] - a[i]) * k) for i in range(3)) + (255,)
    mask = Image.new("L", (size, size), 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, size - 1, size - 1), radius=size // 5, fill=255)
    img.putalpha(mask)
    return img


def badge(size: int) -> Image.Image:
    """The white logo (assets/img/logo.png, transparent) on the orange gradient; "S" if there's no logo."""
    img = gradient_square(size)
    if LOGO.exists():
        inner = round(size * 0.86)
        mark = Image.open(LOGO).convert("RGBA").resize((inner, inner), Image.LANCZOS)
        img.alpha_composite(mark, ((size - inner) // 2, (size - inner) // 2))
    else:
        font = ImageFont.truetype(str(FONT), int(size * 0.72))
        ImageDraw.Draw(img).text((size / 2, size / 2), "S", font=font, fill="white", anchor="mm")
    return img


def favicons() -> None:
    STATIC.mkdir(exist_ok=True)
    big = badge(1024)  # draw large once, downscale: keeps the logo's thin outline crisp
    for name, size in [("favicon-16x16.png", 16), ("favicon-32x32.png", 32), ("apple-touch-icon.png", 180),
                       ("android-chrome-192x192.png", 192), ("android-chrome-512x512.png", 512)]:
        big.resize((size, size), Image.LANCZOS).save(STATIC / name)
    big.resize((64, 64), Image.LANCZOS).save(STATIC / "favicon.ico", sizes=[(16, 16), (32, 32), (48, 48), (64, 64)])
    big.resize((160, 160), Image.LANCZOS).save(ROOT / "assets" / "img" / "logo-badge.png")  # header (shown at 80px)
    (STATIC / "site.webmanifest").write_text(json.dumps({
        "name": "Samarthya", "short_name": "Samarthya",
        "icons": [{"src": "android-chrome-192x192.png", "sizes": "192x192", "type": "image/png"},
                  {"src": "android-chrome-512x512.png", "sizes": "512x512", "type": "image/png"}],
        "theme_color": FAVICON_FROM, "background_color": "#ffffff", "display": "standalone",
    }, indent=2) + "\n", encoding="utf-8")


def main() -> None:
    topics = yaml.safe_load((ROOT / "data" / "covers.yaml").read_text(encoding="utf-8"))["topics"]
    COVERS.mkdir(parents=True, exist_ok=True)
    for t in topics:
        (COVERS / f"{t['name']}.svg").write_text(cover_svg(t), encoding="utf-8")
    favicons()
    print(f"{len(topics)} covers -> {COVERS.relative_to(ROOT)}; favicons -> {STATIC.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
