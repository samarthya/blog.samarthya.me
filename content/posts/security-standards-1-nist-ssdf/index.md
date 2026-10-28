---
title: "Security standards, plainly, part 1: NIST SSDF (SP 800-218)"
date: 2026-10-22T19:30:00-04:00
description: "What NIST's Secure Software Development Framework is, its four groups of practices in plain words, what it asks of a team, why buyers care about it, and what it deliberately leaves out."
categories: ["technical", "ssdlc"]
tags: ["security", "devops", "sdlc"]
series: ["Security standards, plainly"]
series_order: 1
featureimage: "feature.png"
draft: false
---

{{< lead >}}
A building code does not tell you which bricks to buy. It tells you what a safe building must have: exits,
wiring that will not catch fire, a way to stop the roof falling in. NIST's Secure Software Development Framework
is that code for software teams.
{{< /lead >}}

This series explains, for someone who does not live in security, the four names that keep coming up when people
talk about building software safely: **NIST SSDF**, **OWASP SAMM**, **SLSA** and **CISA's KEV catalog with
directive BOD 26-04**. Each post answers three questions: what is it, what does it ask of a team, and what is it
worth. I lean on all four in
[SSDLC when exploits are cheap]({{< relref "/posts/ssdlc-in-the-age-of-ai-exploits" >}}).

## What it is, in one sentence

The **SSDF** (Secure Software Development Framework) is a list of things a software producer should do so that the
software it ships has fewer vulnerabilities, the ones that slip through do less damage, and the same mistake is
not made twice.

