# Safe publishing and privacy checks

This repository is public, and everything in it is published to the web. These guards keep secrets, personal
data and migration leftovers out.

## The privacy check

`tools/privacy/check.py` scans what gets published (`content/`, `static/`, `assets/`, `data/`, `layouts/`,
`config/`) and fails if it finds:

| Rule | Examples |
|---|---|
| `jwt`, `private-key` | JSON Web Tokens, `-----BEGIN … PRIVATE KEY-----` |
| `aws-access-key`, `github-token`, `google-api-key`, `slack-token` | Well-known credential formats |
| `secret-assignment` | `password=…`, `"api_key": "…"`, `token: …` with a real-looking value |
| `local-path` | Windows user folders, temp folders, migration file names (`wp-import/`, `uploads.zip`, `*.sql.gz`) |
| `forbidden-file` | `.sql`, `.zip`, `.php`, `.env`, private notes such as `TODO.md` |
| `image-metadata` | JPEG/PNG/WebP with GPS position, owner/artist, camera serial numbers or copyright |

It deliberately does **not** flag email addresses (example data and the public contact address are intentional)
or documentation placeholders such as `<API_KEY>`, `${TOKEN}`, `$(kubectl …)`, `xxxx` or `changeme`.

Run it before pushing (Python 3.9+, no packages needed):

```sh
python tools/privacy/check.py              # default folders
python tools/privacy/check.py content/posts/my-new-post
python -m unittest discover -s tools/privacy -v
```

Output is `file:line: [rule] masked-value (fp fingerprint)`. Secrets are masked in the output.

**In CI** the same check runs before every deploy (`.github/workflows/hugo.yml`) and on pull requests
(`.github/workflows/validate.yml`, which builds but never deploys). A finding stops the deploy.

### The allowlist

`tools/privacy/allowlist.txt` lists findings that were reviewed and are safe to publish, such as credentials in old
posts that belonged to long-gone lab systems. Entries are a rule plus a fingerprint (the start of a SHA-256 of
the value), so the value isn't repeated, and a *different* secret in the same post still fails. Add an entry
only with a comment explaining why it's harmless. Never allowlist a live credential: remove or rotate it.

## Photos

Phone and camera photos often carry the location where they were taken, the owner's name and serial numbers.
The check reports them. To strip metadata before committing, use any of:

```sh
exiftool -all= -overwrite_original photo.jpg          # ExifTool
magick photo.jpg -strip photo.jpg                      # ImageMagick
```

On Windows: *Properties → Details → Remove Properties and Personal Information*.

## Migration files and local notes

`.gitignore` keeps WordPress exports, database dumps, upload archives, import reports and private notes out of
commits. **It does not protect those files in any other way.** They are still on disk, still copied by backup
and cloud-sync tools, and still readable by anything that compromises the machine. Raw exports from a hacked
site can also contain planted code. So:

- keep raw exports **outside** the repository folder, ideally in encrypted storage
  (an encrypted disk image, a password-manager attachment, or an encrypted archive);
- never extract an upload archive from a compromised server inside the repository;
- delete local copies once the migration is finished and an encrypted backup exists.

## Analytics

Production builds include Google Analytics 4 (`[services.googleAnalytics]` in `config/_default/hugo.toml`);
`hugo server` and development builds do not. The contact page carries a short disclosure. Removing the ID from
the config removes analytics from every page.
