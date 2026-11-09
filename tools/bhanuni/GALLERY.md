# Bhanuni's Studio: how to update the gallery

The gallery lives at <https://samarthya.me/bhanuni/> (and <https://bhanuni.in> redirects there).

| What | Where |
|---|---|
| The list of drawings (titles, dates, favourites, ...) | `data/bhanuni.yaml` |
| The pictures | `content/bhanuni/art/<id>.jpg` |
| The page | `layouts/_default/bhanuni.html`, `layouts/partials/bhanuni-card.html` |
| Page title and description | `content/bhanuni/index.md` |
| Importer | `tools/bhanuni/import_art.py` |

Every drawing has a random 6-letter **id** (for example `8xms7k`). The id is both the file name and the key in
`data/bhanuni.yaml`.

## Find the id of a drawing

Open the gallery, click the drawing, and look at the address bar: `.../bhanuni/#8xms7k`. The part after `#` is the
id. Then search `data/bhanuni.yaml` for `id: 8xms7k`.

## Change a title, a note or anything else

Edit that drawing's entry in `data/bhanuni.yaml`:

```yaml
- id: 8xms7k
  title: "Buddha"                  # her title for it
  date: 2026-04-18                 # when it was drawn
  medium: colour pencil            # digital | pencil | colour pencil | crayon | ink | paint | mixed
  kind: original                   # original | fan-art  (the "My own characters" / "Fan art" filters)
  inspired_by: ""                  # for fan art: the show, game or book, e.g. "Miraculous"
  series: ""                       # drawings that belong together share the same series name
  words: ""                        # one line in HER words, shown in quotes under the picture
  about: ""                        # optional note on what is happening, e.g. one frame of a story
  featured: false                  # true: it can be dealt in the Favourites
  publish: true                    # false: hidden from the site (the picture stays in the repo)
```

Tips:

- Keep the quotes around text that contains a colon (`:`) or starts with a special character.
- She is the artist, so everything shown on the page speaks as her, in the first person ("my", "I"):
  `words` is a line she says about the drawing (shown in quotes), `about` is the story behind it
  ("My take on ...", not "Her take on ...").
- **Stories in frames** (like "The snack table"): give each frame the same `series`, number the titles
  ("..., 1", "..., 2"), and keep the entries in story order in the file. Drawings with the same date are shown in
  file order.
- **Hide** a drawing: `publish: false`. **Remove** it completely: delete its entry and its `art/<id>.jpg`.

## Add new drawings

1. Put the photos or files in any folder (outside the repos).
2. Run:

   ```bash
   python -I tools/bhanuni/import_art.py "<that folder>"
   ```

   It gives each new picture a random id, straightens it, scales it to at most 1800 px, **removes all hidden data
   (GPS location, camera, dates)** and adds an entry at the end of `data/bhanuni.yaml` with `publish: false`.
   Files it has seen before are skipped, so running it twice is safe. (It needs Pillow: `pip install pillow`.)
3. Fill in the new entries (title, medium, kind, ...) and set `publish: true` for the ones she wants to show.

The list of original file names is kept only on this PC in `tools/bhanuni/ids.local.csv` (git-ignored).

## Preview, then publish

```bash
mise exec -- hugo server        # then open http://localhost:1313/bhanuni/
git add data/bhanuni.yaml content/bhanuni
git commit -m "Gallery: <what changed>"
git push origin main            # live a couple of minutes later
```

## Rules for this page

- First name only. No photos of her or other people, no school, no places, no birthday.
- Ask her before a drawing goes up.
- The page is kept out of search engines (`noindex`) and out of the blog's lists, RSS and sitemap.
