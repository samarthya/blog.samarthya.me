---
title: "Rebuilding samarthya.me, part 1: The day the blog fell"
date: 2026-10-25T12:00:00-04:00
description: "A six-year-old WordPress blog was compromised. What the attack looked like, and the first hours of triage."
categories: ["technical"]
tags: ["security", "wordpress", "incident"]
series: ["Rebuilding samarthya.me"]
series_order: 1
draft: false
---

{{< lead >}}
On 10 October 2026 my blog stopped being mine. This series is the diary of getting it back, and of moving
to something simpler: from shared hosting and WordPress to a static site on GitHub Pages behind Cloudflare.
{{< /lead >}}

## What I found

The site had been running WordPress on shared hosting since 2019. When things started to look wrong, a closer
look turned up the classic signs of a compromise:

- **Backdoor files in the uploads folder.** Two small PHP files, each a few lines that `eval()` whatever
  arrives in a request. Uploads is a favourite hiding place: it's writable, and nobody looks there.
- **A rogue administrator account** with a registration date in 1970. A date that's obviously wrong is the
  giveaway that it was inserted straight into the database, not created through WordPress.
- **Plugins I didn't install**, including a file manager and a "code snippets" plugin. Both are perfectly
  legitimate tools, and perfect for an attacker who wants to keep coming back.
- **Posts I never wrote**, published under *my* account. That was the most sobering find: it meant my
  credentials had been used, not just a vulnerable plugin.
- **Four copies of a "Protect Uploads" plugin** in folders with random names (`zqwaarh`, `ivalpno`, …), all at an
  ancient version. A familiar disguise: a harmless-sounding plugin name as cover for a loader.

## The timeline

The database dump turned out to be a better witness than any log file. WordPress quietly records when plugins
are switched off and when snippets are created, and the login-protection plugin kept its own record:

| When (UTC) | What the evidence shows |
|---|---|
| **8 Oct, 10:16** | 15 failed logins for my username through `xmlrpc.php`, 5 lockouts. Someone was guessing passwords |
| **9 Oct, 00:59:41** | **20 plugins deactivated in the same second**, including the brute-force protection and the cache. Only an administrator can do that |
| **9 Oct, 18:44** | A code-snippets plugin installed; three seconds later a snippet called `content-cache-support` |
| **10 Oct, 08:29** | A second `content-cache-support` snippet |
| **10–11 Oct** | Backdoors in uploads, the 1970 administrator, posts under my name, a throwaway `site-tools-…` plugin |

Read top to bottom, it's a textbook takeover: **get in, switch off the defences, install tools, dig in.**

## Was it a known vulnerability?

My first instinct was to blame an outdated plugin, so I checked. WordPress itself was the latest release.
Ten of 27 plugins had updates waiting, so I looked up every installed version in the public vulnerability
databases (checked 25 Oct 2026):

| Plugin, installed version | Known issues | Published | Explains this break-in? |
|---|---|---|---|
| LiteSpeed Cache 7.9.1 | [CVE-2026-113499](https://nvd.nist.gov/vuln/detail/CVE-2026-113499), [-113500](https://nvd.nist.gov/vuln/detail/CVE-2026-113500) (XSS, 7.5), [-113501](https://nvd.nist.gov/vuln/detail/CVE-2026-113501) (3.1) | 23 Oct 2026 | No: published **two weeks after**, and they need a victim to click a link |
| LiteSpeed Cache 7.9.1 | [CVE-2026-84761](https://nvd.nist.gov/vuln/detail/CVE-2026-84761) (SSRF), [CVE-2026-76579](https://nvd.nist.gov/vuln/detail/CVE-2026-76579) (XSS) | 3 and 19 Sep 2026 | No: both already **fixed in 7.9.1** |
| Elementor 4.2.4 | A CSRF in 4.3.0–4.3.1 only; two XSS fixed in 4.3.5 | Sep–Oct 2026 | No: the XSS needs a logged-in contributor, and there were no other users |
| Contact Form 7, the login-protection plugin, the file manager I'd used | None for the installed versions | | No |

**No published vulnerability fits the window.** What fits is the login record: a week of failed attempts from
30 September, then the first successful logins on 7 October, then more in one day than in the previous eleven
months. The most likely explanation is **credential stuffing**. My admin password had also been used on a few
unrelated sites. If any one of them leaked it, the pair "email + password" was all an attacker needed. Add an old
remote-publishing endpoint (`xmlrpc.php`) the site didn't need, and an account without two-factor authentication.

Not an exotic exploit. That's almost more uncomfortable, because no plugin update would have prevented it.

## The first hours

{{< alert "circle-info" >}}
If this ever happens to you: contain first, investigate second, rebuild third. Don't try to "clean" a
compromised WordPress in place and keep running it.
{{< /alert >}}

1. **Take it offline.** Not pretty, but it stops the site from being used against visitors.
2. **Change every password that touched it:** hosting panel, database, mail accounts, and the registrar. Turn on
   two-factor authentication wherever it exists.
3. **Keep evidence before deleting anything:** a content export, a database dump and a copy of the uploads
   folder. You'll need them to recover, and to understand what happened.
4. **Scan, then remove** the planted files and the extra accounts. Then assume you missed something.

But one thing decided the rest of this story: after a takeover like this, I could never be sure I'd found every
backdoor. I could spend weeks hardening a PHP application on a host I no longer trusted. Or I could move the writing somewhere with **nothing to break into**.

## The decision

A personal blog doesn't need a database, a login page or plugins. It needs pages. A static site generator
turns Markdown into plain HTML files, and a static host serves them. There's no server-side code left to exploit.

So the plan became:

| Before | After |
|---|---|
| WordPress + PHP + MySQL on shared hosting | [Hugo](https://gohugo.io/) building plain HTML |
| Plugins for everything | A theme ([Blowfish](https://blowfish.page/)) and a few small templates |
| Edit in a browser | Write Markdown, commit to git |
| Host serves PHP | GitHub Pages serves files |
| DNS at the host | Cloudflare |

## Lessons for me

- **My password was the weakest plugin.** I'd reused it on a few unrelated sites. I never thought of that as
  connected to a blog until one of them, somewhere, leaked.
- **I wasn't watching the signs.** A burst of 141 failed logins in one hour, a week before the break-in, sat in a
  dashboard I never opened. The protection worked; I just never looked.
- **27 plugins was 26 too many.** Every one was code I didn't read, running with full access. Half of them I
  couldn't have named.
- **Backups saved me, by accident.** The copy that rescued most of my images was one I'd forgotten I had.

## Tips for you

{{< alert "circle-info" >}}
Five minutes today beats five weekends later.
{{< /alert >}}

1. **Turn on two-factor authentication** for your email, your bank, and any site with an admin login. With 2FA,
   a leaked password alone isn't enough.
2. **Use a password manager and a unique password per site.** Reuse is how one company's breach becomes yours.
   If a password ever leaks, **change it everywhere it was used, email and finance first.**
3. **Check [haveibeenpwned.com](https://haveibeenpwned.com/)** for your email addresses. It's free and takes a
   minute.
4. **Running WordPress?** No user called `admin`; disable `xmlrpc.php` if you don't post from apps; keep only
   the plugins you actually use; and *look* at your security plugin's dashboard once a month.
5. **If you're hit: contain, preserve, then rebuild.** Take the site offline, keep a copy of everything, change
   passwords, and rebuild somewhere clean rather than "cleaning" in place.

The hardest part wouldn't be the new site. It would be getting six years of posts out of the old one intact.
That's [part 2](../rebuilding-2-salvaging-the-content/).
