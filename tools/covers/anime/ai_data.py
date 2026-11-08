"""Anime covers for the AI & Data posts that had no image of their own (2026-11-08). One character per post,
tied to its lead analogy: explorer girl, beaver engineer, hamster, octopus, boy with an MCP plug, panda hiker,
penguin ice-cream seller. Run from the repo root: python tools/covers/anime/ai_data.py [slug ...]"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from kit import *  # noqa: E402,F403  (svg pieces: sparkles, eye, blush, card, pill, arrow, grad, write, MONO, SANS, INK)

# =====================================================================
# 1. Choosing a framework: an explorer girl reading a map of the AI stack
# =====================================================================
layers = [  # bottom to top
    ("Tensors", "PyTorch", "#f97316"), ("Classic ML", "scikit-learn", "#f59e0b"),
    ("Models", "Hugging Face", "#eab308"), ("Serving", "Ollama", "#22c55e"),
    ("Apps", "LangChain · vector stores", "#06b6d4"), ("MLOps", "MLflow", "#8b5cf6")]
tower = []
for i, (name, tool, col) in enumerate(layers):
    y = 520 - i * 68
    inset = i * 14
    x, w = 640 + inset, 500 - 2 * inset
    tower.append(f'''
  <g filter="url(#drop)">
    <rect x="{x}" y="{y}" width="{w}" height="58" rx="14" fill="#ffffff"/>
    <rect x="{x}" y="{y}" width="14" height="58" rx="7" fill="{col}"/>
    <text x="{x + 30}" y="{y + 37}" font-family="{SANS}" font-size="21" font-weight="800" fill="{INK}">{name}</text>
    <text x="{x + w - 20}" y="{y + 37}" text-anchor="end" font-family="{MONO}" font-size="19" font-weight="700" fill="{col}">{tool}</text>
  </g>''')
pin = '''
  <g filter="url(#drop)" transform="translate(1092 150)">
    <path d="M0 0 C-26 0 -34 30 -18 50 L0 78 L18 50 C34 30 26 0 0 0Z" fill="#ef4444"/><circle cx="0" cy="26" r="11" fill="#ffffff"/>
  </g>'''
girl = f'''
  <defs>{grad("ghair", "#2dd4bf", "#0f766e")}{grad("gshirt", "#fde68a", "#d97706")}{grad("ghat", "#fef3c7", "#d6b26a")}
    {grad("gskin", "#ffe8d6", "#f9cfb2")}</defs>
  <!-- pigtails -->
  <path d="M170 250 C110 290 100 380 140 430 C150 390 170 340 200 300Z" fill="url(#ghair)" filter="url(#drop)"/>
  <path d="M430 250 C490 290 500 380 460 430 C450 390 430 340 400 300Z" fill="url(#ghair)" filter="url(#drop)"/>
  <circle cx="188" cy="262" r="12" fill="#f43f5e"/><circle cx="412" cy="262" r="12" fill="#f43f5e"/>
  <!-- body: explorer shirt and scarf -->
  <path d="M120 640 C126 500 180 450 250 440 L350 440 C420 450 474 500 480 640Z" fill="url(#gshirt)" filter="url(#drop)"/>
  <path d="M262 436 L338 436 L322 480 L278 480Z" fill="#f0c3a3"/>
  <path d="M250 450 C280 488 320 488 350 450 L362 470 C326 510 274 510 238 470Z" fill="#ef4444"/>
  <path d="M300 490 L282 548 L300 540 L312 552Z" fill="#dc2626"/>
  <rect x="190" y="520" width="34" height="40" rx="6" fill="#b45309" opacity="0.55"/>
  <rect x="376" y="520" width="34" height="40" rx="6" fill="#b45309" opacity="0.55"/>
  <!-- face -->
  <path d="M206 250 C206 140 394 140 394 250 C394 330 346 400 300 414 C254 400 206 330 206 250Z" fill="url(#gskin)" filter="url(#drop)"/>
  {blush(240, 330)}{blush(360, 330)}
  {eye(254, 282, 30, 38, "#0e7490", "#67e8f9", look=(9, -3), cid="gL")}
  {eye(346, 282, 30, 38, "#0e7490", "#67e8f9", look=(9, -3), cid="gR")}
  <path d="M222 234 C238 224 262 224 276 232" stroke="#115e59" stroke-width="6" fill="none" stroke-linecap="round"/>
  <path d="M324 232 C338 222 362 222 378 230" stroke="#115e59" stroke-width="6" fill="none" stroke-linecap="round"/>
  <path d="M298 326 L294 336 L301 338" stroke="#d99b7a" stroke-width="3" fill="none" stroke-linecap="round"/>
  <path d="M280 360 C290 376 312 376 322 360 C312 366 290 366 280 360Z" fill="#be123c"/>
  <!-- bangs -->
  <path d="M204 262 C192 170 250 128 300 128 C356 128 408 170 396 262 C388 236 380 220 366 208 C364 226 356 238 344 244 C342 218 330 198 314 186 C310 206 298 220 280 228 C282 206 276 190 266 180 C252 198 242 220 238 244 C226 232 220 216 218 204 C208 220 206 240 204 262Z" fill="url(#ghair)"/>
  <!-- pith helmet -->
  <path d="M206 186 C206 96 394 96 394 186Z" fill="url(#ghat)" filter="url(#drop)"/>
  <path d="M176 192 C230 172 370 172 424 192 C404 210 196 210 176 192Z" fill="#b8913f"/>
  <path d="M210 168 C260 158 340 158 390 168" stroke="#92400e" stroke-width="10" fill="none"/>
  <!-- the map, held up -->
  <g filter="url(#drop)" transform="rotate(-6 420 500)">
    <path d="M330 420 L420 436 L510 420 L600 436 L600 580 L510 564 L420 580 L330 564Z" fill="#fef9c3" stroke="#ca8a04" stroke-width="3"/>
    <path d="M420 436 L420 580 M510 420 L510 564" stroke="#ca8a04" stroke-width="2" opacity="0.6"/>
    <path d="M350 540 C390 520 400 480 450 470 C500 460 520 500 570 456" stroke="#ef4444" stroke-width="4" fill="none" stroke-dasharray="8 7"/>
    <path d="M560 446 L580 466 M580 446 L560 466" stroke="#ef4444" stroke-width="5" stroke-linecap="round"/>
  </g>
  <circle cx="336" cy="512" r="24" fill="url(#gskin)" stroke="#d99b7a" stroke-width="2.5"/>
  <circle cx="590" cy="488" r="24" fill="url(#gskin)" stroke="#d99b7a" stroke-width="2.5"/>'''
write("ai-in-practice-1-choosing-a-framework",
      "Anime illustration: an explorer girl with teal pigtails and a pith helmet studies a treasure map, looking at a "
      "tower of the AI stack: tensors with PyTorch, classic ML with scikit-learn, models with Hugging Face, serving with "
      "Ollama, apps with LangChain and vector stores, MLOps with MLflow, a red pin on top",
      dict(s1="#bae6fd", s2="#e0f2fe", s3="#fef9c3"),
      girl + "".join(tower) + pin + pill(650, 40, "which layer do I need?", "#0f766e", size=22)
      + sparkles([(40, 80, 26), (560, 120, 20), (1160, 600, 22), (600, 360, 16)]))


# =====================================================================
# 2. Vertex AI pipelines: a beaver engineer building a pipeline
# =====================================================================
def stage(x, y, w, label, sub, col):
    return f'''
  <g filter="url(#drop)">
    <rect x="{x}" y="{y}" width="{w}" height="96" rx="18" fill="#ffffff" stroke="{col}" stroke-width="4"/>
    <text x="{x + w / 2}" y="{y + 44}" text-anchor="middle" font-family="{SANS}" font-size="26" font-weight="800" fill="{INK}">{label}</text>
    <text x="{x + w / 2}" y="{y + 74}" text-anchor="middle" font-family="{MONO}" font-size="16" font-weight="700" fill="{col}">{sub}</text>
  </g>'''


pipe = f'''
  <defs>{grad("pipe", "#cbd5e1", "#64748b")}</defs>
  <rect x="560" y="246" width="590" height="26" rx="13" fill="url(#pipe)"/>
  <rect x="1010" y="246" width="26" height="200" rx="13" fill="url(#pipe)"/>
  {stage(580, 210, 160, "train", "@dsl.component", "#2563eb")}
  {stage(780, 210, 180, "evaluate", "-&gt; float", "#7c3aed")}
  <g filter="url(#drop)">
    <path d="M1023 176 L1093 259 L1023 342 L953 259Z" fill="#fef3c7" stroke="#d97706" stroke-width="4"/>
    <text x="1023" y="268" text-anchor="middle" font-family="{SANS}" font-size="22" font-weight="800" fill="#92400e">better?</text>
  </g>
  <g filter="url(#drop)">
    <rect x="900" y="420" width="250" height="96" rx="18" fill="#dcfce7" stroke="#16a34a" stroke-width="4"/>
    <text x="1025" y="462" text-anchor="middle" font-family="{SANS}" font-size="26" font-weight="800" fill="#14532d">endpoint ✓</text>
    <text x="1025" y="492" text-anchor="middle" font-family="{MONO}" font-size="16" font-weight="700" fill="#16a34a">model.deploy()</text>
  </g>
  <g filter="url(#drop)">
    <path d="M600 410 L700 410 L720 430 L720 520 L600 520Z" fill="#ffffff" stroke="#64748b" stroke-width="3"/>
    <path d="M700 410 L700 430 L720 430" fill="#e2e8f0" stroke="#64748b" stroke-width="3"/>
    <text x="660" y="462" text-anchor="middle" font-family="{MONO}" font-size="17" font-weight="800" fill="#334155">train</text>
    <text x="660" y="486" text-anchor="middle" font-family="{MONO}" font-size="17" font-weight="800" fill="#334155">.csv</text>
  </g>
  {arrow("M660 404 C660 360 660 340 660 318", "#2563eb")}
  {arrow("M960 470 C860 470 800 470 742 470", "#16a34a", dash="2 10")}
  <text x="820" y="448" text-anchor="middle" font-family="{SANS}" font-size="17" font-weight="700" fill="#15803d">again next week</text>'''
beaver = f'''
  <defs>{grad("bfur", "#b45309", "#78350f")}{grad("bhat", "#fde047", "#eab308")}{grad("btail", "#57534e", "#292524")}
    <pattern id="scale" width="18" height="18" patternUnits="userSpaceOnUse"><rect width="18" height="18" fill="url(#btail)"/>
      <path d="M0 9 H18 M9 0 V18" stroke="#78716c" stroke-width="2"/></pattern></defs>
  <!-- tail -->
  <ellipse cx="470" cy="560" rx="120" ry="52" fill="url(#scale)" transform="rotate(-18 470 560)" filter="url(#drop)"/>
  <!-- body with work vest -->
  <ellipse cx="290" cy="540" rx="170" ry="150" fill="url(#bfur)" filter="url(#drop)"/>
  <path d="M170 470 C200 440 380 440 410 470 L420 640 L160 640Z" fill="#f97316"/>
  <path d="M180 520 L400 520 M176 570 L404 570" stroke="#fde047" stroke-width="12"/>
  <!-- ears -->
  <circle cx="178" cy="196" r="34" fill="url(#bfur)"/><circle cx="178" cy="196" r="16" fill="#451a03"/>
  <circle cx="402" cy="196" r="34" fill="url(#bfur)"/><circle cx="402" cy="196" r="16" fill="#451a03"/>
  <!-- head -->
  <ellipse cx="290" cy="300" rx="150" ry="130" fill="url(#bfur)" filter="url(#drop)"/>
  <ellipse cx="290" cy="356" rx="78" ry="56" fill="#e7c08f"/>
  {eye(232, 284, 26, 30, "#78350f", "#f59e0b", look=(10, 0), cid="bvL")}
  {eye(348, 284, 26, 30, "#78350f", "#f59e0b", look=(10, 0), cid="bvR")}
  {blush(208, 336)}{blush(372, 336)}
  <ellipse cx="290" cy="336" rx="22" ry="15" fill="#1c1917"/><ellipse cx="284" cy="331" rx="7" ry="4" fill="#ffffff" opacity="0.7"/>
  <path d="M268 358 C278 370 302 370 312 358" stroke="#451a03" stroke-width="4" fill="none" stroke-linecap="round"/>
  <rect x="272" y="364" width="36" height="34" rx="6" fill="#ffffff" stroke="#451a03" stroke-width="3"/>
  <path d="M290 364 L290 398" stroke="#451a03" stroke-width="3"/>
  <!-- hard hat -->
  <path d="M160 214 C160 110 420 110 420 214Z" fill="url(#bhat)" filter="url(#drop)"/>
  <rect x="140" y="206" width="300" height="22" rx="11" fill="#ca8a04"/>
  <path d="M276 124 L276 206 M304 124 L304 206" stroke="#ca8a04" stroke-width="10"/>
  <!-- arm with wrench, pointing at the pipe -->
  <path d="M420 470 C470 430 500 380 520 330" stroke="url(#bfur)" stroke-width="52" fill="none" stroke-linecap="round"/>
  <g filter="url(#drop)" transform="rotate(-35 540 300)">
    <rect x="520" y="230" width="22" height="110" rx="8" fill="#94a3b8"/>
    <path d="M510 230 C500 200 520 186 531 186 C542 186 562 200 552 230 L542 222 L542 204 L520 204 L520 222Z" fill="#94a3b8"/>
  </g>
  <circle cx="522" cy="326" r="26" fill="#e7c08f" stroke="#78350f" stroke-width="3"/>'''
write("ai-in-practice-2-vertex-ai-pipelines",
      "Anime illustration: a beaver engineer in a yellow hard hat and orange safety vest holds up a wrench beside a "
      "pipeline: train.csv flows into train, then evaluate, then a diamond asking better?, then a deployed endpoint, "
      "with a dashed arrow that says again next week",
      dict(s1="#bfdbfe", s2="#dbeafe", s3="#ecfccb"),
      pipe + beaver + pill(600, 70, "Vertex AI Pipelines · KFP", "#1d4ed8", size=22)
      + sparkles([(40, 70, 24), (560, 590, 18), (1160, 70, 24), (760, 140, 16)]))


# =====================================================================
# 3. Tokens: a hamster with cheeks stuffed with token coins
# =====================================================================
chips_txt = ["Lang", "uage", " models", " don", "'t", " read", " words"]
chip_cols = ["#fecaca", "#fde68a", "#bbf7d0", "#bfdbfe", "#ddd6fe", "#fbcfe8", "#a5f3fc"]
chips, x = [], 600
for t, c in zip(chips_txt, chip_cols):
    w = len(t) * 12 + 18
    chips.append(f'<rect x="{x}" y="102" width="{w}" height="46" rx="10" fill="{c}" stroke="#334155" stroke-width="2"/>'
                 f'<text xml:space="preserve" x="{x + 9}" y="132" font-family="{MONO}" font-size="20" font-weight="700" fill="#0f172a">{t.replace(" ", "␣")}</text>')
    x += w + 8
tokens = f'''
  <g filter="url(#drop)">{"".join(chips)}</g>
  <text x="600" y="186" font-family="{SANS}" font-size="20" font-weight="700" fill="#475569">7 tokens · 1 token ≈ 4 characters</text>'''
rows = [("input", "1,000,000 tokens", "× $3"), ("output", "1,000,000 tokens", "× $15")]
receipt_rows = "".join(
    f'<text x="640" y="{300 + i * 46}" font-family="{MONO}" font-size="21" font-weight="700" fill="#334155">{a}</text>'
    f'<text x="1110" y="{300 + i * 46}" text-anchor="end" font-family="{MONO}" font-size="21" font-weight="800" fill="#0f172a">{c}</text>'
    for i, (a, b, c) in enumerate(rows))
receipt = card(610, 220, 530, 300, "per million tokens", body=f'''
  {receipt_rows}
  <path d="M640 368 H1110" stroke="#94a3b8" stroke-width="2" stroke-dasharray="6 6"/>
  <text x="640" y="408" font-family="{MONO}" font-size="21" font-weight="700" fill="#334155">1,000 tokens</text>
  <text x="1110" y="408" text-anchor="end" font-family="{MONO}" font-size="21" font-weight="800" fill="#0f172a">≈ 750 words</text>
  <text x="640" y="452" font-family="{MONO}" font-size="21" font-weight="700" fill="#334155">output costs</text>
  <text x="1110" y="452" text-anchor="end" font-family="{MONO}" font-size="21" font-weight="800" fill="#dc2626">5× input</text>
  <text x="640" y="494" font-family="{SANS}" font-size="16" font-style="italic" fill="#64748b">made-up prices, to show the arithmetic</text>''')


def coin(x, y, r, label, rot=0):
    return f'''
  <g filter="url(#drop)" transform="rotate({rot} {x} {y})">
    <circle cx="{x}" cy="{y}" r="{r}" fill="url(#gold)" stroke="#b45309" stroke-width="3"/>
    <circle cx="{x}" cy="{y}" r="{r - 7}" fill="none" stroke="#fde68a" stroke-width="2"/>
    <text x="{x}" y="{y + r * 0.28}" text-anchor="middle" font-family="{MONO}" font-size="{r * 0.72:.0f}" font-weight="800" fill="#92400e">{label}</text>
  </g>'''


hamster = f'''
  <defs>{grad("hfur", "#fed7aa", "#fb923c")}{grad("gold", "#fef08a", "#f59e0b")}</defs>
  <!-- body -->
  <ellipse cx="300" cy="500" rx="200" ry="170" fill="url(#hfur)" filter="url(#drop)"/>
  <ellipse cx="300" cy="530" rx="120" ry="110" fill="#fff7ed"/>
  <!-- ears -->
  <ellipse cx="180" cy="170" rx="44" ry="40" fill="url(#hfur)"/><ellipse cx="180" cy="172" rx="26" ry="22" fill="#fda4af"/>
  <ellipse cx="420" cy="170" rx="44" ry="40" fill="url(#hfur)"/><ellipse cx="420" cy="172" rx="26" ry="22" fill="#fda4af"/>
  <!-- head with puffed cheeks -->
  <ellipse cx="300" cy="300" rx="170" ry="140" fill="url(#hfur)" filter="url(#drop)"/>
  <ellipse cx="170" cy="350" rx="90" ry="78" fill="url(#hfur)"/>
  <ellipse cx="430" cy="350" rx="90" ry="78" fill="url(#hfur)"/>
  <ellipse cx="300" cy="360" rx="96" ry="66" fill="#fff7ed"/>
  {eye(240, 280, 30, 34, "#1e293b", "#475569", look=(12, -2), cid="hmL")}
  {eye(360, 280, 30, 34, "#1e293b", "#475569", look=(12, -2), cid="hmR")}
  {blush(160, 360, 34, 16)}{blush(440, 360, 34, 16)}
  <ellipse cx="300" cy="332" rx="13" ry="9" fill="#f472b6"/>
  <path d="M300 341 L300 354 M300 354 C292 366 280 366 274 358 M300 354 C308 366 320 366 326 358" stroke="#9a3412" stroke-width="3.5" fill="none" stroke-linecap="round"/>
  <path d="M220 346 L160 334 M222 360 L162 368 M380 346 L440 334 M378 360 L438 368" stroke="#9a3412" stroke-width="2.5" stroke-linecap="round" opacity="0.6"/>
  <!-- coins peeking from the cheeks -->
  {coin(118, 330, 26, "tok", -20)}{coin(486, 334, 26, "en", 18)}
  <!-- paws holding a coin -->
  {coin(300, 470, 54, "tok", -6)}
  <ellipse cx="236" cy="470" rx="28" ry="22" fill="#fed7aa" stroke="#c2410c" stroke-width="2.5"/>
  <ellipse cx="364" cy="470" rx="28" ry="22" fill="#fed7aa" stroke="#c2410c" stroke-width="2.5"/>
  <!-- coin pile -->
  {coin(110, 590, 30, "␣")}{coin(170, 604, 30, "s", 10)}{coin(470, 598, 30, "'t", -12)}{coin(530, 584, 26, "es", 8)}'''
write("ai-in-practice-3-tokens-and-tokenomics",
      "Anime illustration: a hamster with cheeks stuffed with gold coins marked tok and en holds a big tok coin. Beside it "
      "the sentence Language models don't read words is cut into seven coloured token chips, and a receipt reads input "
      "one million tokens times 3 dollars, output times 15 dollars, 1,000 tokens about 750 words, made-up prices",
      dict(s1="#fde68a", s2="#fef3c7", s3="#fff7ed"),
      hamster + tokens + receipt + sparkles([(40, 70, 26), (560, 60, 18), (1160, 600, 24), (560, 420, 16)]))


# =====================================================================
# 4. Tools and agents: an octopus holding a tool in each arm, inside the agent loop
# =====================================================================
def tentacle(d):
    return (f'<path d="{d}" stroke="url(#ofur)" stroke-width="34" fill="none" stroke-linecap="round"/>'
            f'<path d="{d}" stroke="#f5d0fe" stroke-width="8" fill="none" stroke-linecap="round" stroke-dasharray="2 16" opacity="0.9"/>')


octo = f'''
  <defs>{grad("ofur", "#e879f9", "#a21caf")}</defs>
  {tentacle("M230 420 C170 450 120 430 90 380")}
  {tentacle("M260 450 C230 520 160 540 120 520")}
  {tentacle("M300 460 C300 530 290 580 260 610")}
  {tentacle("M340 460 C360 530 400 560 450 560")}
  {tentacle("M370 440 C430 470 480 450 510 410")}
  {tentacle("M220 380 C160 360 120 300 130 240")}
  <!-- head -->
  <path d="M170 330 C150 160 240 90 300 90 C380 90 450 160 430 330 C420 420 180 420 170 330Z" fill="url(#ofur)" filter="url(#drop)"/>
  <ellipse cx="260" cy="150" rx="44" ry="22" fill="#ffffff" opacity="0.25" transform="rotate(-20 260 150)"/>
  {eye(254, 290, 34, 40, "#4c1d95", "#a78bfa", look=(10, 2), cid="ocL")}
  {eye(350, 290, 34, 40, "#4c1d95", "#a78bfa", look=(10, 2), cid="ocR")}
  {blush(226, 350)}{blush(380, 350)}
  <path d="M282 360 C292 374 314 374 324 360" stroke="#701a75" stroke-width="4.5" fill="none" stroke-linecap="round"/>
  <!-- headset: it is an agent at work -->
  <path d="M176 270 C170 150 430 150 424 270" stroke="#334155" stroke-width="10" fill="none"/>
  <rect x="160" y="258" width="28" height="56" rx="12" fill="#334155"/><rect x="412" y="258" width="28" height="56" rx="12" fill="#334155"/>
  <!-- tools in the arms -->
  <g filter="url(#drop)">
    <circle cx="96" cy="210" r="34" fill="#e0f2fe" stroke="#334155" stroke-width="8"/><path d="M120 236 L150 266" stroke="#334155" stroke-width="12" stroke-linecap="round"/>
    <g transform="translate(58 350)"><rect width="66" height="80" rx="10" fill="#334155"/><rect x="8" y="8" width="50" height="20" rx="4" fill="#a7f3d0"/>
      <g fill="#f8fafc"><rect x="8" y="36" width="14" height="12" rx="3"/><rect x="26" y="36" width="14" height="12" rx="3"/><rect x="44" y="36" width="14" height="12" rx="3"/>
      <rect x="8" y="54" width="14" height="12" rx="3"/><rect x="26" y="54" width="14" height="12" rx="3"/><rect x="44" y="54" width="14" height="12" rx="3" fill="#f97316"/></g></g>
    <g transform="translate(82 498)"><path d="M10 40 C-6 40 -6 16 12 16 C14 2 38 -2 44 12 C60 8 70 24 62 40Z" fill="#ffffff" stroke="#64748b" stroke-width="3"/><circle cx="58" cy="10" r="12" fill="#facc15"/></g>
    <g transform="translate(236 588)"><ellipse cx="26" cy="8" rx="26" ry="9" fill="#93c5fd" stroke="#1e40af" stroke-width="3"/>
      <path d="M0 8 V34 C0 46 52 46 52 34 V8" fill="#bfdbfe" stroke="#1e40af" stroke-width="3"/></g>
    <g transform="translate(456 534) rotate(30)"><rect x="0" y="0" width="16" height="70" rx="6" fill="#94a3b8"/>
      <path d="M-10 0 C-18 -24 0 -36 8 -36 C16 -36 34 -24 26 0 L18 -8 L18 -22 L-2 -22 L-2 -8Z" fill="#94a3b8"/></g>
  </g>'''
loop_nodes = [("goal", 760, 140, "#0ea5e9"), ("model", 1010, 200, "#7c3aed"), ("tool call", 1010, 400, "#f97316"), ("result", 760, 450, "#16a34a")]
loop = "".join(f'''
  <g filter="url(#drop)"><rect x="{x - 80}" y="{y - 32}" width="160" height="64" rx="32" fill="#ffffff" stroke="{c}" stroke-width="4"/>
  <text x="{x}" y="{y + 9}" text-anchor="middle" font-family="{SANS}" font-size="24" font-weight="800" fill="{INK}">{t}</text></g>'''
               for t, x, y, c in loop_nodes)
loop = f'''
  {arrow("M842 150 C900 156 940 168 958 172")}
  {arrow("M1010 236 C1010 290 1010 320 1010 362")}
  {arrow("M928 412 C880 430 860 440 846 444")}
  {arrow("M720 418 C640 360 640 220 700 172")}
  <text x="636" y="310" text-anchor="middle" font-family="{SANS}" font-size="19" font-weight="800" fill="#7c3aed" transform="rotate(-90 636 310)">repeat until done</text>
  {loop}
  <g filter="url(#drop)" transform="rotate(4 1060 520)">
    <rect x="930" y="496" width="230" height="56" rx="14" fill="#fee2e2" stroke="#dc2626" stroke-width="3"/>
    <text x="1045" y="532" text-anchor="middle" font-family="{SANS}" font-size="21" font-weight="800" fill="#991b1b">✋ human approves</text>
  </g>
  <g filter="url(#drop)">
    <rect x="610" y="520" width="300" height="50" rx="12" fill="#1e293b"/>
    <text x="760" y="552" text-anchor="middle" font-family="{MONO}" font-size="16" font-weight="700" fill="#a5f3fc">get_weather({{"city": "London"}})</text>
  </g>'''
write("ai-in-practice-4-tools-and-agents",
      "Anime illustration: a cheerful pink octopus wearing a headset holds a different tool in each arm, a magnifying "
      "glass, a calculator, a weather cloud, a database and a wrench, beside the agent loop goal, model, tool call, "
      "result, repeat until done, with a red human approves gate and a get_weather London tool call",
      dict(s1="#99f6e4", s2="#ccfbf1", s3="#f0fdfa"),
      loop + octo + sparkles([(40, 60, 24), (560, 80, 20), (1160, 60, 22), (580, 600, 16)]))


# =====================================================================
# 5. MCP: a boy carrying a giant universal plug to a hub
# =====================================================================
servers = [("files", 1060, 120, "#f59e0b"), ("database", 1080, 300, "#3b82f6"), ("GitHub", 1060, 480, "#334155")]
hub = f'''
  <defs>{grad("hub", "#a78bfa", "#6d28d9")}</defs>
  {"".join(f'<path d="M820 300 C930 300 950 {y} {x - 100} {y}" stroke="{c}" stroke-width="10" fill="none" stroke-linecap="round"/>' for _, x, y, c in servers)}
  {"".join(f'''<g filter="url(#drop)"><rect x="{x - 100}" y="{y - 44}" width="200" height="88" rx="18" fill="#ffffff" stroke="{c}" stroke-width="4"/>
    <text x="{x}" y="{y - 4}" text-anchor="middle" font-family="{SANS}" font-size="24" font-weight="800" fill="{INK}">{t}</text>
    <text x="{x}" y="{y + 24}" text-anchor="middle" font-family="{MONO}" font-size="15" font-weight="700" fill="{c}">MCP server</text></g>''' for t, x, y, c in servers)}
  <path d="M620 140 C700 140 740 220 760 250" stroke="#0ea5e9" stroke-width="10" fill="none" stroke-linecap="round"/>
  <g filter="url(#drop)">
    <rect x="540" y="70" width="190" height="100" rx="14" fill="#1e293b"/><rect x="552" y="82" width="166" height="62" rx="8" fill="#38bdf8"/>
    <text x="635" y="122" text-anchor="middle" font-family="{SANS}" font-size="22" font-weight="800" fill="#0c4a6e">AI app</text>
    <rect x="510" y="168" width="250" height="16" rx="8" fill="#334155"/>
    <text x="635" y="214" text-anchor="middle" font-family="{MONO}" font-size="16" font-weight="700" fill="#0369a1">host + client</text>
  </g>
  <g filter="url(#drop)">
    <circle cx="780" cy="300" r="76" fill="url(#hub)"/>
    <text x="780" y="314" text-anchor="middle" font-family="{SANS}" font-size="40" font-weight="900" fill="#ffffff">MCP</text>
  </g>
  {"".join(pill(x, 560, t, c, size=19) for t, x, c in [("tools", 560, "#f97316"), ("resources", 690, "#0ea5e9"), ("prompts", 866, "#16a34a")])}'''
boy = f'''
  <defs>{grad("yhair", "#334155", "#0f172a")}{grad("yhood", "#38bdf8", "#0369a1")}{grad("yskin", "#fde3cf", "#f2c4a3")}{grad("plug", "#c4b5fd", "#7c3aed")}</defs>
  <!-- hoodie body -->
  <path d="M90 640 C96 500 150 450 220 440 L330 440 C400 450 454 500 460 640Z" fill="url(#yhood)" filter="url(#drop)"/>
  <path d="M240 436 L310 436 L300 476 L250 476Z" fill="#e8b496"/>
  <path d="M220 446 C250 490 300 490 330 446" stroke="#0c4a6e" stroke-width="6" fill="none" opacity="0.4"/>
  <!-- face -->
  <path d="M180 250 C180 146 370 146 370 250 C370 330 322 396 275 410 C228 396 180 330 180 250Z" fill="url(#yskin)" filter="url(#drop)"/>
  {blush(214, 330)}{blush(336, 330)}
  {eye(230, 282, 28, 34, "#78350f", "#fbbf24", look=(10, 0), cid="yL")}
  {eye(320, 282, 28, 34, "#78350f", "#fbbf24", look=(10, 0), cid="yR")}
  <path d="M200 236 C214 226 240 226 254 236" stroke="#0f172a" stroke-width="7" fill="none" stroke-linecap="round"/>
  <path d="M296 236 C310 226 336 226 350 236" stroke="#0f172a" stroke-width="7" fill="none" stroke-linecap="round"/>
  <path d="M250 352 C262 376 296 376 308 352Z" fill="#9f1239"/><path d="M258 354 L300 354" stroke="#ffffff" stroke-width="5"/>
  <!-- spiky hair -->
  <path d="M174 262 C160 196 176 160 196 140 L180 104 L226 124 L236 78 L268 116 L300 74 L314 120 L352 96 L346 140 C372 160 386 200 376 262 C366 230 352 214 336 206 C330 220 318 228 304 232 C302 210 292 196 278 188 C270 208 254 222 236 228 C236 210 230 198 220 190 C206 210 196 236 190 262Z" fill="url(#yhair)"/>
  <!-- headphones round the neck -->
  <path d="M200 440 C200 480 350 480 350 440" stroke="#f97316" stroke-width="10" fill="none"/>
  <!-- arms carrying the plug -->
  <path d="M400 500 C440 470 470 430 500 400" stroke="url(#yhood)" stroke-width="48" fill="none" stroke-linecap="round"/>
  <g filter="url(#drop)" transform="rotate(-28 560 360)">
    <rect x="470" y="320" width="150" height="90" rx="18" fill="url(#plug)"/>
    <rect x="620" y="336" width="54" height="16" rx="5" fill="#cbd5e1"/><rect x="620" y="378" width="54" height="16" rx="5" fill="#cbd5e1"/>
    <text x="566" y="378" text-anchor="middle" font-family="{SANS}" font-size="28" font-weight="900" fill="#ffffff">MCP</text>
    <path d="M470 366 C420 366 380 400 340 420" stroke="#7c3aed" stroke-width="14" fill="none" stroke-linecap="round"/>
  </g>
  <circle cx="500" cy="404" r="28" fill="url(#yskin)" stroke="#d99b7a" stroke-width="2.5"/>
  <!-- sparks where the plug meets the hub -->
  <path d="M676 228 L700 214 M690 260 L716 262 M664 196 L672 172" stroke="#facc15" stroke-width="6" stroke-linecap="round"/>'''
write("ai-in-practice-5-mcp",
      "Anime illustration: a boy with spiky dark hair and a blue hoodie carries a giant purple plug marked MCP toward a "
      "glowing MCP hub that connects one AI app, the host and client, to three MCP servers for files, a database and "
      "GitHub, with pills for tools, resources and prompts",
      dict(s1="#c7d2fe", s2="#e0e7ff", s3="#fdf4ff"),
      hub + boy + sparkles([(40, 70, 24), (470, 90, 20), (1160, 600, 22), (1040, 580, 16)]))


# =====================================================================
# 6. Reading map: a panda hiker on a trail with four stops
# =====================================================================
stops = [("1", "How machines learn", 640, 520, "#f97316"), ("2", "How language models work", 760, 380, "#eab308"),
         ("3", "Building with models", 700, 240, "#22c55e"), ("4", "Letting models act", 880, 110, "#8b5cf6")]
trail = f'''
  <path d="M520 640 C600 560 700 560 680 500 C660 440 860 440 800 380 C740 320 620 300 720 240 C820 180 760 140 900 100"
    stroke="#d6b26a" stroke-width="44" fill="none" stroke-linecap="round" opacity="0.8"/>
  <path d="M520 640 C600 560 700 560 680 500 C660 440 860 440 800 380 C740 320 620 300 720 240 C820 180 760 140 900 100"
    stroke="#fef3c7" stroke-width="4" fill="none" stroke-dasharray="14 12"/>
  {"".join(f'''<g filter="url(#drop)"><path d="M{x} {y} L{x} {y - 70}" stroke="#78350f" stroke-width="7"/>
    <path d="M{x} {y - 98} L{x + 46} {y - 84} L{x} {y - 70}Z" fill="{c}"/>
    <circle cx="{x}" cy="{y}" r="22" fill="{c}" stroke="#ffffff" stroke-width="4"/>
    <text x="{x}" y="{y + 9}" text-anchor="middle" font-family="{SANS}" font-size="24" font-weight="900" fill="#ffffff">{n}</text>
    <rect x="{x + 34}" y="{y - 22}" width="{len(t) * 12 + 30}" height="44" rx="12" fill="#ffffff" opacity="0.95"/>
    <text x="{x + 49}" y="{y + 8}" font-family="{SANS}" font-size="21" font-weight="800" fill="{INK}">{t}</text></g>''' for n, t, x, y, c in stops)}
  <g filter="url(#drop)" transform="translate(1000 470)">
    <rect x="0" y="0" width="160" height="120" rx="10" fill="#92400e"/><rect x="10" y="10" width="140" height="46" fill="#fef3c7"/><rect x="10" y="64" width="140" height="46" fill="#fef3c7"/>
    {"".join(f'<rect x="{14 + i * 19}" y="{16 if i % 2 else 20}" width="15" height="{40 if i % 2 else 36}" rx="2" fill="{c}"/>' for i, c in enumerate(["#ef4444", "#3b82f6", "#22c55e", "#eab308", "#a855f7", "#06b6d4", "#f97316"]))}
    {"".join(f'<rect x="{14 + i * 19}" y="{70 if i % 2 else 74}" width="15" height="{40 if i % 2 else 36}" rx="2" fill="{c}"/>' for i, c in enumerate(["#0ea5e9", "#f43f5e", "#84cc16", "#8b5cf6", "#f59e0b", "#14b8a6", "#64748b"]))}
    <text x="80" y="148" text-anchor="middle" font-family="{SANS}" font-size="19" font-weight="800" fill="#78350f">data shelf</text>
  </g>'''
panda = f'''
  <defs>{grad("pwhite", "#ffffff", "#e5e7eb")}{grad("pblack", "#374151", "#111827")}{grad("pack", "#4ade80", "#15803d")}</defs>
  <!-- backpack -->
  <rect x="80" y="380" width="120" height="180" rx="30" fill="url(#pack)" filter="url(#drop)"/>
  <!-- body -->
  <ellipse cx="270" cy="520" rx="170" ry="150" fill="url(#pwhite)" filter="url(#drop)"/>
  <path d="M120 460 C160 430 380 430 420 460 L420 520 C380 500 160 500 120 520Z" fill="url(#pblack)"/>
  <path d="M170 450 L200 640 M370 450 L340 640" stroke="#15803d" stroke-width="16"/>
  <!-- ears -->
  <circle cx="160" cy="160" r="46" fill="url(#pblack)"/><circle cx="380" cy="160" r="46" fill="url(#pblack)"/>
  <!-- head -->
  <ellipse cx="270" cy="290" rx="170" ry="145" fill="url(#pwhite)" filter="url(#drop)"/>
  <ellipse cx="206" cy="290" rx="44" ry="56" fill="url(#pblack)" transform="rotate(25 206 290)"/>
  <ellipse cx="334" cy="290" rx="44" ry="56" fill="url(#pblack)" transform="rotate(-25 334 290)"/>
  {eye(212, 288, 22, 26, "#78350f", "#fbbf24", look=(8, -4), cid="pdL")}
  {eye(328, 288, 22, 26, "#78350f", "#fbbf24", look=(8, -4), cid="pdR")}
  {blush(176, 352)}{blush(364, 352)}
  <ellipse cx="270" cy="350" rx="18" ry="12" fill="#111827"/>
  <path d="M250 372 C258 388 282 388 290 372" stroke="#111827" stroke-width="4.5" fill="none" stroke-linecap="round"/>
  <!-- bucket hat -->
  <path d="M150 196 C150 110 390 110 390 196Z" fill="#fbbf24" filter="url(#drop)"/>
  <path d="M120 196 C200 176 340 176 420 196 C400 220 140 220 120 196Z" fill="#d97706"/>
  <!-- walking stick and scroll -->
  <path d="M470 280 L430 640" stroke="#92400e" stroke-width="14" stroke-linecap="round"/>
  <circle cx="452" cy="420" r="26" fill="url(#pblack)"/>
  <g filter="url(#drop)" transform="rotate(-10 230 470)">
    <rect x="190" y="420" width="140" height="96" rx="6" fill="#fef9c3" stroke="#ca8a04" stroke-width="3"/>
    <rect x="180" y="410" width="18" height="116" rx="9" fill="#d97706"/><rect x="322" y="410" width="18" height="116" rx="9" fill="#d97706"/>
    <path d="M210 494 C240 470 260 486 280 456 C290 444 300 450 312 436" stroke="#ef4444" stroke-width="3.5" fill="none" stroke-dasharray="6 5"/>
  </g>
  <circle cx="180" cy="480" r="24" fill="url(#pblack)"/>'''
write("ai-reading-map",
      "Anime illustration: a panda hiker in a yellow bucket hat with a green backpack, a walking stick and a scroll map "
      "stands at the start of a winding trail with four flagged stops: 1 how machines learn, 2 how language models "
      "work, 3 building with models, 4 letting models act, and a bookcase labelled data shelf",
      dict(s1="#bbf7d0", s2="#dcfce7", s3="#fefce8"),
      trail + panda + sparkles([(40, 70, 24), (520, 60, 20), (1160, 60, 22), (1120, 380, 16)]))


# =====================================================================
# 7. Forecasting: a penguin ice-cream seller checking two forecasts
# =====================================================================
actual = [42, 55, 61, 48, 70, 83, 66]
fa = [45, 52, 58, 51, 66, 80, 70]
fb = [58, 44, 74, 62, 52, 64, 86]
cx0, cy0, cw, chh = 640, 120, 500, 230  # plot area


def px(i):
    return cx0 + 30 + i * (cw - 60) / 6


def py(v):
    return cy0 + chh - (v - 30) / 60 * chh


bars = "".join(f'<rect x="{px(i) - 18:.0f}" y="{py(v):.0f}" width="36" height="{cy0 + chh - py(v):.0f}" rx="6" fill="#bae6fd"/>'
               for i, v in enumerate(actual))
line = lambda f: " ".join(f'{"M" if i == 0 else "L"}{px(i):.0f} {py(v):.0f}' for i, v in enumerate(f))
dots = lambda f, c: "".join(f'<circle cx="{px(i):.0f}" cy="{py(v):.0f}" r="6" fill="{c}" stroke="#ffffff" stroke-width="2"/>' for i, v in enumerate(f))
days = "".join(f'<text x="{px(i):.0f}" y="{cy0 + chh + 26}" text-anchor="middle" font-family="{SANS}" font-size="16" font-weight="700" fill="#64748b">{d}</text>'
               for i, d in enumerate("MTWTFSS"))
chart = f'''
  <g filter="url(#drop)"><rect x="610" y="40" width="560" height="360" rx="18" fill="#ffffff"/></g>
  <text x="640" y="84" font-family="{SANS}" font-size="24" font-weight="800" fill="{INK}">cones sold vs forecast</text>
  <rect x="640" y="98" width="16" height="12" rx="3" fill="#bae6fd"/><text x="662" y="110" font-family="{SANS}" font-size="15" fill="#475569">actual</text>
  <rect x="728" y="102" width="22" height="4" fill="#16a34a"/><text x="756" y="110" font-family="{SANS}" font-size="15" fill="#475569">model A</text>
  <rect x="838" y="102" width="22" height="4" fill="#ef4444"/><text x="866" y="110" font-family="{SANS}" font-size="15" fill="#475569">model B</text>
  <path d="M{cx0} {cy0 + chh} H{cx0 + cw}" stroke="#cbd5e1" stroke-width="2"/>
  {bars}{days}
  <path d="{line(fb)}" stroke="#ef4444" stroke-width="3" fill="none" stroke-dasharray="8 6"/>{dots(fb, "#ef4444")}
  <path d="{line(fa)}" stroke="#16a34a" stroke-width="3" fill="none"/>{dots(fa, "#16a34a")}'''
score_rows = [("MAE", "3.3", "15.9"), ("RMSE", "3.3", "16.2"), ("MAPE", "5.6%", "26.8%"), ("Theil's U", "0.22", "1.01")]
score = f'''
  <g filter="url(#drop)"><rect x="610" y="420" width="560" height="190" rx="18" fill="#1e293b"/></g>
  <text x="900" y="452" text-anchor="middle" font-family="{SANS}" font-size="17" font-weight="800" fill="#86efac">model A</text>
  <text x="1060" y="452" text-anchor="middle" font-family="{SANS}" font-size="17" font-weight="800" fill="#fca5a5">model B</text>
  {"".join(f'''<text x="640" y="{486 + i * 34}" font-family="{MONO}" font-size="21" font-weight="700" fill="#e2e8f0">{n}</text>
  <text x="900" y="{486 + i * 34}" text-anchor="middle" font-family="{MONO}" font-size="21" font-weight="800" fill="#4ade80">{a}</text>
  <text x="1060" y="{486 + i * 34}" text-anchor="middle" font-family="{MONO}" font-size="21" font-weight="800" fill="#f87171">{b}</text>''' for i, (n, a, b) in enumerate(score_rows))}'''
penguin = f'''
  <defs>{grad("pgb", "#334155", "#0f172a")}{grad("cone", "#fcd34d", "#d97706")}</defs>
  <!-- cart -->
  <g filter="url(#drop)">
    <rect x="300" y="470" width="260" height="130" rx="16" fill="#f472b6"/>
    <path d="M300 500 H560" stroke="#ffffff" stroke-width="10" stroke-dasharray="26 18"/>
    <text x="430" y="566" text-anchor="middle" font-family="{SANS}" font-size="30" font-weight="900" fill="#ffffff">ICE CREAM</text>
    <path d="M290 330 C330 270 530 270 570 330Z" fill="#fde68a"/><path d="M290 330 C330 300 530 300 570 330" stroke="#f59e0b" stroke-width="6" fill="none"/>
    <path d="M320 330 L320 470 M540 330 L540 470" stroke="#94a3b8" stroke-width="8"/>
  </g>
  <!-- penguin body -->
  <ellipse cx="200" cy="440" rx="150" ry="190" fill="url(#pgb)" filter="url(#drop)"/>
  <ellipse cx="200" cy="470" rx="104" ry="150" fill="#ffffff"/>
  <!-- head: dark cap, white face -->
  <ellipse cx="200" cy="262" rx="118" ry="104" fill="url(#pgb)" filter="url(#drop)"/>
  <path d="M118 268 C118 206 168 196 200 222 C232 196 282 206 282 268 C282 316 246 344 200 344 C154 344 118 316 118 268Z" fill="#ffffff"/>
  {eye(160, 262, 24, 30, "#0c4a6e", "#38bdf8", look=(10, -4), cid="pnL")}
  {eye(240, 262, 24, 30, "#0c4a6e", "#38bdf8", look=(10, -4), cid="pnR")}
  {blush(140, 310)}{blush(260, 310)}
  <path d="M180 296 L220 296 L200 322Z" fill="#f59e0b" stroke="#b45309" stroke-width="2"/>
  <!-- scarf -->
  <path d="M90 350 C150 380 250 380 310 350 L314 380 C250 410 150 410 86 380Z" fill="#ef4444"/>
  <path d="M260 384 L276 452 L300 440 L286 380Z" fill="#dc2626"/>
  <!-- flipper holding a cone -->
  <path d="M320 420 C360 400 380 360 390 320" stroke="url(#pgb)" stroke-width="44" fill="none" stroke-linecap="round"/>
  <g filter="url(#drop)">
    <path d="M370 300 L400 240 L430 300Z" fill="url(#cone)" transform="rotate(180 400 270)"/>
    <circle cx="400" cy="222" r="30" fill="#fbcfe8"/><circle cx="380" cy="200" r="24" fill="#a7f3d0"/><circle cx="418" cy="196" r="24" fill="#fde68a"/>
    <circle cx="400" cy="170" r="10" fill="#ef4444"/>
  </g>
  <!-- feet -->
  <ellipse cx="150" cy="622" rx="40" ry="14" fill="#f59e0b"/><ellipse cx="250" cy="622" rx="40" ry="14" fill="#f59e0b"/>'''
write("comparison-of-competing-forecasting-models",
      "Anime illustration: a penguin in a red scarf holds a three-scoop ice-cream cone beside a pink ice-cream cart. A "
      "chart compares a week of cones sold with two forecasts, model A tracking closely and model B zig-zagging, and a "
      "scoreboard reads MAE 3.3 vs 15.9, RMSE 3.3 vs 16.2, MAPE 5.6% vs 26.8%, Theil's U 0.22 vs 1.01",
      dict(s1="#a5f3fc", s2="#e0f2fe", s3="#fdf2f8"),
      penguin + chart + score + sparkles([(40, 60, 24), (470, 80, 20), (580, 420, 16)]))
