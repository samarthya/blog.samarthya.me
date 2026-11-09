"""Shared drawing kit for the anime cover images (1200x630 SVG, rendered to feature.png).

Each cover script in this folder builds `content/posts/<slug>/cover.svg` from these pieces and renders it with
tools/titles/svg_to_png.py. Style: a pastel sky, one character on the left tied to the post's lead analogy, and the
post's real content (a terminal, a diagram, numbers) on the right. Never reuse a character across a series.

Run from the repo root:  python tools/covers/anime/<script>.py [slug ...]   (no slugs = every cover in the script)
"""
import pathlib
import subprocess
import sys

REPO = pathlib.Path(__file__).resolve().parents[3]
MONO = "Consolas, Menlo, monospace"
SANS = "Segoe UI, Arial, sans-serif"
INK = "#1f2937"
_NOCOL = dict(h1="#000", h2="#000", h3="#000", c1="#000", c2="#000")

DEFS = '''<defs>
<linearGradient id="sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{s1}"/><stop offset="0.65" stop-color="{s2}"/><stop offset="1" stop-color="{s3}"/></linearGradient>
<radialGradient id="glow" cx="0.5" cy="0.35" r="0.6"><stop offset="0" stop-color="#ffffff" stop-opacity="0.7"/><stop offset="1" stop-color="#ffffff" stop-opacity="0"/></radialGradient>
<linearGradient id="skin" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#ffe6d2"/><stop offset="1" stop-color="#fbd1b5"/></linearGradient>
<linearGradient id="hair" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{h1}"/><stop offset="0.6" stop-color="{h2}"/><stop offset="1" stop-color="{h3}"/></linearGradient>
<linearGradient id="iris" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#1e3a8a"/><stop offset="0.55" stop-color="#2f7fd6"/><stop offset="1" stop-color="#6fe0e8"/></linearGradient>
<linearGradient id="hoodie" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{c1}"/><stop offset="1" stop-color="{c2}"/></linearGradient>
<linearGradient id="metal" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#9aa4b5"/><stop offset="0.45" stop-color="#4b5563"/><stop offset="1" stop-color="#1f2937"/></linearGradient>
<linearGradient id="robot" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#f1f5f9"/><stop offset="1" stop-color="#b8c4d6"/></linearGradient>
<linearGradient id="qmark" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fff176"/><stop offset="1" stop-color="#ffb300"/></linearGradient>
<filter id="soft" x="-20%" y="-20%" width="140%" height="140%"><feGaussianBlur stdDeviation="3"/></filter>
<filter id="drop" x="-20%" y="-20%" width="140%" height="150%"><feDropShadow dx="0" dy="8" stdDeviation="8" flood-color="#2a1d5c" flood-opacity="0.28"/></filter>
<clipPath id="eyeL"><ellipse cx="540" cy="266" rx="38" ry="50"/></clipPath>
<clipPath id="eyeR"><ellipse cx="664" cy="266" rx="38" ry="50"/></clipPath>
<symbol id="spark" viewBox="-10 -10 20 20" overflow="visible"><path d="M0 -10 Q1.2 -1.2 10 0 Q1.2 1.2 0 10 Q-1.2 1.2 -10 0 Q-1.2 -1.2 0 -10Z" fill="#ffffff"/></symbol>
</defs>'''



def sparkles(pts):
    return "".join(f'<use href="#spark" x="{x}" y="{y}" width="{s}" height="{s}"/>' for x, y, s in pts)


