---
title: "ServiceAccount"
date: "2022-02-16T12:00:00Z"
slug: "serviceaccount"
description: "If you have seen errors like these when deploying using a serviceAccount"
categories: ["kubernetes", "technical"]
tags: ["docker", "kubernetes", "rbac", "serviceaccount"]
aliases: ["/wps/2022/02/16/serviceaccount/"]
recovered: "Internet Archive snapshot 2026-03-13"
---

If you have seen errors like these when deploying using a `serviceAccount`

```text
Error: INSTALLATION FAILED: rendered manifests contain a resource that already exists. Unable to continue with install: could not get information about the resource ConfigMap "spinnaker-hellow-pipline" in namespace "spinnaker": configmaps "spinnaker-hellow-pipline" is forbidden: User "system:serviceaccount:jenkins:default" cannot get resource "configmaps" in API group "" in the namespace "spinnaker"
```

## What?

- A service account provides an identity for processes that run in a Pod.
- Every namespace has a default `service account`
- When you create a pod, if you do not specify a service account, it is automatically assigned the `default` service account in the same namespace.
- To use a non-default service account, set the `spec.serviceAccountName` field of a pod to the name of the service account you wish to use.
- The service account has to exist at the time the pod is created, or it will be rejected.
- The service account of an already created pod cannot be updated

{{< lead >}}
Default RBAC policies grant scoped permissions to control-plane components, `nodes`, and `controllers`, but grant *no permissions* to service accounts outside the `kube-system` namespace (beyond discovery permissions given to all authenticated users).
— Official documentation
{{< /lead >}}

## Example

```text
apiVersion: v1
kind: ServiceAccount
metadata:
  creationTimestamp: "2021-08-27T07:52:20Z"
  name: default
  namespace: default
  resourceVersion: "XXXX"
  uid: XXXX
secrets:
- name: default-token-vcb75
```

Let’s add docker-registry secret to the `SA`. (My secret name is samarthya-docker)

```text
kubectl patch serviceaccount default -p '{"imagePullSecrets": [{"name": "samarthya-docker"}]}'
```

The updated `SA`

```text
apiVersion: v1
imagePullSecrets:
- name: samarthya-docker
kind: ServiceAccount
metadata:
  creationTimestamp: "2021-08-27T07:52:20Z"
  name: default
  namespace: default
  resourceVersion: "XXXX"
  uid: XXXXX
secrets:
- name: default-token-vcb75
```

This helps you ensure you do not get image pull errors as it will be using the secret docker-registry to pull any missing images.

{{< lead >}}
Every `namespace` has a `default` `serviceaccount`
{{< /lead >}}

#### e.g `namespace jenkins`

```text
k get sa default -n jenkins -oyaml
```

```text
apiVersion: v1
kind: ServiceAccount
metadata:
  creationTimestamp: "2022-02-02T10:20:58Z"
  name: default
  namespace: jenkins
  resourceVersion: "25024083"
  uid: 53faa1fb-b30c-4159-94f8-64cee3f63629
secrets:
- name: default-token-lhbgn
```

Managing access controls for the `SA` created needs roles and role binding

### Example

```text
kubectl create rolebinding my-sa-view \
  --clusterrole=view \
  --serviceaccount=my-namespace:my-sa \
  --namespace=my-namespace
```

Listing all the clusterroles

```text
k get clusterroles --show-kind=true
```

```text
> k get rolebinding -n jenkins
NAME                         ROLE                             AGE
jenkins-admin-binding        ClusterRole/admin                6d22h
myjenkins-schedule-agents    Role/myjenkins-schedule-agents   13d
myjenkins-watch-configmaps   Role/myjenkins-casc-reload       13d
```

- Fine-grained role bindings provide greater security.

## Help

- <https://kubernetes.io/docs/reference/access-authn-authz/service-accounts-admin/>
- <https://kubernetes.io/docs/reference/access-authn-authz/rbac/>
