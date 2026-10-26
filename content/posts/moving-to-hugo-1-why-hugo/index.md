---
title: "Moving to Hugo, part 1: Why Hugo"
date: 2026-10-26T07:00:00-04:00
description: "How I chose a new home for a personal blog after a break-in: the requirements, the candidates, and why a static site generator won."
categories: ["technical"]
tags: ["hugo", "wordpress", "migration", "static-site"]
series: ["Moving to Hugo"]
series_order: 1
draft: false
---

{{< lead >}}
After the blog was broken into, I had to decide where it would live next. This is how I made that choice,
written so you can reuse the reasoning even if you end up somewhere else.
{{< /lead >}}

The story of the break-in is in [Rebuilding samarthya.me](../rebuilding-1-the-day-the-blog-fell/). This
series is the practical companion: **why Hugo**, **how to migrate step by step**, and **what living with it
is like**. My own site is the worked example throughout.

## Start from requirements, not tools

It's tempting to start with "which framework is popular". I started with what had gone wrong and what I
actually needed. The list fit on an index card:

| # | Requirement | Why |
|---|---|---|
| 1 | **Nothing to patch on the server** | The old site was a PHP application with plugins, a database and a login page. Every one of those was attack surface I had to maintain. |
| 2 | **Content in plain files I own** | Posts should be readable in ten years without the software that wrote them. |
| 3 | **Version history for everything** | I wanted to see what changed, when, and roll it back. |
| 4 | **Free or nearly free hosting** | It's a personal blog, not a business. |
| 5 | **Old links keep working** | Six years of links from other sites, search results and bookmarks. |
| 6 | **Low maintenance** | I want to write, not babysit a stack. If I don't touch it for a year, it should still build. |
| 7 | **Room to grow** | A portfolio-style homepage, topics, a feed my other site can read. |

Requirement 1 rules out most of the field by itself. A **static site** is a folder of HTML, CSS and images
produced ahead of time. There's no database to inject into, no admin page to guess a password for, no plugin
to update on a Sunday night. The server only hands out files.

## The candidates

I looked at the realistic options for one person writing technical posts:

| Option | What it is | For me |
|---|---|---|
| **WordPress, hardened** | Same platform, with 2FA, fewer plugins, managed hosting | Familiar, but keeps a database, logins and plugins: the exact surface that failed |
| **Ghost** | A modern Node.js blogging platform | Lovely editor, but still a server application to run or pay for |
| **Jekyll** | The original static generator; GitHub Pages builds it natively | Mature, but Ruby toolchain, and builds slow down as sites grow |
| **Eleventy / Astro** | JavaScript static generators | Very flexible, but a `node_modules` tree to keep up to date |
| **Hugo** | A static generator shipped as a single Go binary | One file to install, very fast builds, rich built-in features |

All of the static options would have met requirements 1–4. The difference was in 5, 6 and 7.

## Why Hugo won

**One binary, pinned.** Hugo is a single executable with no runtime and no dependency tree. I pin the exact
version in one line (`hugo-extended = "0.167.0"` in `mise.toml`), and CI installs the same version. "It built
last year" stays true, which is requirement 6 in practice.

**Speed you stop thinking about.** The whole site (155 posts, topic pages, feeds and 351 redirect pages,
about 550 pages in all) builds in about a second on a laptop. When a build is that fast, you preview every change
instead of batching them, and that changes how carefully you work.

**Old links, built in.** Any page can list its old addresses under `aliases:`, and Hugo writes a small
redirect page for each one. That covered all 335 WordPress-era URLs without a server or a plugin
(requirement 5).

**Page bundles.** A post is a folder: `index.md` plus its images. Moving, renaming or deleting a post moves
everything that belongs to it. After losing images in the old setup, keeping each picture next to its text
mattered to me.

**Shortcodes for the rich bits.** My old posts used tabs, accordions and step-by-step blocks. Hugo
shortcodes (`{{</* tabs */>}}`, `{{</* steps */>}}` and so on, many provided by the theme) gave each of those
a Markdown equivalent, so the converter had somewhere to put them.

**Room to grow without plugins.** Custom output formats gave me a `latest.json` feed for my portfolio site.
A *content adapter* generates the topic pages from one data file. Image processing resizes and crops covers
at build time. All of it is part of Hugo itself.

**A theme I don't have to edit.** [Blowfish](https://blowfish.page/) covered dark mode, search, series,
galleries and a profile homepage. Hugo looks in the site's own `layouts/` folder before the theme's, so every
customisation lives in my repository and the theme stays untouched.

## What Hugo costs you

No tool is free of trade-offs. Before choosing it, know these:

- **Go templates are an acquired taste.** `{{ with .Params.x }}…{{ end }}` reads oddly at first, and error
  messages can be terse.
- **Some defaults surprise you.** Many themes read settings as `.Params.x | default site.x`, and Hugo's
  `default` treats `false` as "not set". So `showAuthor: false` on one page can be silently ignored. A small
  template override fixes it, but you have to know to look.
- **No web editor.** You write in a text editor and publish with `git push`. For me that's a feature; for a
  non-technical writer it's a real barrier.
- **Dynamic features need outside help.** Comments, forms and server-side search aren't built in. Blowfish's
  search runs in the browser from a JSON index, which is plenty for a blog this size.
- **Themes move.** A big theme like Blowfish is actively developed. Pinning it as a git submodule means
  updates happen when *you* choose, not when they ship.

## Who shouldn't choose Hugo

- If several non-technical people publish, a hosted platform with a web editor will make everyone happier.
- If you need logins, payments or user-generated content, you need a server somewhere anyway.
- If you already live in the JavaScript ecosystem and want interactive components on every page, Astro may
  fit better.

For one person writing technical posts who never wants to patch a CMS again, Hugo is hard to beat.

## Lessons for me

- **The incident wrote my requirements.** "Nothing to patch on the server" came straight from the
  post-mortem. Without it, I'd probably have rebuilt on WordPress out of habit.
- **Boring is a feature.** The winning arguments weren't exciting ones: one binary, pinned version, fast
  builds, files in git.
- **Picking a well-maintained theme saved weeks.** I spent my time on content and the homepage, not on
  reinventing dark mode.

## Tips for you

1. **Write your requirements before you look at tools**, and number them. Then score each option against the
   list instead of against blog posts about frameworks.
2. **Ask "what does this need from me in a year?"** Updates, renewals, plugins, a database: each is a chore
   and a risk.
3. **Prefer tools you can pin to one exact version.** It's the cheapest insurance against "it worked
   yesterday".
4. **Try the build speed on real content.** Convert ten real posts and time the build before committing.
5. **Keep your content in plain Markdown.** Whatever you choose, plain files make the *next* move easy too.

Next: [part 2](../moving-to-hugo-2-the-migration-playbook/), the migration step by step.
