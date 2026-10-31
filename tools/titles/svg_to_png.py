#!/usr/bin/env python3
"""svg_to_png.py: render a post's illustration (overview.svg, 1200x630) to its feature.png.

Usage: python tools/titles/svg_to_png.py content/posts/<slug>/overview.svg [out.png]
       (out defaults to feature.png next to the SVG)

The SVG goes in the article body as a crisp figure; the PNG is the card and social-preview image, because
LinkedIn and most link previews do not accept SVG. Rendering uses a headless Chromium browser (Edge or Chrome)
so fonts, filters and gradients look exactly as they do on the site. Standard library only.

Two Windows quirks this works around: headless Edge will not screenshot a file:// SVG, so the file is served
over a throwaway local HTTP server; and the screenshot path must be absolute.
"""
import functools
import http.server
import os
import shutil
import subprocess
import sys
import tempfile
import threading
from pathlib import Path

WIDTH, HEIGHT = 1200, 630
BROWSERS = [
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    "msedge", "google-chrome", "chromium", "chromium-browser",
]


def find_browser() -> str:
    for b in BROWSERS:
        if os.path.isfile(b) or shutil.which(b):
            return b
    sys.exit("svg_to_png.py: no Edge or Chrome found")


class Quiet(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *args):
        pass


def main() -> None:
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    svg = Path(sys.argv[1]).resolve()
    out = Path(sys.argv[2]).resolve() if len(sys.argv) > 2 else svg.with_name("feature.png")
    if svg.suffix.lower() != ".svg" or not svg.is_file():
        sys.exit(f"svg_to_png.py: not an SVG file: {svg}")

    # Serve only the SVG's own folder, on a free port, for the length of one screenshot.
    handler = functools.partial(Quiet, directory=str(svg.parent))
    server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), handler)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    url = f"http://127.0.0.1:{server.server_port}/{svg.name}"

    with tempfile.TemporaryDirectory() as profile:  # a fresh profile, so a running browser cannot block it
        subprocess.run([
            find_browser(), "--headless", "--disable-gpu", "--hide-scrollbars",
            f"--user-data-dir={profile}", f"--window-size={WIDTH},{HEIGHT}",
            "--virtual-time-budget=3000", f"--screenshot={out}", url,
        ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=60)
    server.shutdown()

    if not out.is_file():
        sys.exit("svg_to_png.py: the browser did not write a screenshot")
    print(f"{out} ({out.stat().st_size // 1024} KB)")


if __name__ == "__main__":
    main()
