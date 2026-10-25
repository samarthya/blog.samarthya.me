---
title: "Taint Nodes"
date: "2021-01-12T08:57:23Z"
slug: "taint-nodes"
categories: ["docker", "technical"]
tags: ["k8s", "taint"]
aliases: ["/wps/2021/01/12/taint-nodes/"]
wp_id: 1229
---

## Reference

- <https://kubernetes.io/docs/concepts/scheduling-eviction/taint-and-toleration/>
- <https://kubernetes.io/docs/concepts/scheduling-eviction/taint-and-toleration/#example-use-cases>

Before we understand the tainting we should know about the Node Affinity. It the by the virtue of Affinity that pods attracts nodes as a preference or as a basic requirement.

Tainting is the exact opposite - To repel a node from scheduling a pod.

```text
taint node ip-10-0-1-103 node-type=prod:NoSchedule
```

In the case above a taint is placed for Node identified by `ip-10-0-1-103`. The taint has a key value and effect as evident in above example.

- `node-type`
- `prod`
- `NoSchedule`

You can specify toleration for the pod as in the example below

```text
apiVersion: apps/v1
kind: Deployment
metadata:
  name: my-prod
spec:
  replicas: 1
  selector:
    matchLabels:
      app: my-prod
  template:
    metadata:
      labels:
        app: my-prod
    spec:
      containers:
      - args:
        - sleep
        - "3600"
        image: busybox
        name: main
      tolerations:
      - key: node-type
        operator: Equal
        value: prod
        effect: NoSchedule
```

The operator can be `exists` or `equal` for the mentioned example

### Environment

#### K GET NODES

```text
NAME            STATUS   ROLES    AGE   VERSION
ip-10-0-1-101   Ready    master   38m   v1.13.3
ip-10-0-1-102   Ready    <none>   38m   v1.13.3
ip-10-0-1-103   Ready    <none>   38m   v1.13.3
```
