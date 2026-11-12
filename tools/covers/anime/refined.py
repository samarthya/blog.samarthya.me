"""Refined anime covers (2026-11-12): a painted-style bust portrait instead of the chibi figures in kit.py.

What makes it "refined": an anime bust with layered eyes (lid shadow, iris gradient, ring, pupil, three highlights,
lashes), hair built from tapered locks with a shine band and a cast shadow on the forehead, cel shading on skin and
clothes, a rim light, and a scene behind it (halo, colour fields, bokeh, light rays, film grain). The post's content
sits on a frosted-glass panel; a small glowing "hologram" ties the figure to the topic.

Used by ground_up.py. Render: write(slug, alt, scene_svg) -> cover.svg + feature.png.
"""
import math
import pathlib
import subprocess
import sys
from html import escape as _esc

REPO = pathlib.Path(__file__).resolve().parents[3]
SANS = "Segoe UI, system-ui, -apple-system, Roboto, Helvetica, Arial, sans-serif"
MONO = "Consolas, Menlo, monospace"
INK = "#1e1b2e"


# ----------------------------------------------------------------------------------------------- scene
def scene_defs(sky, accent):
    s1, s2, s3 = sky
    return f'''<defs>
  <linearGradient id="sky" x1="0" y1="0" x2="0.35" y2="1"><stop offset="0" stop-color="{s1}"/><stop offset="0.55" stop-color="{s2}"/><stop offset="1" stop-color="{s3}"/></linearGradient>
  <radialGradient id="halo" cx="0.5" cy="0.5" r="0.5"><stop offset="0" stop-color="#ffffff" stop-opacity="0.95"/><stop offset="0.45" stop-color="#ffffff" stop-opacity="0.45"/><stop offset="1" stop-color="#ffffff" stop-opacity="0"/></radialGradient>
  <filter id="blur40" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="40"/></filter>
  <filter id="blur6" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="6"/></filter>
  <filter id="blur2" x="-20%" y="-20%" width="140%" height="140%"><feGaussianBlur stdDeviation="2"/></filter>
  <filter id="glow" x="-60%" y="-60%" width="220%" height="220%"><feGaussianBlur stdDeviation="5" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
  <filter id="shadow" x="-20%" y="-20%" width="140%" height="150%"><feDropShadow dx="0" dy="14" stdDeviation="18" flood-color="#3b0764" flood-opacity="0.18"/></filter>
  <filter id="figshadow" x="-20%" y="-20%" width="140%" height="140%"><feDropShadow dx="6" dy="10" stdDeviation="12" flood-color="#2e1065" flood-opacity="0.22"/></filter>
  <filter id="grain" x="0" y="0" width="100%" height="100%"><feTurbulence type="fractalNoise" baseFrequency="0.85" numOctaves="2" stitchTiles="stitch"/>
    <feColorMatrix values="0 0 0 0 0.2  0 0 0 0 0.1  0 0 0 0 0.3  0 0 0 0.09 0"/></filter>
  <linearGradient id="ray" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#ffffff" stop-opacity="0.55"/><stop offset="1" stop-color="#ffffff" stop-opacity="0"/></linearGradient>
  <linearGradient id="glass" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#ffffff" stop-opacity="0.86"/><stop offset="1" stop-color="#ffffff" stop-opacity="0.70"/></linearGradient>
  <linearGradient id="dglass" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#1e1b4b" stop-opacity="0.94"/><stop offset="1" stop-color="#0f172a" stop-opacity="0.94"/></linearGradient>
  <linearGradient id="acc" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{accent}"/><stop offset="1" stop-color="{accent}" stop-opacity="0.55"/></linearGradient>
</defs>'''


