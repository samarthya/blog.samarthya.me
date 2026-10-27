# Security policy

This repository builds [samarthya.me](https://samarthya.me), a personal static website. It has no server-side
code, logins, forms or database: GitHub Actions builds the pages with Hugo and GitHub Pages serves them.

## Reporting a problem

If you find a security problem with the site or this repository (for example a secret committed by mistake,
personal data that shouldn't be public, or a way to change what the site serves), please report it privately:

- **Preferred:** GitHub's [private vulnerability reporting](https://github.com/samarthya/blog.samarthya.me/security/advisories/new)
- **Or email:** admin@samarthya.me

Please don't open a public issue or pull request for security reports.

## What to expect

This is a one-person project, so replies are best effort, usually within a few days. There is no bug bounty.
The old WordPress site (blog.samarthya.me before October 2026) is being retired and is not maintained;
its addresses redirect to this site.

## Scope

In scope: this repository, its GitHub Actions workflows, and the published site at samarthya.me.
Out of scope: third-party services the site links to, and the Blowfish theme (report those to
[its maintainers](https://github.com/nunocoracao/blowfish)).
