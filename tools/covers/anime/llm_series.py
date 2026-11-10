"""Anime covers for the "How an LLM is built" series (2026-11-10): one character per part, never reused.

  1 the data and the design   an owl holding a book marked 15.5T, beside stages 1-3 with K2's numbers
  2 pre-training              a girl in a headset holding a light bulb, beside the real output of the post's toy run
  3 base model to assistant   a puppy in a graduation cap holding a diploma scroll, beside stages 6-9

The technical diagram of each post stays in its body as overview.svg; this writes cover.svg and feature.png.
Run from the repo root:  python tools/covers/anime/llm_series.py [slug ...]
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from kit import *  # noqa: E402,F403
from kit import _esc  # noqa: E402
from topics import CAST, OK, DIM, KEY, _steps, _term, chips_row  # noqa: E402

SKY = dict(s1="#ddd6fe", s2="#ede9fe", s3="#f5f3ff")
ACCENT = "#6d28d9"


def figure(who, prop_kind, col, label="", **over):
    kind, kw, desc = CAST[who]
    held = prop(prop_kind, col, label)
    kw = dict(kw, **over)
    return (critter(prop=held, **kw) if kind == "a" else kid(prop=held, **kw)), desc


def cover(slug, kicker, fig, panel_svg, alt, chips=(), chips_y=470):
    extra = chips_row(chips, chips_y, ACCENT) if chips else ""
    body = (panel_svg + extra + pill(600, 66, kicker, ACCENT, size=21) + fig
            + sparkles(((40, 70, 24), (560, 40, 18), (1165, 600, 22))))
    write(slug, _esc(alt), SKY, body, only=[slug])


only = sys.argv[1:]

s = "how-an-llm-is-built-1-data-and-design"
if not only or s in only:
    fig, desc = figure("owl", "book", "#7c3aed", "15.5T")
    panel, h = _steps("How an LLM is built · 1", [("1 Data", "15.5T tokens"), ("2 Tokenizer", "160K vocab"),
                                                   ("3 Architecture", "1.04T · 32.6B active")], 140, ACCENT)
    cover(s, "The plan, the data, the design", fig, panel,
          f"Anime illustration: {desc} holding a book marked 15.5T, beside the first three stages of "
          "building Kimi K2: data, 15.5T tokens; tokenizer, 160K vocabulary; architecture, 1.04T parameters with 32.6B "
          "active; chips read web, code, maths, knowledge, Mixture-of-Experts",
          chips=["web · code · maths", "knowledge", "Mixture-of-Experts"], chips_y=140 + h + 22)

s = "how-an-llm-is-built-2-pre-training"
if not only or s in only:
    fig, desc = figure("tealgirl", "bulb", "#facc15", hat="headset", acc="#6d28d9")
    panel, _ = _term("tiny_lm.py", ["$ python tiny_lm.py", ("step   0  loss 2.958", "#f87171"), ("step 100  loss 0.122", KEY),
                                     ("step 300  loss 0.125", OK), ("t up. build again. fall. get up.", "#67e8f9"), "",
                                     ("# Kimi K2: same loop, 15.5T tokens", DIM)], 140)
    cover(s, "Pre-training: guess, check, adjust", fig, panel,
          f"Anime illustration: {desc} wearing a headset and holding a glowing light bulb, beside a terminal running the "
          "post's tiny training loop: loss falls from 2.958 to 0.125 and the model writes back the motto; chips read "
          "MuonClip τ=100, 67M-token batches, 4K→128K",
          chips=["MuonClip τ=100", "67M-token batches", "4K → 128K"])

s = "how-an-llm-is-built-3-base-to-assistant"
if not only or s in only:
    fig, desc = figure("dog", "scroll", "#16a34a", hat="grad_cap")
    panel, _ = _steps("How an LLM is built · 3", [("6 Fine-tuning", "23,000+ tools"), ("7 RL", "graded practice"),
                                                   ("8 Evaluation", "SWE-bench 65.8"), ("9 Release", "~1 TB open weights")], 140, ACCENT)
    cover(s, "From base model to assistant", fig, panel,
          f"Anime illustration: {desc} in a graduation cap holding a diploma scroll, beside the last four stages of building "
          "Kimi K2: fine-tuning with 23,000+ tools, reinforcement learning as graded practice, evaluation with SWE-bench "
          "Verified 65.8, and release as about 1 TB of open weights; chips read verifiable rewards, rubrics, modified MIT",
          chips=["verifiable rewards", "rubrics", "modified MIT"])
