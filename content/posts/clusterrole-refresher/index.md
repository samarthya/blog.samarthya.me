---
title: "ClusterRole: Refresher"
date: "2021-04-06T11:26:35Z"
slug: "clusterrole-refresher"
categories: ["docker"]
tags: ["refresher", "technical"]
aliases: ["/wps/2021/04/06/clusterrole-refresher/"]
wp_id: 1491
---

In this blog I will use `kubectl` to create a `ClusterRole` and a `ClusterRoleBinding` (refer to [link](https://kubernetes.io/docs/reference/access-authn-authz/rbac/))

```text
{
    "kind": "ClusterRole",
    "apiVersion": "rbac.authorization.k8s.io/v1",
    "metadata": {
        "name": "myclusterrole",
        "creationTimestamp": null
    },
    "rules": [
        {
            "verbs": [
                "get",
                "list",
                "watch"
            ],
            "apiGroups": [
                ""
            ],
            "resources": [
                "persistentvolumes"
            ]
        }
    ]
}
```

```text
k create clusterrole myclusterrole --verb=get,list,watch --resource=persistentvolumes
```

```text
k describe clusterrole myclusterrole
```

{{< lead >}}
You can use a `ClusterRole` to

1. define permissions on `namespaced` resources and be granted within individual namespace(s)

2. define permissions on namespaced resources and be granted across all `namespaces`

3. define permissions on cluster-scoped resources
{{< /lead >}}

```text
{
    "kind": "ClusterRoleBinding",
    "apiVersion": "rbac.authorization.k8s.io/v1beta1",
    "metadata": {
        "name": "crb-test",
        "creationTimestamp": null
    },
    "subjects": [
        {
            "kind": "ServiceAccount",
            "name": "default",
            "namespace": "samarthya"
        }
    ],
    "roleRef": {
        "apiGroup": "rbac.authorization.k8s.io",
        "kind": "ClusterRole",
        "name": "myclusterrole"
    }
}
```

```text
kubectl create clusterrolebinding crb-test --clusterrole=myclusterrole --serviceaccount=samarthya:default --dry-run -o json
```

## --help

Before you execute the `clusterrole` creation you can look at the supported options

```text
k create clusterrole --help
```

```text
Create a ClusterRole.

Examples:
  # Create a ClusterRole named "pod-reader" that allows user to perform "get", "watch" and "list" on pods
  kubectl create clusterrole pod-reader --verb=get,list,watch --resource=pods
  
  # Create a ClusterRole named "pod-reader" with ResourceName specified
  kubectl create clusterrole pod-reader --verb=get --resource=pods --resource-name=readablepod
--resource-name=anotherpod
  
  # Create a ClusterRole named "foo" with API Group specified
  kubectl create clusterrole foo --verb=get,list,watch --resource=rs.extensions
  
  # Create a ClusterRole named "foo" with SubResource specified
  kubectl create clusterrole foo --verb=get,list,watch --resource=pods,pods/status
  
  # Create a ClusterRole name "foo" with NonResourceURL specified
  kubectl create clusterrole "foo" --verb=get --non-resource-url=/logs/*
  
  # Create a ClusterRole name "monitoring" with AggregationRule specified
  kubectl create clusterrole monitoring --aggregation-rule="rbac.example.com/aggregate-to-monitoring=true"

Options:
      --aggregation-rule=: An aggregation label selector for combining ClusterRoles.
      --allow-missing-template-keys=true: If true, ignore any errors in templates when a field or map key is missing in
the template. Only applies to golang and jsonpath output formats.
      --dry-run=false: If true, only print the object that would be sent, without sending it.
      --non-resource-url=[]: A partial url that user should have access to.
  -o, --output='': Output format. One of:
json|yaml|name|go-template|go-template-file|template|templatefile|jsonpath|jsonpath-file.
      --resource=[]: Resource that the rule applies to
      --resource-name=[]: Resource in the white list that the rule applies to, repeat this flag for multiple items
      --save-config=false: If true, the configuration of current object will be saved in its annotation. Otherwise, the
annotation will be unchanged. This flag is useful when you want to perform kubectl apply on this object in the future.
      --template='': Template string or path to template file to use when -o=go-template, -o=go-template-file. The
template format is golang templates [http://golang.org/pkg/text/template/#pkg-overview].
      --validate=true: If true, use a schema to validate the input before sending it
      --verb=[]: Verb that applies to the resources contained in the rule

Usage:
  kubectl create clusterrole NAME --verb=verb --resource=resource.group [--resource-name=resourcename] [--dry-run]
[options]

Use "kubectl options" for a list of global command-line options (applies to all commands).
```

```text
kubectl create clusterrolebinding --help
```

```text
Create a ClusterRoleBinding for a particular ClusterRole.

Examples:
  # Create a ClusterRoleBinding for user1, user2, and group1 using the cluster-admin ClusterRole
  kubectl create clusterrolebinding cluster-admin --clusterrole=cluster-admin --user=user1 --user=user2 --group=group1

Options:
      --allow-missing-template-keys=true: If true, ignore any errors in templates when a field or map key is missing in
the template. Only applies to golang and jsonpath output formats.
      --clusterrole='': ClusterRole this ClusterRoleBinding should reference
      --dry-run='none': Must be "none", "server", or "client". If client strategy, only print the object that would be
sent, without sending it. If server strategy, submit server-side request without persisting the resource.
      --field-manager='kubectl-create': Name of the manager used to track field ownership.
      --group=[]: Groups to bind to the clusterrole
  -o, --output='': Output format. One of:
json|yaml|name|go-template|go-template-file|template|templatefile|jsonpath|jsonpath-as-json|jsonpath-file.
      --save-config=false: If true, the configuration of current object will be saved in its annotation. Otherwise, the
annotation will be unchanged. This flag is useful when you want to perform kubectl apply on this object in the future.
      --serviceaccount=[]: Service accounts to bind to the clusterrole, in the format <namespace>:<name>
      --template='': Template string or path to template file to use when -o=go-template, -o=go-template-file. The
template format is golang templates [http://golang.org/pkg/text/template/#pkg-overview].
      --validate=true: If true, use a schema to validate the input before sending it

Usage:
  kubectl create clusterrolebinding NAME --clusterrole=NAME [--user=username] [--group=groupname]
[--serviceaccount=namespace:serviceaccountname] [--dry-run=server|client|none] [options]

Use "kubectl options" for a list of global command-line options (applies to all commands).
```

Do look at the `serviceaccount`

```text
--serviceaccount=[]: Service accounts to bind to the clusterrole, in the format <namespace>:<name>
```
