---
title: "Moving to Hugo, part 3: Living with Hugo"
date: 2026-10-26T07:20:00-04:00
description: "Day-to-day life after the move: writing and publishing a post, updating the theme and Hugo safely, extending the site, and the gotchas that cost me an evening each."
categories: ["technical"]
tags: ["hugo", "github", "workflow", "static-site"]
series: ["Moving to Hugo"]
series_order: 3
draft: false
---

{{< lead >}}
Migrating is a project. Living with the result is a habit. Here's what a normal week with a Hugo site looks
like, and what to do when something needs updating.
{{< /lead >}}

## Writing a post

Every post is a folder. The theme's archetype fills in the front matter for me:

```bash
hugo new content posts/my-new-post/index.md
```

```yaml
---
title: "My New Post"
date: 2026-10-26T09:00:00-04:00
description: ""     # one line; shown on cards and in search results
categories: ["technical"]
tags: []            # reuse existing tags so the right cover and related posts show up
draft: true
---
```

Then:

1. **Write in Markdown** in any editor. Images go in the same folder: `![What the image shows](diagram.png)`.
   The alt text in the square brackets is for people using screen readers, so describe what's in the picture.
2. **Preview live** with `hugo server -D` (`-D` includes drafts). The page reloads every time you save.
3. **Pick a card image** by naming one `feature.jpg`. Without one, my site generates a cover in the colours of
   the post's topic.
4. **Write the description.** It's what appears on cards and in search results. A post that starts with a
   code block makes a terrible automatic summary.
5. **Set `draft: false`** when it's ready.

Short notes go to a separate **Daily** section with a lighter layout. A three-line note shouldn't look like a
tutorial.

## Publishing

```bash
python tools/privacy/check.py      # the same check CI runs
hugo --gc --minify                 # a full production build, to catch errors early
git add content/posts/my-new-post
git commit -m "New post: My New Post"
git push
```

On GitHub, the push starts a workflow: privacy check, then the build, then the deploy to GitHub Pages. About
a minute later it's live. If the privacy check fails, nothing is published, and the log says which file and
line to look at.

That's the whole publishing process. There's no admin panel, no plugin updates, and no database backup to
remember: git *is* the backup.

## Updating the theme

The theme is a git submodule, so updates happen only when I choose:

```bash
git submodule update --remote --merge themes/blowfish
hugo server       # click through: homepage, a long post, a gallery, dark mode, search
```

Before updating, check the theme's supported Hugo range (Blowfish lists it in its `config.toml`). If the build
and the click-through look right, commit the new submodule pointer. If not, `git checkout themes/blowfish`
puts it back.

Because I never edit files inside `themes/`, an update can't overwrite my changes. My overrides in
`layouts/` and `assets/css/custom.css` always win.

## Updating Hugo

The version is pinned in two places, and they must move together:

- `mise.toml` for my laptop: `hugo-extended = "0.167.0"`
- `.github/workflows/hugo.yml` for the build server: `HUGO_VERSION: 0.167.0`

Read the release notes for anything marked deprecated, bump both, build, look, commit. A version mismatch
between laptop and CI is the most common source of "it works on my machine".

## Growing the site

Hugo had room for everything I wanted to add, without plugins:

**A JSON feed for my portfolio.** A custom output format writes `/latest.json` with my newest posts, and my
portfolio site reads it:

```toml
# config/_default/hugo.toml
[outputFormats.Latest]
  mediaType = "application/json"
  baseName = "latest"
  isPlainText = true

[outputs]
  home = ["HTML", "RSS", "JSON", "Latest"]
```

A small template, `layouts/index.latest.json`, decides what goes in it.

**Topic pages from one data file.** A *content adapter* (`content/topics/_content.gotmpl`) reads
`data/covers.yaml` and creates a page for each topic at build time. A new post lands in the right topic based
on its tags, with no extra step.

**A contact page that hides the address from bots.** The link stores the address base64-encoded in a
`data-email` attribute, and a small script from the theme turns it into a `mailto:` link in the browser. The
address never appears in the page source.

## Gotchas that cost me an evening each

| Symptom | Cause | Fix |
|---|---|---|
| A new layout file has no effect | `hugo server` doesn't always notice brand-new template files | Stop and restart the server |
| `showAuthor: false` on a page is ignored | `.Params.x \| default site.x` treats `false` as "not set" | Override the template, or use a small section-specific layout |
| Generated topic pages build but don't render | Content-adapter pages need explicit build options | Give them `render: always` and `publishResources: true` in their build options |
| An email address hidden with HTML entities shows in plain text | The minifier decodes entities | Encode it in a `data-email` attribute and decode it in the browser |
| Old WordPress links 404 | A post's earlier URL wasn't in its `aliases:` | Add it; Hugo writes the redirect page |

## The maintenance calendar

| How often | What |
|---|---|
| Every post | Privacy check and a full build before pushing |
| Every few months | Update the theme; skim Hugo's release notes |
| Twice a year | Open a sample of old posts: broken outside links, images, code that no longer works |
| Once a year | Renew the domain; review who has access to the repository and DNS |

Compare that with the WordPress years: core updates, plugin updates, PHP versions, database backups, and the
login page that eventually let someone in.

## What it costs

GitHub Pages hosting is free for a public repository, and so is the Cloudflare DNS plan I use. The only bill
is the domain name. The real cost is time, and after the migration that's mostly time spent writing.

## Lessons for me

- **A fast feedback loop changes behaviour.** With builds that take about a second, I preview every change instead of
  guessing.
- **Pin, then update deliberately.** Nothing changes under me; when I update, I know exactly what changed.
- **The site is a repository.** History, backups, review and rollback all come from git for free.

## Tips for you

1. **Run the same checks locally that CI runs**, so a failed deploy is never a surprise.
2. **Keep theme changes in your own folders**, never inside `themes/`.
3. **Bump tool versions in one commit**, everywhere they're pinned.
4. **Write the description and the alt text when you write the post.** It's a minute now, and an afternoon
   later for a hundred posts.
5. **Keep a maintenance calendar.** A static site needs very little care, but not none.

That's the series. If you're planning your own move and get stuck, the [contact page](/contact/) has my
details.