def backdrop(blobs, halo=(300, 280, 300)):
    """Sky, soft colour fields, light rays, bokeh and a halo behind the head."""
    hx, hy, hr = halo
    b = ['<rect width="1200" height="630" fill="url(#sky)"/>']
    b += [f'<circle cx="{x}" cy="{y}" r="{r}" fill="{c}" opacity="{o}" filter="url(#blur40)"/>' for x, y, r, c, o in blobs]
    b.append('<g opacity="0.55">'
             '<path d="M-40 -20 L260 -20 L760 630 L520 630Z" fill="url(#ray)" opacity="0.35"/>'
             '<path d="M300 -20 L380 -20 L900 630 L820 630Z" fill="url(#ray)" opacity="0.25"/>'
             '<path d="M480 -20 L520 -20 L1080 630 L1040 630Z" fill="url(#ray)" opacity="0.2"/></g>')
    b.append(f'<circle cx="{hx}" cy="{hy}" r="{hr}" fill="url(#halo)"/>')
    bokeh = [(80, 110, 26, .35), (140, 520, 18, .3), (520, 80, 14, .4), (560, 560, 30, .22), (1120, 70, 22, .35),
             (1160, 560, 34, .25), (610, 330, 9, .5), (70, 330, 12, .4), (980, 600, 14, .35), (860, 40, 10, .45)]
    b += [f'<circle cx="{x}" cy="{y}" r="{r}" fill="#ffffff" opacity="{o}" filter="url(#blur2)"/>'
          f'<circle cx="{x}" cy="{y}" r="{r}" fill="none" stroke="#ffffff" stroke-opacity="{o}" stroke-width="1.5"/>'
          for x, y, r, o in bokeh]
    # tiny floating motes
    motes = [(455, 140), (500, 210), (430, 90), (590, 470), (50, 220), (230, 60), (1010, 120), (700, 600)]
    b += [f'<circle cx="{x}" cy="{y}" r="2.2" fill="#ffffff" opacity="0.9"/>' for x, y in motes]
    return "\n".join(b)


def grain():
    return '<rect width="1200" height="630" filter="url(#grain)" opacity="1" style="mix-blend-mode:multiply"/>'


# ----------------------------------------------------------------------------------------------- figure
def _eye(gid, iris):
    """One left eye drawn around (0, 0); the right eye reuses it mirrored. iris = (dark, mid, light)."""
    d, m, l = iris
    sclera = "M-31 -3 C-27 -24 -2 -33 19 -24 C28 -18 29 -5 25 6 C19 22 1 29 -13 25 C-24 21 -31 11 -31 -3Z"
    return f'''<defs>
    <clipPath id="{gid}c"><path d="{sclera}"/></clipPath>
    <linearGradient id="{gid}i" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{d}"/><stop offset="0.5" stop-color="{m}"/><stop offset="1" stop-color="{l}"/></linearGradient>
  </defs>
  <path d="{sclera}" fill="#fffdfb"/>
  <g clip-path="url(#{gid}c)">
    <ellipse cx="-1" cy="3" rx="19.5" ry="26" fill="url(#{gid}i)"/>
    <ellipse cx="-1" cy="3" rx="19.5" ry="26" fill="none" stroke="{d}" stroke-width="2"/>
    <path d="M-15 14 C-8 24 8 24 15 12 C10 18 -8 20 -15 14Z" fill="{l}" opacity="0.9"/>
    <ellipse cx="-1" cy="5" rx="8.5" ry="12" fill="#0b0a17"/>
    <path d="M-34 -30 L32 -30 L32 -10 C14 -24 -14 -22 -34 -4Z" fill="{d}" opacity="0.38"/>
    <ellipse cx="-8" cy="-7" rx="6.5" ry="8.5" fill="#ffffff"/>
    <circle cx="8" cy="13" r="3.2" fill="#ffffff"/>
    <circle cx="4" cy="-10" r="1.8" fill="#ffffff" opacity="0.85"/>
  </g>
  <path d="M-38 0 C-33 -27 -3 -40 22 -27 C26 -24 28 -20 27 -15 C6 -31 -22 -25 -31 -1 Z" fill="{INK}"/>
  <path d="M-31 -3 L-44 -11 L-35 -14Z M-29 -10 L-41 -20 L-31 -19Z" fill="{INK}"/>
  <path d="M-13 25 C0 29 14 22 22 9" stroke="{INK}" stroke-width="1.6" fill="none" opacity="0.55" stroke-linecap="round"/>
  <path d="M-27 -32 C-12 -42 10 -40 21 -32" stroke="{INK}" stroke-width="1.4" fill="none" opacity="0.3" stroke-linecap="round"/>'''


def _fringe(tips, valleys, dy=0):
    """Front-hair edge from the left temple to the right, as tapered curved locks."""
    p = f"M{valleys[0][0]} {valleys[0][1] + dy}"
    for (tx, ty), (vx, vy) in zip(tips, valleys[1:]):
        lean = 7 if tx < 300 else -7
        p += (f" Q{tx - lean - 4} {ty - 34 + dy} {tx} {ty + dy}"
              f" Q{tx + lean + 2} {ty - 40 + dy} {vx} {vy + dy}")
    return p


