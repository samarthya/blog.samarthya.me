---
title: "IaC: Infrastructure as Code"
date: "2022-02-08T12:00:00Z"
slug: "iac-infrastructure-as-code"
description: "IaC tools like Terraform allows one to manage infrastructure with configuration files rather than through a graphical user interface."
categories: ["iac", "technical"]
tags: ["iac", "terraform"]
aliases: ["/wps/2022/02/08/iac-infrastructure-as-code/"]
recovered: "Internet Archive snapshot 2026-05-18"
---

IaC tools like `Terraform` allows one to manage infrastructure with configuration files rather than through a graphical user interface.

![From the official website of Terraform](https://learn.hashicorp.com/img/terraform/terraform-iac.png "From the official website of Terraform")

## Installation

I will cover steps to install on MAC OS using brew.

### Install Tap

{{< lead >}}
Learn about taps from [here](https://docs.brew.sh/Taps).
— brew official documentation
{{< /lead >}}

```text
brew tap hashicorp/tap
```

validate the tap is installed

```text
> brew tap
hashicorp/tap
```

### Install Terraform

```text
brew install hashicorp/tap/terraform && brew update
```

### Validate installation

```text
terraform -h
Usage: terraform [global options] <subcommand> [args]

The available commands for execution are listed below.
The primary workflow commands are given first, followed by
less common or more advanced commands.

Main commands:
  init          Prepare your working directory for other commands
  validate      Check whether the configuration is valid
  plan          Show changes required by the current configuration
  apply         Create or update infrastructure
  destroy       Destroy previously-created infrastructure

All other commands:
  console       Try Terraform expressions at an interactive command prompt
  fmt           Reformat your configuration in the standard style
  force-unlock  Release a stuck lock on the current workspace
  get           Install or upgrade remote Terraform modules
  graph         Generate a Graphviz graph of the steps in an operation
  import        Associate existing infrastructure with a Terraform resource
  login         Obtain and save credentials for a remote host
  logout        Remove locally-stored credentials for a remote host
  output        Show output values from your root module
  providers     Show the providers required for this configuration
  refresh       Update the state to match remote systems
  show          Show the current state or a saved plan
  state         Advanced state management
  taint         Mark a resource instance as not fully functional
  test          Experimental support for module integration testing
  untaint       Remove the 'tainted' state from a resource instance
  version       Show the current Terraform version
  workspace     Workspace management

Global options (use these before the subcommand, if any):
  -chdir=DIR    Switch to a different working directory before executing the
                given subcommand.
  -help         Show this help output, or the help for
```
