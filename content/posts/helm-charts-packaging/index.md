---
title: "Helm Charts: Packaging"
date: "2020-09-02T09:12:45Z"
slug: "helm-charts-packaging"
categories: ["technical"]
tags: ["helm", "k8s"]
aliases: ["/wps/2020/09/02/helm-charts-packaging/"]
wp_id: 1017
---

Every software cycle includes packaging; which essentially describes how the software written is packaged and shared.

For the software built for Containers Helm is a popular choice of packaging the scripts.

```text
root@master> helm version
```

```text
version.BuildInfo{Version:"v3.2.4", GitCommit:"0ad800ef43d3b826f31a5ad8dfbb4fe05d143688", GitTreeState:"clean", GoVersion:"go1.13.12"}
```

{{< lead >}}
Helm is a tool for managing Kubernetes packages called *charts*.
{{< /lead >}}

Helm enables management of applications built for Kubernetes. It helps you define, install, and upgrade even the most complex Kubernetes application.

## Helm

It allows you to

- Create new charts from scratch
- Package charts into **chart archive** (tgz) files
- Interact with chart repositories where charts are stored
- Install and uninstall charts into an existing Kubernetes cluster
- Manage the release cycle of charts that have been installed with Helm

It has two components

1. Client executable
   - Command line client for end users.
2. Helm Library
   - It provides the logic for executing all Helm operations and interfaces with the Kubernetes API server.
   - The library uses the Kubernetes client library to communicate with Kubernetes.

{{< lead >}}
The Helm client and library is written in the Go programming language.
{{< /lead >}}

Three basic concepts for, Helm (from [helm.sh](https://helm.sh/docs/topics/architecture/))

1. The *chart* is a bundle of information necessary to create an instance of a Kubernetes application.
2. The *config* contains configuration information that can be merged into a packaged chart to create a releasable object.
3. A *release* is a running instance of a *chart*, combined with a specific *config*.

## Charts

{{< lead >}}
A [chart](https://helm.sh/docs/topics/charts/#the-chart-file-structure) is a collection of files that describe a related set of Kubernetes resources.
{{< /lead >}}

The chart name is derived from the directory name. E.g. A chart describing WordPress would be stored in a `wordpress/` directory.

### [Chart.yml](https://helm.sh/docs/topics/charts/#the-chartyaml-file)

```text
apiVersion: v1
name: opendistro-es
# Chart version
version: 1.9.0
description: 'Open Distro for Elasticsearch'
engine: gotpl
kubeVersion: ^1.10.0-0
maintainers:
- email: derek.heldt-werle@viasat.com
  name: Derek Heldt-Werle
- email: kalvin.chau@viasat.com
  name: Kalvin Chau
sources:
- https://pages.git.viasat.com/ATG/charts
# Open Distro for Elasticsearch version
appVersion: 1.9.0
```

When the chart above is used the package `opendistro-es-1.9.0.tgz` will be generated.

## References

- https://helm.sh/docs/topics/charts/#the-chart-file-structure
- https://helm.sh/docs/topics/charts/#the-chartyaml-file