HAIR = {
    # tips/valleys of the fringe and which side locks / back mass to draw
    "short": dict(tips=[(222, 262), (246, 246), (272, 262), (298, 238), (322, 256), (348, 244), (374, 262)],
                  valleys=[(206, 236), (234, 200), (258, 206), (286, 192), (310, 198), (336, 196), (360, 204), (394, 236)],
                  side=(330, 330), back="short"),
    "messy": dict(tips=[(218, 270), (240, 244), (266, 266), (292, 236), (320, 262), (344, 238), (372, 266), (392, 250)],
                  valleys=[(200, 230), (228, 196), (254, 210), (280, 186), (306, 204), (332, 190), (358, 208), (382, 200), (400, 228)],
                  side=(318, 318), back="messy"),
    "long": dict(tips=[(226, 272), (254, 254), (282, 268), (306, 246), (334, 264), (362, 252), (382, 276)],
                 valleys=[(206, 236), (240, 202), (266, 210), (294, 196), (320, 204), (348, 200), (372, 210), (396, 236)],
                 side=(420, 420), back="long"),
    "bob": dict(tips=[(228, 266), (256, 256), (284, 264), (312, 252), (340, 264), (368, 256), (384, 270)],
                valleys=[(206, 236), (242, 206), (270, 210), (298, 200), (326, 206), (354, 202), (376, 214), (396, 236)],
                side=(372, 372), back="bob"),
    "ponytail": dict(tips=[(230, 268), (262, 250), (292, 262), (322, 246), (352, 262), (380, 270)],
                     valleys=[(206, 236), (246, 204), (278, 206), (308, 196), (338, 204), (366, 210), (396, 236)],
                     side=(360, 360), back="ponytail"),
}

_BACK = {
    "short": "M196 262 C178 150 236 100 300 100 C364 100 422 150 404 262 C406 300 404 336 396 368 L384 344 L372 376 L228 376 L216 344 L204 368 C196 336 194 300 196 262Z",
    "messy": "M192 266 C170 150 232 92 300 94 C370 92 432 150 408 266 C412 304 410 340 402 376 L388 350 L378 386 L222 386 L212 350 L198 376 C190 340 188 304 192 266Z",
    "long": "M194 226 C182 128 240 94 300 94 C360 94 418 128 406 226 C412 340 424 480 462 640 L138 640 C176 480 188 340 194 226Z",
    "bob": "M194 230 C182 130 240 96 300 96 C360 96 418 130 406 230 C410 300 414 360 408 404 C390 420 360 418 340 470 L260 470 C240 418 210 420 192 404 C186 360 190 300 194 230Z",
    "ponytail": "M196 262 C178 150 236 100 300 100 C364 100 422 150 404 262 C406 300 404 336 396 368 L384 344 L372 376 L228 376 L216 344 L204 368 C196 336 194 300 196 262Z",
}


