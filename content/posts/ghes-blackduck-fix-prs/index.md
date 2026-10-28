---
title: "From finding to fix: Black Duck pull requests on GitHub Enterprise Server"
date: 2026-10-27T20:05:18-04:00
description: "How to wire Black Duck scans into a self-hosted GitHub Enterprise Server so findings land in code scanning and fixes arrive as pull requests, plus a small script for tools that cannot open PRs themselves."
categories: ["technical"]
tags: ["security", "sast", "github", "devops", "ci"]
featureimage: "feature.png"
draft: false
---

{{< lead >}}
A vulnerability report that nobody reads is a smoke alarm with no battery. The goal is not more findings. The
goal is a pull request that a developer can review and merge before lunch.
{{< /lead >}}

## Why this post

SentinelOne's
[overview of GitHub vulnerability management](https://www.sentinelone.com/cybersecurity-101/cybersecurity/github-vulnerability-management/)
describes the job as "discovering, triaging, and remediating security vulnerabilities in GitHub repositories,
dependencies, and workflows". It lists the usual native tools: Dependabot, code scanning, secret scanning and
security advisories. It also admits the gaps: no asset inventory or risk scoring, and dependencies that
Dependabot cannot track.

Most of that article assumes github.com. My question was narrower. **On a GitHub Enterprise Server (GHES)
instance in your own data centre, running a commercial scanner such as Black Duck, how do you get from "scan
found something" to "here is a pull request that fixes it"?**

This post covers the plumbing that makes that work: what GHES provides, what Black Duck provides, and a small
script for the cases where neither opens a PR for you.

## First, name the tools correctly

"Black Duck" is a company and a product family, and the names get mixed up in conversations about SAST.

| Product | Type | Finds | Can it open a fix PR? |
|---|---|---|---|
| **Black Duck SCA** | Software composition analysis | Vulnerable open-source *dependencies* | Yes, for vulnerable direct dependencies ([docs](https://docs.blackduck.com/r/bridge/latest/bridge-cli-guide/using-the-black-duck-security-scan-action-with-black-duck-sca.html)) |
| **Coverity** | Static analysis (SAST) | Flaws in *your own code* (injection, null dereference, resource leaks) | No; it posts PR comments ([docs](https://docs.blackduck.com/r/bridge/latest/bridge-cli-guide/using-the-black-duck-security-scan-action-with-coverity.html)) |
| **Polaris** | Hosted platform running both | Both | Through the same action |

The difference matters. A dependency fix is mechanical: change `2.14.1` to `2.17.2` in `pom.xml`. A SAST fix
means rewriting logic, and no scanner should push that straight to a branch without a person in the loop. So
the realistic design is:

- **SCA findings:** let the scanner raise the fix PR.
- **SAST findings:** surface them as code scanning alerts and PR comments. Automate a PR only for the narrow
  classes where the fix is deterministic and you have written the transform yourself.

## What changes on a self-hosted GHES

GHES is not github.com running in your basement. Four differences shape the design.

**1. Runners are yours.** GHES has no GitHub-hosted runners, so every job runs on a
[self-hosted runner](https://docs.github.com/en/enterprise-server@latest/admin/managing-github-actions-for-your-enterprise/managing-access-to-actions-from-githubcom/about-using-actions-in-your-enterprise).
The runner needs network access to your GHES API, to your Black Duck server and to wherever the scanner's CLI
is downloaded from.

**2. Marketplace actions are not automatically available.** GHES ships with the official `actions/*` actions.
To use `blackduck-inc/black-duck-security-scan`, either enable **GitHub Connect** (automatic access to
github.com actions, with policies to restrict them) or copy the action in with the **`actions-sync`** tool if the
instance is air-gapped
([GitHub docs](https://docs.github.com/en/enterprise-server@latest/admin/managing-github-actions-for-your-enterprise/managing-access-to-actions-from-githubcom/about-using-actions-in-your-enterprise)).

**3. Code scanning is licensed and switched on by a site administrator.** Uploading third-party results needs
code scanning enabled on the appliance
([docs](https://docs.github.com/en/enterprise-server@latest/code-security/how-tos/find-and-fix-code-vulnerabilities/integrate-with-existing-tools/upload-sarif-file)),
and code scanning is part of the paid **GitHub Code Security** product. Dependabot *alerts* are included in all
plans
([docs](https://docs.github.com/en/enterprise-server@latest/get-started/learning-about-github/about-github-advanced-security)).

**4. Dependabot needs a link to the outside world.** Dependabot alerts on GHES need GitHub Connect and the
dependency graph. Advisory data syncs from the GitHub Advisory Database once an hour. Dependabot *security
updates* (its own PRs) also need TLS and dedicated self-hosted runners, and are not available on clustered
installs
([docs](https://docs.github.com/en/enterprise-server@latest/admin/configuration/configuring-github-connect/enabling-dependabot-for-your-enterprise)).

The fourth point is why many enterprises bring in Black Duck in the first place. When the appliance cannot
connect to github.com, or policy requires a licence and vulnerability database already approved internally,
Dependabot is not available and something else has to raise the PRs.

## The flow

Each step below is a numbered stage in the workflow.

1. A push to `main` triggers a **full** Black Duck SCA scan on a self-hosted runner.
2. The scan writes a **SARIF** report and uploads it to GHES code scanning. Findings show up in the Security tab
   next to CodeQL and any other tool.
3. For each vulnerable *direct* dependency that has upgrade guidance, the action opens a **fix PR**.
4. On every pull request, a **rapid** scan comments on newly introduced issues only.
5. Coverity runs on pull requests too and comments on new SAST issues.

SARIF (Static Analysis Results Interchange Format) is the JSON format code scanning reads. Any tool that can
produce it can feed the Security tab, which is how one dashboard can show results from more than one scanner.

## The workflow

The inputs below come from Black Duck's
[action reference](https://docs.blackduck.com/r/bridge/latest/bridge-cli-guide/using-the-black-duck-security-scan-action-with-black-duck-sca.html)
for action `v2`. Pin the exact release you synced to your instance.

```yaml
# .github/workflows/blackduck.yml
name: black-duck
on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  sca:
    runs-on: [self-hosted, linux]
    permissions:
      contents: write          # fix PRs push a branch
      pull-requests: write     # fix PRs and PR comments
      security-events: write   # SARIF upload to code scanning
    steps:
      - uses: actions/checkout@v5

      # Pull request: rapid scan, comment on new issues only
      - name: Black Duck SCA (PR)
        if: ${{ github.event_name == 'pull_request' }}
        uses: blackduck-inc/black-duck-security-scan@v2
        with:
          blackducksca_url: ${{ vars.BLACKDUCK_URL }}
          blackducksca_token: ${{ secrets.BLACKDUCK_TOKEN }}
          blackducksca_scan_full: false
          blackducksca_prComment_enabled: true
          github_token: ${{ secrets.GITHUB_TOKEN }}

      # Main: full scan, SARIF to code scanning, fix PRs for critical/high
      - name: Black Duck SCA (full)
        if: ${{ github.event_name != 'pull_request' }}
        uses: blackduck-inc/black-duck-security-scan@v2
        env:
          DETECT_PROJECT_NAME: ${{ github.event.repository.name }}
        with:
          blackducksca_url: ${{ vars.BLACKDUCK_URL }}
          blackducksca_token: ${{ secrets.BLACKDUCK_TOKEN }}
          blackducksca_scan_full: true
          blackducksca_reports_sarif_create: true
          blackducksca_reports_sarif_severities: 'Critical,High'
          blackducksca_upload_sarif_report: true
          blackducksca_fixpr_enabled: true
          blackducksca_fixpr_maxCount: 5
          blackducksca_fixpr_filter_severities: 'CRITICAL,HIGH'
          blackducksca_fixpr_useUpgradeGuidance: 'SHORT_TERM,LONG_TERM'
          github_token: ${{ secrets.GITHUB_TOKEN }}
```

A few details to watch, all from the vendor documentation:

- **Fix PRs and SARIF come only from full scans.** SARIF creation is not supported on PR scans, so the split
  between the two steps is required, not a matter of style.
- **`useUpgradeGuidance` picks the target version.** `SHORT_TERM` is the nearest version without the
  vulnerability; `LONG_TERM` is the version with the fewest known issues. The first value wins. If Black Duck has
  no guidance, no PR is created.
- **`maxCount` caps PRs per branch.** Start small. Twenty PRs on the first day is how a team learns to ignore a
  bot.
- **PR comments need a baseline.** A full scan of the target branch must already exist on the Black Duck server.
- **GHES version.** Black Duck says SARIF upload "has been verified on Enterprise Server version 3.15". Newer
  versions should work because the upload API is the same, but test on yours.
- **Input spelling.** The vendor pages show both `blackducksca_prcomment_enabled` and
  `blackducksca_prComment_enabled`. Check against the release you pin.

## The token trap

The workflow above uses `GITHUB_TOKEN`, and that is fine for a first test. It causes two problems in practice.

First, a repository setting, **"Allow GitHub Actions to create and approve pull requests"**, must be on, and the
default token is often read-only
([docs](https://docs.github.com/en/enterprise-server@latest/repositories/managing-your-repositorys-settings-and-features/enabling-features-for-your-repository/managing-github-actions-settings-for-a-repository)).

Second, and less obvious: "events triggered by the `GITHUB_TOKEN` will not create a new workflow run"
([docs](https://docs.github.com/en/enterprise-server@latest/actions/how-tos/write-workflows/choose-when-workflows-run/trigger-a-workflow)).
A fix PR opened with that token **does not run your build or tests**. The PR sits there with no checks, and a
reviewer has to guess whether the upgrade broke anything. That makes a fix PR less useful than it looks.

Use a **GitHub App** installed on the organisation, with `contents`, `pull_requests` and `security_events`
permissions. Mint an installation token at the start of the job and pass it as `github_token`. PRs then trigger
CI like any other PR, and the audit log shows a named bot instead of a generic token.

## When the scanner cannot open the PR: a small script

Coverity, an in-house linter or a rule you wrote yourself will not open fix PRs. If the fix is deterministic, for
example a lint autofix, a banned-function replacement or a config hardening change, you can raise the PR
yourself with two REST calls against the GHES API.

On a GHES runner, `GITHUB_API_URL` is already set to `https://HOSTNAME/api/v3`
([docs](https://docs.github.com/en/enterprise-server@latest/actions/reference/workflows-and-actions/variables)),
so the same script works on any instance.

```bash
#!/usr/bin/env bash
# raise-fix-pr.sh: commit the working-tree fix on a branch and open (or reuse) a PR.
# Usage: raise-fix-pr.sh <rule-id> <title> <body-file>
set -euo pipefail

rule="$1"; title="$2"; body_file="$3"
base="${GITHUB_BASE_REF:-main}"
branch="security/fix-${rule}"
owner="${GITHUB_REPOSITORY%%/*}"
auth=(-H "Authorization: Bearer ${GH_TOKEN}" -H "Accept: application/vnd.github+json")

if git diff --quiet; then
  echo "No changes for ${rule}; nothing to raise."; exit 0
fi

git config user.name  "security-bot"
git config user.email "security-bot@example.com"
git switch -C "$branch"
git commit -am "fix(security): ${title}"
git push --force-with-lease origin "$branch"

# One open PR per rule: if it exists, the push above already updated it.
existing=$(curl -fsS "${auth[@]}" \
  "${GITHUB_API_URL}/repos/${GITHUB_REPOSITORY}/pulls?state=open&head=${owner}:${branch}" \
  | jq 'length')
if [ "$existing" -gt 0 ]; then
  echo "PR for ${branch} already open; updated."; exit 0
fi

jq -n --arg t "$title" --rawfile b "$body_file" --arg h "$branch" --arg base "$base" \
  '{title:$t, body:$b, head:$h, base:$base, draft:true}' \
| curl -fsS "${auth[@]}" -X POST \
    "${GITHUB_API_URL}/repos/${GITHUB_REPOSITORY}/pulls" -d @- \
| jq -r '.html_url'
```

Three design choices are worth explaining:

- **One branch per rule, not per finding.** Fifty instances of the same weak-hash call become one PR that a
  reviewer reads once. Re-running the job updates that PR instead of adding a duplicate.
- **Draft by default.** The bot proposes and a person decides. Automated fixes should start as drafts until the
  team trusts that rule.
- **The fix is a separate step.** The script only does the Git and GitHub part. The transform (`sed`, a
  codemod, a linter's `--fix`) runs before it, so each rule's logic stays small and testable.

The `pulls` endpoint and the `head=owner:branch` filter are documented in the
[GHES REST reference](https://docs.github.com/en/enterprise-server@latest/rest/pulls/pulls#create-a-pull-request).

If the tool produces SARIF but has no action, upload it directly with
`POST /repos/{owner}/{repo}/code-scanning/sarifs`, sending the file gzipped and base64-encoded:

```bash
sarif=$(gzip -c results.sarif | base64 -w0)
jq -n --arg s "$sarif" --arg sha "$GITHUB_SHA" --arg ref "$GITHUB_REF" \
  '{commit_sha:$sha, ref:$ref, sarif:$s, tool_name:"my-sast"}' \
| curl -fsS -H "Authorization: Bearer ${GH_TOKEN}" -X POST \
    "${GITHUB_API_URL}/repos/${GITHUB_REPOSITORY}/code-scanning/sarifs" -d @-
```

The API accepts it with a `202` and processes it asynchronously. Poll `/code-scanning/sarifs/{id}` for
`processing_status`. Limits apply: 20 runs per file, and only the top 5,000 results per run by severity are kept
([docs](https://docs.github.com/en/enterprise-server@latest/rest/code-scanning/code-scanning#upload-an-analysis-as-sarif-data)).
If two tools upload for the same commit, give each a distinct category (`runAutomationDetails.id`), or the second
upload replaces the first.

## Guard rails I would not skip

- **Branch protection on `main`:** required reviews and required status checks. A bot PR goes through the same
  checks as a human PR. The SentinelOne article lists this too.
- **Severity filter first, widen later.** Start with `CRITICAL,HIGH` and a small `maxCount`. Add `MEDIUM` once the
  team merges bot PRs quickly.
- **`CODEOWNERS` on lock files and build files** so dependency PRs reach someone who understands the upgrade.
- **Time-box the queue.** A fix PR open for a month is worse than none, because it gives the impression the issue is
  handled. Report on the age of open bot PRs as well as the alert count.

## Takeaways

- On GHES, check four things before designing the flow: self-hosted runners, access to actions (GitHub Connect or
  `actions-sync`), a Code Security licence for code scanning, and whether Dependabot can reach github.com.
- Black Duck **SCA** can raise fix PRs for vulnerable direct dependencies; **Coverity** (SAST) comments on PRs.
  Expect automated PRs for dependencies and reviewer-led fixes for code.
- Send every scanner's results to code scanning as SARIF so there is one place to triage.
- Use a GitHub App token, not `GITHUB_TOKEN`, so fix PRs run CI.
- For your own rules, a 30-line script plus one branch per rule gives deduplicated, draft fix PRs on any GHES
  instance.

## References

- [Upload a SARIF file (GHES 3.22)](https://docs.github.com/en/enterprise-server@latest/code-security/how-tos/find-and-fix-code-vulnerabilities/integrate-with-existing-tools/upload-sarif-file): GitHub Docs, admin prerequisite, `upload-sarif`, categories and replacement behaviour
- [REST API: code scanning, upload an analysis as SARIF data](https://docs.github.com/en/enterprise-server@latest/rest/code-scanning/code-scanning#upload-an-analysis-as-sarif-data): GitHub Docs, endpoint, encoding, status polling and limits
- [REST API: pulls, create a pull request](https://docs.github.com/en/enterprise-server@latest/rest/pulls/pulls#create-a-pull-request): GitHub Docs, PR endpoint and parameters
- [About using actions in your enterprise](https://docs.github.com/en/enterprise-server@latest/admin/managing-github-actions-for-your-enterprise/managing-access-to-actions-from-githubcom/about-using-actions-in-your-enterprise): GitHub Docs, self-hosted runners, GitHub Connect, `actions-sync`
- [Enabling Dependabot for your enterprise](https://docs.github.com/en/enterprise-server@latest/admin/configuration/configuring-github-connect/enabling-dependabot-for-your-enterprise): GitHub Docs, Dependabot requirements on GHES
- [About GitHub Advanced Security](https://docs.github.com/en/enterprise-server@latest/get-started/learning-about-github/about-github-advanced-security): GitHub Docs, Code Security and Secret Protection products
- [Triggering a workflow](https://docs.github.com/en/enterprise-server@latest/actions/how-tos/write-workflows/choose-when-workflows-run/trigger-a-workflow): GitHub Docs, `GITHUB_TOKEN` events do not start workflow runs
- [Managing GitHub Actions settings for a repository](https://docs.github.com/en/enterprise-server@latest/repositories/managing-your-repositorys-settings-and-features/enabling-features-for-your-repository/managing-github-actions-settings-for-a-repository): GitHub Docs, workflow permissions and the PR-creation setting
- [Variables reference](https://docs.github.com/en/enterprise-server@latest/actions/reference/workflows-and-actions/variables): GitHub Docs, `GITHUB_API_URL` on GHES
- [Using the Black Duck Security Scan Action with Black Duck SCA](https://docs.blackduck.com/r/bridge/latest/bridge-cli-guide/using-the-black-duck-security-scan-action-with-black-duck-sca.html): Black Duck, fix PR, PR comment and SARIF inputs; GHES verification note
- [Quickstart: Black Duck Security Scan Action with Black Duck SCA](https://docs.blackduck.com/r/bridge/latest/bridge-cli-guide/quickstart-black-duck-security-scan-action-with-black-duck-sca.html): Black Duck, baseline workflow and token requirements
- [Using the Black Duck Security Scan Action with Coverity](https://docs.blackduck.com/r/bridge/latest/bridge-cli-guide/using-the-black-duck-security-scan-action-with-coverity.html): Black Duck, Coverity (SAST) inputs and PR comments
- [black-duck-security-scan](https://github.com/blackduck-inc/black-duck-security-scan): Black Duck on GitHub, the action's repository
- [GitHub Vulnerability Management](https://www.sentinelone.com/cybersecurity-101/cybersecurity/github-vulnerability-management/): SentinelOne, the starting reference for native features, best practices and gaps (vendor article)

Related on this site: [DAST]({{< relref "/posts/dast" >}}), the runtime counterpart to the static scanning here.
