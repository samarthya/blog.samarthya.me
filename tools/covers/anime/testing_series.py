"""Anime covers for "Testing code an AI wrote" (parts 1-4): a different character in each post.
Part 1 detective cat, part 2 bear chef, part 3 startled girl, part 4 a thinking server and a sly fox.
Run from the repo root: python tools/covers/anime/testing_series.py [slug ...]"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from kit import *  # noqa: E402,F403  (svg pieces: sparkles, eye, blush, card, pill, arrow, grad, write, MONO, SANS, INK)

_kit_eye = eye


def eye(*a, **k):
    """These covers were drawn with a slightly smaller highlight."""
    return _kit_eye(*a, hl=0.22, **k)


HAND_FONT = "Segoe Print, Comic Sans MS, Segoe UI, sans-serif"


def bubble(cx, cy, rx, ry, tail):
    """A cloud-shaped thought bubble with trailing dots toward `tail`."""
    tx, ty = tail
    puffs = "".join(
        f'<circle cx="{cx + rx * dx:.0f}" cy="{cy + ry * dy:.0f}" r="{r:.0f}"/>'
        for dx, dy, r in [(-0.7, -0.35, ry * 0.6), (-0.2, -0.7, ry * 0.62), (0.35, -0.65, ry * 0.6),
                          (0.75, -0.25, ry * 0.55), (0.7, 0.4, ry * 0.5), (0.1, 0.65, ry * 0.55), (-0.6, 0.45, ry * 0.5)])
    mx, my = (cx + tx) / 2, (cy + ry * 0.8 + ty) / 2
    return f'''
  <g filter="url(#drop)" fill="#ffffff">
    <ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}"/>{puffs}
    <circle cx="{mx:.0f}" cy="{my:.0f}" r="13"/><circle cx="{tx}" cy="{ty}" r="8"/>
  </g>'''


# =====================================================================
# Part 1: a detective cat reading the code through a magnifying glass
# =====================================================================
code_lines = []
y = 170
rows = [("def perform_action(", None), ("    if action == 'recycle':", None), ("        send2trash(file_path)", "#ef4444"),
        ("    elif action == 'quarantine':", None), ("        shutil.move(file_path, dest)", "#ef4444"),
        ("    elif action == 'delete':", None), ("        os.remove(file_path)", "#ef4444"),
        ("", None), ("def restore(log_file):", None), ("    shutil.move(new, original)", "#ef4444"),
        ("", None), ("def scan(paths):", None), ("    # only reads files", None)]
for text, hl in rows:
    if hl:
        code_lines.append(f'<rect x="62" y="{y - 22}" width="392" height="30" rx="6" fill="#fee2e2"/>')
    if text:
        code_lines.append(f'<text xml:space="preserve" x="74" y="{y}" font-family="{MONO}" font-size="19" font-weight="700" '
                          f'fill="{hl or "#475569"}">{text}</text>')
    y += 32
paper = f'''
  <g filter="url(#drop)" transform="rotate(-3 260 350)">
    <rect x="40" y="110" width="440" height="470" rx="16" fill="#ffffff"/>
    <rect x="40" y="110" width="440" height="34" rx="16" fill="#e2e8f0"/><rect x="40" y="128" width="440" height="16" fill="#e2e8f0"/>
    <circle cx="64" cy="127" r="6" fill="#ef4444"/><circle cx="84" cy="127" r="6" fill="#f59e0b"/><circle cx="104" cy="127" r="6" fill="#22c55e"/>
    <text x="130" y="133" font-family="{MONO}" font-size="16" font-weight="700" fill="#334155">cleaner.py</text>
    {"".join(code_lines)}
  </g>'''

cat = f'''
  <defs>{grad("fur", "#fdba74", "#ea580c")}{grad("tweed", "#a16207", "#713f12")}
    <pattern id="check" width="16" height="16" patternUnits="userSpaceOnUse"><rect width="16" height="16" fill="url(#tweed)"/>
      <path d="M0 8 H16 M8 0 V16" stroke="#fde68a" stroke-width="1.5" opacity="0.45"/></pattern></defs>
  <!-- tail -->
  <path d="M880 560 C990 560 1060 480 1030 380 C1020 350 1060 330 1070 360 C1100 470 1030 600 880 600Z" fill="url(#fur)" filter="url(#drop)"/>
  <path d="M1036 372 C1030 352 1058 336 1068 358 L1060 380Z" fill="#7c2d12" opacity="0.5"/>
  <!-- body -->
  <ellipse cx="780" cy="520" rx="160" ry="135" fill="url(#fur)" filter="url(#drop)"/>
  <ellipse cx="780" cy="545" rx="86" ry="96" fill="#fff7ed"/>
  <path d="M700 420 C690 440 692 470 700 490 M860 420 C870 440 868 470 860 490" stroke="#9a3412" stroke-width="7" fill="none" stroke-linecap="round" opacity="0.5"/>
  <!-- ears -->
  <path d="M640 250 L652 120 L740 200Z" fill="url(#fur)"/><path d="M660 225 L666 152 L716 200Z" fill="#fda4af"/>
  <path d="M920 250 L908 120 L820 200Z" fill="url(#fur)"/><path d="M900 225 L894 152 L844 200Z" fill="#fda4af"/>
  <!-- head -->
  <ellipse cx="780" cy="310" rx="160" ry="128" fill="url(#fur)" filter="url(#drop)"/>
  <path d="M700 250 C710 262 712 276 708 290 M780 236 L780 270 M860 250 C850 262 848 276 852 290" stroke="#9a3412" stroke-width="8" fill="none" stroke-linecap="round" opacity="0.55"/>
  <ellipse cx="780" cy="380" rx="72" ry="44" fill="#fff7ed"/>
  <!-- deerstalker -->
  <path d="M672 222 C676 136 884 136 888 222Z" fill="url(#check)" filter="url(#drop)"/>
  <path d="M640 228 C700 206 860 206 920 228 C900 246 660 246 640 228Z" fill="#713f12"/>
  <path d="M760 146 C770 128 790 128 800 146" stroke="#713f12" stroke-width="10" fill="none" stroke-linecap="round"/>
  <!-- eyes: one wide, one narrowed in suspicion -->
  {eye(722, 320, 36, 42, "#065f46", "#4ade80", look=(-10, 4), cid="catL")}
  <path d="M680 270 C700 262 740 262 760 272" stroke="#7c2d12" stroke-width="7" fill="none" stroke-linecap="round"/>
  <path d="M800 326 C818 312 852 312 870 324" stroke="#1f2937" stroke-width="7" fill="none" stroke-linecap="round"/>
  <path d="M806 330 C826 340 850 340 866 330" stroke="#1f2937" stroke-width="4" fill="none" stroke-linecap="round"/>
  <ellipse cx="836" cy="334" rx="11" ry="5" fill="#16a34a"/>
  <path d="M798 300 C820 286 852 288 876 302" stroke="#7c2d12" stroke-width="7" fill="none" stroke-linecap="round"/>
  <!-- nose, mouth, whiskers -->
  <path d="M770 366 L790 366 L780 378Z" fill="#f472b6"/>
  <path d="M780 378 C778 392 764 396 756 388 M780 378 C782 392 796 396 804 388" stroke="#7c2d12" stroke-width="4" fill="none" stroke-linecap="round"/>
  <path d="M700 380 L620 368 M702 394 L622 402 M860 380 L940 368 M858 394 L938 402" stroke="#7c2d12" stroke-width="3" stroke-linecap="round"/>
  <!-- arm and magnifier -->
  <path d="M680 470 C620 500 560 500 520 470" stroke="url(#fur)" stroke-width="54" fill="none" stroke-linecap="round"/>
  <g filter="url(#drop)">
    <path d="M318 430 L500 470" stroke="#7c4a24" stroke-width="24" stroke-linecap="round"/>
    <circle cx="250" cy="372" r="98" fill="#e0f2fe" fill-opacity="0.5" stroke="#f59e0b" stroke-width="20"/>
    <circle cx="250" cy="372" r="98" fill="none" stroke="#b45309" stroke-width="5"/>
    <text x="250" y="386" text-anchor="middle" font-family="{MONO}" font-weight="800" font-size="31" fill="#dc2626">os.remove</text>
    <path d="M190 322 C204 300 228 290 252 288" stroke="#ffffff" stroke-width="9" stroke-linecap="round" fill="none" opacity="0.8"/>
  </g>
  <circle cx="512" cy="470" r="34" fill="url(#fur)" stroke="#9a3412" stroke-width="3"/>
  <path d="M500 448 L500 462 M516 446 L516 462" stroke="#9a3412" stroke-width="3" stroke-linecap="round"/>
'''
note = bubble(1040, 150, 120, 70, (930, 240)) + f'''
  <text x="1040" y="140" text-anchor="middle" font-family="{HAND_FONT}" font-weight="700" font-size="25" fill="#334155">who calls</text>
  <text x="1040" y="176" text-anchor="middle" font-family="{MONO}" font-weight="800" font-size="25" fill="#dc2626">os.remove?</text>'''
write("testing-ai-code-1-read-before-you-run",
      "Anime illustration: a ginger detective cat in a checked deerstalker, one eye narrowed in suspicion, holds a "
      "magnifying glass over a page of generated code where the lines that delete or move files are highlighted in red; "
      "a thought bubble asks who calls os.remove?",
      dict(s1="#93c5fd", s2="#c4b5fd", s3="#fdf2f8", h1="#000", h2="#000", h3="#000", c1="#000", c2="#000"),
      paper + cat + note + sparkles([(1150, 330, 24), (560, 80, 22), (600, 600, 18), (1160, 560, 20)]))

# =====================================================================
# Part 2: a bear chef whose recipe forgot the eggs
# =====================================================================
rows = [("✓", "test_clean_dry_run", "#16a34a"), ("✓", "test_scan_folders", "#16a34a"),
        ("✓", "test_scan_exact_duplicates", "#16a34a"), ("✓", "test_hash_file", "#16a34a"),
        ("✓", "test_calculate_similarity", "#16a34a"), ("✗", "same_name_different_content", "#dc2626"),
        ("✗", "similarity_different", "#dc2626"), ("✗", "test_web_serve  403", "#dc2626")]
board_rows = "".join(
    f'<text x="790" y="{214 + i * 38}" font-family="{SANS}" font-weight="900" font-size="24" fill="{c}">{m}</text>'
    f'<text x="822" y="{214 + i * 38}" font-family="{MONO}" font-weight="700" font-size="19" fill="#1e293b">{n}</text>'
    for i, (m, n, c) in enumerate(rows))
board = f'''
  <g filter="url(#drop)">
    <rect x="760" y="120" width="410" height="440" rx="18" fill="#ffffff"/>
    <rect x="760" y="120" width="410" height="56" rx="18" fill="#1e293b"/><rect x="760" y="150" width="410" height="26" fill="#1e293b"/>
    <text x="786" y="157" font-family="{MONO}" font-weight="800" font-size="24" fill="#a5f3fc">$ pytest</text>
    <g transform="rotate(10 1100 150)"><rect x="1040" y="128" width="116" height="46" rx="23" fill="#f59e0b"/>
    <text x="1098" y="160" text-anchor="middle" font-family="{SANS}" font-weight="900" font-size="24" fill="#ffffff">5 / 8</text></g>
  </g>
  {board_rows}'''

cups = ""
for i in range(6):
    cx = 494 + i * 46
    cups += f'<ellipse cx="{cx}" cy="514" rx="20" ry="10" fill="#a8896a"/>'
    if i < 4:
        cups += (f'<ellipse cx="{cx}" cy="494" rx="18" ry="24" fill="#fffbeb" stroke="#d6c4a8" stroke-width="2"/>'
                 f'<ellipse cx="{cx - 6}" cy="484" rx="5" ry="8" fill="#ffffff"/>')
carton = f'''
  <g filter="url(#drop)">
    <path d="M462 510 L756 510 L744 566 L474 566Z" fill="#d6c4a8"/>
    <path d="M462 510 L756 510" stroke="#b7a184" stroke-width="4"/>
    {cups}
    <text x="609" y="550" text-anchor="middle" font-family="{SANS}" font-weight="800" font-size="16" fill="#78573a">dependencies</text>
  </g>
  <path d="M640 370 C660 420 670 460 678 496" stroke="#7c3aed" stroke-width="3" stroke-dasharray="6 6" fill="none"/>
  <path d="M700 446 C712 470 718 486 724 500" stroke="#7c3aed" stroke-width="3" stroke-dasharray="6 6" fill="none"/>
  <g filter="url(#drop)">
    <rect x="560" y="320" width="160" height="50" rx="14" fill="#ffffff" stroke="#7c3aed" stroke-width="3" stroke-dasharray="8 6"/>
    <text x="640" y="353" text-anchor="middle" font-family="{MONO}" font-weight="800" font-size="20" fill="#7c3aed">chardet ?</text>
    <rect x="600" y="396" width="150" height="50" rx="14" fill="#ffffff" stroke="#7c3aed" stroke-width="3" stroke-dasharray="8 6"/>
    <text x="675" y="429" text-anchor="middle" font-family="{MONO}" font-weight="800" font-size="20" fill="#7c3aed">requests ?</text>
  </g>
  <g filter="url(#drop)" transform="rotate(-4 560 150)"><rect x="480" y="128" width="170" height="46" rx="23" fill="#22c55e"/>
  <text x="565" y="159" text-anchor="middle" font-family="{SANS}" font-weight="800" font-size="20" fill="#ffffff">pip install ✓</text></g>'''

bear = f'''
  <defs>{grad("bear", "#a16207", "#713f12")}</defs>
  <!-- body and apron -->
  <ellipse cx="250" cy="560" rx="185" ry="160" fill="url(#bear)" filter="url(#drop)"/>
  <path d="M160 470 C200 452 300 452 340 470 L360 640 L140 640Z" fill="#ffffff"/>
  <path d="M190 470 C200 430 300 430 310 470" stroke="#ffffff" stroke-width="8" fill="none"/>
  <rect x="200" y="520" width="100" height="56" rx="10" fill="#fee2e2"/>
  <text x="250" y="555" text-anchor="middle" font-family="{SANS}" font-weight="800" font-size="18" fill="#b91c1c">recipe</text>
  <!-- ears -->
  <circle cx="135" cy="205" r="46" fill="url(#bear)"/><circle cx="135" cy="205" r="24" fill="#fcd9b6"/>
  <circle cx="365" cy="205" r="46" fill="url(#bear)"/><circle cx="365" cy="205" r="24" fill="#fcd9b6"/>
  <!-- head -->
  <circle cx="250" cy="300" r="132" fill="url(#bear)" filter="url(#drop)"/>
  <ellipse cx="250" cy="352" rx="66" ry="50" fill="#fcd9b6"/>
  <ellipse cx="250" cy="328" rx="22" ry="14" fill="#1f2937"/><ellipse cx="244" cy="323" rx="7" ry="4" fill="#ffffff" opacity="0.7"/>
  <path d="M250 342 L250 360 M226 372 C236 362 244 380 252 370 C260 360 268 378 276 368" stroke="#1f2937" stroke-width="4" fill="none" stroke-linecap="round"/>
  {eye(200, 284, 24, 28, "#78350f", "#f59e0b", look=(4, 2), cid="bearL")}
  {eye(300, 284, 24, 28, "#78350f", "#f59e0b", look=(4, 2), cid="bearR")}
  <path d="M170 244 C184 236 206 236 222 244" stroke="#3f2a10" stroke-width="7" fill="none" stroke-linecap="round"/>
  <path d="M278 230 C294 220 316 220 330 232" stroke="#3f2a10" stroke-width="7" fill="none" stroke-linecap="round"/>
  <ellipse cx="176" cy="330" rx="20" ry="9" fill="#fb7185" opacity="0.45" filter="url(#soft)"/>
  <ellipse cx="324" cy="330" rx="20" ry="9" fill="#fb7185" opacity="0.45" filter="url(#soft)"/>
  <!-- chef hat -->
  <g filter="url(#drop)" fill="#ffffff">
    <circle cx="196" cy="128" r="48"/><circle cx="252" cy="100" r="56"/><circle cx="308" cy="128" r="48"/>
    <rect x="180" y="132" width="144" height="54" rx="10"/>
  </g>
  <path d="M184 170 H320" stroke="#e5e7eb" stroke-width="4"/>
  <!-- paw scratching head, paw holding an egg -->
  <path d="M390 480 C450 400 440 300 392 250" stroke="url(#bear)" stroke-width="58" fill="none" stroke-linecap="round"/>
  <circle cx="388" cy="246" r="32" fill="#fcd9b6" stroke="#713f12" stroke-width="4"/>
  <path d="M112 480 C70 450 70 410 96 392" stroke="url(#bear)" stroke-width="56" fill="none" stroke-linecap="round"/>
  <ellipse cx="96" cy="372" rx="22" ry="28" fill="#fffbeb" stroke="#d6c4a8" stroke-width="2"/>
  <circle cx="96" cy="402" r="28" fill="#fcd9b6" stroke="#713f12" stroke-width="4"/>
  <!-- sweat drop and a small question mark -->
  <path d="M420 150 C404 176 408 196 422 196 C436 196 438 176 420 150Z" fill="#a5e4f7" stroke="#4aa5d6" stroke-width="2.5"/>
  <text x="440" y="110" font-family="{SANS}" font-weight="900" font-size="64" fill="#fbbf24" stroke="#7c3aed" stroke-width="4" paint-order="stroke" transform="rotate(12 460 90)">?</text>'''
write("testing-ai-code-2-installs-but-tests-fail",
      "Anime illustration: a puzzled brown bear in a chef's hat and apron scratches its head, holding one egg, next to "
      "an egg carton labelled dependencies with two empty cups tagged chardet? and requests?, a green pip install badge "
      "above, and a pytest board showing five passes and three failures, scored 5 of 8",
      dict(s1="#86efac", s2="#bbf7d0", s3="#fefce8", h1="#000", h2="#000", h3="#000", c1="#000", c2="#000"),
      board + carton + bear + sparkles([(560, 240, 22), (1150, 600, 22), (720, 70, 24), (40, 80, 26)]))

# =====================================================================
# Part 3: a startled girl under a smoke alarm with no battery
# =====================================================================
def paper_icon(x, y, rot):
    return (f'<g transform="rotate({rot} {x} {y})" filter="url(#drop)"><path d="M{x - 26} {y - 34} h38 l14 14 v54 h-52Z" fill="#ffffff" stroke="#94a3b8" stroke-width="2"/>'
            f'<path d="M{x + 12} {y - 34} v14 h14" fill="#e2e8f0" stroke="#94a3b8" stroke-width="2"/>'
            f'<rect x="{x - 18}" y="{y - 10}" width="30" height="4" rx="2" fill="#cbd5e1"/><rect x="{x - 18}" y="{y}" width="36" height="4" rx="2" fill="#cbd5e1"/>'
            f'<rect x="{x - 18}" y="{y + 10}" width="24" height="4" rx="2" fill="#cbd5e1"/></g>')


alarm = f'''
  <rect x="0" y="0" width="1200" height="34" fill="#e2e8f0"/><rect x="0" y="34" width="1200" height="6" fill="#cbd5e1"/>
  <g filter="url(#drop)">
    <ellipse cx="960" cy="58" rx="96" ry="32" fill="#f8fafc" stroke="#cbd5e1" stroke-width="3"/>
    <ellipse cx="960" cy="52" rx="60" ry="16" fill="#e2e8f0"/>
    <circle cx="1010" cy="66" r="6" fill="#94a3b8"/>
  </g>
  <path d="M930 86 C926 130 950 150 944 190" stroke="#ef4444" stroke-width="4" fill="none"/>
  <path d="M948 86 C952 128 976 148 968 190" stroke="#1f2937" stroke-width="4" fill="none"/>
  <g transform="rotate(14 956 230)" filter="url(#drop)">
    <rect x="926" y="188" width="60" height="96" rx="10" fill="#1f2937"/><rect x="942" y="178" width="28" height="14" rx="4" fill="#94a3b8"/>
    <rect x="926" y="188" width="60" height="34" rx="10" fill="#f59e0b"/>
    <text x="956" y="262" text-anchor="middle" font-family="{SANS}" font-weight="900" font-size="22" fill="#ffffff">9V</text>
  </g>
  <text x="1060" y="130" font-family="{SANS}" font-weight="800" font-size="22" fill="#334155">never beeps</text>
  <g filter="url(#drop)">
    <path d="M830 420 L1150 420 L1130 580 L850 580Z" fill="#a16207"/>
    <path d="M818 400 L1162 400 L1150 430 L830 430Z" fill="#ca8a04"/>
    <rect x="886" y="468" width="208" height="54" rx="10" fill="#fef3c7"/>
    <text x="990" y="505" text-anchor="middle" font-family="{SANS}" font-weight="900" font-size="26" fill="#92400e" letter-spacing="2">QUARANTINE</text>
  </g>
  {paper_icon(700, 330, -20)}{paper_icon(830, 290, 12)}{paper_icon(1000, 330, -8)}
  <path d="M600 400 C680 300 780 270 900 340" stroke="#ffffff" stroke-width="4" stroke-dasharray="4 10" fill="none" stroke-linecap="round"/>
  <g filter="url(#drop)" transform="rotate(-6 640 500)">
    <rect x="570" y="470" width="150" height="60" rx="12" fill="#ffffff"/>
    <text x="645" y="508" text-anchor="middle" font-family="{MONO}" font-weight="800" font-size="22" fill="#2563eb">dry-run</text>
  </g>
  <g filter="url(#drop)" transform="rotate(-6 680 170)"><rect x="585" y="146" width="190" height="46" rx="23" fill="#ef4444"/>
  <text x="680" y="177" text-anchor="middle" font-family="{SANS}" font-weight="800" font-size="21" fill="#ffffff">0 copies left</text></g>'''

girl = f'''
  <defs>{grad("ghair", "#f472b6", "#9d174d")}{grad("gskin", "#ffe6d2", "#fbd1b5")}{grad("navy", "#1e3a8a", "#172554")}</defs>
  <!-- twin tails behind -->
  <path d="M130 230 C40 300 40 470 90 600 C110 520 120 440 160 330Z" fill="url(#ghair)" filter="url(#drop)"/>
  <path d="M410 230 C500 300 500 470 450 600 C430 520 420 440 380 330Z" fill="url(#ghair)" filter="url(#drop)"/>
  <!-- back hair -->
  <path d="M140 300 C120 160 200 90 270 90 C340 90 420 160 400 300 C398 360 390 400 370 420 L170 420 C150 400 142 360 140 300Z" fill="url(#ghair)"/>
  <!-- sailor uniform -->
  <path d="M110 640 C114 520 170 470 230 458 L310 458 C370 470 426 520 430 640Z" fill="#f8fafc" filter="url(#drop)"/>
  <path d="M190 462 L270 560 L350 462 L320 458 L270 520 L220 458Z" fill="url(#navy)"/>
  <path d="M150 500 L230 462 L248 486 Z M390 500 L310 462 L292 486Z" fill="url(#navy)"/>
  <path d="M244 540 L270 560 L296 540 L300 590 L270 572 L240 590Z" fill="#ef4444"/>
  <path d="M246 420 L246 466 C258 480 282 480 294 466 L294 420Z" fill="#f0bf9f"/>
  <!-- face -->
  <path d="M164 280 C164 168 376 168 376 280 C376 350 324 422 270 436 C216 422 164 350 164 280Z" fill="url(#gskin)"/>
  {eye(222, 300, 36, 46, "#4c1d95", "#c084fc", look=(0, 0), iris_scale=0.5, cid="gL")}
  {eye(318, 300, 36, 46, "#4c1d95", "#c084fc", look=(0, 0), iris_scale=0.5, cid="gR")}
  <path d="M186 236 C200 222 236 220 254 232" stroke="#831843" stroke-width="6" fill="none" stroke-linecap="round"/>
  <path d="M286 232 C304 220 340 222 354 236" stroke="#831843" stroke-width="6" fill="none" stroke-linecap="round"/>
  <ellipse cx="196" cy="366" rx="22" ry="10" fill="#ff9aa2" opacity="0.55" filter="url(#soft)"/>
  <ellipse cx="344" cy="366" rx="22" ry="10" fill="#ff9aa2" opacity="0.55" filter="url(#soft)"/>
  <ellipse cx="270" cy="392" rx="16" ry="20" fill="#9f1239"/><ellipse cx="270" cy="400" rx="9" ry="8" fill="#fb7185"/>
  <!-- bangs -->
  <path d="M156 280 C140 170 210 104 270 104 C336 104 402 170 384 280 C376 252 366 230 352 214 C346 234 336 246 322 254 C320 228 308 206 290 192 C284 216 270 232 248 242 C250 220 244 202 234 190 C220 210 210 230 206 256 C196 244 190 228 190 214 C174 234 164 254 156 280Z" fill="url(#ghair)"/>
  <path d="M210 136 C240 116 290 112 328 126 C292 126 246 134 214 154Z" fill="#ffffff" opacity="0.25"/>
  <!-- ribbons -->
  <path d="M142 214 L112 186 L114 236Z M142 214 L170 190 L166 236Z" fill="#facc15" stroke="#ca8a04" stroke-width="2"/>
  <path d="M398 214 L428 186 L426 236Z M398 214 L370 190 L374 236Z" fill="#facc15" stroke="#ca8a04" stroke-width="2"/>
  <!-- hands on cheeks -->
  <path d="M150 600 C110 540 120 470 168 424 M390 600 C430 540 420 470 372 424" stroke="#f8fafc" stroke-width="40" fill="none" stroke-linecap="round" filter="url(#drop)"/>
  <path d="M154 440 L186 418 M386 440 L354 418" stroke="url(#navy)" stroke-width="12" stroke-linecap="round"/>
  <g fill="url(#gskin)" stroke="#d99b7a" stroke-width="2.5">
    <path d="M168 424 C160 396 166 362 182 352 C190 348 196 356 194 366 C200 352 210 354 210 366 C214 380 206 404 196 418Z"/>
    <path d="M372 424 C380 396 374 362 358 352 C350 348 344 356 346 366 C340 352 330 354 330 366 C326 380 334 404 344 418Z"/>
  </g>
  <!-- shock lines and exclamation marks -->
  <path d="M430 150 L470 120 M440 190 L490 184 M100 150 L64 118" stroke="#be185d" stroke-width="6" stroke-linecap="round"/>
  <text x="470" y="250" font-family="{SANS}" font-weight="900" font-size="90" fill="#ef4444" stroke="#ffffff" stroke-width="6" paint-order="stroke" transform="rotate(10 490 220)">!!</text>'''
write("testing-ai-code-3-one-fix-from-disaster",
      "Anime illustration: a startled girl with pink twin tails and a sailor uniform, hands on her cheeks and mouth open, "
      "looks up at a ceiling smoke alarm whose 9-volt battery dangles from its wires, while files labelled dry-run fly "
      "into a QUARANTINE box and a red badge reads 0 copies left",
      dict(s1="#fdba74", s2="#fde68a", s3="#fff7ed", h1="#000", h2="#000", h3="#000", c1="#000", c2="#000"),
      alarm + girl + sparkles([(40, 60, 26), (1150, 330, 22), (540, 210, 20), (520, 580, 18)]))

# =====================================================================
# Part 4: the server is the doorman and thinks it's fine; a fox walks in
# =====================================================================
scene = f'''
  <path d="M0 560 L1200 560 L1200 630 L0 630Z" fill="#64748b"/><path d="M0 552 L1200 552 L1200 562 L0 562Z" fill="#94a3b8"/>
  <rect x="860" y="120" width="230" height="440" rx="8" fill="#334155"/>
  <rect x="876" y="136" width="198" height="424" fill="#0f172a"/>
  <path d="M1074 136 L1150 110 L1150 590 L1074 560Z" fill="#b45309" filter="url(#drop)"/>
  <circle cx="1130" cy="350" r="8" fill="#fde68a"/>
  <text x="975" y="108" text-anchor="middle" font-family="{MONO}" font-weight="800" font-size="22" fill="#1e293b">127.0.0.1:8767</text>
  <g filter="url(#drop)">
    <path d="M960 220 h44 l14 14 v56 h-58Z" fill="#ffffff"/><path d="M1004 220 v14 h14" fill="#e2e8f0"/>
    <text x="990" y="322" text-anchor="middle" font-family="{MONO}" font-size="15" font-weight="700" fill="#e2e8f0">secret.txt</text>
  </g>
  <g filter="url(#drop)" transform="rotate(-8 975 450)"><rect x="900" y="426" width="150" height="46" rx="10" fill="#ef4444"/>
  <text x="975" y="457" text-anchor="middle" font-family="{SANS}" font-weight="800" font-size="20" fill="#ffffff">POST → 501</text></g>'''

server = f'''
  <defs>{grad("case", "#e2e8f0", "#94a3b8")}</defs>
  <!-- legs -->
  <rect x="160" y="530" width="40" height="34" rx="8" fill="#475569"/><rect x="310" y="530" width="40" height="34" rx="8" fill="#475569"/>
  <!-- tower -->
  <rect x="110" y="250" width="290" height="300" rx="34" fill="url(#case)" stroke="#64748b" stroke-width="4" filter="url(#drop)"/>
  <rect x="138" y="276" width="234" height="132" rx="22" fill="#0f172a"/>
  <!-- happy closed eyes and a smile on the screen -->
  <path d="M182 344 Q206 314 230 344" stroke="#22d3ee" stroke-width="8" fill="none" stroke-linecap="round"/>
  <path d="M280 344 Q304 314 328 344" stroke="#22d3ee" stroke-width="8" fill="none" stroke-linecap="round"/>
  <path d="M226 372 Q255 394 284 372" stroke="#22d3ee" stroke-width="6" fill="none" stroke-linecap="round"/>
  <ellipse cx="170" cy="380" rx="16" ry="7" fill="#f472b6" opacity="0.6"/><ellipse cx="340" cy="380" rx="16" ry="7" fill="#f472b6" opacity="0.6"/>
  <!-- drive bays and LEDs -->
  <rect x="146" y="428" width="218" height="22" rx="6" fill="#cbd5e1"/><rect x="146" y="460" width="218" height="22" rx="6" fill="#cbd5e1"/>
  <rect x="146" y="492" width="218" height="22" rx="6" fill="#cbd5e1"/>
  <circle cx="344" cy="439" r="5" fill="#22c55e"/><circle cx="344" cy="471" r="5" fill="#22c55e"/><circle cx="344" cy="503" r="5" fill="#f59e0b"/>
  <!-- antenna -->
  <path d="M255 250 L255 214" stroke="#64748b" stroke-width="6" stroke-linecap="round"/><circle cx="255" cy="206" r="11" fill="#22d3ee"/>
  <!-- waving arm toward the door -->
  <path d="M398 420 C450 420 480 390 500 350" stroke="#64748b" stroke-width="18" fill="none" stroke-linecap="round"/>
  <circle cx="504" cy="340" r="20" fill="#e2e8f0" stroke="#64748b" stroke-width="4"/>
  <path d="M112 420 C80 430 70 460 76 490" stroke="#64748b" stroke-width="18" fill="none" stroke-linecap="round"/>'''

thought = bubble(560, 128, 200, 80, (330, 216)) + f'''
  <text x="560" y="116" text-anchor="middle" font-family="{MONO}" font-weight="800" font-size="20" fill="#1e293b">host.startswith('localhost')</text>
  <text x="560" y="156" text-anchor="middle" font-family="{HAND_FONT}" font-weight="700" font-size="24" fill="#16a34a">✓ looks local to me!</text>'''

fox = f'''
  <defs>{grad("foxfur", "#fb923c", "#c2410c")}{grad("coat", "#d6a35c", "#92622a")}</defs>
  <!-- tail peeking out of the coat -->
  <path d="M760 500 C820 470 850 400 830 350 C860 380 880 460 840 520 C820 545 790 548 770 540Z" fill="url(#foxfur)" filter="url(#drop)"/>
  <path d="M830 350 C850 366 862 392 860 420 C846 396 836 376 822 366Z" fill="#ffffff"/>
  <!-- trench coat -->
  <path d="M650 340 L770 340 L806 556 L614 556Z" fill="url(#coat)" filter="url(#drop)"/>
  <path d="M710 344 L710 556" stroke="#7c4a1e" stroke-width="3"/>
  <rect x="628" y="450" width="164" height="16" fill="#7c4a1e"/>
  <path d="M650 340 L700 400 L690 340Z M770 340 L720 400 L730 340Z" fill="#b07a3a" stroke="#7c4a1e" stroke-width="2"/>
  <rect x="644" y="546" width="44" height="18" rx="8" fill="#1f2937"/><rect x="732" y="546" width="44" height="18" rx="8" fill="#1f2937"/>
  <!-- head -->
  <path d="M638 232 L614 166 L672 210Z" fill="url(#foxfur)"/><path d="M640 220 L626 184 L660 210Z" fill="#1f2937"/>
  <path d="M782 232 L806 166 L748 210Z" fill="url(#foxfur)"/><path d="M780 220 L794 184 L760 210Z" fill="#1f2937"/>
  <ellipse cx="710" cy="272" rx="80" ry="66" fill="url(#foxfur)" filter="url(#drop)"/>
  <path d="M642 290 C670 340 750 340 778 290 C752 306 668 306 642 290Z" fill="#ffffff"/>
  <!-- sly half-closed eyes -->
  <ellipse cx="680" cy="270" rx="16" ry="10" fill="#facc15"/><ellipse cx="683" cy="271" rx="4" ry="8" fill="#111827"/>
  <ellipse cx="740" cy="270" rx="16" ry="10" fill="#facc15"/><ellipse cx="743" cy="271" rx="4" ry="8" fill="#111827"/>
  <path d="M660 266 C670 258 692 258 700 266 L700 260 C690 250 670 250 660 260Z" fill="#7c2d12"/>
  <path d="M720 266 C730 258 752 258 760 266 L760 260 C750 250 730 250 720 260Z" fill="#7c2d12"/>
  <path d="M660 252 L700 258 M720 258 L760 252" stroke="#431407" stroke-width="5" stroke-linecap="round"/>
  <ellipse cx="710" cy="300" rx="10" ry="7" fill="#111827"/>
  <path d="M686 312 Q712 332 740 308" stroke="#431407" stroke-width="4" fill="none" stroke-linecap="round"/>
  <!-- fedora -->
  <path d="M664 216 L670 168 C700 158 724 158 752 168 L758 216Z" fill="#374151" filter="url(#drop)"/>
  <rect x="666" y="198" width="90" height="12" fill="#b91c1c"/>
  <ellipse cx="711" cy="218" rx="88" ry="13" fill="#1f2937"/>
  <!-- the badge -->
  <path d="M690 340 L700 404 M730 340 L722 404" stroke="#1f2937" stroke-width="3"/>
  <g filter="url(#drop)" transform="rotate(-5 710 420)">
    <rect x="610" y="400" width="206" height="40" rx="10" fill="#ffffff" stroke="#dc2626" stroke-width="3"/>
    <text x="713" y="426" text-anchor="middle" font-family="{MONO}" font-weight="800" font-size="16" fill="#dc2626">localhost.evil.example</text>
  </g>'''
write("testing-ai-code-4-web-ui-front-door",
      "Anime illustration: a cheerful server tower with a smiling screen face and closed happy eyes thinks "
      "host.startswith('localhost'), looks local to me!, and waves through a sly fox in a trench coat and fedora "
      "wearing a localhost.evil.example badge, toward an open door marked 127.0.0.1:8767 with secret.txt inside "
      "and a red POST 501 sign",
      dict(s1="#c4b5fd", s2="#ddd6fe", s3="#f5f3ff", h1="#000", h2="#000", h3="#000", c1="#000", c2="#000"),
      scene + server + thought + fox + sparkles([(40, 100, 26), (1160, 60, 22), (520, 470, 20)]))
