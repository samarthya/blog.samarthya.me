---
title: "OWASP Top 10:2025, plainly: the ten risks and a cheat card for each"
date: 2026-10-20T19:30:00-04:00
description: "A short introduction to the OWASP Top 10:2025 for people who build software: what the list is and is not, what changed since 2021, why each category matters, and ten cheat cards to keep next to your keyboard."
categories: ["technical", "ssdlc"]
tags: ["security", "owasp", "appsec", "sdlc"]
featureimage: "feature.png"
draft: false
---

{{< lead >}}
A pilot's checklist does not list every way a plane can fail. It lists the few that keep happening, in the order
that matters. The OWASP Top 10 is that checklist for web applications.
{{< /lead >}}

When a scanner says a finding is "A05" or a security review mentions "Top 10 coverage", this is the list they
mean. This post is a quick introduction: what the list is, what changed in 2025, why each category matters, and
a cheat card for each one.

## What it is, and what it is not

The **OWASP Top 10** is an awareness document from OWASP, the open-source application security community. It
names the ten most important categories of web application security risk, based on data and a community survey.
The [2025 edition](https://top10.owasp.org/2025) is the current one.

How it is built, from the
[2025 introduction](https://top10.owasp.org/2025/0x00_2025-Introduction/):

- Contributors donated testing data for **over 2.8 million applications**.
- The team analysed **589 CWEs** (CWE is MITRE's catalogue of weakness types, such as CWE-79 for cross-site
  scripting) and used about **175,000 CVE records** from the NVD to score exploitability and impact.
- **Eight categories come from the data** and **two from a community survey**, which picks up risks that testing
  data is slow to show.

What it is **not**: a complete standard, a compliance checklist, or a test plan. Each category is a bucket of
related weaknesses (A10 alone holds 24 CWEs). For a requirements list you can test against, OWASP points people to
its Application Security Verification Standard (ASVS).

## What changed since 2021

| 2025 | Category | 2021 rank | What happened |
|---|---|---|---|
| A01 | Broken Access Control | #1 | Still #1; now also includes SSRF (server-side request forgery) |
| A02 | Security Misconfiguration | #5 | Up three places |
| A03 | Software Supply Chain Failures | (A06) | Expanded from "Vulnerable and Outdated Components" to the whole supply chain |
| A04 | Cryptographic Failures | #2 | Down two |
| A05 | Injection | #3 | Down two |
| A06 | Insecure Design | #4 | Down two |
| A07 | Authentication Failures | #7 | Renamed from "Identification and Authentication Failures" |
| A08 | Software or Data Integrity Failures | #8 | Same place |
| A09 | Security Logging and Alerting Failures | #9 | Renamed: "Monitoring" became "Alerting" |
| A10 | Mishandling of Exceptional Conditions | new | New category for 2025 |

Two changes stand out. **Supply chain** rose to #3: it ranked first in the community survey and has the highest
average incidence rate in the contributed data, 5.19%
([A03](https://top10.owasp.org/2025/A03_2025-Software_Supply_Chain_Failures/)). And **error handling** got its own
category, A10, because software that fails in an unknown state is software an attacker can steer.

## The cheat cards

Each card has three lines: what the category **means**, what it **looks like** in real code, and the **first
defence** to reach for. The badge colour groups them: red for the top three, orange for the middle, blue for
the rest.

{{< cheatcards >}}
{{< cheat id="A01" title="Broken Access Control" meta="#1 · 2021: #1" color="#dc2626" >}}
**Means:** users can act outside their permissions.

**Looks like:** changing `/orders/1001` to `/orders/1002` shows someone else's order; SSRF makes the server fetch internal URLs.

**First defence:** deny by default; check ownership on the server for every request.
{{< /cheat >}}
{{< cheat id="A02" title="Security Misconfiguration" meta="#2 · 2021: #5" color="#dc2626" >}}
**Means:** unsafe defaults, open settings, extra features left on.

**Looks like:** a public storage bucket, a debug page in production, default admin passwords.

**First defence:** hardened, repeatable configuration as code, scanned in CI.
{{< /cheat >}}
{{< cheat id="A03" title="Software Supply Chain Failures" meta="#3 · new scope" color="#dc2626" >}}
**Means:** risk from what you build *with*: dependencies, build tools, update channels.

**Looks like:** Log4Shell in a library; the 2025 Shai-Hulud npm worm stealing publish tokens.

**First defence:** an SBOM, continuous dependency scanning, signed builds.
{{< /cheat >}}
{{< cheat id="A04" title="Cryptographic Failures" meta="#4 · 2021: #2" color="#ea580c" >}}
**Means:** data that should be secret is not well protected.

**Looks like:** passwords hashed with MD5, plain HTTP, home-made encryption.

**First defence:** TLS everywhere; standard libraries; slow password hashes such as Argon2 or bcrypt.
{{< /cheat >}}
{{< cheat id="A05" title="Injection" meta="#5 · 2021: #3" color="#ea580c" >}}
**Means:** user input is run as code or as a query.

**Looks like:** SQL injection, command injection, cross-site scripting.

**First defence:** parameterised queries; output encoding; never build commands from strings.
{{< /cheat >}}
{{< cheat id="A06" title="Insecure Design" meta="#6 · 2021: #4" color="#ea580c" >}}
**Means:** the flaw is in the plan, not the code.

**Looks like:** a password reset that relies on a guessable question; no limit on how fast you can try.

**First defence:** threat modelling before building; abuse cases next to use cases.
{{< /cheat >}}
{{< cheat id="A07" title="Authentication Failures" meta="#7 · 2021: #7" color="#ea580c" >}}
**Means:** the system cannot be sure who you are.

**Looks like:** credential stuffing works; sessions never expire; no MFA on admin.

**First defence:** MFA, rate limits on login, a proven identity provider.
{{< /cheat >}}
{{< cheat id="A08" title="Software or Data Integrity Failures" meta="#8 · 2021: #8" color="#2563eb" >}}
**Means:** code or data is trusted without checking it has not been changed.

**Looks like:** auto-updates without signatures; unsafe deserialisation of user data.

**First defence:** verify signatures; protect the CI/CD pipeline; avoid deserialising untrusted data.
{{< /cheat >}}
{{< cheat id="A09" title="Security Logging and Alerting Failures" meta="#9 · renamed" color="#2563eb" >}}
**Means:** attacks happen and nobody notices.

**Looks like:** failed logins not logged; logs nobody reads; no alert on mass data export.

**First defence:** log security events, and alert on the ones that matter.
{{< /cheat >}}
{{< cheat id="A10" title="Mishandling of Exceptional Conditions" meta="#10 · new" color="#2563eb" >}}
**Means:** errors leave the system in an unknown or unsafe state.

**Looks like:** stack traces shown to users; a failed transfer that half-completes; code that "fails open".

**First defence:** catch errors where they happen, roll back, fail closed.
{{< /cheat >}}
{{< /cheatcards >}}

## Why it is worth knowing

- **It is a shared language.** "This is an A01" tells a developer, a tester and a manager the same thing.
  Scanners, pentest reports and many tools tag findings with Top 10 categories.
- **It tells you where to start.** If you can only train a team on three things this year, A01, A02 and A03 are a
  defensible choice.
- **It is evidence-based and free.** The data, the method and every category page are public.
- **It connects to attacks.** A Top 10 category is a weakness *in your code*. MITRE ATT&CK describes what an
  *attacker does* with it. The two meet in my
  [SSDLC post]({{< relref "/posts/ssdlc-in-the-age-of-ai-exploits" >}}), where each pipeline level is tagged with
  both, and are introduced together in
  [MITRE ATT&CK, plainly]({{< relref "/posts/mitre-attack-explained" >}}).

## What scanners cover, and what they miss

Automated tools are good at some categories and poor at others. Roughly:

| Good tool coverage | Partial | Needs people |
|---|---|---|
| A03 supply chain (SCA), A05 injection (SAST), A02 misconfiguration (IaC scanners) | A04 crypto, A07 authentication, A08 integrity, A10 error handling | A01 access control, A06 insecure design, A09 logging |

That is why the SSDLC post maps scanners to A02, A03, A05 and A08, and leaves A01 and A06 to threat modelling and
review on purpose.

## Takeaways

- The OWASP Top 10 is a checklist of the most common web application risks, not a full standard.
- 2025 brings **Software Supply Chain Failures** to #3 and adds **Mishandling of Exceptional Conditions** at #10.
- Broken Access Control is still #1, and it is the one scanners help with least.
- Use the cards as a shared vocabulary, and pair them with ATT&CK to talk about what attackers do next.

## References

- [OWASP Top 10:2025](https://top10.owasp.org/2025): OWASP, the ten categories and their official names
- [Introduction to the 2025 Top 10](https://top10.owasp.org/2025/0x00_2025-Introduction/): OWASP, changes since 2021, rank movements, methodology (2.8 million applications, 589 CWEs, 175,000 CVE records, eight data and two survey categories)
- [A03:2025 Software Supply Chain Failures](https://top10.owasp.org/2025/A03_2025-Software_Supply_Chain_Failures/): OWASP, survey rank, 5.19% incidence rate, Shai-Hulud and Log4Shell examples, SBOM and signing advice
- [A10:2025 Mishandling of Exceptional Conditions](https://top10.owasp.org/2025/A10_2025-Mishandling_of_Exceptional_Conditions/): OWASP, 24 CWEs, examples (verbose errors, half-completed transactions), "fail closed" advice

Related: the plain-words series on [SSDF]({{< relref "/posts/security-standards-1-nist-ssdf" >}}),
[SAMM]({{< relref "/posts/security-standards-2-owasp-samm" >}}),
[SLSA]({{< relref "/posts/security-standards-3-slsa" >}}) and
[KEV with BOD 26-04]({{< relref "/posts/security-standards-4-cisa-kev-bod-26-04" >}}).