def figure(hair_style, hair, iris, skin=("#ffe8d9", "#f5c6ad", "#e7a993"), outfit=("#4338ca", "#312e81"),
           shirt="#f8fafc", acc="#f472b6", glasses=False, headphones=False, clip=False, earring=False, tie=None,
           mouth="smile"):
    """Bust portrait centred on x=300 (head ~y 280, shoulders to the bottom edge). hair/iris = (light, mid, dark)."""
    hl, hm, hd = hair
    sk, sks, skd = skin
    oc, od = outfit
    H = HAIR[hair_style]
    tips, valleys = H["tips"], H["valleys"]
    face = "M212 240 C210 318 238 378 300 414 C362 378 390 318 388 240 C388 168 350 140 300 140 C250 140 212 168 212 240Z"
    b = [f'''<defs>
  <linearGradient id="fhair" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{hl}"/><stop offset="0.45" stop-color="{hm}"/><stop offset="1" stop-color="{hd}"/></linearGradient>
  <linearGradient id="fhairback" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{hm}"/><stop offset="1" stop-color="{hd}"/></linearGradient>
  <linearGradient id="fskin" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{sk}"/><stop offset="1" stop-color="{sks}"/></linearGradient>
  <linearGradient id="fout" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{oc}"/><stop offset="1" stop-color="{od}"/></linearGradient>
  <clipPath id="fface"><path d="{face}"/></clipPath>
</defs>''']
    g = ['<g filter="url(#figshadow)">']
    # back hair
    g.append(f'<path d="{_BACK[H["back"]]}" fill="url(#fhairback)" stroke="{hd}" stroke-width="2" stroke-linejoin="round"/>')
    if H["back"] == "ponytail":
        g.append(f'<path d="M380 170 C470 170 500 260 488 380 C484 440 470 500 446 540 C452 470 448 400 430 340 C418 300 400 270 380 250Z" fill="url(#fhairback)"/>'
                 f'<path d="M402 200 C452 230 470 300 462 380" stroke="{hl}" stroke-width="3" fill="none" opacity="0.5"/>'
                 f'<ellipse cx="392" cy="182" rx="14" ry="18" fill="{acc}" transform="rotate(30 392 182)"/>')
    # body
    g.append(f'<path d="M84 640 C84 560 110 512 200 492 L250 480 L350 480 L400 492 C490 512 516 560 516 640Z" fill="url(#fout)" stroke="{od}" stroke-width="2"/>')
    g.append(f'<path d="M262 462 L300 528 L338 462 L356 474 L300 556 L244 474Z" fill="{shirt}"/>')
    if tie:
        g.append(f'<path d="M292 530 L308 530 L314 600 L300 618 L286 600Z" fill="{tie}"/><path d="M290 518 L310 518 L306 534 L294 534Z" fill="{tie}"/>')
    g.append(f'<path d="M244 474 L300 556 L270 640 L214 640 C226 570 232 520 244 474Z" fill="{od}" opacity="0.55"/>'
             f'<path d="M356 474 L300 556 L330 640 L386 640 C374 570 368 520 356 474Z" fill="{od}" opacity="0.35"/>')
    g.append(f'<path d="M244 474 L300 556 M356 474 L300 556" stroke="{od}" stroke-width="3" fill="none"/>'
             '<circle cx="300" cy="590" r="0" fill="none"/>'
             f'<circle cx="252" cy="600" r="6" fill="{od}"/><circle cx="252" cy="600" r="2.5" fill="#ffffff" opacity="0.5"/>'
             '')
    g.append('<path d="M200 486 C240 470 360 470 400 486 C380 520 220 520 200 486Z" fill="#000000" opacity="0.10" filter="url(#blur6)"/>')
    g.append('<path d="M370 480 C436 504 482 552 492 630" stroke="#ffffff" stroke-opacity="0.18" stroke-width="3" fill="none" stroke-linecap="round"/>')
    # neck
    g.append(f'<path d="M268 380 L266 470 C288 484 312 484 334 470 L332 380Z" fill="url(#fskin)"/>'
             f'<path d="M268 392 C286 428 314 428 332 392 L333 448 C312 460 288 460 267 448Z" fill="{skd}" opacity="0.55"/>')
    if headphones:
        g.append(f'<path d="M228 470 C232 520 368 520 372 470" stroke="#cbd5e1" stroke-width="10" fill="none"/><path d="M228 470 C232 520 368 520 372 470" stroke="#ffffff" stroke-width="3" fill="none" opacity="0.6"/>'
                 f'<rect x="206" y="446" width="40" height="52" rx="16" fill="{acc}" transform="rotate(-20 226 472)"/>'
                 f'<rect x="354" y="446" width="40" height="52" rx="16" fill="{acc}" transform="rotate(20 374 472)"/>'
                 '<rect x="216" y="456" width="20" height="32" rx="8" fill="#ffffff" opacity="0.35" transform="rotate(-20 226 472)"/>')
    # ears
    g.append(f'<ellipse cx="212" cy="300" rx="12" ry="22" fill="{sks}"/><ellipse cx="388" cy="300" rx="12" ry="22" fill="{sks}"/>')
    if earring:
        g.append(f'<circle cx="386" cy="326" r="5" fill="{acc}"/><path d="M386 331 L386 346" stroke="{acc}" stroke-width="2"/><circle cx="386" cy="350" r="4" fill="#ffffff" stroke="{acc}" stroke-width="2"/>')
    # face + shading
    g.append(f'<path d="{face}" fill="url(#fskin)" stroke="{skd}" stroke-width="1.8"/>')
    g.append(f'<g clip-path="url(#fface)">'
             f'<path d="M212 300 C220 360 250 396 300 414 C262 392 236 356 226 300Z" fill="{sks}" opacity="0.7"/>'
             f'<path d="{_fringe(tips, valleys, 16)} L400 120 L200 120Z" fill="{skd}" opacity="0.5" filter="url(#blur2)"/>'
             f'</g>')
    # blush with hatching
    for cx in (246, 354):
        g.append(f'<ellipse cx="{cx}" cy="338" rx="24" ry="10" fill="#ff8fa3" opacity="0.45" filter="url(#blur6)"/>'
                 f'<path d="M{cx - 12} 342 l6 -8 M{cx - 3} 342 l6 -8 M{cx + 6} 342 l6 -8" stroke="#f472b6" stroke-width="1.6" stroke-linecap="round" opacity="0.6"/>')
    # eyes
    g.append(f'<g transform="translate(258 292) scale(1.1)">{_eye("eL", iris)}</g>')
    g.append(f'<g transform="translate(342 292) scale(-1.1 1.1)">{_eye("eR", iris)}</g>')
    # nose and mouth
    g.append(f'<path d="M302 318 L298 336 L305 338" stroke="{skd}" stroke-width="2.2" fill="none" stroke-linecap="round" stroke-linejoin="round"/>')
    g.append({
        "smile": f'<path d="M284 364 Q300 375 316 364" stroke="#9f1239" stroke-width="3" fill="none" stroke-linecap="round"/>'
                 f'<path d="M292 372 Q300 376 308 372" stroke="{skd}" stroke-width="2" fill="none" opacity="0.6"/>',
        "open": '<path d="M286 362 Q300 362 314 362 Q312 380 300 382 Q288 380 286 362Z" fill="#9f1239"/>'
                '<path d="M290 374 Q300 382 310 374 Q306 381 300 381 Q294 381 290 374Z" fill="#fb7185"/>',
        "soft": f'<path d="M290 366 Q300 371 310 366" stroke="#9f1239" stroke-width="2.6" fill="none" stroke-linecap="round"/>',
    }[mouth])
    if glasses:
        g.append(f'<g fill="#ffffff" fill-opacity="0.12" stroke="{INK}" stroke-width="3.2">'
                 '<rect x="218" y="258" width="80" height="66" rx="22"/><rect x="302" y="258" width="80" height="66" rx="22"/></g>'
                 f'<path d="M298 284 Q300 280 302 284 M218 278 L206 274 M382 278 L394 274" stroke="{INK}" stroke-width="3" fill="none"/>'
                 '<path d="M230 270 L250 262 M314 270 L334 262" stroke="#ffffff" stroke-width="3" opacity="0.8" stroke-linecap="round"/>')
    # front hair: crown + fringe
    g.append(f'<path d="{_fringe(tips, valleys)} C410 150 362 104 300 104 C238 104 190 150 {valleys[0][0]} {valleys[0][1]}Z" fill="url(#fhair)" stroke="{hd}" stroke-width="1.8" stroke-linejoin="round"/>')
    # side locks framing the face
    sl, sr = H["side"]
    g.append(f'<path d="M206 236 C196 280 198 {sl - 40} 214 {sl} C218 {sl - 50} 222 300 236 262Z" fill="url(#fhair)"/>'
             f'<path d="M394 236 C404 280 402 {sr - 40} 386 {sr} C382 {sr - 50} 378 300 364 262Z" fill="url(#fhair)"/>'
             f'<path d="M206 236 C196 280 198 {sl - 40} 214 {sl} M394 236 C404 280 402 {sr - 40} 386 {sr}" stroke="{hd}" stroke-width="1.8" fill="none"/>')
    # strand lines and shine band
    for (tx, ty) in tips[1::2]:
        g.append(f'<path d="M{300 + (tx - 300) * 0.4:.0f} 120 Q{(tx + 300) / 2:.0f} {ty - 70} {tx} {ty - 8}" stroke="{hd}" stroke-width="1.4" fill="none" opacity="0.22"/>')
    g.append('<path d="M228 176 Q300 120 372 176 Q300 150 228 176Z" fill="#ffffff" opacity="0.30" filter="url(#blur2)"/>')
    g.append(f'<path d="M236 168 Q300 128 364 168" stroke="{hl}" stroke-width="2" fill="none" opacity="0.7"/>')
    if clip:
        g.append(f'<g transform="rotate(-25 236 214)"><rect x="216" y="206" width="44" height="12" rx="6" fill="{acc}"/>'
                 '<rect x="220" y="208" width="14" height="4" rx="2" fill="#ffffff" opacity="0.6"/></g>')
    g.append("</g>")
    return "\n".join(b + g)


