---
title: "SCM for git clone"
date: "2021-12-08T09:55:42Z"
slug: "scm-for-git-clone"
categories: ["technical"]
tags: ["checkout", "git", "pat", "scm"]
aliases: ["/wps/2021/12/08/scm-for-git-clone/"]
wp_id: 1818
---

Having used SCM plugins for quite sometime, I thought - WHY I have never used them to clone a repository and while I employ the personal access token (NOW)- The weapon of choice, I have never tried it myself.

So in this blog, I will attempt to define the basic steps needed to do that.

## Assumptions

I am assuming basic knowledge of Maven and plugins, else drop by and ask questions will try to address when I can.

{{< lead >}}
Learn more about [Personal Access Token]({{< relref "/posts/personal-access-token" >}})
{{< /lead >}}

## General Mistake

### Using git@hostname for checkout.

```text
mvn scm:checkout -DcheckoutDirectory=./helm-chart2 -DconnectionUrl=scm:git:git@github.com:GRP/helm-chart.git
```

If you use this you will get an error like below

```text
[ERROR] Provider message:
[ERROR] The git-clone command failed.
[ERROR] Command output:
[ERROR] Cloning into 'helm-chart2'...
git@github.com: Permission denied (publickey).
fatal: Could not read from remote repository.

Please make sure you have the correct access rights
and the repository exists.
```

Though error is self explanatory but the issue is you are trying to use SSH to checkout and if you read the official documentaion about PAT

