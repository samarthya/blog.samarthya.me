"""Anime covers for the "AI from the ground up" series, in the refined bust-portrait style (refined.py, 2026-11-12).

One character per part, never reused:
  0 a maths cheat sheet       a girl with long navy hair and a pink hair clip, cream blazer; vector hologram
  1 the maths behind an LLM   a boy with silver-blue hair and glasses, navy blazer; matrix hologram
  2 probability               a girl with a rose-pink bob and teal eyes, lavender cardigan; probability bars
  3 what GPUs do              a boy with messy auburn hair and headphones round his neck, slate hoodie; chip
  4 frontier models           a girl with a blonde ponytail, teal jacket; constellation
  5 using models effectively  a boy with black hair and gold eyes, charcoal jacket; checklist

The technical diagram of each post stays in its body as overview.svg; this writes cover.svg and feature.png.
Run from the repo root:  python tools/covers/anime/ground_up.py [slug ...]
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))
import refined as R  # noqa: E402

SKY = ("#e9d5ff", "#fae8ff", "#fff7ed")
ACCENT = "#a21caf"
OK, KEY, WARN, DIM = "#4ade80", "#fde68a", "#fb923c", "#94a3b8"
only = sys.argv[1:]
PX, PY, PW = 640, 128, 510


def cover(slug, kicker, desc, fig, holo, panel, blobs, chips=()):
    if only and slug not in only:
        return
    psvg, h = panel
    body = fig + R.holo(holo, ACCENT) + R.kicker(PX, 92, kicker, ACCENT) + psvg
    if chips:
        body += R.chips(PX, PY + h + 22, chips, ACCENT)
    R.write(slug, f"Anime illustration: {desc}", SKY, ACCENT, blobs, body)


def steps(title, rows):
    return R.steps_panel(PX, PY, PW, title, rows, ACCENT)


def term(title, lines):
    return R.term_panel(PX, PY, PW, title, lines, ACCENT)


cover("ai-ground-up-0-maths-cheat-sheet", "AI from the ground up · 0",
      "a girl with long navy hair, amber eyes and a pink hair clip, in a cream blazer, beside a glowing pair of vector "
      "arrows and a cheat sheet: a vector [3, 4], its size 5, cosine as the dot product over both sizes, and a matrix "
      "that rotates 90 degrees; chips read dot picks T-102 and cosine picks T-101",
      R.figure("long", ("#4c4f9e", "#2e2f6e", "#15163a"), ("#3b1d0e", "#b45309", "#fcd34d"),
               outfit=("#fef3c7", "#e7c9a0"), acc="#f472b6", clip=True, tie="#a21caf"),
      "vector",
      steps("A maths cheat sheet", [("Vector", "[3, 4]"), ("Size ‖a‖", "√(3²+4²) = 5"),
                                    ("Cosine", "a·b / (‖a‖ ‖b‖)"), ("Matrix", "rotate 90°")]),
      [(1050, 100, 200, "#f0abfc", .5), (120, 560, 220, "#c4b5fd", .55), (700, 600, 180, "#fbcfe8", .5)],
      chips=["dot picks T-102", "cosine picks T-101"])

cover("ai-ground-up-1-maths-behind-llms", "AI from the ground up · 1",
      "a boy with silver-blue hair and glasses, in a navy blazer, beside a glowing matrix and the four ideas: vectors "
      "(cat and dog similarity 0.99), matrix multiplication (about 2 n cubed operations), softmax (0.88, 0.07, 0.04) and "
      "gradients (w from 0 to 2); chips read softmax(QKᵀ/√d)·V and 2× context = 4× attention",
      R.figure("short", ("#c7d2fe", "#7c8fc9", "#3b4a7a"), ("#2e1065", "#7c3aed", "#c4b5fd"),
               outfit=("#334155", "#1e293b"), tie="#22d3ee", glasses=True, mouth="soft"),
      "matrix",
      steps("The maths behind an LLM", [("Vectors", "cat·dog 0.99"), ("Matrix multiply", "≈ 2·n³ ops"),
                                        ("Softmax", "0.88 · 0.07 · 0.04"), ("Gradients", "w: 0 → 2")]),
      [(1050, 90, 210, "#c4b5fd", .55), (110, 560, 220, "#a5f3fc", .45), (720, 610, 170, "#f0abfc", .45)],
      chips=["softmax(QKᵀ/√d)·V", "2× context = 4× attention"])

cover("ai-ground-up-2-probability", "AI from the ground up · 2",
      "a girl with a rose-pink bob and teal eyes, in a lavender cardigan, beside glowing probability bars and a terminal "
      "showing temperature sampling: Paris 99% at temperature 0.5, 85% at 1.0, 67% at 1.5, and top-p 0.9 keeping only "
      "Paris and London",
      R.figure("bob", ("#fecdd3", "#f472b6", "#9d174d"), ("#134e4a", "#0d9488", "#5eead4"),
               outfit=("#ddd6fe", "#a78bfa"), shirt="#ffffff", acc="#22d3ee", earring=True, clip=True, mouth="open"),
      "bars",
      term("sampling.py", ["$ python sampling.py", ("T=0.5: Paris 99%  London 1%", KEY), ("T=1.0: Paris 85%  London 7%", OK),
                           ("T=1.5: Paris 67%  London 13%", WARN), ("top-p 0.9: Paris 92%  London 8%", "#67e8f9"), "",
                           ("# P(attack | alert) = 4.7%", DIM)]),
      [(1060, 110, 200, "#fbcfe8", .55), (120, 560, 220, "#99f6e4", .45), (700, 600, 170, "#ddd6fe", .5)])

cover("ai-ground-up-3-what-gpus-do", "AI from the ground up · 3",
      "a boy with messy auburn hair and green eyes, headphones round his neck and a slate hoodie, beside a glowing chip "
      "and four GPU facts: thousands of cores in warps of 32, tensor cores where FP8 is about 60 times FP64, the memory "
      "wall at about 209 tokens per second for an 8B model on one H100, and 72 GPUs in a Rubin rack; chips read H100 "
      "3.35 TB/s, FlashAttention 3×, NVLink",
      R.figure("messy", ("#fdba74", "#c2410c", "#6b1d0a"), ("#14532d", "#16a34a", "#86efac"),
               outfit=("#475569", "#1e293b"), shirt="#334155", acc="#f97316", headphones=True, mouth="smile"),
      "chip",
      steps("What GPUs actually do", [("Thousands of cores", "warps of 32"), ("Tensor cores", "FP8 ≈ 60× FP64"),
                                      ("Memory wall", "≈ 209 tok/s, 8B"), ("Scale out", "72 GPUs a rack")]),
      [(1050, 100, 210, "#fed7aa", .5), (110, 560, 220, "#c4b5fd", .5), (720, 610, 170, "#fbcfe8", .45)],
      chips=["H100: 3.35 TB/s", "FlashAttention 3×", "NVLink"])

cover("ai-ground-up-4-frontier-models", "AI from the ground up · 4",
      "a girl with a blonde ponytail and blue eyes, in a teal jacket, beside a glowing constellation and the late-2026 "
      "frontier releases: Claude Fable 5.2 on 9 November, Gemini 4 Argon on 30 September, GPT-6 Astra on 3 September and "
      "Kimi K3 with open weights on 16 July; chips read EU 10^25, SB 53 10^26, 4-5 times a year",
      R.figure("ponytail", ("#fef08a", "#eab308", "#854d0e"), ("#1e3a8a", "#2563eb", "#93c5fd"),
               outfit=("#0f766e", "#134e4a"), acc="#a21caf", mouth="smile"),
      "stars",
      steps("The frontier, Nov 2026", [("Claude Fable 5.2", "9 Nov"), ("Gemini 4 Argon", "30 Sep"),
                                       ("GPT-6 Astra", "3 Sep"), ("Kimi K3 (open)", "16 Jul")]),
      [(1050, 100, 210, "#bfdbfe", .55), (120, 560, 220, "#f0abfc", .45), (700, 610, 170, "#fde68a", .45)],
      chips=["EU: 10²⁵", "SB 53: 10²⁶", "4–5× a year"])

cover("ai-ground-up-5-using-models-well", "AI from the ground up · 5",
      "a boy with black hair and gold eyes, in a charcoal jacket, beside a glowing checklist and a terminal running a "
      "small evaluation: six tickets right, two wrong, accuracy 75%, and the failures become the rules",
      R.figure("short", ("#475569", "#1e293b", "#020617"), ("#78350f", "#d97706", "#fde68a"),
               outfit=("#3f3f46", "#18181b"), shirt="#f8fafc", tie="#a21caf", acc="#a21caf", earring=True, mouth="soft"),
      "check",
      term("eval.py", ["$ python eval.py", ("ok   kubernetes <- kubernetes", OK), ("ok   kafka      <- kafka", OK),
                       ("BAD  elastic    <- other", WARN), ("BAD  other      <- kubernetes", WARN), ("accuracy: 75%", KEY), "",
                       ("# the failures become the rules", DIM)]),
      [(1050, 100, 210, "#fde68a", .5), (120, 560, 220, "#c4b5fd", .5), (720, 610, 170, "#f0abfc", .45)])