# ----------------------------------------------------------------------------------------------- holograms
def holo(kind, accent, x=540, y=200):
    """A small glowing symbol beside the figure."""
    c = accent
    inner = {
        "vector": f'<path d="M-40 40 L-40 -50 M-40 40 L50 40" stroke="{c}" stroke-width="2" opacity="0.6"/>'
                  f'<path d="M-40 40 L20 -30" stroke="{c}" stroke-width="4" stroke-linecap="round"/><path d="M20 -30 L6 -24 L14 -14Z" fill="{c}"/>'
                  f'<path d="M-40 40 L40 0" stroke="#22d3ee" stroke-width="4" stroke-linecap="round"/><path d="M40 0 L26 -2 L30 10Z" fill="#22d3ee"/>'
                  f'<path d="M-16 12 A30 30 0 0 0 -22 18" stroke="#f59e0b" stroke-width="3" fill="none"/>',
        "matrix": "".join(f'<rect x="{-42 + j * 22}" y="{-42 + i * 22}" width="18" height="18" rx="4" fill="{c}" opacity="{0.25 + 0.6 * ((i * 5 + j * 3) % 4) / 4:.2f}"/>'
                          for i in range(4) for j in range(4)),
        "bars": "".join(f'<rect x="{-48 + i * 20}" y="{40 - h}" width="14" height="{h}" rx="3" fill="{c}" opacity="{0.4 + h / 160:.2f}"/>'
                        for i, h in enumerate([12, 30, 64, 84, 56, 26])) + f'<path d="M-50 30 C-30 20 -18 -40 0 -44 C18 -40 30 10 70 30" stroke="#22d3ee" stroke-width="3" fill="none"/>',
        "chip": f'<rect x="-36" y="-36" width="72" height="72" rx="10" fill="none" stroke="{c}" stroke-width="3"/>'
                f'<rect x="-20" y="-20" width="40" height="40" rx="5" fill="{c}" opacity="0.5"/>'
                + "".join(f'<path d="M{p} -36 V-50 M{p} 36 V50 M-36 {p} H-50 M36 {p} H50" stroke="{c}" stroke-width="3" stroke-linecap="round"/>' for p in (-20, 0, 20)),
        "stars": f'<path d="M-46 30 L-14 -20 L22 6 L50 -40" stroke="{c}" stroke-width="2" fill="none" opacity="0.7"/>'
                 + "".join(f'<path transform="translate({sx} {sy}) scale({s})" d="M0 -10 Q1.5 -1.5 10 0 Q1.5 1.5 0 10 Q-1.5 1.5 -10 0 Q-1.5 -1.5 0 -10Z" fill="#ffffff"/>'
                           for sx, sy, s in [(-46, 30, 0.9), (-14, -20, 1.2), (22, 6, 0.8), (50, -40, 1.5)]),
        "check": "".join(f'<rect x="-46" y="{-44 + i * 30}" width="20" height="20" rx="5" fill="none" stroke="{c}" stroke-width="2.5"/>'
                         f'<path d="M-42 {-34 + i * 30} l5 6 l9 -12" stroke="{"#22c55e" if i != 2 else "#f97316"}" stroke-width="3" fill="none" stroke-linecap="round"/>'
                         f'<rect x="-16" y="{-38 + i * 30}" width="{56 - (i % 2) * 14}" height="8" rx="4" fill="{c}" opacity="0.45"/>' for i in range(3)),
    }[kind]
    return (f'<g transform="translate({x} {y})">'
            f'<circle r="74" fill="#ffffff" opacity="0.35"/><circle r="74" fill="none" stroke="{c}" stroke-opacity="0.35" stroke-width="1.5" stroke-dasharray="3 6"/>'
            f'<g filter="url(#glow)">{inner}</g></g>')


