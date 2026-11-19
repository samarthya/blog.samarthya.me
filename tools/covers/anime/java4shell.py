"""Anime cover for the Java4Shell (CVE-2026-114938) explainer, in the refined bust-portrait style (refined.py).

Character: a boy with messy teal-black hair, violet eyes and glasses, in a coffee-brown jacket, beside a glowing
chip (the bug lives in a CPU-specific decoder), with a terminal showing the trigger and the two-line check.
Run from the repo root:  python tools/covers/anime/java4shell.py
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))
import refined as R  # noqa: E402

ACCENT = "#c2410c"
OK, KEY, WARN, DIM = "#4ade80", "#fde68a", "#fb923c", "#94a3b8"

body = (R.figure("messy", ("#5eead4", "#0f766e", "#042f2e"), ("#3b0764", "#7c3aed", "#c4b5fd"),
                 outfit=("#7c4a2d", "#4a2c1a"), shirt="#f8fafc", acc="#f97316", glasses=True, mouth="soft")
        + R.holo("chip", ACCENT)
        + R.kicker(640, 92, "CVE-2026-114938 · Java4Shell", ACCENT)
        + R.term_panel(640, 128, 510, "Base64.getDecoder()", [
            "$ decode(\"AAAA…AAAA=\")   # 64 × A, one =",
            ("62 bytes written past a 50-byte buffer", WARN),
            ("Java 17.0.6+  ·  x86-64 AVX-512 VBMI", KEY),
            "",
            "$ export JAVA_TOOL_OPTIONS=\\",
            ("    \"-XX:-UseBASE64Intrinsics\"   # stopgap", OK),
            ("# real fix: update the JDK", DIM)], ACCENT)[0]
        + R.chips(640, 470, ["CVSS 8.1 / 9.8", "pre-login RCE", "patch now"], ACCENT))

R.write("java4shell-cve-2026-114938",
        "Anime illustration: a boy with messy teal hair, violet eyes and glasses, in a brown jacket, beside a glowing "
        "chip and a terminal: decoding 64 letters A and one equals sign writes 62 bytes past a 50-byte buffer on Java "
        "17.0.6 or newer with AVX-512 VBMI; the stopgap is -XX:-UseBASE64Intrinsics and the real fix is updating the "
        "JDK; chips read CVSS 8.1 / 9.8, pre-login RCE, patch now",
        ("#fed7aa", "#ffedd5", "#fff7ed"), ACCENT,
        [(1050, 100, 200, "#fdba74", .5), (120, 560, 220, "#99f6e4", .45), (720, 610, 170, "#ddd6fe", .45)],
        body)
