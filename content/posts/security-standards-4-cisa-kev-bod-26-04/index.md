---
title: "Security standards, plainly, part 4: CISA KEV and BOD 26-04"
date: 2026-10-28T17:04:00-04:00
description: "CISA's Known Exploited Vulnerabilities catalog and directive BOD 26-04 in plain words: what makes a CVE 'known exploited', the four questions that set a fix deadline, the 3-day to fix-on-upgrade timelines, and how to use both outside government."
categories: ["technical", "ssdlc"]
tags: ["security", "devops", "sdlc"]
series: ["Security standards, plainly"]
series_order: 4
featureimage: "feature.png"
draft: false
---

{{< lead >}}
A hospital emergency room does not treat patients in the order they arrive, or by how loudly they shout. A triage
nurse asks a few quick questions and sends the bleeding patient in first. CISA's KEV catalog and directive
BOD 26-04 are triage for vulnerabilities.
{{< /lead >}}

The first three parts of this series, [SSDF]({{< relref "/posts/security-standards-1-nist-ssdf" >}}),
[SAMM]({{< relref "/posts/security-standards-2-owasp-samm" >}}) and
[SLSA]({{< relref "/posts/security-standards-3-slsa" >}}), share one gap: none of them says **how fast** a
vulnerability must be fixed. This part is about the clock.

## Two things, one agency

**CISA** is the US Cybersecurity and Infrastructure Security Agency. It publishes two things that work together:

- **KEV**, the Known Exploited Vulnerabilities catalog: a public list of vulnerabilities that attackers are
  actually using.
- **BOD 26-04**, a Binding Operational Directive: an order to US federal civilian agencies that says how quickly
  to fix vulnerabilities, using KEV as one of its inputs.

KEV answers "is this being exploited?". BOD 26-04 answers "so how many days do I have?".

## KEV: the "this is real" list

