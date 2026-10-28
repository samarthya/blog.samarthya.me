---
title: "MITRE ATT&CK, plainly: tactics, technique IDs and a cheat card for each tactic"
date: 2026-10-21T19:30:00-04:00
description: "A short introduction to MITRE ATT&CK for people who build software: how to read an ID like T1552.001, the 15 Enterprise tactics in v20 (including the new Stealth and Defense Impairment), a cheat card for each, and how developers can use it."
categories: ["technical", "ssdlc"]
tags: ["security", "mitre", "attack", "sdlc"]
featureimage: "feature.png"
draft: false
---

{{< lead >}}
A football coach studies match footage of the other team: how they open, how they press, how they score. MITRE
ATT&CK is the match footage of real attackers, cut into named and numbered moves.
{{< /lead >}}

The [OWASP Top 10]({{< relref "/posts/owasp-top-10-2025-explained" >}}) describes weaknesses *in your software*.
ATT&CK describes what *attackers do*: how they get in, stay in, move around and take what they came for. You
will see its IDs, such as `T1190` or `T1552.001`, in threat reports, detection rules and, increasingly, in
pipeline designs like the one in my
[SSDLC post]({{< relref "/posts/ssdlc-in-the-age-of-ai-exploits" >}}). This post explains how to read them.

## What it is

MITRE's own definition is short: ATT&CK is a "knowledge base of adversarial techniques based on real-world
observations" ([ATT&CK resources](https://attack.mitre.org/resources/)). It is free to use, and every entry links
to the public reports it was built from.

There are three matrices: **Enterprise** (Windows, Linux, macOS, cloud, containers, network devices), **Mobile**
and **ICS** (industrial control systems). This post covers Enterprise.

