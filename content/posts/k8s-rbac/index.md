---
title: "K8S RBAC"
date: "2021-12-13T13:03:56Z"
slug: "k8s-rbac"
categories: ["kubernetes", "technical"]
tags: ["k8s", "rbac"]
aliases: ["/wps/2021/12/13/k8s-rbac/"]
wp_id: 1841
---

## What?

- Role Based Access Control(s) is a way of regulating access to entities like storage, network etc.
- RBAC authorization uses `rbac.authorization.k8s.io` API group.

## API Objects

There are 4 kind of kubernetes object

{{< lead >}}
Permissions are always additive.
{{< /lead >}}

### Role

Role allows you to set permissions within a particular namespace.

{{< lead >}}
When you define a Role you have must specify the namespace it belongs to.
{{< /lead >}}

### ClusterRole

A ClusterRole can be used to grant the same permissions as a Role. It a non name-space bound resource & has several uses

1. Define permissions on namespaced resources and be granted within individual namespace(s)
2. Define permissions on namespaced resources and be granted across all namespaces
3. Define permissions on cluster-scoped resources

### RoleBinding

A role binding grants the permissions defined in a `role` to a user or set of users. It uses a list of *subjects* (users, groups, or service accounts), and a reference to the role being granted.

A RoleBinding grants permissions within a **specific namespace** whereas a ClusterRoleBinding grants that access cluster-wide.

{{< lead >}}
The name of a RoleBinding or ClusterRoleBinding object must be a valid [path segment name](https://kubernetes.io/docs/concepts/overview/working-with-objects/names#path-segment-names).
— Official API documentation
{{< /lead >}}

### ClusterRoleBinding

To grant permissions across a whole cluster, you can use a ClusterRoleBinding.

After you create a binding, you cannot change the Role or ClusterRole that it refers to. If you try to change a binding's `roleRef`, you get a validation error. If you do want to change the `roleRef` for a binding, you need to remove the binding object and create a replacement.
