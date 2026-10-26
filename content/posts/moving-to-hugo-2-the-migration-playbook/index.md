---
title: "Moving to Hugo, part 2: The migration playbook"
date: 2026-10-26T07:10:00-04:00
description: "A step-by-step guide to moving a WordPress blog to Hugo: back up, inventory, convert with a script, rescue images, keep every link, then go live."
categories: ["technical"]
tags: ["hugo", "wordpress", "migration", "python", "github"]
series: ["Moving to Hugo"]
series_order: 2
draft: false
---

{{< lead >}}
Ten phases, in the order that kept my risk low. Each one ends with something you can check, so you always
know whether it's safe to move on.
{{< /lead >}}

The numbers come from my own move: **137 WordPress posts** from six years, a few hundred images, and a domain
that also carried email. Your numbers will differ; the order shouldn't.

{{< alert "circle-info" >}}
**The golden rule:** the old site stays untouched until the new one is live and checked. Every phase below
works on copies, so you can stop at any point and lose nothing.
{{< /alert >}}

## Phase 0: Back up everything, and keep it out of the repo

Collect three things from WordPress:

1. **The export** (*Tools → Export → All content*): one XML file with every post, page, date and tag.
2. **The uploads folder** (`wp-content/uploads`): your images.
3. **A database dump**, if you can get one. It holds details the export leaves out.

Put them in a dated folder **outside** your new repository, on a disk you control. Raw exports contain things you'll never want public: draft posts,
email addresses, sometimes passwords in old posts.

If the site was compromised, treat these files as hostile. My uploads folder held two PHP backdoors. I never
extracted that archive; the converter read it as a zip and only took files that proved to be images.

**Check:** you can open the XML and count the `<item>` entries of type `post`.

## Phase 1: Take inventory

Before writing any code, list what you're dealing with:

| Question | Mine |
|---|---|
| How many published posts? | 139, minus 2 planted by the attacker = **137** |
| Which editor? | Both classic and block (Gutenberg) posts |
| Special blocks or plugins in posts? | Tabs, accordions, step lists, galleries, alerts |
| URL pattern? | `/wps/YYYY/MM/DD/slug/` |
| Images referenced by posts? | A few hundred, many only as resized copies |
| Anything else on the domain? | **Email.** That changed the whole cut-over plan ([see here](../rebuilding-4-moving-the-domain/)) |

This table turns into your to-do list. Every "special block" needs a Hugo equivalent; every URL pattern needs
a redirect plan.

**Check:** you can name every kind of thing your converter will meet.

## Phase 2: A skeleton site that builds

```bash
hugo new site myblog && cd myblog
git init
git submodule add -b main https://github.com/nunocoracao/blowfish.git themes/blowfish
```

Then three decisions that are painful to change later:

