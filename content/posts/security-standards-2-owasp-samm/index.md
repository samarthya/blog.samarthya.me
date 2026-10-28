---
title: "Security standards, plainly, part 2: OWASP SAMM v2.0"
date: 2026-10-23T19:30:00-04:00
description: "OWASP's Software Assurance Maturity Model in plain words: five business functions, fifteen practices, three maturity levels, how a self-assessment works, and why a score you choose beats a score you are given."
categories: ["technical", "ssdlc"]
tags: ["security", "devops", "sdlc"]
series: ["Security standards, plainly"]
series_order: 2
featureimage: "feature.png"
draft: false
---

{{< lead >}}
A fitness tracker does not make you fit. It tells you where you are today, lets you pick a goal you can reach, and
shows whether you are moving towards it. OWASP SAMM is a fitness tracker for how an organisation builds secure
software.
{{< /lead >}}

In [part 1]({{< relref "/posts/security-standards-1-nist-ssdf" >}}) NIST's SSDF gave us a list of *what* a secure
development process should include. It did not say how well you do each thing, or what to improve first. That is
the gap SAMM fills.

## What it is, in one sentence

**SAMM** (Software Assurance Maturity Model) is a free, open model from OWASP that breaks software security into
fifteen practices, describes what "basic", "better" and "best" look like for each, and helps you measure where you
are and plan the next step.

The current version is **SAMM 2.0**, published under the
[CC BY-SA 4.0 licence](https://owaspsamm.org/about/). OWASP (Open Worldwide Application Security Project) is the
same non-profit community behind the OWASP Top 10.

## Five functions, fifteen practices

SAMM groups the work into five **business functions**, each with three **security practices**
([SAMM model](https://owaspsamm.org/model/)):

| Business function | What it covers | Its three practices |
|---|---|---|
| **Governance** | How security is managed and taught | Strategy & Metrics · Policy & Compliance · Education & Guidance |
| **Design** | Thinking about threats before building | Threat Assessment · Security Requirements · Secure Architecture |
| **Implementation** | Building and shipping safely | Secure Build · Secure Deployment · Defect Management |
| **Verification** | Checking that it worked | Architecture Assessment · Requirements-driven Testing · Security Testing |
| **Operations** | Running it safely in production | Incident Management · Environment Management · Operational Management |

{{< mermaid >}}
flowchart LR
  G["Governance<br/>strategy, policy, education"] --> D["Design<br/>threats, requirements, architecture"]
  D --> I["Implementation<br/>build, deploy, defects"]
  I --> V["Verification<br/>architecture, requirements, testing"]
  V --> O["Operations<br/>incidents, environment, operations"]
  O -- feedback --> G
{{< /mermaid >}}

Notice what is in there besides scanning: education, threat modelling, incident response. A team can run every
scanner in the world and still score low on SAMM, and that is the point.

## Three levels and two streams

For each practice, SAMM defines **three maturity levels**, each "a successively more sophisticated objective with
specific activities" ([About SAMM](https://owaspsamm.org/about/)). Lower levels are easier and less formal. Each
practice is also split into **two streams**, two different sides of the same practice.

*Education & Guidance* is a good example because it is the practice people most often forget
([SAMM: Education & Guidance](https://owaspsamm.org/model/governance/education-and-guidance/)):

| Level | Stream A: Training and Awareness | Stream B: Organization and Culture |
|---|---|---|
| **1** | Security awareness training for everyone involved in development | A Security Champion in each development team |
| **2** | Guidance specific to each role and technology, such as language and platform pitfalls | A secure software centre of excellence that leads developers and architects |
| **3** | In-house guidance standardised around your own secure development standards | A secure software community across the whole organisation |

Read the table as a staircase, not a checklist. Level 1 in both streams is a sensible first year for most teams.

## How an assessment works

SAMM is meant to be used, not just read. The [quick-start steps](https://owaspsamm.org/docs/getting-started/) are:

1. **Prepare:** choose the scope (one team, one product, the whole company) and the people to talk to.
2. **Assess:** score the current maturity in each of the 15 practices.
3. **Set the target:** pick a target score that points at the activities that matter most for you.
4. **Define the plan:** build a roadmap to the next level.
5. **Implement:** do the activities.
6. **Roll out:** make sure the improvements are used across the organisation.

OWASP says steps 1 to 4 can be done by one person in a day or two; steps 5 and 6 take months.

The assessment itself is an interview. The free
[SAMM Toolbox](https://owaspsamm.org/assessment/) (an Excel or Google Sheets workbook) lists questions for each
activity, each with quality criteria. The guidance is strict: if the criteria are not completely met, the answer
is "No". The scorecard tab then updates with your maturity score. Online tools such as SAMMwise (self-hosted) and
SAMMY do the same job in a browser.

## Why it is worth anything

- **It turns "be more secure" into a next step.** "Move Education & Guidance from level 0 to level 1 by naming a
  champion in each team" is a goal someone can own this quarter.
- **You pick the target.** SAMM does not say every team must reach level 3. A small internal tool and a payment
  service deserve different targets, and SAMM lets you say so.
- **It shows progress.** Reassess every six or twelve months and you have a chart that management can read.
- **It covers the people side.** Training, culture and threat modelling are practices with levels, not footnotes.
- **It connects to the SSDF.** The SSDF's reference column maps its practices to SAMM, so the "what" (SSDF) and
  the "how well" (SAMM) line up.

## What it does not do

- **It does not tell you how fast to fix things.** Like the SSDF, there is no "N days" anywhere.
  [Part 4]({{< relref "/posts/security-standards-4-cisa-kev-bod-26-04" >}}) is about that clock.
- **It is self-assessed.** A generous assessor gives a flattering score. Use the quality criteria strictly, and
  ask for evidence.
- **It does not go deep on the build pipeline.** Secure Build is one practice; the detailed requirements for
  tamper-proof builds live in SLSA, in [part 3]({{< relref "/posts/security-standards-3-slsa" >}}).

## Takeaways

- SAMM is a fitness tracker for software security: measure where you are, pick a goal, track progress.
- **5 business functions × 3 practices = 15 practices**, each with **3 maturity levels** in **2 streams**.
- The free Toolbox makes a first assessment a one- or two-day job for one person.
- Its strength is choosing your own target, and that it covers people and culture, not just tools.

## References

- [OWASP SAMM model](https://owaspsamm.org/model/): OWASP, version 2.0, the five business functions and fifteen practices
- [About SAMM](https://owaspsamm.org/about/): OWASP, three maturity levels, two streams per practice, CC BY-SA 4.0 licence
- [Education & Guidance](https://owaspsamm.org/model/governance/education-and-guidance/): OWASP, the two streams and their activities at each level
- [Getting started](https://owaspsamm.org/docs/getting-started/): OWASP, the six quick-start steps and time estimates
- [SAMM assessment](https://owaspsamm.org/assessment/): OWASP, the Toolbox interview and scorecard, SAMMwise and SAMMY
- [SP 800-218, SSDF Version 1.1](https://csrc.nist.gov/pubs/sp/800/218/final): NIST, the reference column that maps SSDF practices to SAMM

Previous: [part 1, NIST SSDF]({{< relref "/posts/security-standards-1-nist-ssdf" >}}). Next:
[part 3, SLSA]({{< relref "/posts/security-standards-3-slsa" >}}).
