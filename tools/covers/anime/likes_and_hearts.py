"""Anime cover for "Likes and hearts: a basic interactive interface for my site", refined style (refined.py).

Character: a girl with a dark-teal bob, amber eyes and a hair clip, in a mustard-brown cardigan, beside a glowing heart
with small hearts floating off it (one tap leaves a mark), with the three reactions on a glass panel.
Run from the repo root:  python tools/covers/anime/likes_and_hearts.py
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))
import refined as R  # noqa: E402

ACCENT = "#db2777"
PX, PY, PW = 640, 128, 510

panel, h = R.steps_panel(PX, PY, PW, "Leave a mark, not a comment", [
    ("👍 like", "one tap"),
    ("👎 dislike", "one tap"),
    ("❤️ heart", "one tap"),
    ("login needed", "none")], ACCENT)

body = (R.figure("bob", ("#2dd4bf", "#0f766e", "#042f2e"), ("#b45309", "#f59e0b", "#fde68a"),
                 outfit=("#ca8a04", "#854d0e"), shirt="#f8fafc", acc=ACCENT, clip=True, mouth="smile")
        + R.holo("hearts", ACCENT)
        + R.kicker(PX, 92, "Static site · interactive", ACCENT)
        + panel
        + R.chips(PX, PY + h + 22, ["no comments", "nothing personal stored"], ACCENT))

R.write("likes-and-hearts",
        "Anime illustration: a girl with a dark-teal bob, amber eyes and a hair clip, in a mustard-brown cardigan, beside a "
        "glowing pink heart with small hearts floating off it, and a panel titled Leave a mark, not a comment: like, "
        "dislike and heart, each one tap, and no login needed; chips read no comments and nothing personal stored",
        ("#fbcfe8", "#fce7f3", "#fff7ed"), ACCENT,
        [(1050, 100, 200, "#f9a8d4", .5), (120, 560, 220, "#99f6e4", .45), (720, 610, 170, "#fde68a", .45)],
        body)
