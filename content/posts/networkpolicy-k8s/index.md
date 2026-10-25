---
title: "NetworkPolicy: K8S"
date: "2020-08-24"
slug: "networkpolicy-k8s"
categories: ["technical"]
tags: ["k8s", "networkpolicy"]
aliases: ["/wps/2020/08/24/networkpolicy-k8s/", "/wps/2026/10/23/networkpolicy-k8s/"]
wp_id: 961
---

How can a pod communicate with the other pod? The answer to this question is through a network policy.

Network Policy is a specification of how groups of [pods](https://kubernetes.io/docs/concepts/workloads/pods/) are allowed to communicate with each other and other network endpoints.

Like Services, it uses labels to select the pods.

{{< lead >}}
The kubelet has a single default network plugin, and a default network common to the entire cluster.
{{< /lead >}}

`Pod` by default is NON-ISOLATED, implying they accept traffic from any source, by virtue of `NetworkPolicy` an isolation is defined.

{{< lead >}}
Once there is any NetworkPolicy in a namespace selecting a particular pod, that `pod` will reject any connections that are not allowed by any NetworkPolicy.
{{< /lead >}}

Network policies are additive by nature.

```text
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: my-network-policy
  namespace: default
spec:
  podSelector:
    matchLabels:
      app: my-running-pod
  policyTypes:
  - Ingress
  - Egress
```

Mandatory fields for a `NetworkPolicy`

- apiVersion
- kind
- metadata

{{< lead >}}
Type of Services (popular)

1. ClusterIP

2. NodePort

3. LoadBalancer
{{< /lead >}}

## podSelector

Each `NetworkPolicy` defines a podSelector, which identifies the pods to which the policy applies. In our example (above) the policy is applied to all pods with label `app: my-running-pod`

{{< lead >}}
An empty `podSelector` selects all pods in the namespace.
{{< /lead >}}

## policyTypes

It can be either of `Ingress` (default), `Egress` or `both`.

### Ingress

Each rule allows traffic which matches both the `from` and `ports` sections.

### Egress

Each rule allows traffic which matches both the `to` and `ports` sections.

## References

- https://kubernetes.io/docs/concepts/extend-kubernetes/compute-storage-net/network-plugins/
- https://kubernetes.io/docs/tasks/configure-pod-container/configure-pod-configmap/
- https://kubernetes.io/docs/concepts/overview/working-with-objects/object-management/