{{< lead >}}
Personal access tokens can only be used for HTTPS Git operations. If your repository uses an SSH remote URL, you will need to [switch the remote from SSH to HTTPS](https://docs.github.com/en/enterprise-server@3.1/github/getting-started-with-github/managing-remote-repositories/#switching-remote-urls-from-ssh-to-https).
— github.com
{{< /lead >}}

Many overlook these details and hence try looking everywhere for a quick solution. So, remember to read the documentation before you search elsewhere.

{{< lead >}}
Change to HTTPS instead of GIT
{{< /lead >}}

```text
mvn scm:checkout -DcheckoutDirectory=./helm-chart2 -DconnectionUrl=scm:git:https://github.com/GRP/helm-chart.git
```

Once you do this you will also need the creds to be used which I have configured in my `settings.xml` for server with id as the hostname `github.com`.

```text
<servers>
 <server>
      <id>github.com</id>
      <username>USERNAME</username>
      <password>YOUR PERSONAL ACCESS TOKEN</password>
    </server>
</servers>
```

Once you make the changes and issue the command you will eventually see the message below

```text
[INFO] Working directory: /Users/samarthya/sourcebox/github.com/helm-chart2
[INFO] ------------------------------------------------------------------------
[INFO] BUILD SUCCESS
[INFO] ------------------------------------------------------------------------
[INFO] Total time:  17.082 s
[INFO] Finished at: 2021-12-08T14:11:38+05:30
[INFO] ------------------------------------------------------------------------
```

The essential two steps `prepare` and `perform` for the release plugin can also be followed subsequently to validate artifact generation as covered in other blog [here]({{< relref "/posts/building-your-artifacts" >}}).

### mvn `release:prepare`

For my code base the sample output is as under

```text

samarthya@Admins-MacBook-Pro helmchart % mvn release:prepare
[INFO] Scanning for projects...
[INFO] 
[INFO] ------------------------< com.samarthya:restmon >------------------------
[INFO] Building Open data connector helm chart 21.4.0-SNAPSHOT
[INFO] --------------------------------[ helm ]--------------------------------
[INFO] 
[INFO] --- maven-release-plugin:3.0.0-M4:prepare (default-cli) @ restmon ---
[INFO] phase verify-release-configuration
[INFO] starting prepare goal, composed of 17 phases: check-poms, scm-check-modifications, check-dependency-snapshots, create-backup-poms, map-release-versions, input-variables, map-development-versions, rewrite-poms-for-release, generate-release-poms, run-preparation-goals, scm-commit-release, scm-tag, rewrite-poms-for-development, remove-release-poms, run-completion-goals, scm-commit-development, end-release
[INFO] [prepare] 1/17 check-poms
[INFO] [prepare] 2/17 scm-check-modifications
[INFO] Verifying that there are no local modifications...
[INFO]   ignoring changes on: **/pom.xml.releaseBackup, **/pom.xml.next, **/pom.xml.tag, **/pom.xml.branch, **/release.properties, **/pom.xml.backup
[INFO] Executing: /bin/sh -c cd /Users/samarthya/sourcebox/github.com/helmchart && git rev-parse --show-prefix
[INFO] Working directory: /Users/samarthya/sourcebox/github.com/helmchart
[INFO] Executing: /bin/sh -c cd /Users/samarthya/sourcebox/github.com/helmchart && git status --porcelain .
[INFO] Working directory: /Users/samarthya/sourcebox/github.com/helmchart
[INFO] [prepare] 3/17 check-dependency-snapshots
[INFO] Checking dependencies and plugins for snapshots ...
[INFO] [prepare] 4/17 create-backup-poms
[INFO] [prepare] 5/17 map-release-versions
[INFO] [prepare] 6/17 input-variables
[INFO] [prepare] 7/17 map-development-versions
[INFO] [prepare] 8/17 rewrite-poms-for-release
[INFO] Transforming 'My connector helm chart'...
[INFO] [prepare] 9/17 generate-release-poms
[INFO] Not generating release POMs
[INFO] [prepare] 10/17 run-preparation-goals
[INFO] Executing goals 'clean verify'...
[INFO] [INFO] Scanning for projects...
[INFO] [INFO] 
[INFO] [INFO] ------------------------< com.samarthya:mychart >------------------------
[INFO] [INFO] Building Open data connector helm chart 21.4.0
[INFO] [INFO] --------------------------------[ helm ]--------------------------------
[INFO] [INFO] 
[INFO] [INFO] --- maven-clean-plugin:2.5:clean (default-clean) @ restmon ---
[INFO] [INFO] 
[INFO] [INFO] --- helm-maven-plugin:5.9:init (default-init) @ restmon ---
[INFO] [INFO] Initializing Helm...
[INFO] [INFO] Creating output directory...
[INFO] [INFO] Using local HELM binary [/usr/local/bin/helm]
[INFO] [INFO] 
[INFO] [INFO] --- helm-maven-plugin:5.9:lint (default-lint) @ restmon ---
[INFO] [INFO] 
[INFO] 
[INFO] Testing chart /Users/samarthya/sourcebox/github.com/helmchart/src...
[INFO] [INFO] ==> Linting /Users/samarthya/sourcebox/github.com/helmchart/src
[INFO] [INFO] [INFO] Chart.yaml: icon is recommended
[INFO] [INFO] 
[INFO] [INFO] 1 chart(s) linted, 0 chart(s) failed
[INFO] [INFO] 
[INFO] [INFO] --- helm-maven-plugin:5.9:package (default-package) @ restmon ---
[INFO] [INFO] Packaging chart /Users/samarthya/sourcebox/github.com/helmchart/src...
[INFO] [INFO] Setting chart version to 21.4.0
[INFO] [INFO] Setting App version to 21.4.0
[INFO] [INFO] Successfully packaged chart and saved it to: /Users/samarthya/sourcebox/github.com/helmchart/target/restmon-21.4.0.tgz
[INFO] [INFO] ------------------------------------------------------------------------
[INFO] [INFO] BUILD SUCCESS
[INFO] [INFO] ------------------------------------------------------------------------
[INFO] [INFO] Total time:  0.683 s
[INFO] [INFO] Finished at: 2021-12-08T15:55:46+05:30
[INFO] [INFO] ------------------------------------------------------------------------
[INFO] [prepare] 11/17 scm-commit-release
[INFO] Checking in modified POMs...
[INFO] Executing: /bin/sh -c cd /Users/samarthya/sourcebox/github.com/helmchart && git add -- pom.xml
[INFO] Working directory: /Users/samarthya/sourcebox/github.com/helmchart
[INFO] Executing: /bin/sh -c cd /Users/samarthya/sourcebox/github.com/helmchart && git rev-parse --show-prefix
[INFO] Working directory: /Users/samarthya/sourcebox/github.com/helmchart
[INFO] Executing: /bin/sh -c cd /Users/samarthya/sourcebox/github.com/helmchart && git status --porcelain .
[INFO] Working directory: /Users/samarthya/sourcebox/github.com/helmchart
[INFO] Executing: /bin/sh -c cd /Users/samarthya/sourcebox/github.com/helmchart && git commit --verbose -F /var/folders/n5/25dlb6295m9_7nnslmz4wdmc0000gp/T/maven-scm-2136851052.commit
[INFO] Working directory: /Users/samarthya/sourcebox/github.com/helmchart
[INFO] Executing: /bin/sh -c cd /Users/samarthya/sourcebox/github.com/helmchart && git symbolic-ref HEAD
[INFO] Working directory: /Users/samarthya/sourcebox/github.com/helmchart
[INFO] Executing: /bin/sh -c cd /Users/samarthya/sourcebox/github.com/helmchart && git push https://samarthya:********@github.com/GRP/helmchart.git refs/heads/integration:refs/heads/integration
[INFO] Working directory: /Users/samarthya/sourcebox/github.com/helmchart
[INFO] [prepare] 12/17 scm-tag
[INFO] Tagging release with the label 21.4.0...
[INFO] Executing: /bin/sh -c cd /Users/samarthya/sourcebox/github.com/helmchart && git tag -F /var/folders/n5/25dlb6295m9_7nnslmz4wdmc0000gp/T/maven-scm-2144724858.commit 21.4.0
[INFO] Working directory: /Users/samarthya/sourcebox/github.com/helmchart
[INFO] Executing: /bin/sh -c cd /Users/samarthya/sourcebox/github.com/helmchart && git push https://samarthya:********@github.com/GRP/helmchart.git refs/tags/21.4.0
[INFO] Working directory: /Users/samarthya/sourcebox/github.com/helmchart
[INFO] Executing: /bin/sh -c cd /Users/samarthya/sourcebox/github.com/helmchart && git ls-files
[INFO] Working directory: /Users/samarthya/sourcebox/github.com/helmchart
[INFO] [prepare] 13/17 rewrite-poms-for-development
[INFO] Transforming 'My connector helm chart'...
[INFO] [prepare] 14/17 remove-release-poms
[INFO] Not removing release POMs
[INFO] [prepare] 15/17 run-completion-goals
[INFO] [prepare] 16/17 scm-commit-development
[INFO] Checking in modified POMs...
[INFO] Executing: /bin/sh -c cd /Users/samarthya/sourcebox/github.com/helmchart && git add -- pom.xml
[INFO] Working directory: /Users/samarthya/sourcebox/github.com/helmchart
[INFO] Executing: /bin/sh -c cd /Users/samarthya/sourcebox/github.com/helmchart && git rev-parse --show-prefix
[INFO] Working directory: /Users/samarthya/sourcebox/github.com/helmchart
[INFO] Executing: /bin/sh -c cd /Users/samarthya/sourcebox/github.com/helmchart && git status --porcelain .
[INFO] Working directory: /Users/samarthya/sourcebox/github.com/helmchart
[INFO] Executing: /bin/sh -c cd /Users/samarthya/sourcebox/github.com/helmchart && git commit --verbose -F /var/folders/n5/25dlb6295m9_7nnslmz4wdmc0000gp/T/maven-scm-663764717.commit
[INFO] Working directory: /Users/samarthya/sourcebox/github.com/helmchart
[INFO] Executing: /bin/sh -c cd /Users/samarthya/sourcebox/github.com/helmchart && git symbolic-ref HEAD
[INFO] Working directory: /Users/samarthya/sourcebox/github.com/helmchart
[INFO] Executing: /bin/sh -c cd /Users/samarthya/sourcebox/github.com/helmchart && git push https://samarthya:********@github.com/GRP/helmchart.git refs/heads/integration:refs/heads/integration
[INFO] Working directory: /Users/samarthya/sourcebox/github.com/helmchart
[INFO] [prepare] 17/17 end-release
[INFO] Release preparation complete.
[INFO] ------------------------------------------------------------------------
[INFO] BUILD SUCCESS
[INFO] ------------------------------------------------------------------------
[INFO] Total time:  21.736 s
[INFO] Finished at: 2021-12-08T15:56:05+05:30
[INFO] ------------------------------------------------------------------------
```

### mvn `release:perform`

```text
samarthya@Admins-MacBook-Pro helmchart % mvn release:perform
[INFO] Scanning for projects...
[INFO] 
[INFO] ------------------------< com.samarthya:mychart >------------------------
[INFO] Building My connector helm chart 21.4.1-SNAPSHOT
[INFO] --------------------------------[ helm ]--------------------------------
[INFO] 
[INFO] --- maven-release-plugin:3.0.0-M4:perform (default-cli) @ mychart ---
[INFO] phase verify-release-configuration
[INFO] starting perform goal, composed of 3 phases: verify-completed-prepare-phases, checkout-project-from-scm, run-perform-goals
[INFO] [perform] 1/3 verify-completed-prepare-phases
[INFO] [perform] 2/3 checkout-project-from-scm
[INFO] Checking out the project to perform the release ...
[INFO] Executing: /bin/sh -c cd /Users/samarthya/sourcebox/github.com/helmchart/target && git clone --depth 1 --branch 21.4.0 https://samarthya:********@github.com/ESD/helmchart.git checkout
[INFO] Working directory: /Users/samarthya/sourcebox/github.com/helmchart/target
[INFO] Executing: /bin/sh -c cd /var/folders/n5/25dlb6295m9_7nnslmz4wdmc0000gp/T/ && git ls-remote https://samarthya:********@github.com/ESD/helmchart.git
[INFO] Working directory: /var/folders/n5/25dlb6295m9_7nnslmz4wdmc0000gp/T
[INFO] Executing: /bin/sh -c cd /Users/samarthya/sourcebox/github.com/helmchart/target/checkout && git fetch https://samarthya:********@github.com/ESD/helmchart.git
[INFO] Working directory: /Users/samarthya/sourcebox/github.com/helmchart/target/checkout
[INFO] Executing: /bin/sh -c cd /Users/samarthya/sourcebox/github.com/helmchart/target/checkout && git checkout 21.4.0
[INFO] Working directory: /Users/samarthya/sourcebox/github.com/helmchart/target/checkout
[INFO] Executing: /bin/sh -c cd /Users/samarthya/sourcebox/github.com/helmchart/target/checkout && git ls-files
[INFO] Working directory: /Users/samarthya/sourcebox/github.com/helmchart/target/checkout
[INFO] [perform] 3/3 run-perform-goals
[INFO] Invoking perform goals in directory /Users/samarthya/sourcebox/github.com/helmchart/target/checkout
[INFO] Executing goals 'deploy'...
[INFO] pomFileName is already set, ignoring the -f argument
[INFO] [INFO] Scanning for projects...
[INFO] [INFO] 
[INFO] [INFO] ------------------------< com.samarthya:mychart >------------------------
[INFO] [INFO] Building Open data connector helm chart 21.4.0
[INFO] [INFO] --------------------------------[ helm ]--------------------------------
[INFO] [INFO] 
[INFO] [INFO] --- helm-maven-plugin:5.9:init (default-init) @ mychart ---
[INFO] [INFO] Initializing Helm...
[INFO] [INFO] Creating output directory...
[INFO] [INFO] Using local HELM binary [/usr/local/bin/helm]
[INFO] [INFO] 
[INFO] [INFO] --- helm-maven-plugin:5.9:lint (default-lint) @ mychart ---
[INFO] [INFO] 
[INFO] 
[INFO] Testing chart /Users/samarthya/sourcebox/github.com/helmchart/target/checkout/src...
[INFO] [INFO] ==> Linting /Users/samarthya/sourcebox/github.com/helmchart/target/checkout/src
[INFO] [INFO] [INFO] Chart.yaml: icon is recommended
[INFO] [INFO] 
[INFO] [INFO] 1 chart(s) linted, 0 chart(s) failed
[INFO] [INFO] 
[INFO] [INFO] --- helm-maven-plugin:5.9:package (default-package) @ mychart ---
[INFO] [INFO] Packaging chart /Users/samarthya/sourcebox/github.com/helmchart/target/checkout/src...
[INFO] [INFO] Setting chart version to 21.4.0
[INFO] [INFO] Setting App version to 21.4.0
[INFO] [INFO] Successfully packaged chart and saved it to: /Users/samarthya/sourcebox/github.com/helmchart/target/checkout/target/mychart-21.4.0.tgz
[INFO] [INFO] 
[INFO] [INFO] --- helm-maven-plugin:5.9:package (install) @ mychart ---
[INFO] [INFO] Packaging chart /Users/samarthya/sourcebox/github.com/helmchart/target/checkout/src...
[INFO] [INFO] Setting chart version to 21.4.0
[INFO] [INFO] Setting App version to 21.4.0
[INFO] [INFO] Successfully packaged chart and saved it to: /Users/samarthya/sourcebox/github.com/helmchart/target/checkout/target/mychart-21.4.0.tgz
[INFO] [INFO] 
[INFO] [INFO] --- helm-maven-plugin:5.9:upload (default-upload) @ mychart ---
[INFO] [INFO] Uploading to https://helm-release-local.artifactory.samarthya.net:443/artifactory/helm-release-local/odc/21.4.0/mychart
[INFO] 
[INFO] [INFO] Uploading /Users/samarthya/sourcebox/github.com/helmchart/target/checkout/target/mychart-21.4.0.tgz...
[INFO] [INFO] 201 - {
[INFO]   "repo" : "helm-release-local",
[INFO]   "path" : "/odc/21.4.0/mychart/mychart-21.4.0.tgz",
[INFO]   "created" : "2021-12-08T02:26:34.414-08:00",
[INFO]   "createdBy" : "samarthya",
[INFO]   "downloadUri" : "https://helm-release-local.artifactory.samarthya.net:443/artifactory/helm-release-local/odc/21.4.0/mychart/mychart-21.4.0.tgz",
[INFO]   "mimeType" : "application/x-gzip",
[INFO]   "size" : "13998",
[INFO]   "checksums" : {
[INFO]     "sha1" : "455a8badc378b210edf4fd2c6e7331cd9c30fc09",
[INFO]     "md5" : "baa150bcb8c0c2046e4c1ae3b2839a27",
[INFO]     "sha256" : "16fabb165fb7554b5265d9cf6b1954b487e3195afb3c872eef764b232d22bdc2"
[INFO]   },
[INFO]   "originalChecksums" : {
[INFO]     "sha256" : "16fabb165fb7554b5265d9cf6b1954b487e3195afb3c872eef764b232d22bdc2"
[INFO]   },
[INFO]   "uri" : "https://helm-release-local.artifactory.samarthya.net:443/artifactory/helm-release-local/odc/21.4.0/mychart/mychart-21.4.0.tgz"
[INFO] }
[INFO] [INFO] ------------------------------------------------------------------------
[INFO] [INFO] BUILD SUCCESS
[INFO] [INFO] ------------------------------------------------------------------------
[INFO] [INFO] Total time:  5.531 s
[INFO] [INFO] Finished at: 2021-12-08T15:56:34+05:30
[INFO] [INFO] ------------------------------------------------------------------------
[INFO] phase cleanup
[INFO] Cleaning up after release...
[INFO] ------------------------------------------------------------------------
[INFO] BUILD SUCCESS
[INFO] ------------------------------------------------------------------------
[INFO] Total time:  22.591 s
[INFO] Finished at: 2021-12-08T15:56:34+05:30
[INFO] ------------------------------------------------------------------------
```
