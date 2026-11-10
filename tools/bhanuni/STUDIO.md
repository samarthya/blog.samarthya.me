# Publishing a new drawing to Bhanuni's Studio

Step by step, from a drawing (on paper or on the tablet) to <https://bhanuni.in>.
For what each field means, see [GALLERY.md](GALLERY.md).

All commands run in PowerShell from the blog folder (the folder of this repo):

```powershell
cd <blog folder>
```

---

## 1. Get the picture

| Kind of drawing | How |
|---|---|
| Digital (tablet/app) | Export it as PNG or JPG. |
| On paper | Photograph it in daylight, flat on a plain surface, straight from above, no shadow of the phone. Crop away the table. |

Put the new files in an **empty folder outside the repos**, for example
`Pictures\bhanuni-new\` in your user folder. Several drawings at once is fine.

## 2. Import

```powershell
tools\bhanuni\.venv\Scripts\python -I tools\bhanuni\import_art.py "<path to>\bhanuni-new"
```

It prints one line per new drawing, for example:

```text
new   my-drawing.jpg -> k7f2qa.jpg  1800x1350  2026-11-20
1 imported
```

For each new drawing it has:

- made a copy with a random id as its name, `content/bhanuni/art/<id>.jpg` (at most 1800 px, rotation fixed)
- **removed all hidden data from the copy** (GPS location, camera, dates)
- added an entry at the **end** of `data/bhanuni.yaml`, with `publish: false`

Your original files are not changed. A drawing that was imported before is skipped.

> First time on a new PC, or if `.venv` is missing:
> `python -m venv tools\bhanuni\.venv` then
> `tools\bhanuni\.venv\Scripts\python -m pip install --use-feature=truststore pillow`

## 3. Fill in the details (with her)

Open `data/bhanuni.yaml`, go to the end, and fill in the new entry:

```yaml
- id: k7f2qa
  title: "Vixen Veda, the comeback"
  date: 2026-11-20
  medium: digital                 # digital | pencil | colour pencil | crayon | ink | paint | mixed
  kind: fan-art                   # original (her own character) | fan-art
  inspired_by: "Miraculous Ladybug"
  series: "Miraculous Ladybug"    # same spelling as the other drawings in that series, or ""
  words: "I worked on her hair for two days!"
  about: "Vixen Veda is back with a new costume."
  featured: false                 # true: it can be dealt in the Favourites
  publish: true                   # <- set to true when she says yes
```

Checklist:

- [ ] `title`: her title
- [ ] `date`: when it was drawn (the import guesses from the photo; fix it if wrong)
- [ ] `words` / `about`: in **her voice**: "my", "I"
- [ ] `series`: copy the exact name from an existing drawing (the 📚 chips on the page show them all)
- [ ] `publish: true`

**Part of a story film?** Give it the story's `series`, place its entry in the right position among the other frames
in `data/bhanuni.yaml` (frames play in file order), and add one more camera move to that story's `moves` in
`data/bhanuni_stories.yaml`. A new story gets a new entry there (see GALLERY.md, "Story films").

## 4. Preview

```powershell
mise exec -- hugo server
```

Open <http://localhost:1313/bhanuni/>. The new drawing is first in **All drawings** (newest first). Click it and check
the title, the note and that the picture is the right way up. Stop the server with `Ctrl+C`.

## 5. Publish

```powershell
git add content/bhanuni/art data/bhanuni.yaml data/bhanuni_stories.yaml
git commit -m "Studio: new drawing - Vixen Veda, the comeback"
git push origin main
```

It is live on <https://bhanuni.in> about two minutes later. To send someone straight to the new drawing, open it on
the page and copy the address: `https://samarthya.me/bhanuni/#k7f2qa`.

---

## Changes later

| I want to... | Do this |
|---|---|
| Rename it or change its note | Edit its entry in `data/bhanuni.yaml`, then steps 4-5 |
| Hide it for now | `publish: false`, then step 5 |
| Remove it for good | Delete its entry **and** `content/bhanuni/art/<id>.jpg`, then step 5 (`git add -A content/bhanuni`) |
| Make it a favourite | `featured: true` |
| Replace it with a better photo | Delete the old entry and file, import the new photo (step 2), fill in again |
| Find a drawing's id | Click it on the page; the address ends in `#<id>` |

## Rules

- First name only. No photos of her or anyone else, no school, no places, no birthday.
- She says yes before anything goes up.
- The original files stay with you. `tools/bhanuni/ids.local.csv` (on this PC only, never committed) remembers which
  originals were imported.