Most CVEs are never exploited. KEV is the short list of the ones that are. CISA calls it "the authoritative source
of vulnerabilities that have been exploited in the wild"
([KEV catalog](https://www.cisa.gov/known-exploited-vulnerabilities-catalog)), and at the time of writing it holds
**1,762 entries**. Compare that with the roughly 48,000 CVEs published in 2025 alone.

A vulnerability is added only when it meets **three criteria**
([KEV criteria](https://www.cisa.gov/known-exploited-vulnerabilities)):

1. It has a **CVE ID**.
2. There is **reliable evidence of active exploitation in the wild**.
3. There is a **clear remediation action**, such as a vendor update.

"Active exploitation" means an attacker actually ran malicious code on a system without the owner's permission,
or tried to. Scanning, security research and proof-of-concept code do **not** count. That is what makes the list
short and trustworthy.

Each entry shows the CVE, vendor and product, a description, the date added, a due date, whether it is known to be
used in ransomware campaigns, and whether BOD 26-04 requires forensic triage. The catalog is free to download as
**CSV or JSON**. Checking a CVE takes two lines:

```bash
curl -sSfo kev.json https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json
python3 -c "import json; ids={v['cveID'] for v in json.load(open('kev.json'))['vulnerabilities']}; print('CVE-2021-44228' in ids)"
```

```text
True
```

## BOD 26-04: four questions, one deadline

[BOD 26-04](https://www.cisa.gov/news-events/directives/bod-26-04-prioritizing-security-updates-based-risk), issued
on **10 June 2026**, replaced two older directives, BOD 19-02 and BOD 22-01. Instead of one deadline for every
"critical", it asks four yes-or-no questions about each vulnerability **on each asset**:

| Question | In plain words |
|---|---|
| **Asset exposure** | Can someone on the internet reach this system? |
| **KEV status** | Is the CVE in the KEV catalog? |
| **Exploit automation** | Can an attacker automate every step of the attack? |
| **Technical impact** | Does it give the attacker partial or total control? |

The combination of answers maps to a deadline. Tenable's
[summary of Table 1](https://www.tenable.com/blog/cisa-bod-26-04-FAQ-vulnerability-remediation-impact) lists
five tiers:

| Deadline | Examples from the summary |
|---|---|
| **3 days, with forensic triage** | In KEV and gives total control, whether or not it is exposed or automatable |
| **3 days** | Not in KEV, but exposed, automatable and gives total control |
| **14 days** | Most other KEV entries, plus several high-risk non-KEV combinations |
| **60 days** | For example, not exposed, automatable, partial control |
| **Fix on system upgrade** | None of the four criteria apply |

{{< mermaid >}}
flowchart LR
  V([Vulnerability on an asset]) --> Q1{In KEV?}
  Q1 --> Q2{Internet-exposed?}
  Q2 --> Q3{Automatable?}
  Q3 --> Q4{Total or partial control?}
  Q4 --> T["Deadline from Table 1:<br/>3 days · 14 days · 60 days · next upgrade"]
{{< /mermaid >}}

The deadline can move. Take a system off the internet and its timeline gets longer; CISA adds the CVE to KEV and
it gets shorter immediately. CISA will also review the timelines once each fiscal year.

The directive is explicit about why it exists now: adversaries' use of AI "may further narrow the time defenders
have to react between patch release and possible exploitation".

## Why it is worth anything, even if you are not a US agency

BOD 26-04 binds only US federal civilian agencies. The idea travels anywhere.

- **It makes most of the pile not urgent, officially.** CISA
  [reports](https://www.cisa.gov/news-events/news/patch-smarter-not-harder) that at one large agency only 1% of
  vulnerability instances fell into the fastest category, and over 60% could wait for the next planned upgrade.
  That is a gift to tired teams.
- **It replaces severity with risk.** A CVSS 9.8 on an internal test box and the same CVE on your login page are
  not the same emergency. The four questions capture that difference.
- **KEV is free and public.** Any team can download it every night and flag matches in its findings. That one
  join changes how a vulnerability list reads.
- **It gives you a defensible policy.** "We follow the BOD 26-04 model" is easier to agree with than a home-made
  rule.

In the [SSDLC post]({{< relref "/posts/ssdlc-in-the-age-of-ai-exploits" >}}) I use a simplified version: KEV plus
exposure plus [EPSS](https://www.first.org/epss/) (a daily probability that a CVE will be exploited), with
3, 14 and 30-day tiers. The [triage script](https://github.com/samarthya/ssdlc-triage) that implements it is about
ten lines of policy. Mine is stricter than BOD 26-04's 60-day tier; choose what fits your risk.

## What it does not do

- **It does not find vulnerabilities.** It ranks the ones your scanners find. Without an inventory of assets and
  their CVEs, there is nothing to rank.
- **KEV lags reality.** A vulnerability can be exploited for days before reliable evidence reaches CISA. That is
  why exposure and likelihood (EPSS) still matter for CVEs not yet on the list.
- **"Exposed" and "automatable" need your knowledge.** CISA cannot know which of your services face the internet.
  You need an asset inventory with that tag, which is exactly what the directive asks agencies to build.

## Takeaways

- **KEV** is the short, trustworthy list of CVEs attackers are really using: three criteria, free JSON and CSV.
- **BOD 26-04** (10 June 2026) turns four questions into a deadline from **3 days** to **fix on next upgrade**.
- Most vulnerabilities land in the slow lanes. Fix a small set very fast, and stop pretending the rest is urgent.
- It is the clock the other three standards leave out. Together: SSDF says what, SAMM says how well, SLSA proves
  where from, and KEV with BOD 26-04 says how fast.

## References

- [BOD 26-04: Prioritizing Security Updates Based on Risk](https://www.cisa.gov/news-events/directives/bod-26-04-prioritizing-security-updates-based-risk): CISA, issue date, scope, superseded directives, four criteria, AI statement, annual review, asset tagging
- [CISA BOD 26-04 FAQ](https://www.tenable.com/blog/cisa-bod-26-04-FAQ-vulnerability-remediation-impact): Tenable, the five remediation tiers and examples from Table 1, how timelines change
- [Patch Smarter, Not Harder](https://www.cisa.gov/news-events/news/patch-smarter-not-harder): CISA, the 1% and over-60% figures
- [Known Exploited Vulnerabilities Catalog](https://www.cisa.gov/known-exploited-vulnerabilities-catalog): CISA, entry count, entry fields, CSV and JSON downloads
- [Reducing the Significant Risk of Known Exploited Vulnerabilities](https://www.cisa.gov/known-exploited-vulnerabilities): CISA, the three KEV criteria and the definition of active exploitation
- [Exploit Prediction Scoring System (EPSS)](https://www.first.org/epss/): FIRST, the daily exploitation probability used in my triage

Previous: [part 3, SLSA]({{< relref "/posts/security-standards-3-slsa" >}}). Start of the series:
[part 1, NIST SSDF]({{< relref "/posts/security-standards-1-nist-ssdf" >}}).