It is published by NIST, the US National Institute of Standards and Technology, as
[Special Publication 800-218](https://csrc.nist.gov/pubs/sp/800/218/final). The current final version is
**SSDF 1.1, from February 2022**. A **version 1.2** was released as an
[initial public draft](https://csrc.nist.gov/pubs/sp/800/218/r1/ipd) on 17 December 2025; its comment period
closed on 30 January 2026, and as I write it is still a draft.

Two words in NIST's own description matter most. The SSDF is a set of **high-level** practices that can be
**integrated into each SDLC implementation**
([SP 800-218 abstract](https://csrc.nist.gov/pubs/sp/800/218/final)). High-level means it says *what*, not
*which tool*. Integrated means it does not replace how you already build software, whether that is Scrum,
Kanban or a yearly waterfall release. It adds to it.

## The four groups, in plain words

The SSDF has four groups of practices. Each practice has an ID, such as `PW.7`, so teams and buyers can point at
the same thing.

| Group | ID | In plain words | Example practice from SSDF 1.1 |
|---|---|---|---|
| **Prepare the Organization** | PO | Get people, process and tools ready *before* the code is written | PO.3 Implement Supporting Toolchains |
| **Protect the Software** | PS | Stop anyone tampering with the code or the releases | PS.1 Protect All Forms of Code from Unauthorized Access and Tampering |
| **Produce Well-Secured Software** | PW | Design, write, review and test with security in mind | PW.7 Review and/or Analyze Human-Readable Code to Identify Vulnerabilities |
| **Respond to Vulnerabilities** | RV | When a hole is found after release, fix it and learn from it | RV.3 Analyze Vulnerabilities to Identify Their Root Causes |

The full list in 1.1 has 19 practices. A few more, to give the flavour:

- **PO.1** Define Security Requirements for Software Development
- **PO.2** Implement Roles and Responsibilities
- **PS.3** Archive and Protect Each Software Release
- **PW.4** Reuse Existing, Well-Secured Software When Feasible Instead of Duplicating Functionality
- **PW.8** Test Executable Code to Identify Vulnerabilities
- **PW.9** Configure Software to Have Secure Settings by Default
- **RV.1** Identify and Confirm Vulnerabilities on an Ongoing Basis
- **RV.2** Assess, Prioritize, and Remediate Vulnerabilities

Each practice breaks down into **tasks** (for example `PO.1.1`), **notional implementation examples** (ideas, not
rules) and **references** that map the practice to other standards such as OWASP SAMM, BSIMM and ISO 27034. That
last column is useful: if your organisation already follows one of those, you can see what you already cover.

{{< mermaid >}}
flowchart LR
  PO["PO: Prepare<br/>people, rules, tools"] --> PW["PW: Produce<br/>design, code, review, test"]
  PS["PS: Protect<br/>code and releases"] --> PW
  PW --> REL([Release])
  REL --> RV["RV: Respond<br/>find, fix, find the root cause"]
  RV -- lessons --> PO
{{< /mermaid >}}

## What it looks like on a real team

Here is how a few SSDF practices turn into everyday work. None of this needs a big budget.

| SSDF practice | What it becomes |
|---|---|
| PO.3 Supporting toolchains | A secrets scanner, a code scanner and a dependency scanner in the CI pipeline |
| PO.4 Criteria for security checks | A written rule: "a PR with a new critical finding or a leaked secret cannot merge" |
| PS.1 Protect code | Branch protection, required reviews, no shared admin accounts |
| PS.3 Archive each release | Keep the exact build, its SBOM (list of components) and its signature for every release |
| PW.7 / PW.8 Review and test | Code review plus automated scans on every pull request |
| RV.1 Ongoing identification | Rescan shipped releases against new CVEs every night |
| RV.3 Root causes | When the same kind of bug appears three times, fix the pattern (a library, a lint rule, a training session) |

The SSDLC post builds exactly this loop and puts time limits on it.

## Why it is worth anything

**For a development team**, it is a checklist that is hard to argue with. "NIST says we should rescan released
software" ends a debate faster than "I think we should".

**For managers**, it gives a shared vocabulary. Instead of "are we secure?", the question becomes "which of the
19 practices do we do, and which do we skip on purpose?"

**For buyers**, it is the language of procurement. NIST says the SSDF gives software purchasers "a common
vocabulary" for talking to suppliers ([SSDF project page](https://csrc.nist.gov/projects/ssdf)). Appendix A of
SP 800-218 maps the software-security clauses of US Executive Order 14028 to SSDF practices, which is why the
framework turns up in US government purchasing. If you sell software to a large organisation, expect to be asked
about it.

**For AI work**, NIST has added a companion,
[SP 800-218A](https://csrc.nist.gov/projects/ssdf), a "community profile" that extends the same practices to
generative AI and foundation models.

## What it does not do

This is the part most summaries skip.

- **It does not say how fast.** There is no "fix critical issues within N days". That clock comes from elsewhere,
  for example CISA's directive in [part 4]({{< relref "/posts/security-standards-4-cisa-kev-bod-26-04" >}}).
- **It does not measure maturity.** It lists practices; it does not say whether you do them well. That is what
  OWASP SAMM is for, in [part 2]({{< relref "/posts/security-standards-2-owasp-samm" >}}).
- **It is guidance, not a certificate.** NIST publishes the practices; it does not audit you against them.
  Claims of conformance come from the producer.
- **It does not name tools.** Picking Semgrep or a commercial scanner is your decision.

## Takeaways

- The SSDF is a building code for software: what a safe process must include, not which tools to use.
- Four groups: **Prepare** the organisation, **Protect** the software, **Produce** well-secured software,
  **Respond** to vulnerabilities. Version 1.1 (February 2022) is final; 1.2 is a draft from December 2025.
- Its value is a shared vocabulary between developers, managers and buyers, with IDs you can point at.
- It leaves out speed and maturity on purpose; other standards fill those gaps.

## References

- [SP 800-218, SSDF Version 1.1](https://csrc.nist.gov/pubs/sp/800/218/final): NIST, title, February 2022 date, abstract, practice and task structure, Appendix A mapping to EO 14028
- [SP 800-218 Rev. 1 (Initial Public Draft), SSDF Version 1.2](https://csrc.nist.gov/pubs/sp/800/218/r1/ipd): NIST, 17 December 2025 draft and 30 January 2026 comment deadline
- [Secure Software Development Framework project](https://csrc.nist.gov/projects/ssdf): NIST, the four practice groups, the "common vocabulary" purpose, SP 800-218A for generative AI
- [Draft SSDF version 1.2 announcement](https://csrc.nist.gov/News/2025/draft-ssdf-version-1-2): NIST, why the revision was published (Executive Order 14306)

Next in the series: [part 2, OWASP SAMM]({{< relref "/posts/security-standards-2-owasp-samm" >}}).
