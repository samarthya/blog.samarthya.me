"""Anime cover for "bhanuni.in: a domain, a redirect and a gallery that keeps her safe" (2026-11-09).

A red panda (not a child: no likeness of anyone) holds a pencil beside the post's real steps: the proxied
placeholder record, the 302 redirect rule and the importer that strips GPS. The technical diagram stays in the
post body as overview.svg; this writes cover.svg and feature.png.

Run from the repo root:  python tools/covers/anime/bhanuni_domain.py
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from kit import *  # noqa: E402,F403
from topics import CAST, _steps, chips_row  # noqa: E402

SLUG = "bhanuni-in-a-domain-for-her-art"
ACCENT = "#7c3aed"

kind, kw, desc = CAST["redpanda"]
figure = critter(prop=prop("pencil", "#f472b6"), **dict(kw, hat="beret"))
steps, h = _steps("bhanuni.in → her gallery", [
    ("Nameservers", "→ Cloudflare"),
    ("A @, www", "192.0.2.1 proxied"),
    ("Redirect rule", "302 /bhanuni/"),
    ("Every drawing", "GPS stripped"),
], 140, ACCENT)
chips = chips_row(["noindex", "random ids", "SPF -all", "DMARC reject"], 140 + h + 18, ACCENT)
alt = (f"Anime illustration: {desc} in a beret holding a pencil, beside the steps: nameservers to Cloudflare, "
       "A records for @ and www on the proxied placeholder 192.0.2.1, a redirect rule returning 302 to /bhanuni/, "
       "and GPS stripped from every drawing; chips read noindex, random ids, SPF -all, DMARC reject")
body = (steps + chips + pill(600, 66, "A domain for her art", ACCENT, size=21) + figure
        + sparkles(((40, 70, 24), (560, 40, 18), (1165, 600, 22))))
write(SLUG, alt, dict(s1="#ddd6fe", s2="#fce7f3", s3="#fdf4ff"), body, only=[SLUG])
print("ok", SLUG)