The current release is **ATT&CK v20**, from **13 October 2026**. Its Enterprise matrix has **15 tactics,
227 techniques and 479 sub-techniques** ([ATT&CK updates](https://attack.mitre.org/resources/updates/)).

## How to read an ID

ATT&CK has a small vocabulary. MITRE puts it this way: tactics are the **why**, techniques are the **how**.

| Prefix | Is a… | Example | Answers |
|---|---|---|---|
| `TA` | **Tactic**: the attacker's goal at this step | `TA0001` Initial Access | *Why* are they doing this? |
| `T` | **Technique**: a way to reach that goal | `T1552` Unsecured Credentials | *How*, in general? |
| `T….nnn` | **Sub-technique**: a more specific way | `T1552.001` Credentials In Files | *How*, exactly? |
| `M` | **Mitigation**: a defence that helps | `M1047` Audit | What *stops* it? |
| `G`, `S` | **Group** and **Software**: who uses it, with which tools | | *Who* has done it? |

So `T1552.001` reads as: technique 1552, *Unsecured Credentials*, sub-technique 001, *Credentials In Files*
([T1552.001](https://attack.mitre.org/techniques/T1552/001/)). It falls under the Credential Access tactic, and
MITRE lists mitigations such as auditing for password files (M1047) and password policies that forbid storing
them (M1027). That is a leaked `.env` file in a repository, described in a way every security tool understands.

One technique can serve several tactics. `T1078` *Valid Accounts*, logging in with stolen but real credentials,
is listed under Initial Access, Persistence, Privilege Escalation and Stealth, because a real account helps with
all four.

## What changed recently: Defense Evasion was split

If you learned ATT&CK a few years ago, you will remember 14 tactics, including *Defense Evasion*. That tactic is
gone. In its place are two
([Sophos](https://www.sophos.com/blog/mitre-enterprise-attack-grew-15th-tactic-practical-dfir-field-guide)):

- **Stealth** (`TA0005`, the old ID): "The adversary is trying to hide and conceal their actions, appearing as
  normal behavior", for example *Masquerading* (`T1036`) or *Obfuscated Files or Information* (`T1027`)
  ([TA0005](https://attack.mitre.org/tactics/TA0005/)).
- **Defense Impairment** (`TA0112`, new, created in April 2026): "The adversary is trying to break security
  mechanisms, pipelines, and tooling so defenders can't see or trust what's happening", for example
  *Disable or Modify Tools* (`T1685`) ([TA0112](https://attack.mitre.org/tactics/TA0112/)).

The difference is useful: hiding *from* your defences versus breaking them. Note the word "pipelines" in the new
tactic. Tampering with a CI system's security checks is now a named attacker goal. Older reports and tools still
use Defense Evasion; map them to one of the two.

## The cheat cards: 15 tactics

One card per tactic, in the order an attack usually unfolds. Each has the tactic ID, its goal in plain words, one
example technique and what a development team can do about it. The colours group the phases: **blue** for
getting in, **orange** for gaining a foothold, **purple** for spreading, **red** for the payoff.

{{< cheatcards >}}
{{< cheat id="TA0043" title="Reconnaissance" meta="1 · getting in" color="#2563eb" >}}
**Goal:** learn about the target.

**Example:** `T1595` Active Scanning of your public hosts.

**Dev angle:** expose less; no version banners or debug endpoints.
{{< /cheat >}}
{{< cheat id="TA0042" title="Resource Development" meta="2 · getting in" color="#2563eb" >}}
**Goal:** prepare tools and infrastructure.

**Example:** `T1583` Acquire Infrastructure, such as look-alike domains.

**Dev angle:** mostly outside your control; watch for typo-squatted packages.
{{< /cheat >}}
{{< cheat id="TA0001" title="Initial Access" meta="3 · getting in" color="#2563eb" >}}
**Goal:** get a first foothold.

**Example:** `T1190` Exploit Public-Facing Application; `T1195` Supply Chain Compromise.

**Dev angle:** patch exposed services first; scan dependencies.
{{< /cheat >}}
{{< cheat id="TA0002" title="Execution" meta="4 · foothold" color="#ea580c" >}}
**Goal:** run their code.

**Example:** `T1059` Command and Scripting Interpreter.

**Dev angle:** never pass user input to a shell; parameterise.
{{< /cheat >}}
{{< cheat id="TA0003" title="Persistence" meta="5 · foothold" color="#ea580c" >}}
**Goal:** stay in after a restart or a password change.

**Example:** `T1053` Scheduled Task/Job.

**Dev angle:** immutable images; rebuild rather than patch in place.
{{< /cheat >}}
{{< cheat id="TA0004" title="Privilege Escalation" meta="6 · foothold" color="#ea580c" >}}
**Goal:** get more rights than they started with.

**Example:** `T1068` Exploitation for Privilege Escalation.

**Dev angle:** run as non-root; least-privilege service accounts.
{{< /cheat >}}
{{< cheat id="TA0005" title="Stealth" meta="7 · foothold" color="#ea580c" >}}
**Goal:** hide, and look like normal activity.

**Example:** `T1036` Masquerading as a legitimate binary.

**Dev angle:** signed artifacts; know what normal looks like.
{{< /cheat >}}
{{< cheat id="TA0112" title="Defense Impairment" meta="8 · foothold · new" color="#ea580c" >}}
**Goal:** break the defences, including pipelines.

**Example:** `T1685` Disable or Modify Tools.

**Dev angle:** protect CI config; alert when a security check is removed.
{{< /cheat >}}
{{< cheat id="TA0006" title="Credential Access" meta="9 · spreading" color="#7c3aed" >}}
**Goal:** steal account names and passwords.

**Example:** `T1552.001` Credentials In Files.

**Dev angle:** secret scanning on every commit; a secrets manager.
{{< /cheat >}}
{{< cheat id="TA0007" title="Discovery" meta="10 · spreading" color="#7c3aed" >}}
**Goal:** learn the environment from inside.

**Example:** `T1082` System Information Discovery.

**Dev angle:** minimal images with no extra tools to explore with.
{{< /cheat >}}
{{< cheat id="TA0008" title="Lateral Movement" meta="11 · spreading" color="#7c3aed" >}}
**Goal:** move to other systems.

**Example:** `T1021` Remote Services.

**Dev angle:** network policies; no shared credentials between services.
{{< /cheat >}}
{{< cheat id="TA0009" title="Collection" meta="12 · payoff" color="#dc2626" >}}
**Goal:** gather the data they want.

**Example:** `T1213` Data from Information Repositories, such as wikis and code hosts.

**Dev angle:** access reviews; nothing secret in tickets or wikis.
{{< /cheat >}}
{{< cheat id="TA0011" title="Command and Control" meta="13 · payoff" color="#dc2626" >}}
**Goal:** talk to compromised systems.

**Example:** `T1071` Application Layer Protocol, hiding in normal web traffic.

**Dev angle:** restrict outbound traffic from workloads.
{{< /cheat >}}
{{< cheat id="TA0010" title="Exfiltration" meta="14 · payoff" color="#dc2626" >}}
**Goal:** get the data out.

**Example:** `T1041` Exfiltration Over C2 Channel.

**Dev angle:** egress limits; alert on unusual data volumes.
{{< /cheat >}}
{{< cheat id="TA0040" title="Impact" meta="15 · payoff" color="#dc2626" >}}
**Goal:** disrupt, destroy or hold to ransom.

**Example:** `T1486` Data Encrypted for Impact (ransomware).

**Dev angle:** tested backups; infrastructure you can rebuild from code.
{{< /cheat >}}
{{< /cheatcards >}}

## How a developer uses it

ATT&CK was built for defenders and threat hunters, but it is useful one step earlier, in the pipeline.

1. **Name what each control stops.** "Gitleaks on commit" is a tool. "Gitleaks on commit stops `T1552.001`" is a
   reason. The SSDLC post tags every pipeline level this way:

   | Pipeline level | Technique it guards against | MITRE mitigation |
   |---|---|---|
   | Commit: secret scanning | `T1552.001` Credentials In Files | M1047 Audit |
   | PR and build: dependency scanning | `T1195.001` Compromise Software Dependencies and Development Tools | M1016 Vulnerability Scanning |
   | Build: signed provenance | `T1195.002` Compromise Software Supply Chain | M1013 Application Developer Guidance |
   | Nightly rescan of exposed apps | `T1190` Exploit Public-Facing Application | M1051 Update Software |

   Techniques from [T1195](https://attack.mitre.org/techniques/T1195/) and
   [T1190](https://attack.mitre.org/techniques/T1190/); mitigations as MITRE lists them.

2. **Find the gaps.** Shade the techniques you cover in the free
   [ATT&CK Navigator](https://mitre-attack.github.io/attack-navigator/). The white areas are the conversation for
   your next planning meeting.
3. **Speak the same language as the security team.** A finding tagged with an OWASP category (the weakness) and
   an ATT&CK technique (the attack) is understood by developers and by the people who write detections.

## What it does not do

- **It does not rank anything.** ATT&CK does not say which technique is most dangerous for you. Use exposure,
  KEV and EPSS for that, as in [part 4 of the standards series]({{< relref "/posts/security-standards-4-cisa-kev-bod-26-04" >}}).
- **It is not a checklist to complete.** Hundreds of techniques, many irrelevant to a given system. Pick the ones
  your architecture makes possible.
- **IDs change.** Techniques get added, moved and occasionally replaced; in 2026 even a tactic was split. Note the
  version when you tag findings.

## Takeaways

- ATT&CK is match footage of real attackers: **tactics** are the why (`TA…`), **techniques** the how (`T…`),
  **sub-techniques** the exact how (`T….001`).
- **v20** (13 October 2026): 15 Enterprise tactics, 227 techniques, 479 sub-techniques. Defense Evasion became
  **Stealth** and **Defense Impairment**.
- For developers, the value is naming what each control stops and spotting what nothing stops.
- OWASP Top 10 describes the weakness; ATT&CK describes the attack. Use both.

## References

- [MITRE ATT&CK](https://attack.mitre.org/): MITRE, the three matrices and the Enterprise tactic list with IDs
- [ATT&CK updates](https://attack.mitre.org/resources/updates/): MITRE, v20 release date (13 October 2026) and Enterprise counts
- [ATT&CK resources](https://attack.mitre.org/resources/): MITRE, the definition, tactics as "why" and techniques as "how", ATT&CK Navigator
- [TA0005 Stealth](https://attack.mitre.org/tactics/TA0005/) and [TA0112 Defense Impairment](https://attack.mitre.org/tactics/TA0112/): MITRE, descriptions, creation date, example techniques
- [T1552.001 Credentials In Files](https://attack.mitre.org/techniques/T1552/001/): MITRE, description and mitigations M1047, M1027
- [T1195 Supply Chain Compromise](https://attack.mitre.org/techniques/T1195/): MITRE, sub-techniques .001 to .003 and mitigations
- [T1190 Exploit Public-Facing Application](https://attack.mitre.org/techniques/T1190/): MITRE, tactic, description, mitigations M1051, M1035, M1030, M1050
- Technique pages used for the cheat cards: [T1595](https://attack.mitre.org/techniques/T1595/), [T1583](https://attack.mitre.org/techniques/T1583/), [T1059](https://attack.mitre.org/techniques/T1059/), [T1053](https://attack.mitre.org/techniques/T1053/), [T1068](https://attack.mitre.org/techniques/T1068/), [T1036](https://attack.mitre.org/techniques/T1036/), [T1685](https://attack.mitre.org/techniques/T1685/), [T1082](https://attack.mitre.org/techniques/T1082/), [T1021](https://attack.mitre.org/techniques/T1021/), [T1213](https://attack.mitre.org/techniques/T1213/), [T1071](https://attack.mitre.org/techniques/T1071/), [T1041](https://attack.mitre.org/techniques/T1041/), [T1486](https://attack.mitre.org/techniques/T1486/), [T1078](https://attack.mitre.org/techniques/T1078/): MITRE, names and tactics as of v20
- [MITRE Enterprise ATT&CK grew a 15th tactic](https://www.sophos.com/blog/mitre-enterprise-attack-grew-15th-tactic-practical-dfir-field-guide): Sophos, that Stealth and Defense Impairment replaced Defense Evasion