**Pin the Hugo version.** I use [mise](https://mise.jdx.dev/) with a one-line `mise.toml`:

```toml
[tools]
hugo-extended = "0.167.0"
```

**Choose your URLs now.** New posts live at `/posts/<slug>/`:

```toml
# config/_default/hugo.toml
[permalinks]
  posts = "/posts/:slugorcontentbasename/"
```

**Use page bundles.** Each post is a folder (`content/posts/<slug>/index.md`) with its images beside it.

Don't edit the theme. If a template needs to change, copy that one file from `themes/blowfish/layouts/` to
your own `layouts/` and change it there. Hugo uses yours first.

**Check:** `hugo server` shows an empty site with your theme, and `git status` shows no changes under
`themes/`.

## Phase 3: Convert with a script, not a plugin

Export plugins work for simple blogs. Mine had a mix of editors and block plugins, so I wrote a converter in
Python (about 600 lines, using BeautifulSoup and markdownify). Whatever you use, insist on these properties:

- **Re-runnable.** You will run it dozens of times. It must produce the same output every time, from the
  original export, so fixes accumulate instead of being overwritten.
- **One post per folder**, with front matter Hugo understands:

```yaml
---
title: "Kafka: Deploy & Test"
date: "2022-02-11T08:17:19Z"
slug: "kafka-deploy-test"
categories: ["kubernetes", "technical"]
tags: ["deploy", "helm", "kafka"]
aliases: ["/wps/2022/02/11/kafka-deploy-test/"]
---
```

- **Map every special block** to a shortcode: WordPress tabs to `{{</* tabs */>}}`, accordions to
  `{{</* accordion */>}}`, and so on.
- **A report**, not silence. For every post: images copied, images missing, notes. You read the report, not
  137 posts.
- **Privacy built in.** My converter replaces my real name with my screen name, redacts tokens and private
  keys it recognises, and **refuses to run** if the name rules are missing. A careless run then can't publish
  what you meant to hide.

Watch out for **dates**. 36 of my posts showed the date of an earlier re-publish, not when they were written.
WordPress keeps the original in a hidden field (`_wp_old_date`); the converter restores it.

**Check:** convert ten posts of different kinds, then compare each one side by side with the old page.

## Phase 4: Rescue the images

Images are where migrations quietly lose things. My recovery came from several sources, tried in order:

1. **The uploads folder.** WordPress keeps resized copies (`photo-1024x768.png`); match on the name without
   the size suffix and take the largest.
2. **Older backups.** An old copy I'd forgotten about supplied most of the originals.
3. **The Internet Archive**, for a few.

Two rules kept this safe:

- **Check the first bytes.** Only accept a file if it really starts like a PNG, JPEG, GIF or WebP. A
  renamed PHP file never gets through.
- **Never drop silently.** A missing image becomes a visible marker, `*[image unavailable: name]*`, and a line
  in a tracking list. I kept that list outside the repo and ticked items off as files turned up.

**Check:** every marker on your missing list is either found or consciously given up.

## Phase 5: Keep every old link

Every URL a post ever had goes into its `aliases:`. Hugo writes a small redirect page for each. I ended up
with 335 of them.

Then test a sample: open twenty old URLs from search results or your analytics and confirm each lands on the
right post.

**Check:** no old URL you know of returns a 404.

## Phase 6: Fixes that survive a re-import

Once the bulk conversion works, you'll want to fix individual posts: alt text for images, a better summary,
a broken figure. If you edit the generated Markdown by hand, the next converter run overwrites it.

My answer was an **overrides file** that the converter applies on every run:

```yaml
# tools/wp2hugo/overrides.yaml
a-different-take-siem:
  alt:
    logs-data.png: "Typical log sources for a SIEM: identity and access management, firewall, endpoints and a VPN gateway"
map-and-flatmap:
  description: "Java 8 streams: what map and flatMap do, with small examples of each."
adding-node-to-a-cluster:
  replace:
  - from: "*[image unavailable: claps-1.gif — Finally!]*"
    to: "> 🎉 Finally!"
```

Edited images (screenshots with personal details blanked out, photos rotated upright) live in a
`media/<slug>/` folder that the converter uses in place of the originals. If an override stops matching
anything, the converter stops and says which one.

This is where I wrote alt text for all 103 images that had none, after looking at each one.

**Check:** run the converter into a temporary folder and diff it against `content/`. The only differences
should be the ones you meant.

## Phase 7: Make it yours

Only now does styling pay off: the content is final, so you're designing for real posts. Two habits:

- **Measure.** Contrast ratios, image counts, line lengths. My link colour "looked fine" and measured 3.56:1,
  below the 4.5:1 minimum.
- **Small reviewable steps.** Change one thing, build, look at it in light and dark mode, commit.

## Phase 8: Automate the publish, with a safety gate

A GitHub Actions workflow builds and deploys on every push to `main`. The step I'd add for anyone: **a
privacy check before the build**, so a mistake fails the deploy instead of going live.

```yaml
- name: Privacy check (secrets, local paths, image metadata)
  run: python3 tools/privacy/check.py

- name: Build
  run: hugo --gc --minify
```

Mine is about 200 lines of standard-library Python. It looks for credential-shaped text, local file paths,
leftover migration files, and personal metadata inside images (GPS, owner names, serial numbers).

**Check:** commit a fake token on a branch and watch the check fail.

## Phase 9: Go live

Test the new site at its temporary address (`username.github.io/repo/`) first. Then move the domain. If your
domain also carries email, read
[part 4 of the other series](../rebuilding-4-moving-the-domain/) first. The short version: move DNS
without changing anything, confirm mail still works, and only then point the website at the new host.

**Check:** the site loads on your domain over HTTPS, old links redirect, and you can send and receive mail.

## Phase 10: Retire the old site

Only after the new site has run for a while:

- Delete the old WordPress files and its database from the host.
- Remove anything else on that server you no longer use.
- Keep the backup folder from Phase 0, encrypted, somewhere that isn't the cloud.

## Lessons for me

- **The re-runnable converter was the best decision.** Every fix went into the script or the overrides file,
  so nothing I fixed ever came back.
- **Privacy has to be a gate, not a habit.** I found my real name in screenshots weeks after I thought the
  content was clean. Automated checks catch text; images still need a human look.
- **The order matters more than the tools.** Content first, then images, then links, then design, then the
  domain. Every time I jumped ahead, I redid work.

## Tips for you

1. **Back up first, outside the repo**, and never run anything from a compromised backup.
2. **Inventory before code.** A one-page table of what you have saves days.
3. **Make conversion repeatable**, and put every manual fix in a file the converter applies.
4. **Add redirects for every old URL**, then test a sample.
5. **Put a privacy check in front of the deploy**, and look at your screenshots with fresh eyes.
6. **Leave the old site running until the new one is proven.**

Next: [part 3](../moving-to-hugo-3-living-with-hugo/), what day-to-day life with Hugo looks like.
