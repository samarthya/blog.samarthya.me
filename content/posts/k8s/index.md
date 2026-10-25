---
title: "K8S"
date: "2020-08-17T07:56:44Z"
slug: "k8s"
categories: ["technical"]
tags: ["container", "k8s"]
aliases: ["/wps/2020/08/17/k8s/"]
wp_id: 925
---

## What is K8S?

To manage distributed containerised workloads, you use Kubernetes.

- It is resilient declarative configuration.
- It is open source platform.
- It allows you to bundle and run your application.

![From the official Kubernetes documentation.](https://d33wubrfki0l68.cloudfront.net/26a177ede4d7b032362289c6fccd448fc4a91174/eb693/images/docs/container_evolution.svg "From the official Kubernetes documentation.")

## Kubernetes objects

K8S objects are the persistent entities in the K8S system and thee entities are used to represent the state of the cluster.

In general, most of the objects have

- spec - Defines the desired state.
- status - Describes the current state.

```text
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx
spec:
.....
```

## References

- https://github.com/kubernetes/community/blob/master/contributors/devel/sig-architecture/api-conventions.md#types-kinds