# ----------------------------------------------------------------------------------------------- panels
def kicker(x, y, text, accent):
    return (f'<text x="{x}" y="{y}" font-family="{SANS}" font-size="17" font-weight="700" letter-spacing="3.5" fill="{accent}">{_esc(text.upper())}</text>'
            f'<rect x="{x}" y="{y + 12}" width="56" height="3" rx="1.5" fill="{accent}"/>')


def steps_panel(x, y, w, title, rows, accent):
    h = 86 + 70 * len(rows)
    b = [f'<g filter="url(#shadow)"><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="26" fill="url(#glass)" stroke="#ffffff" stroke-width="2"/></g>',
         f'<rect x="{x + 1}" y="{y + 1}" width="{w - 2}" height="40" rx="25" fill="#ffffff" opacity="0.35"/>',
         f'<text x="{x + 34}" y="{y + 56}" font-family="{SANS}" font-size="30" font-weight="800" fill="{INK}">{_esc(title)}</text>']
    for i, (label, value) in enumerate(rows):
        ry = y + 86 + i * 70
        b.append(f'<line x1="{x + 34}" y1="{ry}" x2="{x + w - 34}" y2="{ry}" stroke="{INK}" stroke-opacity="0.09" stroke-width="1.5"/>')
        b.append(f'<circle cx="{x + 54}" cy="{ry + 35}" r="17" fill="none" stroke="{accent}" stroke-width="2"/>'
                 f'<text x="{x + 54}" y="{ry + 41}" text-anchor="middle" font-family="{SANS}" font-size="16" font-weight="800" fill="{accent}">{i + 1}</text>')
        b.append(f'<text x="{x + 88}" y="{ry + 43}" font-family="{SANS}" font-size="24" font-weight="700" fill="{INK}">{_esc(label)}</text>')
        b.append(f'<text x="{x + w - 34}" y="{ry + 43}" text-anchor="end" font-family="{MONO}" font-size="21" font-weight="700" fill="{accent}">{_esc(value)}</text>')
    return "\n".join(b), h


