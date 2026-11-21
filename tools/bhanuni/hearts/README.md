# Hearts for Bhanuni's Studio

A ♥ button in the gallery viewer. Visitors can give each drawing one heart (per browser); the tiles show the count.
There are **no comments and nothing personal is stored**: the database has one table with two columns, the drawing
id and a number.

| Piece | Where |
|---|---|
| The counter (Cloudflare Worker) | `src/worker.js`, served at `https://hearts.bhanuni.in` |
| The database (Cloudflare D1) | `bhanuni-hearts`, table from `schema.sql` |
| The button and counts on the page | `layouts/_default/bhanuni.html` (search for "Hearts") |
| Switch it on or off | `heartsApi` in `content/bhanuni/index.md` (remove the line to hide the hearts) |

How it keeps out junk:

- A heart is accepted only for a drawing id that is on the live gallery page.
- Only the gallery (`https://samarthya.me`, and `http://localhost:1313` for previews) may send hearts.
- One heart per drawing per browser is remembered in that browser. Someone determined could still add more
  hearts; for a heart counter that's an acceptable risk. If it ever happens, add Cloudflare's free rate-limiting
  rule for `hearts.bhanuni.in/hearts/*`, or reset a count (below).

## Set up (once)

From this folder, `tools/bhanuni/hearts`:

```bash
mise exec -- npx wrangler login                                   # opens the browser; sign in to Cloudflare
mise exec -- npx wrangler d1 create bhanuni-hearts                # prints a database_id: paste it into wrangler.toml
mise exec -- npx wrangler d1 execute bhanuni-hearts --remote --file schema.sql
mise exec -- npx wrangler deploy                                  # also creates the hearts.bhanuni.in DNS record
```

Then put `heartsApi: "https://hearts.bhanuni.in"` in `content/bhanuni/index.md` and publish the site.

Check it:

```bash
curl -s https://hearts.bhanuni.in/hearts                 # {} at first
```

## Look at or change the counts

```bash
mise exec -- npx wrangler d1 execute bhanuni-hearts --remote --command "SELECT * FROM hearts ORDER BY n DESC"
mise exec -- npx wrangler d1 execute bhanuni-hearts --remote --command "UPDATE hearts SET n = 3 WHERE id = 'c93dhk'"
mise exec -- npx wrangler d1 execute bhanuni-hearts --remote --command "DELETE FROM hearts"     # start again from zero
```

Free plan limits (Workers: 100,000 requests a day; D1: 100,000 writes a day) are far above what a family gallery
needs.

## Reactions on blog posts

The same Worker counts 👍 / 👎 / ❤️ under every post, instead of comments. It uses a second table, `reactions`
(post slug, kind, count), and accepts a reaction only for a post that is in the live `sitemap.xml`. A browser can
pick one reaction per post.

| Piece | Where |
|---|---|
| The buttons | `layouts/partials/comments.html` (Blowfish shows it because `showComments = true` in `config/_default/params.toml`) |
| Switch it on or off | `reactionsApi` in `config/_default/params.toml` |

```bash
mise exec -- npx wrangler d1 execute bhanuni-hearts --remote --command "SELECT * FROM reactions ORDER BY n DESC"
mise exec -- npx wrangler d1 execute bhanuni-hearts --remote --command "DELETE FROM reactions WHERE slug = 'my-post'"
```
