---
title: "Security standards, plainly, part 3: SLSA v1.2"
date: 2026-10-28T17:03:00-04:00
description: "SLSA (Supply-chain Levels for Software Artifacts) in plain words: provenance as a receipt for a build, the Build and Source tracks and their levels, a two-step GitHub example, and what it protects against."
categories: ["technical", "ssdlc"]
tags: ["security", "devops", "ci", "sdlc"]
series: ["Security standards, plainly"]
series_order: 3
featureimage: "feature.png"
draft: false
---

{{< lead >}}
A sealed medicine bottle tells you two things: who made it, and that nobody has opened it since. You do not need
to test the pills yourself. SLSA gives software the same seal and the same label.
{{< /lead >}}

[Part 1]({{< relref "/posts/security-standards-1-nist-ssdf" >}}) (SSDF) listed what a secure process should do.
[Part 2]({{< relref "/posts/security-standards-2-owasp-samm" >}}) (SAMM) measured how well you do it. Both mostly
look at the code. SLSA looks at the journey from code to the thing you ship, because attackers have learned that
it is often easier to tamper with a build than to find a bug.

## What it is, in one sentence

**SLSA** (Supply-chain Levels for Software Artifacts, pronounced "salsa") is "a specification for describing and
incrementally improving supply chain security, established by industry consensus"
([SLSA v1.2](https://slsa.dev/spec/v1.2/)). It tells you what to do, step by step, so that anyone can check *where*
a piece of software came from and *how* it was built.

Version **1.2** was announced on
[24 November 2025](https://slsa.dev/blog/2025/11/announce-slsa-v1.2). It is backwards compatible with 1.1, and its
headline change is a new **Source track**.

## The key idea: provenance

**Provenance** is a receipt for a build: metadata that says which platform built the artifact, which build process
it used, and what the top-level inputs were, such as the source commit
([Build track basics](https://slsa.dev/spec/v1.2/build-track-basics)).

Why a receipt matters: if your release binary comes with a signed receipt saying "built by the CI system from
commit `a1b2c3` of `my-org/my-app`", then a binary built on someone's laptop, or swapped on the download server,
will not have a matching receipt. The check becomes mechanical.

## Two tracks, each a staircase

SLSA v1.2 has two **tracks**. Each has **levels**, so you can climb one step at a time.

### Build track: can I trust how it was built?

| Level | Name | In plain words | What it stops |
|---|---|---|---|
| **L0** | No guarantees | SLSA not applied | Nothing |
| **L1** | Provenance exists | The build platform writes a receipt automatically | Release mistakes; it helps debugging. The receipt is easy to forge |
| **L2** | Hosted build platform | A hosted platform builds and **signs** the receipt; consumers check the signature | Tampering *after* the build |
| **L3** | Hardened builds | Builds cannot affect each other, and the signing key is out of reach of the build steps | Tampering *during* the build, including by insiders or stolen credentials |

### Source track: can I trust the code that went in?

| Level | Name | In plain words |
|---|---|---|
| **L1** | Version controlled | The code lives in a modern version control system |
| **L2** | History & Provenance | Branch history is continuous, cannot be rewritten, is kept, and each revision gets a provenance record |
| **L3** | Continuous technical controls | The source control system enforces your rules (for example branch protection) on named branches |
| **L4** | Two-party review | Two trusted people must review every change to protected branches |

Levels come from the [Source track requirements](https://slsa.dev/spec/v1.2/source-requirements).

{{< mermaid >}}
flowchart LR
  subgraph src["Source track"]
    S["Code in version control<br/>protected branches, two-person review"]
  end
  subgraph bld["Build track"]
    B["Hosted, hardened build<br/>writes and signs provenance"]
  end
  S --> B --> A(["Artifact + signed receipt"])
  A --> C{"Consumer verifies<br/>the receipt"}
  C -- matches --> OK([Deploy])
  C -- missing or wrong --> NO([Reject])
{{< /mermaid >}}

## What it looks like in practice

On GitHub, two steps get you most of the way. GitHub's own documentation says artifact attestations
"by itself provides SLSA v1.0 Build Level 2", and that running the build in a shared reusable workflow can take
it to Build Level 3 ([GitHub docs](https://docs.github.com/en/actions/concepts/security/artifact-attestations)).

**1. Write the receipt in the workflow that builds the release:**

```yaml
permissions:
  id-token: write      # lets the job get a short-lived signing identity
  contents: read
  attestations: write  # lets the job store the attestation

steps:
  # ... your build steps produce dist/my-app ...
  - name: Generate artifact attestation
    uses: actions/attest@v4
    with:
      subject-path: dist/my-app
```

**2. Check the receipt before you deploy or install:**

```bash
gh attestation verify dist/my-app -R my-org/my-app
```

If the file was not built by that repository's workflow, verification fails. The commands follow
[GitHub's how-to guide](https://docs.github.com/en/actions/how-tos/secure-your-work/use-artifact-attestations/use-artifact-attestations).
On GitHub Enterprise Server, check your version's documentation before relying on this.

## Why it is worth anything

- **It covers a blind spot.** Code scanners look at source. Nobody scans the gap between a clean commit and the
  binary on the download page. SLSA does.
- **It is checkable by machines.** A deploy pipeline can refuse anything without a valid receipt, with no human
  judgement needed.
- **It climbs in small steps.** Build L1 is an afternoon's work; L3 can wait until the basics are in place.
- **Buyers can ask for it.** "Show me SLSA Build L2 provenance" is a precise request, much better than "is your
  build secure?".

## What it does not do

- **It does not say the code is safe.** A perfectly signed receipt can describe a build of vulnerable code.
  Provenance proves *origin*, not *quality*. Scanning (SSDF practices PW.7 and PW.8) still matters.
- **It does not cover your dependencies' bugs.** SLSA's announcement says work continues on future tracks, including
  a Dependency track; today, known CVEs in your dependencies are a job for SCA scanners and the triage in
  [part 4]({{< relref "/posts/security-standards-4-cisa-kev-bod-26-04" >}}).
- **It does not set deadlines.** Like the SSDF and SAMM, there is no clock in it.

## Takeaways

- SLSA is the sealed bottle with a label: a signed **provenance** receipt saying who built the software, how, and
  from what.
- **Build track L0–L3** protects the build; **Source track L1–L4** (new in v1.2, November 2025) protects the code
  going in.
- On GitHub, `actions/attest` plus `gh attestation verify` gets a team to Build L2 quickly.
- It proves origin, not quality: keep scanning.

## References

- [SLSA specification v1.2](https://slsa.dev/spec/v1.2/): SLSA, definition, tracks, approved status
- [Announcing SLSA v1.2](https://slsa.dev/blog/2025/11/announce-slsa-v1.2): SLSA, 24 November 2025 date, Source track, backwards compatibility, future tracks
- [Build track basics](https://slsa.dev/spec/v1.2/build-track-basics): SLSA, Build levels L0–L3 and the definition of provenance
- [Source track requirements](https://slsa.dev/spec/v1.2/source-requirements): SLSA, Source levels L1–L4
- [Artifact attestations](https://docs.github.com/en/actions/concepts/security/artifact-attestations): GitHub Docs, Build Level 2 by default, Level 3 with reusable workflows, `gh attestation verify`
- [Using artifact attestations](https://docs.github.com/en/actions/how-tos/secure-your-work/use-artifact-attestations/use-artifact-attestations): GitHub Docs, workflow permissions, `actions/attest@v4`, verification command

Previous: [part 2, OWASP SAMM]({{< relref "/posts/security-standards-2-owasp-samm" >}}). Next:
[part 4, CISA KEV and BOD 26-04]({{< relref "/posts/security-standards-4-cisa-kev-bod-26-04" >}}).
