"""Body diagram (overview.svg) for "Likes and hearts: a basic interactive interface for my site".

Same smooth technical look as the Cloudflare series (it reuses those helpers), but the banner (feature.png) is an
anime cover from tools/covers/anime/likes_and_hearts.py, so this script never writes feature.png.

Run from the repo root:  python tools/covers/likes_and_hearts.py [preview.png]
"""
import pathlib
import subprocess
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from cloudflare_series import (ROOT, ORANGE, AMBER, CYAN, VIOLET, GREEN, RED, INK, SOFT, DIM, FONT,  # noqa: E402
                               esc, defs, backdrop, card, t, pill, flowline, dot, cloud)

SLUG = "likes-and-hearts"

b = backdrop([(250, 450, 190, VIOLET, .22), (640, 400, 200, ORANGE, .26), (1060, 430, 190, CYAN, .2)])
b += (f'<text x="60" y="76" fill="{ORANGE}" font-size="17" font-weight="700" letter-spacing="3.5">STATIC SITE · INTERACTIVE</text>'
      f'<text x="60" y="128" fill="{INK}" font-size="46" font-weight="800">Likes and hearts</text>'
      f'<text x="60" y="166" fill="{SOFT}" font-size="21">One tap, no login, nothing personal kept.</text>')
# two static pages
b += card(60, 206, 300, 176)
b += t(84, 238, "BLOG POST", 13, CYAN, 700, ls=2.5)
for i in range(3):
    b += f'<rect x="84" y="{254 + i * 16}" width="{230 - i * 50}" height="7" rx="3.5" fill="#ffffff" fill-opacity=".12"/>'
b += t(84, 322, "Was this useful?", 13, SOFT)
for i, (e, n) in enumerate([("👍", "3"), ("👎", "0"), ("❤️", "5")]):
    x = 84 + i * 82
    b += f'<rect x="{x}" y="334" width="72" height="30" rx="15" fill="none" stroke="{SOFT}" stroke-opacity=".45"/>'
    b += t(x + 24, 354, e, 15, INK, 400, "middle") + t(x + 50, 354, n, 14, SOFT, 700, "middle")
b += card(60, 400, 300, 176)
b += t(84, 432, "GALLERY", 13, VIOLET, 700, ls=2.5)
for i, n in enumerate(["4", "1", "2"]):
    x = 84 + i * 86
    b += f'<rect x="{x}" y="446" width="76" height="70" rx="10" fill="{VIOLET}" fill-opacity=".14" stroke="{VIOLET}" stroke-opacity=".5"/>'
    b += f'<circle cx="{x + 38}" cy="474" r="14" fill="none" stroke="{SOFT}" stroke-opacity=".5"/>'
    b += t(x + 38, 540, "♥ " + n, 14, "#f472b6", 700, "middle")
b += t(84, 562, "GitHub Pages: static files", 12, DIM)
# the worker
b += f'<circle cx="640" cy="390" r="112" fill="{ORANGE}" opacity=".08"/>'
b += card(500, 250, 280, 280, stroke="url(#edge)")
b += cloud(640, 290, .7, ORANGE)
b += t(640, 334, "WORKER", 15, INK, 800, "middle", ls=4)
b += t(640, 356, "a tiny counter", 13, AMBER, 600, "middle")
for i, lab in enumerate(["from my site?", "post or drawing exists?", "like · dislike · heart?"]):
    y = 384 + i * 36
    b += f'<rect x="522" y="{y}" width="236" height="28" rx="9" fill="#ffffff" fill-opacity=".04"/>'
    b += dot(540, y + 14, GREEN, 4) + t(556, y + 19, lab, 13, SOFT)
b += t(640, 510, "else refused", 12, RED, 700, "middle")
b += flowline("M362 294 C430 294 440 340 498 352")
b += flowline("M362 488 C430 488 440 440 498 428")
b += t(430, 400, "one tap", 13, ORANGE, 700, "middle")
# D1
b += card(870, 206, 270, 370)
b += f'<ellipse cx="1005" cy="246" rx="58" ry="14" fill="none" stroke="{CYAN}" stroke-width="2"/>'
b += f'<path d="M947 246 V282 A58 14 0 0 0 1063 282 V246" fill="none" stroke="{CYAN}" stroke-width="2"/>'
b += t(1005, 314, "D1", 16, INK, 800, "middle", ls=3)
b += f'<rect x="892" y="330" width="226" height="66" rx="10" fill="#ffffff" fill-opacity=".04"/>'
b += t(906, 354, "hearts", 14, CYAN, 700, mono=True) + t(906, 380, "id · n", 14, SOFT, 400, mono=True)
b += f'<rect x="892" y="406" width="226" height="66" rx="10" fill="#ffffff" fill-opacity=".04"/>'
b += t(906, 430, "reactions", 14, CYAN, 700, mono=True) + t(906, 456, "slug · kind · n", 14, SOFT, 400, mono=True)
b += pill(892, 486, "no names · no IPs", GREEN, w=226)
b += t(1005, 548, "free: 100k writes / day", 13, DIM, 400, "middle")
# slight curve: a flat line has a zero-height box, so its gradient and glow would vanish
b += flowline("M784 392 C816 380 840 380 872 392", ORANGE, 3)
b += t(828, 368, "upsert", 12, AMBER, 700, "middle", mono=True)

ALT = ("Two pages on GitHub Pages, a blog post with like, dislike and heart buttons and the gallery with a heart per "
       "drawing, send one-tap requests to a small Cloudflare Worker. The Worker checks that the request comes from my "
       "site, that the post or drawing exists and that the reaction is like, dislike or heart, then does one upsert "
       "into D1, which has two tables: hearts (id, n) and reactions (slug, kind, n). No names or IP addresses are "
       "stored; the free plan allows 100,000 writes a day.")

svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 630" width="1200" height="630" font-family="{FONT}">'
       f'<title>{esc(ALT)}</title>{defs()}{b}</svg>\n')
path = ROOT / "content" / "posts" / SLUG / "overview.svg"
path.write_text(svg, encoding="utf-8")
print("wrote", path)
if len(sys.argv) > 1:   # render a preview somewhere else; feature.png is the anime cover
    subprocess.run([sys.executable, "-I", str(ROOT / "tools/titles/svg_to_png.py"), str(path), sys.argv[1]], check=True)
