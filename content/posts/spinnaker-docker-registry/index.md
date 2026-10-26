---
title: "Spinnaker: docker-registry"
date: "2022-02-04T12:00:00Z"
slug: "spinnaker-docker-registry"
description: "You will need a valid docker registry before you add any trigger in the pipeline in Spinnaker"
categories: ["docker", "technical"]
tags: ["docker", "linux", "provider", "spinnaker"]
aliases: ["/wps/2022/02/04/spinnaker-docker-registry/"]
recovered: "Internet Archive snapshot 2026-05-18"
---

You will need a valid docker registry before you add any trigger in the pipeline in `Spinnaker`

{{< lead >}}
[Official documentation](https://spinnaker.io/docs/setup/install/providers/docker-registry/) is a good resource to seek more clarifications
— Spinnaker
{{< /lead >}}

In my case I have already added an account my-docker-registry as under (The final result after you successfully configure Docker.

```text
bash-5.0$ hal config provider docker-registry account list
+ Get current deployment
  Success
+ Get the dockerRegistry provider
  Success
+ Accounts for dockerRegistry:
  - my-docker-registry
```

To get the details I used for adding using the **hal** to get the account

```text
bash-5.0$ hal config provider docker-registry account get my-docker-registry 
+ Get current deployment
  Success
+ Get my-docker-registry account
  Success
+ Account my-docker-registry: 
DockerRegistryAccount(address=https://index.docker.io, username=samarthya, password=-------------------, passwordCommand=null, email=owner@example.com, cacheIntervalSeconds=30, clientTimeoutMillis=60000, cacheThreads=1, paginateSize=100, sortTagsByDate=false, trackDigests=false, insecureRegistry=false, repositories=[samarthya/spinnaker], repositoriesRegex=null, passwordFile=null, dockerconfigFile=null)
+ MY-DOCKER-REGISTRY

DockerRegistryAccount(address=https://index.docker.io, username=samarthya,
password=-------------------, passwordCommand=null,
email=owner@example.com, cacheIntervalSeconds=30, clientTimeoutMillis=60000,
cacheThreads=1, paginateSize=100, sortTagsByDate=false, trackDigests=false,
insecureRegistry=false, repositories=[samarthya/spinnaker],
repositoriesRegex=null, passwordFile=null, dockerconfigFile=null)
```

## How to add?

Seek help at the console using the `-h` flag

```text
bash-5.0$ hal config provider docker-registry -h
DOCKER-REGISTRY

  Manage and view Spinnaker configuration for the dockerRegistry provider

USAGE

  hal config provider docker-registry [parameters] [subcommands]

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

  --deployment
    If supplied, use this Halyard deployment. This will _not_ create a new
    deployment.

  --no-validate=false
    Skip validation.

SUBCOMMANDS

  account
    Manage and view Spinnaker configuration for the dockerRegistry provider's
    account

  disable
    Set the dockerRegistry provider as disabled

  enable
    Set the dockerRegistry provider as enabled
```

## Adding account

The basic configuration options for docker-registry are add, delete, get (look below)

```text
bash-5.0$ hal config provider docker-registry account -h
ACCOUNT

  Manage and view Spinnaker configuration for the dockerRegistry provider's
  account

USAGE

  hal config provider docker-registry account [parameters] [subcommands]

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

SUBCOMMANDS

  add
    Add an account to the dockerRegistry provider.

  delete
    Delete a specific dockerRegistry account by name.

  edit
    Edit an account in the dockerRegistry provider.

  get
    Get the specified account details for the dockerRegistry provider.

  list
    List the account names for the dockerRegistry provider.
```

## `hal config provider docker-registry account add`

{{< lead >}}
The DockerHub registry address is `index.docker.io`
— ADDRESS=index.docker.io
{{< /lead >}}

- Options 1 name of the account `my-docker-registry`
- Option 2 `--email`=<a valid email>
- Option 3 `--username`
- Option 4 `--address=index.docker.io`
- Option 4 `--password`

```text
PARAMETERS

  ACCOUNT
    The name of the account to operate on.

  --address=gcr.io (required)
    The registry address you want to pull and deploy images from. For example:
    
    index.docker.io     - DockerHub
    quay.io             - Quay
    gcr.io              - Google Container Registry (GCR)
    [us|eu|asia].gcr.io - Regional GCR
    localhost           - Locally deployed registry

  --cache-interval-seconds=30
    How many seconds elapse between polling your docker registry. Certain registries
    are sensitive to over-polling, and larger intervals (e.g. 10 minutes = 600
    seconds) are desirable if you're seeing rate limiting.

  --cache-threads=1
    How many threads to cache all provided repos on. Really only useful if you have
    a ton of repos.

  --client-timeout-millis=60000
    Timeout time in milliseconds for this repository.

  --deployment
    If supplied, use this Halyard deployment. This will _not_ create a new
    deployment.

  --email=fake.email@spinnaker.io
    Your docker registry email (often this only needs to be well-formed, rather than
    be a real address)

  --environment
    The environment name for the account. Many accounts can share the same
    environment (e.g. dev, test, prod)

  --insecure-registry=false
    Treat the docker registry as insecure (don't validate the ssl cert).

  --no-validate=false
    Skip validation.

  --paginate-size=100
    Paginate size for the docker repository _catalog endpoint.

  --password (sensitive data - user will be prompted)
    Your docker registry password

  --password-command
    Command to retrieve docker token/password, commands must be available in
    environment

  --password-file
    The path to a file containing your docker password in plaintext (not a
    docker/config.json file)

  --read-permissions=[]
    A user must have at least one of these roles in order to view this account's
    cloud resources.

  --repositories=[]
    An optional list of repositories to cache images from. If not provided,
    Spinnaker will attempt to read accessible repositories from the registries
    _catalog endpoint

  --repositories-regex
    Allows to specify a Regular Expression to filter the repositories.

  --required-group-membership=[]
    A user must be a member of at least one specified group in order to make changes
    to this account's cloud resources.

  --sort-tags-by-date=false
    Sort tags by creation date. Not recommended for use with large registries;
    sorting performance scales poorly due to limitations of the Docker V2 API.

  --track-digests=false
    Track digest changes. This is not recommended as it consumes a high QPM, and
    most registries are flaky.

  --username
    Your docker registry username

  --write-permissions=[]
    A user must have at least one of these roles in order to make changes to this
    account's cloud resources.
```
