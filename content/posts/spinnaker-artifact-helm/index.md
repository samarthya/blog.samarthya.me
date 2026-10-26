---
title: "Spinnaker: Artifact Helm"
date: "2022-02-05T12:00:00Z"
slug: "spinnaker-artifact-helm"
description: "In this blog let’s try add a helm account and enable for use in the pipelines"
categories: ["technical"]
tags: ["artifactory", "helm", "spinnaker"]
aliases: ["/wps/2022/02/05/spinnaker-artifact-helm/"]
recovered: "Internet Archive snapshot 2026-03-13"
---

In this blog let’s try add a helm account and enable for use in the pipelines

```text
bash-5.0$ hal config artifact helm account get dev-helm-ac
+ Get current deployment
  Success
+ Get dev-helm-ac artifact account
  Success
+ Artifact account dev-helm-ac: 
HelmArtifactAccount(name=dev-helm-ac, repository=https://helm-dev-local.artifactory.net/artifactory/helm-dev-local, username=myaccount, password=samplepassword, usernamePasswordFile=/home/spinnaker/.hal/helm_password)
```

The steps I followed are explained in detail [here](https://spinnaker.io/docs/setup/other_config/artifacts/helm/).

## Enable

```text
hal config artifact helm enable
```

## Adding account for helm

### Help

```text
bash-5.0$ hal config artifact helm account add -h
ADD

  Add an artifact account to the helm artifact provider.

USAGE

  hal config artifact helm account add [parameters]

GLOBAL PARAMETERS

  --daemon-endpoint
    If supplied, connect to the daemon at this address.

  --options
    Get options for the specified field name.

  -a, --alpha
    Enable alpha halyard features.

  -c, --color
    Enable terminal color output.

  -d, --debug
    Show detailed network traffic with halyard daemon.

  -h, --help=false
    Display help text about this command.

  -l, --log
    Set the log level of the CLI.

  -o, --output
    Format the CLIs output.

  -q, --quiet
    Show no task information or messages. When set, ANSI formatting will be
    disabled, and all prompts will be accepted.

PARAMETERS

  ACCOUNT
    The name of the account to operate on.

  --deployment
    If supplied, use this Halyard deployment. This will _not_ create a new
    deployment.

  --no-validate=false
    Skip validation.

  --password (sensitive data - user will be prompted)
    Helm chart repository basic auth password

  --repository
    Helm chart repository

  --username
    Helm chart repository basic auth username

  --username-password-file
    File containing "username:password" to use for helm chart repository basic
```

```text
helm config artifact helm account add dev-helm-ac \
--username <username> \
--repository <repository> \
--password
```

## Apply

```text
hal deploy apply
```

Check in the pipeline

*[image unavailable: Screenshot-2022-02-05-at-9.29.53-PM-1024x363.png]*
