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