def term_panel(x, y, w, title, lines, accent):
    """Dark glass terminal. lines: str or (text, colour)."""
    h = 74 + 34 * len(lines)
    b = [f'<g filter="url(#shadow)"><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="22" fill="url(#dglass)" stroke="#ffffff" stroke-opacity="0.18" stroke-width="1.5"/></g>',
         f'<circle cx="{x + 30}" cy="{y + 28}" r="6.5" fill="#f87171"/><circle cx="{x + 52}" cy="{y + 28}" r="6.5" fill="#fbbf24"/><circle cx="{x + 74}" cy="{y + 28}" r="6.5" fill="#4ade80"/>',
         f'<text x="{x + w / 2}" y="{y + 34}" text-anchor="middle" font-family="{MONO}" font-size="16" font-weight="700" fill="#a5b4fc" opacity="0.85">{_esc(title)}</text>',
         f'<line x1="{x}" y1="{y + 54}" x2="{x + w}" y2="{y + 54}" stroke="#ffffff" stroke-opacity="0.08"/>']
    ty = y + 92
    for ln in lines:
        text, col = (ln, "#e2e8f0") if isinstance(ln, str) else ln
        if text.startswith("$ "):
            b.append(f'<text xml:space="preserve" x="{x + 30}" y="{ty}" font-family="{MONO}" font-size="19" font-weight="700">'
                     f'<tspan fill="#4ade80">$ </tspan><tspan fill="#f8fafc">{_esc(text[2:])}</tspan></text>')
        elif text:
            b.append(f'<text xml:space="preserve" x="{x + 30}" y="{ty}" font-family="{MONO}" font-size="19" font-weight="700" fill="{col}">{_esc(text)}</text>')
        ty += 34
    return "\n".join(b), h


def chips(x, y, items, accent):
    b, cx = [], x
    for it in items:
        w = int(len(it) * 10.4) + 40
        b.append(f'<rect x="{cx}" y="{y}" width="{w}" height="40" rx="20" fill="#ffffff" fill-opacity="0.75" stroke="{accent}" stroke-opacity="0.55" stroke-width="1.5"/>'
                 f'<text x="{cx + w / 2}" y="{y + 26}" text-anchor="middle" font-family="{MONO}" font-size="17" font-weight="700" fill="{accent}">{_esc(it)}</text>')
        cx += w + 12
    return "\n".join(b)


# ----------------------------------------------------------------------------------------------- output
def write(slug, alt, sky, accent, blobs, body):
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 630" width="1200" height="630">\n'
           f'<title>{_esc(alt)}</title>\n{scene_defs(sky, accent)}\n{backdrop(blobs)}\n{body}\n</svg>\n')  # grain() quadruples the PNG size for little visible gain
    p = REPO / "content" / "posts" / slug / "cover.svg"
    p.write_text(svg, encoding="utf-8")
    subprocess.run([sys.executable, "-I", str(REPO / "tools/titles/svg_to_png.py"), str(p)], check=True)