def svg(title, colours, body):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 630" width="1200" height="630">
  <title>{title}</title>
  {DEFS.format(**colours)}
  <rect width="1200" height="630" fill="url(#sky)"/>
  <rect width="1200" height="630" fill="url(#glow)"/>
{body}
</svg>
'''


def grad(id_, a, b, horizontal=False):
    x2, y2 = ("1", "0") if horizontal else ("0", "1")
    return f'<linearGradient id="{id_}" x1="0" y1="0" x2="{x2}" y2="{y2}"><stop offset="0" stop-color="{a}"/><stop offset="1" stop-color="{b}"/></linearGradient>'


def eye(cx, cy, rx, ry, iris_a, iris_b, look=(0, 0), iris_scale=0.75, cid="e", hl=0.24):
    ix, iy = cx + look[0], cy + look[1]
    irx, iry = rx * iris_scale, ry * iris_scale
    return f'''
  <defs><clipPath id="{cid}"><ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}"/></clipPath>{grad(cid + "g", iris_a, iris_b)}</defs>
  <ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="#ffffff"/>
  <g clip-path="url(#{cid})">
    <ellipse cx="{ix}" cy="{iy}" rx="{irx}" ry="{iry}" fill="url(#{cid}g)"/>
    <ellipse cx="{ix}" cy="{iy - 2}" rx="{irx * 0.45}" ry="{iry * 0.5}" fill="#111827"/>
    <circle cx="{ix - irx * 0.35}" cy="{iy - iry * 0.4}" r="{rx * hl}" fill="#ffffff"/>
    <circle cx="{ix + irx * 0.35}" cy="{iy + iry * 0.35}" r="{rx * 0.1}" fill="#ffffff"/>
  </g>
  <ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="none" stroke="{INK}" stroke-width="4"/>'''


def blush(x, y, rx=22, ry=10):
    return f'<ellipse cx="{x}" cy="{y}" rx="{rx}" ry="{ry}" fill="#ff8fa3" opacity="0.5" filter="url(#soft)"/>'


def card(x, y, w, h, head, head_fill="#1e293b", head_ink="#a5f3fc", body=""):
    return f'''
  <g filter="url(#drop)">
    <rect x="{x}" y="{y}" width="{w}" height="{h}" rx="18" fill="#ffffff"/>
    <path d="M{x} {y + 56} V{y + 18} Q{x} {y} {x + 18} {y} H{x + w - 18} Q{x + w} {y} {x + w} {y + 18} V{y + 56}Z" fill="{head_fill}"/>
    <text x="{x + 24}" y="{y + 37}" font-family="{MONO}" font-size="24" font-weight="800" fill="{head_ink}">{head}</text>
  </g>{body}'''


def pill(x, y, text, fill, ink="#ffffff", size=20, w=None, rot=0, mono=False):
    w = w or int(len(text) * size * (0.62 if mono else 0.56)) + 36
    from html import escape
    text = escape(text, quote=False)  # "&" in a label would break the SVG
    fam = MONO if mono else SANS
    return f'''
  <g filter="url(#drop)" transform="rotate({rot} {x + w / 2} {y + 22})">
    <rect x="{x}" y="{y}" width="{w}" height="44" rx="22" fill="{fill}"/>
    <text x="{x + w / 2}" y="{y + 29}" text-anchor="middle" font-family="{fam}" font-size="{size}" font-weight="800" fill="{ink}">{text}</text>
  </g>'''


def arrow(d, colour="#7c3aed", width=5, dash=""):
    """A path with an arrowhead; each colour gets its own marker so the head matches the line."""
    mid = "arr" + colour.lstrip("#")
    da = f' stroke-dasharray="{dash}"' if dash else ""
    return (f'<defs><marker id="{mid}" viewBox="0 0 10 10" refX="7" refY="5" markerWidth="5" markerHeight="5" '
            f'orient="auto"><path d="M0 0 L10 5 L0 10Z" fill="{colour}"/></marker></defs>'
            f'<path d="{d}" stroke="{colour}" stroke-width="{width}" fill="none" stroke-linecap="round" '
            f'stroke-linejoin="round"{da} marker-end="url(#{mid})"/>')

def write(slug, title, sky, body, only=None):
    """Write cover.svg for a post and render feature.png next to it. `sky` = dict(s1, s2, s3) top to bottom."""
    only = sys.argv[1:] if only is None else only
    if only and slug not in only:
        return
    p = REPO / "content" / "posts" / slug / "cover.svg"
    p.write_text(svg(title, dict(sky, **_NOCOL), body), encoding="utf-8")
    subprocess.run([sys.executable, "-I", str(REPO / "tools/titles/svg_to_png.py"), str(p)], check=True)




# ---------------------------------------------------------------------------------------------------------
# A terminal panel and a configurable chibi animal, so a cover is mostly data (see linux.py).
# ---------------------------------------------------------------------------------------------------------
import math
from html import escape as _esc


def terminal(x, y, w, h, title, lines, size=19, gap=31):
    """A dark terminal window. `lines`: strings, or (text, colour). Lines starting with '$ ' get a green prompt."""
    rows, ty = [], y + 92
    for ln in lines:
        text, col = (ln, "#e2e8f0") if isinstance(ln, str) else ln
        if text.startswith("$ "):
            rows.append(f'<text xml:space="preserve" x="{x + 26}" y="{ty}" font-family="{MONO}" font-size="{size}" font-weight="700">'
                        f'<tspan fill="#4ade80">$ </tspan><tspan fill="{"#f8fafc" if col == "#e2e8f0" else col}">{_esc(text[2:])}</tspan></text>')
        elif text:
            rows.append(f'<text xml:space="preserve" x="{x + 26}" y="{ty}" font-family="{MONO}" font-size="{size}" '
                        f'font-weight="700" fill="{col}">{_esc(text)}</text>')
        ty += gap
    return f'''
  <g filter="url(#drop)">
    <rect x="{x}" y="{y}" width="{w}" height="{h}" rx="18" fill="#0f172a"/>
    <path d="M{x} {y + 50} V{y + 18} Q{x} {y} {x + 18} {y} H{x + w - 18} Q{x + w} {y} {x + w} {y + 18} V{y + 50}Z" fill="#1e293b"/>
    <circle cx="{x + 28}" cy="{y + 25}" r="7" fill="#ef4444"/><circle cx="{x + 50}" cy="{y + 25}" r="7" fill="#f59e0b"/><circle cx="{x + 72}" cy="{y + 25}" r="7" fill="#22c55e"/>
    <text x="{x + w / 2}" y="{y + 32}" text-anchor="middle" font-family="{MONO}" font-size="18" font-weight="700" fill="#94a3b8">{_esc(title)}</text>
  </g>
  {"".join(rows)}'''


HAND = (450, 392)  # where critter() puts the raised paw; draw props around it

_EARS = {
    "round": '<circle cx="150" cy="175" r="48" fill="url(#cfur)"/><circle cx="150" cy="178" r="25" fill="{inner}"/>'
             '<circle cx="390" cy="175" r="48" fill="url(#cfur)"/><circle cx="390" cy="178" r="25" fill="{inner}"/>',
    "small": '<circle cx="165" cy="190" r="28" fill="url(#cfur)"/><circle cx="375" cy="190" r="28" fill="url(#cfur)"/>',
    "pointy": '<path d="M130 240 L140 100 L230 170Z" fill="url(#cfur)"/><path d="M150 215 L154 135 L205 175Z" fill="{inner}"/>'
              '<path d="M410 240 L400 100 L310 170Z" fill="url(#cfur)"/><path d="M390 215 L386 135 L335 175Z" fill="{inner}"/>',
    "long": '<ellipse cx="205" cy="100" rx="34" ry="105" fill="url(#cfur)" transform="rotate(-12 205 100)"/>'
            '<ellipse cx="205" cy="110" rx="16" ry="80" fill="{inner}" transform="rotate(-12 205 110)"/>'
            '<ellipse cx="335" cy="100" rx="34" ry="105" fill="url(#cfur)" transform="rotate(12 335 100)"/>'
            '<ellipse cx="335" cy="110" rx="16" ry="80" fill="{inner}" transform="rotate(12 335 110)"/>',
    "tufts": '<path d="M140 200 L150 110 L215 175Z M400 200 L390 110 L325 175Z" fill="url(#cfur)"/>',
    "bat": '<path d="M120 230 L110 60 L230 170Z" fill="url(#cfur)"/><path d="M140 205 L136 105 L205 172Z" fill="{inner}"/>'
           '<path d="M420 230 L430 60 L310 170Z" fill="url(#cfur)"/><path d="M400 205 L404 105 L335 172Z" fill="{inner}"/>',
    "frog": '<circle cx="200" cy="200" r="62" fill="url(#cfur)"/><circle cx="340" cy="200" r="62" fill="url(#cfur)"/>',
}

_HATS = {
    "tophat": '<g filter="url(#drop)"><rect x="200" y="70" width="140" height="100" rx="10" fill="#111827"/><rect x="200" y="140" width="140" height="18" fill="#dc2626"/><ellipse cx="270" cy="170" rx="110" ry="18" fill="#111827"/></g>',
    "beret": '<g filter="url(#drop)"><ellipse cx="250" cy="165" rx="130" ry="50" fill="#dc2626" transform="rotate(-8 250 165)"/><circle cx="250" cy="112" r="10" fill="#dc2626"/></g>',
    "crown": '<g filter="url(#drop)"><path d="M190 175 L180 95 L225 135 L270 80 L315 135 L360 95 L350 175Z" fill="#facc15" stroke="#b45309" stroke-width="4"/><circle cx="270" cy="150" r="10" fill="#ef4444"/></g>',
    "goggles": '<g filter="url(#drop)"><path d="M110 210 C170 170 370 170 430 210" stroke="#334155" stroke-width="16" fill="none"/><circle cx="215" cy="195" r="36" fill="#7dd3fc" stroke="#334155" stroke-width="9"/><circle cx="325" cy="195" r="36" fill="#7dd3fc" stroke="#334155" stroke-width="9"/><circle cx="204" cy="184" r="9" fill="#ffffff"/><circle cx="314" cy="184" r="9" fill="#ffffff"/></g>',
    "headlamp": '<g filter="url(#drop)"><path d="M110 200 C170 150 370 150 430 200" stroke="#f59e0b" stroke-width="18" fill="none"/><circle cx="270" cy="160" r="30" fill="#fde047" stroke="#b45309" stroke-width="6"/><circle cx="270" cy="160" r="14" fill="#ffffff"/></g>',
    "grad_cap": '<g filter="url(#drop)"><path d="M150 140 L270 90 L390 140 L270 190Z" fill="#111827"/><path d="M205 160 L205 200 C240 220 300 220 335 200 L335 160" fill="#1f2937"/><path d="M390 140 L392 210" stroke="#facc15" stroke-width="5"/><circle cx="392" cy="214" r="9" fill="#facc15"/></g>',
    "nightcap": '<g filter="url(#drop)"><path d="M150 190 C170 100 300 70 420 120 C440 140 450 170 470 200 C420 170 380 160 380 190Z" fill="#6366f1"/><path d="M140 186 C220 160 320 160 400 186 C400 206 140 206 140 186Z" fill="#e0e7ff"/><circle cx="472" cy="206" r="18" fill="#e0e7ff"/></g>',
    "bow": '<g filter="url(#drop)"><path d="M270 150 L200 110 L205 190Z M270 150 L340 110 L335 190Z" fill="#ec4899"/><circle cx="270" cy="150" r="16" fill="#be185d"/></g>',
}

_MOUTHS = {
    "smile": '<path d="M248 366 C258 382 282 382 292 366" stroke="#3f1d0b" stroke-width="4.5" fill="none" stroke-linecap="round"/>',
    "open": '<path d="M250 364 C256 392 284 392 290 364Z" fill="#be123c"/>',
    "o": '<ellipse cx="270" cy="378" rx="10" ry="13" fill="#be123c"/>',
    "grin": '<path d="M238 362 C250 396 290 396 302 362Z" fill="#be123c"/><path d="M244 366 L296 366" stroke="#ffffff" stroke-width="6"/>',
}


def critter(fur=("#fdba74", "#ea580c"), belly="#fff7ed", face=None, ears="round", ear_inner="#fda4af", snout="nose",
            iris=("#1e293b", "#475569"), look=(10, -2), eye_y=290, sleepy=False, mask=None, back=(), hat=None,
            glasses=False, scarf=None, mouth="smile", nose_col="#1f2937", beak_col=("#fdba74", "#f97316"), prop="",
            hand_col=None, tail_col=None):
    """A chibi animal in the left half of the cover (head ~(270,290), body ~(270,530), raised paw at HAND).

    ears:  round | pointy | long | floppy | tufts | small | bat | frog | none
    snout: nose | beak | bill | none                 mask: raccoon | owl | sloth | meerkat | puffin | None
    back (drawn behind): spikes | shell | wings | bat_wings | tail_fluffy | tail_curl | tail_stripes | crest | tuft
    hat:   tophat | beret | crown | goggles | headlamp | grad_cap | nightcap | bow | None
    prop:  SVG drawn just before the raised paw, so the paw holds it (see HAND)
    """
    tc = tail_col or "url(#cfur)"
    b = [f'<defs>{grad("cfur", *fur)}{grad("cbeak", *beak_col)}<linearGradient id="cshine" x1="0" y1="0" x2="0" y2="1">'
         '<stop offset="0" stop-color="#ffffff" stop-opacity="0.35"/><stop offset="1" stop-color="#ffffff" stop-opacity="0"/></linearGradient></defs>']
    # behind the body
    if "tail_fluffy" in back:
        b.append(f'<path d="M380 600 C520 600 560 470 500 360 C470 300 520 250 560 300 C640 420 560 640 400 640Z" fill="{tc}" filter="url(#drop)"/>')
    if "tail_stripes" in back:
        b.append(f'<g filter="url(#drop)" transform="rotate(-30 470 560)"><rect x="400" y="530" width="230" height="64" rx="32" fill="{tc}"/>'
                 + "".join(f'<rect x="{430 + i * 46}" y="530" width="20" height="64" fill="#1f2937" opacity="0.8"/>' for i in range(4)) + "</g>")
    if "tail_curl" in back:
        b.append(f'<path d="M400 600 C520 610 560 520 520 470 C490 430 440 460 460 500 C475 525 505 505 495 490" stroke="{tc}" '
                 'stroke-width="30" fill="none" stroke-linecap="round" filter="url(#drop)"/>')
    if "wings" in back:
        b.append('<path d="M120 470 C40 480 30 580 90 620 C110 560 130 520 150 500Z M420 470 C500 480 510 580 450 620 C430 560 410 520 390 500Z" fill="url(#cfur)" filter="url(#drop)"/>')
    if "bat_wings" in back:
        b.append('<g fill="#4c1d95" filter="url(#drop)"><path d="M140 450 C60 380 10 420 10 470 C40 450 50 480 40 510 C70 490 90 520 80 550 C110 520 140 530 150 540Z"/>'
                 '<path d="M400 450 C480 380 530 420 530 470 C500 450 490 480 500 510 C470 490 450 520 460 550 C430 520 400 530 390 540Z"/></g>')
    if "shell" in back:
        b.append('<g filter="url(#drop)"><ellipse cx="270" cy="520" rx="200" ry="170" fill="#65a30d"/>'
                 '<path d="M270 360 L340 420 L320 510 L220 510 L200 420Z M120 460 L200 420 M420 460 L340 420 M220 510 L170 600 M320 510 L370 600" '
                 'stroke="#365314" stroke-width="7" fill="none" opacity="0.7"/>'
                 '<ellipse cx="270" cy="520" rx="200" ry="170" fill="none" stroke="#3f6212" stroke-width="10"/></g>')
    if "spikes" in back:
        pts = []
        for i in range(15):
            a = 2.75 + i * 0.27
            p = [(270 + r * math.cos(a + d), 290 + r * 0.86 * math.sin(a + d)) for r, d in ((168, 0), (232, 0.13), (168, 0.26))]
            pts.append("M" + " L".join(f"{x:.0f} {y:.0f}" for x, y in p) + "Z")
        b.append(f'<path d="{" ".join(pts)}" fill="#78350f" filter="url(#drop)"/>')
    if "crest" in back:
        b.append('<path d="M200 170 C210 90 250 70 270 40 C280 80 300 100 330 90 C320 120 340 150 350 170Z" fill="#f43f5e" filter="url(#drop)"/>')
    if "tuft" in back:
        b.append('<path d="M250 160 C240 110 260 90 280 70 C276 100 290 120 300 160Z" fill="url(#cfur)"/>')
    # body
    b.append('<ellipse cx="270" cy="530" rx="165" ry="140" fill="url(#cfur)" filter="url(#drop)"/>'
             f'<ellipse cx="270" cy="560" rx="105" ry="100" fill="{belly}"/>')
    if scarf:
        b.append(f'<path d="M150 420 C210 455 330 455 390 420 L396 450 C330 490 210 490 144 450Z" fill="{scarf}"/>'
                 f'<path d="M330 460 L350 540 L374 528 L356 452Z" fill="{scarf}" opacity="0.85"/>')
    b.append(_EARS.get(ears, "").replace("{inner}", ear_inner))
    # head
    b.append('<ellipse cx="270" cy="290" rx="165" ry="138" fill="url(#cfur)" filter="url(#drop)"/>'
             '<ellipse cx="230" cy="190" rx="70" ry="28" fill="url(#cshine)" transform="rotate(-15 230 190)"/>')
    if face:
        b.append(f'<ellipse cx="270" cy="345" rx="92" ry="62" fill="{face}"/>')
    b.append({
        "raccoon": '<path d="M140 280 C160 240 240 250 270 290 C300 250 380 240 400 280 C380 330 300 330 270 310 C240 330 160 330 140 280Z" fill="#1f2937"/>',
        "owl": '<circle cx="212" cy="292" r="62" fill="#fef3c7"/><circle cx="328" cy="292" r="62" fill="#fef3c7"/>',
        "sloth": '<ellipse cx="270" cy="300" rx="130" ry="95" fill="#f5e6d3"/>'
                 '<path d="M150 290 C170 260 230 270 245 300 C230 330 170 330 150 290Z M390 290 C370 260 310 270 295 300 C310 330 370 330 390 290Z" fill="#57534e"/>',
        "meerkat": '<ellipse cx="212" cy="292" rx="46" ry="52" fill="#57534e"/><ellipse cx="328" cy="292" rx="46" ry="52" fill="#57534e"/>',
        "puffin": '<path d="M140 300 C140 220 200 200 270 230 C340 200 400 220 400 300 C400 370 340 400 270 400 C200 400 140 370 140 300Z" fill="#f8fafc"/>',
    }.get(mask, ""))
    if ears == "floppy":
        b.append('<ellipse cx="115" cy="290" rx="42" ry="100" fill="#78350f" transform="rotate(18 115 290)" filter="url(#drop)"/>'
                 '<ellipse cx="425" cy="290" rx="42" ry="100" fill="#78350f" transform="rotate(-18 425 290)" filter="url(#drop)"/>')
    # eyes
    ey = 205 if ears == "frog" else eye_y
    b.append(eye(212, ey, 30, 36, *iris, look=look, cid="cL") + eye(328, ey, 30, 36, *iris, look=look, cid="cR"))
    if sleepy:
        b.append(f'<path d="M178 {ey - 4} C186 {ey - 44} 238 {ey - 44} 246 {ey - 4}Z M294 {ey - 4} C302 {ey - 44} 354 {ey - 44} 362 {ey - 4}Z" fill="url(#cfur)"/>'
                 f'<path d="M178 {ey - 4} L246 {ey - 4} M294 {ey - 4} L362 {ey - 4}" stroke="{INK}" stroke-width="5" stroke-linecap="round"/>')
    if glasses:
        b.append(f'<g fill="none" stroke="{INK}" stroke-width="6"><circle cx="212" cy="{ey}" r="46"/><circle cx="328" cy="{ey}" r="46"/>'
                 f'<path d="M258 {ey} L282 {ey}"/></g>')
    b.append(blush(176, 356) + blush(364, 356))
    # snout and mouth
    if snout == "nose":
        b.append(f'<ellipse cx="270" cy="340" rx="17" ry="12" fill="{nose_col}"/><ellipse cx="264" cy="335" rx="6" ry="3.5" fill="#ffffff" opacity="0.6"/>')
    elif snout == "beak":
        b.append('<path d="M236 326 Q270 310 304 326 L270 380Z" fill="url(#cbeak)" stroke="#9a3412" stroke-width="3" stroke-linejoin="round"/>')
    elif snout == "bill":
        b.append('<ellipse cx="270" cy="350" rx="62" ry="26" fill="url(#cbeak)" stroke="#c2410c" stroke-width="3"/>'
                 '<path d="M220 352 Q270 362 320 352" stroke="#c2410c" stroke-width="3" fill="none"/>')
    if snout in ("nose", "none"):
        b.append(_MOUTHS.get(mouth, ""))
    b.append(_HATS.get(hat, ""))
    # paws: one on the belly, one raised holding the prop
    hc = hand_col or "url(#cfur)"
    b.append(f'<path d="M400 500 C430 470 445 440 {HAND[0]} {HAND[1] + 20}" stroke="url(#cfur)" stroke-width="48" fill="none" stroke-linecap="round"/>')
    b.append(prop)
    b.append(f'<circle cx="{HAND[0]}" cy="{HAND[1]}" r="28" fill="{hc}" stroke="#000000" stroke-opacity="0.2" stroke-width="3"/>'
             f'<ellipse cx="200" cy="520" rx="34" ry="26" fill="{hc}" stroke="#000000" stroke-opacity="0.2" stroke-width="3"/>')
    return "\n  ".join(b)


# ---------------------------------------------------------------------------------------------------------
# A configurable anime boy or girl (head ~(275,270), raised hand at HAND), drawn like the AI & Data covers.
# ---------------------------------------------------------------------------------------------------------
_HAIR_BACK = {
    "pigtails": '<path d="M150 240 C90 290 80 390 120 450 C134 400 156 340 186 300Z M400 240 C460 290 470 390 430 450 C416 400 394 340 364 300Z" fill="url(#khair)" filter="url(#drop)"/>'
                '<circle cx="166" cy="252" r="12" fill="{acc}"/><circle cx="384" cy="252" r="12" fill="{acc}"/>',
    "long": '<path d="M160 230 C120 320 120 440 150 560 L400 560 C430 440 430 320 390 230Z" fill="url(#khair)" filter="url(#drop)"/>',
    "ponytail": '<path d="M370 190 C450 200 480 290 450 400 C440 330 420 280 380 260Z" fill="url(#khair)" filter="url(#drop)"/>'
                '<circle cx="380" cy="200" r="13" fill="{acc}"/>',
    "bob": '<path d="M160 240 C150 320 160 380 190 410 L360 410 C390 380 400 320 390 240Z" fill="url(#khair)" filter="url(#drop)"/>',
    "buns": '<circle cx="180" cy="150" r="44" fill="url(#khair)" filter="url(#drop)"/><circle cx="370" cy="150" r="44" fill="url(#khair)" filter="url(#drop)"/>',
}
_FRINGE = {
    "spiky": 'M168 262 C154 196 170 160 190 140 L174 104 L220 124 L230 78 L262 116 L294 74 L308 120 L346 96 L340 140 C366 160 380 200 370 262 C360 230 346 214 330 206 C324 220 312 228 298 232 C296 210 286 196 272 188 C264 208 248 222 230 228 C230 210 224 198 214 190 C200 210 190 236 184 262Z',
    "swept": 'M170 262 C156 170 220 120 280 122 C340 124 394 166 380 262 C370 220 350 196 320 186 C290 210 240 222 200 216 C190 230 180 246 176 262Z',
    "soft": 'M178 262 C166 170 224 128 274 128 C330 128 382 170 370 262 C362 236 354 220 340 208 C338 226 330 238 318 244 C316 218 304 198 288 186 C284 206 272 220 254 228 C256 206 250 190 240 180 C226 198 216 220 212 244 C200 232 194 216 192 204 C182 220 180 240 178 262Z',
    "curly": 'M172 262 C150 220 160 170 190 150 C186 120 220 100 246 112 C262 90 300 90 316 112 C344 100 376 124 370 152 C398 170 402 222 378 262 C370 236 356 220 340 214 C330 230 300 238 276 226 C252 238 222 232 210 214 C192 222 180 240 172 262Z',
}
_KID_HATS = {
    "cap": '<path d="M178 190 C182 110 368 110 372 190Z" fill="{acc}" filter="url(#drop)"/><path d="M300 186 C350 176 410 180 440 196 C410 208 340 206 300 200Z" fill="{acc}" opacity="0.85"/>',
    "beanie": '<path d="M172 200 C170 100 380 100 378 200Z" fill="{acc}" filter="url(#drop)"/><rect x="166" y="186" width="218" height="30" rx="14" fill="#ffffff" opacity="0.85"/><circle cx="275" cy="98" r="20" fill="#ffffff"/>',
    "headset": '<path d="M166 270 C150 140 400 140 384 270" stroke="#334155" stroke-width="14" fill="none"/><rect x="150" y="252" width="30" height="56" rx="12" fill="{acc}"/><rect x="370" y="252" width="30" height="56" rx="12" fill="{acc}"/><path d="M168 300 C180 360 220 370 250 368" stroke="#334155" stroke-width="6" fill="none"/><circle cx="254" cy="368" r="8" fill="#334155"/>',
    "hardhat": '<path d="M176 196 C176 100 374 100 374 196Z" fill="#facc15" filter="url(#drop)"/><rect x="156" y="188" width="238" height="22" rx="10" fill="#eab308"/><rect x="264" y="104" width="22" height="86" rx="8" fill="#fde047"/>',
    "wizard": '<path d="M160 200 L275 10 L390 200Z" fill="{acc}" filter="url(#drop)"/><ellipse cx="275" cy="200" rx="140" ry="22" fill="{acc}"/><use href="#spark" x="246" y="90" width="22" height="22"/><use href="#spark" x="290" y="140" width="16" height="16"/>',
    "headband": '<path d="M172 206 C220 180 330 180 378 206" stroke="{acc}" stroke-width="16" fill="none" stroke-linecap="round"/><path d="M372 204 L410 230 M372 210 L400 250" stroke="{acc}" stroke-width="10" stroke-linecap="round"/>',
    "flower": '<g transform="translate(360 180)"><circle r="14" cx="0" cy="-16" fill="{acc}"/><circle r="14" cx="15" cy="-5" fill="{acc}"/><circle r="14" cx="9" cy="13" fill="{acc}"/><circle r="14" cx="-9" cy="13" fill="{acc}"/><circle r="14" cx="-15" cy="-5" fill="{acc}"/><circle r="9" fill="#fde047"/></g>',
}


def kid(hair=("#334155", "#0f172a"), style="spiky", back=None, outfit=("#38bdf8", "#0369a1"), iris=("#78350f", "#fbbf24"),
        hat=None, acc="#f43f5e", glasses=False, mouth="grin", look=(10, 0), skin=("#fde3cf", "#f2c4a3"), prop="", collar=None):
    """An anime kid in the left half. style: spiky | swept | soft | curly (fringe). back: pigtails | long | ponytail |
    bob | buns | None. hat: cap | beanie | headset | hardhat | wizard | headband | flower | None. prop: at HAND."""
    b = [f'<defs>{grad("khair", *hair)}{grad("kout", *outfit)}{grad("kskin", *skin)}</defs>']
    if back:
        b.append(_HAIR_BACK[back].replace("{acc}", acc))
    b.append('<path d="M90 640 C96 500 150 450 220 440 L330 440 C400 450 454 500 460 640Z" fill="url(#kout)" filter="url(#drop)"/>'
             '<path d="M240 436 L310 436 L300 476 L250 476Z" fill="#e8b496"/>'
             '<path d="M220 446 C250 490 300 490 330 446" stroke="#000000" stroke-width="6" fill="none" opacity="0.18"/>')
    if collar:
        b.append(f'<path d="M226 444 L275 486 L324 444 L334 462 L275 512 L216 462Z" fill="{collar}"/>')
    b.append('<path d="M180 250 C180 146 370 146 370 250 C370 330 322 396 275 410 C228 396 180 330 180 250Z" fill="url(#kskin)" filter="url(#drop)"/>')
    b.append(blush(214, 330) + blush(336, 330))
    b.append(eye(230, 282, 28, 34, *iris, look=look, cid="kL") + eye(320, 282, 28, 34, *iris, look=look, cid="kR"))
    b.append(f'<path d="M200 236 C214 226 240 226 254 236 M296 236 C310 226 336 226 350 236" stroke="{hair[1]}" stroke-width="7" fill="none" stroke-linecap="round"/>')
    if glasses:
        b.append(f'<g fill="none" stroke="{INK}" stroke-width="5"><rect x="190" y="248" width="80" height="68" rx="20"/><rect x="280" y="248" width="80" height="68" rx="20"/><path d="M270 276 L280 276"/></g>')
    b.append({
        "grin": '<path d="M250 352 C262 376 296 376 308 352Z" fill="#9f1239"/><path d="M258 354 L300 354" stroke="#ffffff" stroke-width="5"/>',
        "smile": '<path d="M256 356 C266 370 290 370 300 356" stroke="#9f1239" stroke-width="5" fill="none" stroke-linecap="round"/>',
        "o": '<ellipse cx="278" cy="362" rx="11" ry="14" fill="#9f1239"/>',
        "open": '<path d="M254 352 C260 384 296 384 302 352Z" fill="#be123c"/>',
    }[mouth])
    b.append(f'<path d="{_FRINGE[style]}" fill="url(#khair)"/>')
    if hat:
        b.append(_KID_HATS[hat].replace("{acc}", acc))
    b.append(f'<path d="M400 500 C430 470 445 440 {HAND[0]} {HAND[1] + 20}" stroke="url(#kout)" stroke-width="48" fill="none" stroke-linecap="round"/>')
    b.append(prop)
    b.append(f'<circle cx="{HAND[0]}" cy="{HAND[1]}" r="27" fill="url(#kskin)" stroke="#d99b7a" stroke-width="2.5"/>')
    return "\n  ".join(b)


# ---------------------------------------------------------------------------------------------------------
# Props held at HAND. Each is a function of (accent colour, label) returning SVG; label may be "".
# ---------------------------------------------------------------------------------------------------------
def _t(x, y, s, size=20, fill="#ffffff", anchor="middle", fam=None, w=800):
    return (f'<text x="{x}" y="{y}" text-anchor="{anchor}" font-family="{fam or SANS}" font-size="{size}" '
            f'font-weight="{w}" fill="{fill}">{_esc(s)}</text>')


def prop(kind, col="#7c3aed", label=""):
    x, y = HAND
    if kind == "wheel":  # a ship's helm (Kubernetes, Helm)
        spokes = "".join(f'<path d="M{x + 30 + 74 * math.cos(a):.0f} {y - 90 + 74 * math.sin(a):.0f} L{x + 30 + 104 * math.cos(a):.0f} {y - 90 + 104 * math.sin(a):.0f}" stroke="#92400e" stroke-width="16" stroke-linecap="round"/>'
                         f'<path d="M{x + 30} {y - 90} L{x + 30 + 74 * math.cos(a):.0f} {y - 90 + 74 * math.sin(a):.0f}" stroke="#b45309" stroke-width="9"/>'
                         for a in [i * math.pi / 4 for i in range(8)])
        return (f'<g filter="url(#drop)">{spokes}<circle cx="{x + 30}" cy="{y - 90}" r="74" fill="none" stroke="#b45309" stroke-width="16"/>'
                f'<circle cx="{x + 30}" cy="{y - 90}" r="24" fill="{col}"/></g>')
    if kind == "box":  # a parcel / container / chart package
        return (f'<g filter="url(#drop)" transform="rotate(-8 {x + 30} {y - 70})"><rect x="{x - 40}" y="{y - 150}" width="150" height="120" rx="12" fill="{col}"/>'
                f'<path d="M{x - 40} {y - 112} H{x + 110}" stroke="#000" stroke-opacity="0.2" stroke-width="6"/>'
                f'<rect x="{x + 14}" y="{y - 150}" width="42" height="40" fill="#ffffff" opacity="0.5"/>'
                + (_t(x + 35, y - 58, label, 24) if label else "") + '</g>')
    if kind == "key":
        return (f'<g filter="url(#drop)" transform="rotate(-40 {x} {y})"><circle cx="{x + 40}" cy="{y - 60}" r="40" fill="none" stroke="{col}" stroke-width="18"/>'
                f'<path d="M{x + 40} {y - 20} V{y + 90} M{x + 40} {y + 50} h30 M{x + 40} {y + 78} h22" stroke="{col}" stroke-width="18" stroke-linecap="round"/></g>')
    if kind == "shield":
        return (f'<g filter="url(#drop)"><path d="M{x + 30} {y - 190} L{x + 120} {y - 156} C{x + 120} {y - 70} {x + 90} {y - 20} {x + 30} {y + 10} '
                f'C{x - 30} {y - 20} {x - 60} {y - 70} {x - 60} {y - 156}Z" fill="{col}" stroke="#ffffff" stroke-width="7"/>'
                + (_t(x + 30, y - 76, label, 26) if label else f'<path d="M{x} {y - 96} l24 24 l44 -50" stroke="#fff" stroke-width="12" fill="none" stroke-linecap="round"/>') + '</g>')
    if kind == "lens":  # magnifying glass
        return (f'<g filter="url(#drop)"><path d="M{x} {y} L{x + 50} {y - 60}" stroke="#78350f" stroke-width="18" stroke-linecap="round"/>'
                f'<circle cx="{x + 90}" cy="{y - 110}" r="62" fill="#e0f2fe" fill-opacity="0.65" stroke="{col}" stroke-width="14"/>'
                f'<path d="M{x + 60} {y - 140} q18 -16 40 -12" stroke="#ffffff" stroke-width="8" fill="none" stroke-linecap="round"/></g>')
    if kind == "wrench":
        return (f'<g filter="url(#drop)" transform="rotate(32 {x} {y})"><rect x="{x - 12}" y="{y - 150}" width="26" height="160" rx="12" fill="url(#metal)"/>'
                f'<path d="M{x - 40} {y - 210} a42 42 0 1 0 84 0 l-18 0 l0 24 l-48 0 l0 -24Z" fill="url(#metal)"/></g>')
    if kind == "bulb":
        return (f'<g filter="url(#drop)"><circle cx="{x + 20}" cy="{y - 120}" r="60" fill="#fde047"/><circle cx="{x + 20}" cy="{y - 120}" r="84" fill="#fde047" opacity="0.25"/>'
                f'<rect x="{x - 8}" y="{y - 68}" width="56" height="40" rx="8" fill="#94a3b8"/>'
                f'<path d="M{x} {y - 128} l12 22 l16 -30 l12 22" stroke="#b45309" stroke-width="5" fill="none"/></g>')
    if kind == "flag":
        return (f'<g filter="url(#drop)"><path d="M{x} {y + 10} V{y - 220}" stroke="#78350f" stroke-width="10" stroke-linecap="round"/>'
                f'<path d="M{x} {y - 220} C{x + 60} {y - 240} {x + 100} {y - 190} {x + 170} {y - 210} V{y - 130} C{x + 100} {y - 110} {x + 60} {y - 160} {x} {y - 140}Z" fill="{col}"/>'
                + (_t(x + 84, y - 162, label, 22) if label else "") + '</g>')
    if kind == "mug":
        return (f'<g filter="url(#drop)"><rect x="{x - 30}" y="{y - 120}" width="100" height="110" rx="14" fill="{col}"/>'
                f'<path d="M{x + 70} {y - 96} c40 0 40 60 0 60" stroke="{col}" stroke-width="14" fill="none"/>'
                f'<path d="M{x - 6} {y - 140} q10 -20 0 -40 M{x + 24} {y - 140} q10 -20 0 -40" stroke="#94a3b8" stroke-width="6" fill="none" stroke-linecap="round"/>'
                + (_t(x + 20, y - 56, label, 22) if label else "") + '</g>')
    if kind == "scroll":
        return (f'<g filter="url(#drop)" transform="rotate(-10 {x + 40} {y - 80})"><rect x="{x - 30}" y="{y - 170}" width="150" height="160" fill="#fef3c7"/>'
                f'<rect x="{x - 44}" y="{y - 184}" width="178" height="22" rx="11" fill="#d6b26a"/><rect x="{x - 44}" y="{y - 20}" width="178" height="22" rx="11" fill="#d6b26a"/>'
                + "".join(f'<path d="M{x - 10} {y - 140 + i * 24} H{x + 100}" stroke="{col}" stroke-width="5" stroke-linecap="round"/>' for i in range(5)) + '</g>')
    if kind == "book":
        return (f'<g filter="url(#drop)" transform="rotate(-12 {x + 40} {y - 70})"><rect x="{x - 20}" y="{y - 160}" width="130" height="160" rx="10" fill="{col}"/>'
                f'<rect x="{x - 20}" y="{y - 160}" width="22" height="160" rx="6" fill="#000" opacity="0.25"/>'
                + (_t(x + 56, y - 76, label, 24) if label else "") + '</g>')
    if kind == "lantern":
        return (f'<g filter="url(#drop)"><path d="M{x + 10} {y - 10} V{y - 40}" stroke="#334155" stroke-width="8"/>'
                f'<circle cx="{x + 10}" cy="{y - 110}" r="90" fill="#fde68a" opacity="0.3"/>'
                f'<rect x="{x - 30}" y="{y - 160}" width="80" height="110" rx="20" fill="#fde047" stroke="#334155" stroke-width="8"/>'
                f'<path d="M{x - 30} {y - 160} h80 l-10 -20 h-60Z" fill="#334155"/></g>')
    if kind == "balloon":
        return (f'<g filter="url(#drop)"><path d="M{x} {y} C{x + 20} {y - 60} {x - 10} {y - 100} {x + 20} {y - 150}" stroke="#64748b" stroke-width="3" fill="none"/>'
                f'<ellipse cx="{x + 30}" cy="{y - 220}" rx="62" ry="74" fill="{col}"/><ellipse cx="{x + 8}" cy="{y - 246}" rx="14" ry="22" fill="#ffffff" opacity="0.5"/>'
                + (_t(x + 30, y - 212, label, 26) if label else "") + '</g>')
    if kind == "wand":
        return (f'<g filter="url(#drop)"><path d="M{x} {y} L{x + 100} {y - 140}" stroke="#4c1d95" stroke-width="12" stroke-linecap="round"/>'
                f'<use href="#spark" x="{x + 70}" y="{y - 190}" width="64" height="64"/><use href="#spark" x="{x + 150}" y="{y - 140}" width="26" height="26"/>'
                f'<use href="#spark" x="{x + 40}" y="{y - 210}" width="20" height="20"/></g>')
    if kind == "pencil":
        return (f'<g filter="url(#drop)" transform="rotate(35 {x} {y})"><rect x="{x - 14}" y="{y - 200}" width="30" height="180" fill="{col}"/>'
                f'<path d="M{x - 14} {y - 20} L{x + 1} {y + 22} L{x + 16} {y - 20}Z" fill="#fde68a"/><rect x="{x - 14}" y="{y - 216}" width="30" height="20" rx="4" fill="#f9a8d4"/></g>')
    if kind == "padlock":
        return (f'<g filter="url(#drop)"><path d="M{x - 10} {y - 110} V{y - 150} a40 40 0 0 1 80 0 V{y - 110}" stroke="url(#metal)" stroke-width="16" fill="none"/>'
                f'<rect x="{x - 36}" y="{y - 116}" width="132" height="100" rx="16" fill="{col}"/><circle cx="{x + 30}" cy="{y - 72}" r="12" fill="#1f2937"/></g>')
    if kind == "telescope":
        return (f'<g filter="url(#drop)" transform="rotate(-62 {x} {y})"><rect x="{x - 20}" y="{y - 40}" width="180" height="46" rx="12" fill="{col}"/>'
                f'<rect x="{x + 150}" y="{y - 52}" width="40" height="70" rx="10" fill="#334155"/><rect x="{x - 50}" y="{y - 30}" width="40" height="26" rx="6" fill="#334155"/></g>')
    if kind == "envelope":
        return (f'<g filter="url(#drop)" transform="rotate(-10 {x + 40} {y - 80})"><rect x="{x - 40}" y="{y - 150}" width="170" height="112" rx="10" fill="#ffffff" stroke="{col}" stroke-width="5"/>'
                f'<path d="M{x - 40} {y - 150} L{x + 45} {y - 90} L{x + 130} {y - 150}" stroke="{col}" stroke-width="5" fill="none"/></g>')
    if kind == "plug":
        return (f'<g filter="url(#drop)" transform="rotate(-28 {x + 60} {y - 50})"><rect x="{x - 20}" y="{y - 90}" width="130" height="80" rx="16" fill="{col}"/>'
                f'<rect x="{x + 110}" y="{y - 76}" width="46" height="14" rx="5" fill="#cbd5e1"/><rect x="{x + 110}" y="{y - 40}" width="46" height="14" rx="5" fill="#cbd5e1"/>'
                + (_t(x + 45, y - 40, label, 24) if label else "") + '</g>')
    if kind == "sign":  # a placard with a word on it
        w = max(140, int(len(label) * 15) + 40)
        return (f'<g filter="url(#drop)" transform="rotate(-6 {x} {y - 120})"><path d="M{x} {y + 10} V{y - 90}" stroke="#78350f" stroke-width="12"/>'
                f'<rect x="{x - w / 2}" y="{y - 180}" width="{w}" height="90" rx="14" fill="{col}"/>'
                + _t(x, y - 124, label, 26, fam=MONO) + '</g>')
    raise KeyError(kind)
