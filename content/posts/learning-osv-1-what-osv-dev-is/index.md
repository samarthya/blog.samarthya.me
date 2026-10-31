---
title: "Learning OSV, part 1: what osv.dev is and how to read a record"
date: 2026-10-31T07:00:00-04:00
description: "A proof-of-concept series on OSV, Google's open vulnerability database and scanner. Part 1: the problem OSV solves, how to navigate osv.dev, how to read a vulnerability record, and the one API call worth knowing."
categories: ["technical"]
tags: ["security", "learning", "ssdlc"]
series: ["Learning OSV"]
series_order: 1
featureimage: "feature.png"
draft: false
---

{{< lead >}}
A CVE tells you *that* something is broken. It rarely tells you, in a way a machine can use, *which package*
and *which versions*. OSV exists to answer exactly that.
{{< /lead >}}

![Diagram: advisories from GitHub, PyPA, Go, RustSec and malware reports flow into OSV.dev, which publishes a record for GHSA-xvch-5gv4-984h showing npm/minimist affected from 1.0.0 (introduced) to 1.2.6 (fixed), with version 1.2.5 inside the vulnerable range](overview.svg "One record, read as data: the affected range runs from introduced 1.0.0 to fixed 1.2.6, so 1.2.5 is vulnerable and the upgrade target is 1.2.6.")

I am learning which free tools can carry real weight in a secure development life cycle. This short series is my
proof of concept with **OSV**: the database, the scanner and its fix command. I run everything for real and keep
the output. This part is about the concept and the website.

## The problem OSV solves

Say your project uses `minimist 1.2.5`. Is it vulnerable? With a CVE record alone you have to map a product name
to your package and read the affected versions from prose. OSV's own FAQ says the older way of doing this (CPEs)
makes it "difficult to do in an automated way" ([OSV FAQ](https://google.github.io/osv.dev/faq)).

OSV fixes this with three pieces:

| Piece | What it is |
|---|---|
| **OSV schema** | A JSON format where affected versions are written in the package ecosystem's own terms |
| **OSV.dev** | A database and API that "aggregates, enriches and indexes" advisories from sources such as GitHub Security Advisories, PyPA and RustSec |
| **OSV-Scanner** | The official command-line front end: reads your lockfiles and asks OSV.dev what is affected |

The key idea is **precision**. A record does not say "lodash before 4.17.21 is bad" in a sentence; it says it in
data that a scanner can compare with your lockfile.

## Navigating osv.dev

**The list** ([osv.dev/list](https://osv.dev/list)) has a search box and an ecosystem filter. The ecosystems go
well beyond language packages: npm, PyPI, Maven, Go, crates.io and NuGet, but also Debian, Ubuntu, Alpine, Red Hat,
GitHub Actions and even VS Code extensions. Each row shows the ID, the packages, a summary, when it was published,
and whether a fix exists.

**The ID prefix tells you where a record came from.** A few you will meet often:

| Prefix | Source |
|---|---|
| `GHSA-` | GitHub Security Advisories |
| `PYSEC-` | Python Packaging Authority |
| `GO-` | Go vulnerability database |
| `RUSTSEC-` | Rust advisory database |
| `MAL-` | **Malicious packages**, not bugs: code published to steal or attack |

That last one surprised me. Scrolling the list on a normal morning shows `MAL-` records published hours earlier:
packages that are malware by design. A scanner that knows about them catches something no CVE ever will.

## Reading a record

Open a record, for example
[GHSA-xvch-5gv4-984h](https://osv.dev/vulnerability/GHSA-xvch-5gv4-984h), prototype pollution in `minimist`. The page
reads top to bottom:

1. **Aliases**: the same issue elsewhere. Here, `CVE-2021-44906`. This is how you join OSV with CVE-based tools.
2. **Published / Modified**: published March 2022, modified as recently as March 2026. Records keep improving.
3. **Severity**: `9.8 (Critical)` with the CVSS vector.
4. **Details** and **Database specific**: the description, the CWE (`CWE-1321`), and whether GitHub reviewed it.
5. **References**: advisory, fix commits, issues.
6. **Affected packages**: the part that matters. For `npm / minimist` it lists **ranges**: introduced `1.0.0`,
   fixed `1.2.6`; and separately introduced `0`, fixed `0.2.4`.

So `1.2.5` is affected, `1.2.6` is not, and the upgrade path is one patch version. No reading between the lines.

The **JSON Data** link shows the raw record. Its fields follow the
[OSV schema](https://ossf.github.io/osv-schema/): `id`, `aliases`, `severity`, `affected[].ranges[].events`
(`introduced`, `fixed`, `last_affected`) and `references`.

## The one API call worth knowing

Ask OSV.dev directly whether one package version is affected:

```bash
curl -s -X POST https://api.osv.dev/v1/query \
  -d '{"package":{"name":"minimist","ecosystem":"npm"},"version":"1.2.5"}'
```

The answer (trimmed) names the record and its CVE alias:

```text
GHSA-xvch-5gv4-984h  aliases: CVE-2021-44906  Prototype Pollution in minimist
```

`GET https://api.osv.dev/v1/vulns/<ID>` returns one full record. That is enough to script small checks, but for a
whole project the scanner in [part 2]({{< relref "/posts/learning-osv-2-scanning-with-osv-scanner" >}}) does the
work.

## What I took from this part

- OSV answers *which package, which versions*, in data, which is what automation needs.
- The ID prefix tells you the source; **`MAL-` means malware**, a class of risk CVEs do not cover.
- On a record, go straight to **Affected packages** and the **fixed** event: that is your upgrade target.
- **Aliases** connect OSV to the CVE world.

## References

- [OSV FAQ](https://google.github.io/osv.dev/faq): OSV.dev, the three parts of OSV, aggregation and enrichment, the CPE matching problem
- [OSV schema](https://ossf.github.io/osv-schema/): OpenSSF repository, record fields and range events
- [OSV.dev vulnerability list](https://osv.dev/list): ecosystems, search, list columns, `MAL-` records
- [GHSA-xvch-5gv4-984h](https://osv.dev/vulnerability/GHSA-xvch-5gv4-984h): OSV.dev, the example record and its page layout
- [OSV API: query](https://google.github.io/osv.dev/post-v1-query/): OSV.dev, request format used above

Next: [part 2, scanning a project]({{< relref "/posts/learning-osv-2-scanning-with-osv-scanner" >}}).
