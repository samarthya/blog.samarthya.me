---
title: "Deployments: K8S"
date: "2020-08-24T12:29:53Z"
slug: "deployments-k8s"
categories: ["technical"]
tags: ["deployments", "k8s"]
aliases: ["/wps/2020/08/24/deployments-k8s/"]
wp_id: 968
---

A declarative way of maintaining the desired state.

Continuing my example from the last blog

```text
--- # Pod deployment
apiVersion: apps/v1
kind: Deployment
metadata:
  name: go-server-deployment
spec:
  replicas: 2
  selector:
    matchLabels:
      app: my-go-server
  template:
    metadata:
      labels:
        app: my-go-server
    spec:
      containers:
        - name: go-server
          image: samarthya/epserver:2.0
          resources:
            limits:
              memory: "256Mi"
              cpu: "1024m"
          env:
            - name: SERVERPORT
              value: "9090"
          ports:
            - containerPort: 9090
# Reference - https://kubernetes.io/docs/concepts/workloads/controllers/deployment/
```

In my deployment, I have two replicas configured, which can be increased to three using the command like the one below.

```text
k scale deployment/go-server-deployment --replicas=3
```

If I wish rollout a change for all pods, which can be conveniently managed via deployments it is as easy as issuing a single command.

```text
k set image deployment/go-server-deployment go-server=samarthya/epserver:1.0 --record=true
```

History is also maintained

```text
k rollout history deployment go-server-deployment 
REVISION  CHANGE-CAUSE
1         <none>
2         k set image deployment/go-server-deployment go-server=samarthya/epserver:2.0 --record=true
```

Other command that you can issue for rollout are as under

```text
Available Commands:
  history     View rollout history
  pause       Mark the provided resource as paused
  restart     Restart a resource
  resume      Resume a paused resource
  status      Show the status of the rollout
  undo        Undo a previous rollout
```

```text
k rollout undo
```

## References

- https://kubernetes.io/docs/concepts/workloads/controllers/deployment/#creating-a-deployment
