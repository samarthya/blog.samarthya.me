"""Anime cover for "Security standards, part 5: CVE, CWE, NVD and CVSS", refined style (refined.py).

Character: a girl with a dark auburn ponytail, green eyes and a gold earring, in a navy blazer with a red tie,
beside glowing severity bars (CVSS is the ruler), with the four names and their jobs on a glass panel.
Run from the repo root:  python tools/covers/anime/security_standards_5.py
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))
import refined as R  # noqa: E402

ACCENT = "#b91c1c"
PX, PY, PW = 640, 128, 510

panel, h = R.steps_panel(PX, PY, PW, "Four names, one bug", [
    ("CVE · the name", "CVE-2025-30065"),
    ("CWE · the kind", "CWE-502"),
    ("NVD · the library", "Analyzed"),
    ("CVSS · the ruler", "9.8 / 10.0")], ACCENT)

body = (R.figure("ponytail", ("#b45309", "#7c2d12", "#3b0f06"), ("#14532d", "#16a34a", "#86efac"),
                 outfit=("#1e3a8a", "#172554"), shirt="#f8fafc", acc="#fbbf24", earring=True, tie=ACCENT,
                 mouth="smile")
        + R.holo("bars", ACCENT)
        + R.kicker(PX, 92, "Security standards · 5", ACCENT)
        + panel
        + R.chips(PX, PY + h + 22, ["CVSS v2 → 3.1 → 4.0", "severity ≠ risk"], ACCENT))

R.write("security-standards-5-cve-cwe-nvd-cvss",
        "Anime illustration: a girl with a dark auburn ponytail, green eyes and a gold earring, in a navy blazer with "
        "a red tie, beside glowing severity bars and a panel titled Four names, one bug: CVE the name, CVE-2025-30065; "
        "CWE the kind, CWE-502; NVD the library, Analyzed; CVSS the ruler, 9.8 and 10.0; chips read CVSS v2 to 3.1 "
        "to 4.0 and severity is not risk",
        ("#fecaca", "#fee2e2", "#fff7ed"), ACCENT,
        [(1050, 100, 200, "#fca5a5", .5), (120, 560, 220, "#bfdbfe", .45), (720, 610, 170, "#fde68a", .45)],
        body)
