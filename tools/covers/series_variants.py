"""Make the four "Rebuilding samarthya.me" feature images from one source picture.

Each variant is written as feature.jpg into its post bundle, where both the card image logic
(layouts/partials/functions/feature-image.html) and Blowfish's *feature* match pick it up.

    tools\\.venv\\Scripts\\python.exe -I tools\\covers\\series_variants.py
"""
from pathlib import Path

from PIL import Image, ImageEnhance, ImageFilter, ImageOps

ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "assets" / "img" / "covers" / "security-stethescope.jpg"
POSTS = ROOT / "content" / "posts"
SIZE = (1200, 800)  # 3:2, Blowfish's default thumbnail ratio


def crop(img, box):
    """Crop to box (left, top, right, bottom) in source pixels, then fill SIZE."""
    return ImageOps.fit(img.crop(box), SIZE, Image.LANCZOS)


def vignette(img, strength=0.55):
    w, h = img.size
    mask = Image.new("L", (w, h), 0)
    inner = Image.new("L", (int(w * 0.7), int(h * 0.7)), 255)
    mask.paste(inner, ((w - inner.width) // 2, (h - inner.height) // 2))
    mask = mask.filter(ImageFilter.GaussianBlur(min(w, h) // 5))
    dark = ImageEnhance.Brightness(img).enhance(1 - strength)
    return Image.composite(img, dark, mask)


def duotone(img, dark, light):
    return ImageOps.colorize(ImageOps.grayscale(img), black=dark, white=light).convert("RGB")


def main():
    src = Image.open(SOURCE).convert("RGB")
    w, h = src.size  # 1408 x 768
    full = (w - 1152) // 2, 0, (w + 1152) // 2, h  # centred 3:2 window

    variants = {
        # Part 1: the incident, desaturated with a red cast and a vignette
        "rebuilding-1-the-day-the-blog-fell":
            vignette(ImageEnhance.Contrast(duotone(crop(src, full), "#3d0505", "#ffc2b3")).enhance(1.25), 0.6),
        # Part 2: searching for what's left, the magnifier and the eyes
        "rebuilding-2-salvaging-the-content":
            ImageEnhance.Contrast(crop(src, (210, 150, 870, 590))).enhance(1.08),
        # Part 3: healthy again, the original colours
        "rebuilding-3-a-new-home-on-hugo":
            crop(src, (w - 1152 - 60, 0, w - 60, h)),
        # Part 4: infrastructure, a cool indigo duotone (the DevOps topic colour)
        "rebuilding-4-moving-the-domain":
            ImageEnhance.Contrast(duotone(crop(src, full), "#151245", "#c7d2fe")).enhance(1.3),
    }
    for slug, img in variants.items():
        out = POSTS / slug / "feature.jpg"
        img.save(out, "JPEG", quality=82, optimize=True, progressive=True)
        print(f"{out.relative_to(ROOT)}  {img.size[0]}x{img.size[1]}  {out.stat().st_size // 1024} KB")


if __name__ == "__main__":
    main()
