"""Render a title image for a new post from a small JSON spec, in the site's title-card style.

Reuses the layouts of make_titles.py (steps, cards, compare) and takes the colours of any topic in
data/covers.yaml, so every new post gets a 1200x630 card that matches the recovered ones.

    tools\\.venv\\Scripts\\python.exe -I tools\\titles\\title_card.py path\\to\\spec.json

Spec (JSON):
    {
      "topic":  "kubernetes",                      # a name from data/covers.yaml
      "layout": "steps" | "cards" | "compare",
      "kicker": "Kubernetes · networking",          # small line above the title
      "title":  "How a Service finds its Pods",     # keep it to one line (about 40 characters)
      "note":   "One sentence shown at the bottom",
      "items":  [["Heading", "detail"], ...],       # steps (3-5) and cards (3-8)
      "left": "A", "right": "B",                    # compare only
      "rows":  [["label", "left text", "right text"], ...],   # compare only (3-4 rows)
      "out":   "content/posts/<slug>/feature.png"
    }
"""
import json
import sys
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))  # -I drops the script's folder from sys.path
import make_titles as mt  # noqa: E402

LAYOUTS = {"steps", "cards", "compare"}


def main(spec_path):
    spec = json.loads(Path(spec_path).read_text(encoding="utf-8"))
    topics = yaml.safe_load((mt.ROOT / "data" / "covers.yaml").read_text(encoding="utf-8"))["topics"]
    colours = {t["name"]: (t["from"], t["to"]) for t in topics}
    topic = spec["topic"]
    if topic not in colours:
        sys.exit(f"unknown topic {topic!r}; choose one of: {', '.join(colours)}")
    mt.TOPIC.update(colours)  # make_titles only lists the topics it needed; give it all of them

    layout = spec.get("layout", "cards")
    if layout not in LAYOUTS:
        sys.exit(f"layout must be one of {sorted(LAYOUTS)}")
    note = spec.get("note", "")
    if layout == "compare":
        im = mt.compare(topic, spec["kicker"], spec["title"], spec["left"], spec["right"],
                        [tuple(r) for r in spec["rows"]], note)
    else:
        draw = mt.steps if layout == "steps" else mt.cards
        im = draw(topic, spec["kicker"], spec["title"], [tuple(i) for i in spec["items"]], note)

    out = mt.ROOT / spec["out"]
    out.parent.mkdir(parents=True, exist_ok=True)
    im.save(out, optimize=True)
    print(out.relative_to(mt.ROOT))


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    main(sys.argv[1])
