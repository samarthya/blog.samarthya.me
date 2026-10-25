---
title: "Network Policy Restrictions"
date: "2020-09-04"
slug: "network-policy-restrictions"
categories: ["technical"]
aliases: ["/wps/2020/09/04/network-policy-restrictions/", "/wps/2026/10/23/network-policy-restrictions/"]
wp_id: 1027
---

```text
kubectl run --namespace=np-demo nginx --replicas=2 --image=nginx
```

```text
kind: NetworkPolicy
apiVersion: networking.k8s.io/v1
metadata:
  name: default-deny
  namespace: np-demo
spec:
  podSelector:
    matchLabels: {}
```

```text
k expose --namespace=np-demo deployment nginx --port=80
```

```text
kind: NetworkPolicy
apiVersion: networking.k8s.io/v1
metadata:
  name: access-nginx
  namespace: np-demo
spec:
  podSelector:
    matchLabels:
      run: nginx
  ingress:
    - from:
      - podSelector:
          matchLabels:
            run: allowed
```

```text
k run --namespace=np-demo no-access --rm -ti --image busybox /bin/sh
```

```text
wget -q --timeout=5 nginx -O -
```

```text
 k run --namespace=policy-demo allowed --rm -ti --image busybox /bin/sh
```
