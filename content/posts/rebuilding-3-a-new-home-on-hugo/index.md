---
title: "Rebuilding samarthya.me, part 3: A new home on Hugo"
date: 2026-10-25T12:20:00-04:00
description: "Hugo, Blowfish and GitHub Pages: a portal homepage, topics that sort themselves, and accessibility measured rather than guessed."
categories: ["technical"]
tags: ["hugo", "github", "css", "accessibility"]
series: ["Rebuilding samarthya.me"]
series_order: 3
heroStyle: "big"  # full-width feature.jpg above the title (series artwork)
draft: false
---

{{< lead >}}
The content was safe. Now it needed a home that's easy to keep alive: something I can write in, push, and
forget about.
{{< /lead >}}

## The stack

- **[Hugo](https://gohugo.io/)**, pinned to one exact version with [mise](https://mise.jdx.dev/), so a future
  release can't silently break the build.
- **[Blowfish](https://blowfish.page/)** as the theme, added as a git submodule and **never edited**. Every
  change lives in the site's own `layouts/` and `assets/css/`, so theme updates stay a one-line operation.
- **GitHub Actions → GitHub Pages.** Push to `main`, and about a minute later the site is rebuilt and live.

## A portal, not just a blog

The first version looked like what it was: an unmodified theme with 137 blank tiles. Imported posts have no
"feature image", so every card was empty. Three changes turned it into a place:

1. **Topic covers.** Each post is assigned a topic (Kubernetes, Go, Elastic, Security…) from its tags,
   categories and title words. Posts without a picture get a generated cover in that topic's colours.
2. **Topics that sort themselves.** Topic pages are generated at build time from one data file
   (`data/covers.yaml`). A new post lands in the right topic without any extra step.
3. **A homepage with a story:** what the site is for, the milestones (including the day it fell), a small
   posts-per-year chart, a hand-picked "trophy shelf", and the latest posts.

## Measure, don't guess

Before styling anything, I measured. A few numbers that changed the plan:

| Finding | Number |
|---|---|
| Body link colour contrast | **3.56:1**, below the 4.5:1 WCAG minimum, even though it "looked fine" |
| White text on my own topic chips | as low as **2.15:1** at the light end of the gradient |
| Images without alt text | **102** |
| Posts with code lines over 100 characters | **116 of 137** |

The fixes were small: a darker link shade (5.18:1), gradients that start 30% toward the dark end (now at least
4.95:1 everywhere), wider code blocks on large screens, and a visible keyboard focus ring.

{{< alert "circle-info" >}}
A theme gotcha worth knowing: many Hugo themes read page settings as `.Params.x | default site.x`. Hugo's
`default` treats `false` as "not set", so `showAuthor: false` on a page is silently ignored when the site
default is true. A small template override was the only reliable fix.
{{< /alert >}}

## Two kinds of writing

The site now separates long **Posts** from short **Daily** entries. Daily entries have their own dated list and a
lighter page: no cover, no table of contents, no author box. A three-line note shouldn't be dressed up like a
2,500-word tutorial.

## Lessons for me

- **"Looks fine" isn't a measurement.** My link colour looked perfectly readable to me, and it failed the
  accessibility minimum. So did my own pretty topic chips.
- **Don't edit the theme.** Keeping every change in my own folders meant I could undo anything, and theme
  updates stay painless.
- **Small, reviewable steps.** Each change was built, screenshotted and checked before the next. The two times I
  skipped that, I shipped something broken.

## Tips for you

1. **Pin your tools' versions** (Hugo, Node, Python…). "It built yesterday" should still be true next year.
2. **Check contrast with numbers.** Body text needs **4.5:1** against its background, large text 3:1. Any
   contrast checker will tell you in seconds.
3. **Write alt text for every image**: a short description of what it shows, for people using screen readers.
4. **Prefer overrides to edits** in any theme or framework: copy the one file you need into your project and
   change it there.
5. **A static site is enough for most personal blogs.** No database, no login, no plugins: nothing to patch on a
   Sunday night.

The last step was moving the domain: [part 4](../rebuilding-4-moving-the-domain/).
