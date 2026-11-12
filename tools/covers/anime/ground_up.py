"""Anime covers for the "AI from the ground up" series (2026-11-10): one character per part, never reused.

  0 a maths cheat sheet        a fox holding a book, beside vector, size, cosine and matrix
  1 the maths behind an LLM     a boy with blue hair and glasses holding a pencil, beside the four ideas
  2 probability                 a girl with pink pigtails holding an "85%" balloon, beside the sampling output
  3 what GPUs do                a bear holding a wrench, beside the four GPU facts
  4 frontier models             a penguin with a telescope, beside the late-2026 frontier releases
  5 using models effectively    a curly-haired boy holding an "eval 75%" sign, beside the harness output

The technical diagram of each post stays in its body as overview.svg; this writes cover.svg and feature.png.
Run from the repo root:  python tools/covers/anime/ground_up.py [slug ...]
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from kit import *  # noqa: E402,F403
from kit import _esc  # noqa: E402
from topics import CAST, OK, DIM, KEY, WARN, _steps, _term, chips_row  # noqa: E402

SKY = dict(s1="#f5d0fe", s2="#fae8ff", s3="#fdf4ff")
ACCENT = "#a21caf"
only = sys.argv[1:]


def figure(who, prop_kind, col, label="", **over):
    kind, kw, desc = CAST[who]
    held = prop(prop_kind, col, label)
    kw = dict(kw, **over)
    return (critter(prop=held, **kw) if kind == "a" else kid(prop=held, **kw)), desc


def cover(slug, kicker, who, prop_args, over, panel, alt_tail, chips=()):
    if only and slug not in only:
        return
    fig, desc = figure(who, *prop_args, **over)
    psvg, h = panel
    extra = chips_row(chips, 140 + h + 22, ACCENT) if chips else ""
    body = psvg + extra + pill(600, 66, kicker, ACCENT, size=21) + fig + sparkles(((40, 70, 24), (560, 40, 18), (1165, 600, 22)))
    write(slug, _esc(f"Anime illustration: {desc}{alt_tail}"), SKY, body, only=[slug])


cover("ai-ground-up-0-maths-cheat-sheet", "AI from the ground up · 0", "fox", ("book", "#a21caf"), {},
      _steps("A maths cheat sheet", [("Vector", "[3, 4]"), ("Size ‖a‖", "√(3²+4²) = 5"),
                                     ("Cosine", "a·b / (‖a‖ ‖b‖)"), ("Matrix", "rotate 90°")], 140, ACCENT),
      " holding a book, beside a four-step cheat sheet: a vector [3, 4], its size 5, cosine as the dot product over both "
      "sizes, and a matrix that rotates an arrow 90 degrees; chips read dot picks T-102 and cosine picks T-101",
      chips=["dot picks T-102", "cosine picks T-101"])

cover("ai-ground-up-1-maths-behind-llms", "AI from the ground up · 1", "blueboy", ("pencil", "#a21caf"), {},
      _steps("The maths behind an LLM", [("Vectors", "cat·dog 0.99"), ("Matrix multiply", "≈ 2·n³ ops"),
                                         ("Softmax", "0.88 · 0.07 · 0.04"), ("Gradients", "w: 0 → 2")], 140, ACCENT),
      " holding a pencil, beside the four ideas: vectors (cat and dog similarity 0.99), matrix multiplication (about 2 n cubed "
      "operations), softmax (0.88, 0.07, 0.04) and gradients (w from 0 to 2); chips read softmax(QKᵀ/√d)·V and 2× context = 4× attention",
      chips=["softmax(QKᵀ/√d)·V", "2× context = 4× attention"])

cover("ai-ground-up-2-probability", "AI from the ground up · 2", "redgirl", ("balloon", "#06b6d4", "85%"), {},
      _term("sampling.py", ["$ python sampling.py", ("T=0.5: Paris 99%  London 1%", KEY), ("T=1.0: Paris 85%  London 7%", OK),
                            ("T=1.5: Paris 67%  London 13%", WARN), ("top-p 0.9: Paris 92%  London 8%", "#67e8f9"), "",
                            ("# P(attack | alert) = 4.7%", DIM)], 140),
      " holding a balloon marked 85%, beside a terminal showing temperature sampling: Paris 99% at temperature 0.5, 85% at 1.0, "
      "67% at 1.5, and top-p 0.9 keeping only Paris and London")

cover("ai-ground-up-3-what-gpus-do", "AI from the ground up · 3", "bear", ("wrench", "#0369a1"), {},
      _steps("What GPUs actually do", [("Thousands of cores", "warps of 32"), ("Tensor cores", "FP8 ≈ 60× FP64"),
                                       ("Memory wall", "≈ 209 tok/s, 8B"), ("Scale out", "72 GPUs a rack")], 140, ACCENT),
      " holding a wrench, beside four GPU facts: thousands of cores in warps of 32, tensor cores where FP8 is about "
      "60 times FP64, the memory wall at about 209 tokens per second for an 8B model on one H100, and 72 GPUs in a Rubin rack; chips "
      "read H100 3.35 TB/s, FlashAttention 3×, NVLink",
      chips=["H100: 3.35 TB/s", "FlashAttention 3×", "NVLink"])

cover("ai-ground-up-4-frontier-models", "AI from the ground up · 4", "penguin", ("telescope", "#a21caf"), {},
      _steps("The frontier, Nov 2026", [("Claude Fable 5.2", "9 Nov"), ("Gemini 4 Argon", "30 Sep"),
                                        ("GPT-6 Astra", "3 Sep"), ("Kimi K3 (open)", "16 Jul")], 140, ACCENT),
      " looking through a telescope, beside the late-2026 frontier releases: Claude Fable 5.2 on 9 November, Gemini 4 Argon on "
      "30 September, GPT-6 Astra on 3 September and Kimi K3 with open weights on 16 July; chips read EU 10^25, SB 53 10^26, "
      "4-5 times a year",
      chips=["EU: 10²⁵", "SB 53: 10²⁶", "4–5× a year"])

cover("ai-ground-up-5-using-models-well", "AI from the ground up · 5", "curlyboy", ("sign", "#a21caf", "eval 75%"), {},
      _term("eval.py", ["$ python eval.py", ("ok   kubernetes <- kubernetes", OK), ("ok   kafka      <- kafka", OK),
                        ("BAD  elastic    <- other", WARN), ("BAD  other      <- kubernetes", WARN), ("accuracy: 75%", KEY), "",
                        ("# the failures become the rules", DIM)], 140),
      " holding a sign reading eval 75%, beside a terminal running a small evaluation: six tickets right, two wrong, accuracy 75%, "
      "and the failures become the rules")
