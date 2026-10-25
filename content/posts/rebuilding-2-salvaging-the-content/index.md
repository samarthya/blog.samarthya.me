---
title: "Rebuilding samarthya.me, part 2: Salvaging the content"
date: 2026-10-25T12:10:00-04:00
description: "Converting 137 WordPress posts to Markdown, recovering lost images from backups, and keeping every old link alive."
categories: ["technical"]
tags: ["wordpress", "hugo", "migration", "python"]
series: ["Rebuilding samarthya.me"]
series_order: 2
heroStyle: "big"  # full-width feature.jpg above the title (series artwork)
draft: false
---

{{< lead >}}
Text is easy to save. Dates, images, code blocks and six years of links are where a migration quietly loses
things. Here's what it took to bring them across.
{{< /lead >}}

## The raw material

WordPress can export everything as one XML file (WXR). Together with a database dump and a copy of the
uploads folder, that's the whole site. The export held **139 published posts**. Two were the attacker's, so
they were excluded permanently: **137 posts** to convert.

## A converter instead of a plugin

Off-the-shelf exporters exist, but these posts used a mix of the classic editor and Gutenberg blocks, including
tabs, accordions and step-by-step blocks from a block plugin. So I wrote a small Python converter
(BeautifulSoup + markdownify) that:

- turns block markup into the theme's equivalents (`tabs`, `accordion`, `steps`, `gallery`, `alert`)
- rebuilds paragraphs for classic-editor posts, which store text without `<p>` tags
- rewrites links between posts so they keep working on the new site
- marks every image that couldn't be found, instead of silently dropping it
- **redacts secrets**: one old post had a Kubernetes service-account token pasted into a code block

{{< alert >}}
Old posts are full of things you'd never publish today: tokens in code samples, internal hostnames, real
names in example data. A migration is the moment to scrub them, and a converter does it consistently.
{{< /alert >}}

## Dates that lied

36 posts claimed to be written on the same day: the day they'd been re-published during an earlier recovery.
WordPress keeps the original date in a hidden field (`_wp_old_date`), so the converter restores it. The
"Writing over the years" chart on the homepage is only honest because of that one detail.

## Every old link still works

Old addresses looked like `/wps/2022/02/11/kafka-deploy-test/`. New ones are `/posts/kafka-deploy-test/`.
Hugo can generate a redirect page for any old path listed in a post's `aliases:`, so the converter writes one
for every URL a post ever had: **335 redirects** in total. Bookmarks, search results and links from other
sites all still land on the right page.

## The images

This was the painful part. The server had been serving error pages where images used to be, and the uploads
copy turned out to be mostly retina (`@2x`) duplicates. Recovery came in layers:

| Source | What it gave |
|---|---|
| The uploads copy | Resized variants: matched by file name, ignoring size suffixes |
| The Internet Archive | A few originals |
| **An old backup I'd forgotten about** | Almost everything else |
| | **126 images recovered, 15 still missing** |

The converter only accepts files whose first bytes prove they're really images. The uploads folder was where
the backdoors had lived, and nothing executable gets carried over by accident.

The missing 15 are on a list. Some are screenshots that may still be on an old laptop. Some were hotlinked
from other websites that have since moved them. That's the price of linking instead of hosting.

## Lessons for me

- **The content is the asset; the platform is replaceable.** I spent years thinking of "my WordPress site".
  What mattered was 137 posts and their links.
- **My images lived in only one place.** The posts survived in the export; the pictures needed three sources and
  luck. Losing them was the real cost of the attack.
- **Old posts held secrets I'd forgotten.** A service-account token sat in a code block for years. Writing a
  converter forced me to read everything again.

## Tips for you

1. **Export your blog now, while it works.** In WordPress: *Tools → Export → All content*. Keep it next to a
   copy of `wp-content/uploads`. Repeat every few months.
2. **Follow 3-2-1 for anything you'd hate to lose:** three copies, on two kinds of storage, one off-site.
3. **Keep your own copy of every image you publish.** Hotlinking from other sites means borrowing something
   that can disappear.
4. **Never paste real tokens, passwords or internal hostnames into a post**, even "temporarily". Use
   placeholders like `<TOKEN>`.
5. **When you move a site, redirect every old URL.** Links are years of earned trust; a 404 throws them away.

Next: [part 3](../rebuilding-3-a-new-home-on-hugo/), building the new site itself.
