---
title: "Learning OSV, part 3: guided remediation with osv-scanner fix"
date: 2026-10-31T07:30:00-04:00
description: "Proof of concept: let OSV-Scanner fix the vulnerable Node project. The safe in-place strategy fixed 7 of 50; the relax strategy fixed all 50 by changing three lines, two of them breaking upgrades. What each strategy does, why the numbers differ, and how to use it without getting burned."
categories: ["technical"]
tags: ["security", "learning", "ssdlc"]
series: ["Learning OSV"]
series_order: 3
featureimage: "feature.png"
draft: false
---

{{< lead >}}
Finding 49 vulnerabilities is easy. Deciding which three lines to change so that most of them go away is the hard
part. That is what `osv-scanner fix` tries to do.
{{< /lead >}}

![Diagram comparing two fix strategies. in-place edits only the lockfile, upgrades lodash and axios within range, and fixes 7 of 50. relax edits package.json and relocks, upgrading jsonwebtoken to a new major, axios across 0.x and minimist by a patch, and fixes 50 of 50](overview.svg "in-place is the safe small win; relax fixes everything but chose a major upgrade.")

In [part 2]({{< relref "/posts/learning-osv-2-scanning-with-osv-scanner" >}}) the scanner found 49 known
vulnerabilities in a small Node project. This part tries the **guided remediation** command on it.

## What it is

`osv-scanner fix` proposes "a small set of concrete changes" to your manifest and lockfile, and can apply them
([guided remediation docs](https://google.github.io/osv-scanner/experimental/guided-remediation/)). It is listed
as **experimental**. Today it supports:

| File | Strategy | What it changes |
|---|---|---|
| `package-lock.json` | **in-place** | Only the lockfile: swaps vulnerable versions for safe ones that still satisfy existing ranges |
| `package.json` | **relax** | Raises ranges in `package.json` where needed, then relocks the whole tree |
| `pom.xml` | **override** | Maven: adds versions to `<dependencyManagement>` and bumps direct dependencies |

It prints a warning first, and it is worth repeating: on an **untrusted** project, the package manager may run
scripts or contact registries the project names. Run it only on code you trust.

## Strategy 1: in-place (low risk)

```bash
osv-scanner fix --strategy=in-place -L package-lock.json
```

```text
Found 50 vulnerabilities matching the filter
Can fix 7/50 matching vulnerabilities by changing 2 dependencies
UPGRADED-PACKAGE: lodash,4.17.15,4.18.1
UPGRADED-PACKAGE: axios,0.21.1,0.21.4
REMAINING-VULNS: 43
```

(The fix command counts 50; the scan showed 49 rows because two IDs for one `path-to-regexp` issue share a row.)

**Only 7.** `package.json` did not change at all. lodash and axios could move inside their caret ranges. Express
could not help, and the reason is instructive: **Express 4.17.1 pins its own dependencies to exact versions**
(`qs 6.7.0`, `body-parser 1.19.0`, ...). No lockfile edit can move a package its parent has pinned exactly. The
fix has to come from a newer Express.

## Strategy 2: relax (fixes more, may break things)

```bash
osv-scanner fix --strategy=relax -M package.json -L package-lock.json
```

```text
Can fix 50/50 matching vulnerabilities by changing 3 dependencies
UPGRADED-PACKAGE: axios,^0.21.1,^0.34.0
UPGRADED-PACKAGE: jsonwebtoken,^8.5.1,^9.0.3
UPGRADED-PACKAGE: minimist,1.2.5,^1.2.8
REMAINING-VULNS: 0
```

**Three lines changed, all 50 gone.** Express's range did not even change: relocking resolved Express 4.22.3, the
newest 4.x, which brings fixed versions of everything it pins. But read the three upgrades carefully:

| Change | Risk |
|---|---|
| `jsonwebtoken` 8 → 9 | **Major version**: breaking changes by definition |
| `axios` 0.21 → 0.34 | Under 0.x versioning, a minor bump can break things too |
| `minimist` 1.2.5 → ^1.2.8 | Patch-level; safe |

A rescan proves the result:

```text
Scanned ./package-lock.json file and found 92 packages
No issues found
```

Note the package count: **68 became 92**. A relock reshapes the tree; newer versions bring new dependencies.

## Keeping it under control

The flags I would use in practice
([docs](https://google.github.io/osv-scanner/experimental/guided-remediation/)):

| Flag | Use |
|---|---|
| `--upgrade-config=minor` | Never propose a major upgrade; can be set per package |
| `--max-depth=1` | Only vulnerabilities in direct dependencies |
| `--min-severity=7` | Ignore findings below a CVSS score |
| `--ignore-dev` | Skip `devDependencies` |
| `--no-introduce` | Reject patches that would add new vulnerabilities |
| `--apply-top=N` | Apply only the N best patches |
| `--format=json` | Output for a bot to turn into a pull request |

And three caveats from the docs to keep in mind:

- It **edits your files**. Commit first.
- It does **not** reinstall `node_modules`. Run `npm ci` and your tests afterwards.
- It does **not** read `osv-scanner.toml`; pass accepted risks with `--ignore-vulns`.

## What I took from this part

- **in-place** is a safe, small win (7 of 50 here): lockfile-only, no new ranges. Good for automatic PRs.
- **relax** gets everything (50 of 50) but chose a major upgrade. That needs a human and the test suite.
- Pinned transitive dependencies are why lockfile fixes stall: the fix is to upgrade the parent.
- The tool proposes; **the test suite and a reviewer decide**.

## References

- [Guided remediation](https://google.github.io/osv-scanner/experimental/guided-remediation/): OSV-Scanner docs, supported files, strategies, flags, risks and limitations
- [OSV-Scanner releases](https://github.com/google/osv-scanner/releases): GitHub, v2.7.0 used for these runs

Previous: [part 2]({{< relref "/posts/learning-osv-2-scanning-with-osv-scanner" >}}). Next:
[part 4, my recommendation]({{< relref "/posts/learning-osv-4-recommendation" >}}).
