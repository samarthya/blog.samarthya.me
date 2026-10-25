---
title: "Probes: K8S"
date: "2020-08-22T10:53:05Z"
slug: "probes-k8s"
categories: ["technical"]
tags: ["k8s", "probes"]
aliases: ["/wps/2020/08/22/probes-k8s/"]
wp_id: 944
---

In this blog we will be talking about Liveness, Readiness and Startup probes of a container.

{{< lead >}}
A ***[Service]({{< relref "/posts/services-k8s" >}})*** in Kubernetes is an abstraction which defines a logical set of Pods and a policy by which to access them.
— - Life without a service
{{< /lead >}}

## What is Kubelet?

- `Kubelet` is a primary node agent that runs on every node.
- Works in term of PodSpec, that describes a POD (JSON or Yaml).

## Liveness Probe

- It is used by `kubelet` to decide when to restart the container.
- `periodSeconds` defines when the `kubelet` check periodically.
- `initialDelaySeconds` specifies the initial wait before checking.

I just created a single container pod that will run `touch` command to create a file and then it deletes that specific file after a delay, on which the livenessProbe is listening on and then once liveness fails we can check the container.

```text
--- # Liveness Probe example
apiVersion: v1
kind: Pod
metadata:
  name: pod-bbox-lp
  labels:
    name: liveness-probe-pod
# Container specs
spec:
  containers:
    - name: bbox-pod
      image: busybox:latest
      livenessProbe:
        exec:
          command:
            - cat
            - /tmp/healthy
        initialDelaySeconds: 5
        periodSeconds: 5
      args:
        - /bin/sh
        - -c
        - touch /tmp/healthy; sleep 30; rm -rf /tmp/healthy; sleep 600
      resources:
        limits:
          memory: "128Mi"
          cpu: "500m"
```

Liveness will be checked by issuing command `cat /tmp/healthy`

```text
 k get pods
NAME          READY   STATUS              RESTARTS   AGE
pod-bbox-lp   0/1     ContainerCreating   0          2s
```

{{< lead >}}
Describe to see details `k describe pod/pod-bbox-lp`
{{< /lead >}}

```text
Name:         pod-bbox-lp
Namespace:    default
Priority:     0
Node:         docker-desktop/192.168.65.3
Start Time:   Sat, 22 Aug 2020 16:30:52 +0530
Labels:       name=liveness-probe-pod
Annotations:  kubectl.kubernetes.io/last-applied-configuration:
                {"apiVersion":"v1","kind":"Pod","metadata":{"annotations":{},"labels":{"name":"liveness-probe-pod"},"name":"pod-bbox-lp","namespace":"defa...
Status:       Running
IP:           10.1.0.92
IPs:
  IP:  10.1.0.92
Containers:
  bbox-pod:
    Container ID:  docker://817a11380e645cbde80f66fa34aa5652dcd6744f89788d0f1fe337c685280a10
    Image:         busybox:latest
    Image ID:      docker-pullable://busybox@sha256:4f47c01fa91355af2865ac10fef5bf6ec9c7f42ad2321377c21e844427972977
    Port:          <none>
    Host Port:     <none>
    Args:
      /bin/sh
      -c
      touch /tmp/healthy; sleep 30; rm -rf /tmp/healthy; sleep 600
    State:          Running
      Started:      Sat, 22 Aug 2020 16:31:00 +0530
    Ready:          True
    Restart Count:  0
    Limits:
      cpu:     500m
      memory:  128Mi
    Requests:
      cpu:        500m
      memory:     128Mi
    Liveness:     exec [cat /tmp/healthy] delay=5s timeout=1s period=5s #success=1 #failure=3
    Environment:  <none>
    Mounts:
      /var/run/secrets/kubernetes.io/serviceaccount from default-token-ksbmz (ro)
Conditions:
  Type              Status
  Initialized       True 
  Ready             True 
  ContainersReady   True 
  PodScheduled      True 
Volumes:
  default-token-ksbmz:
    Type:        Secret (a volume populated by a Secret)
    SecretName:  default-token-ksbmz
    Optional:    false
QoS Class:       Guaranteed
Node-Selectors:  <none>
Tolerations:     node.kubernetes.io/not-ready:NoExecute for 300s
                 node.kubernetes.io/unreachable:NoExecute for 300s
Events:
  Type    Reason     Age        From                     Message
  ----    ------     ----       ----                     -------
  Normal  Scheduled  <unknown>  default-scheduler        Successfully assigned default/pod-bbox-lp to docker-desktop
  Normal  Pulling    18s        kubelet, docker-desktop  Pulling image "busybox:latest"
  Normal  Pulled     10s        kubelet, docker-desktop  Successfully pulled image "busybox:latest"
  Normal  Created    10s        kubelet, docker-desktop  Created container bbox-pod
  Normal  Started    10s        kubelet, docker-desktop  Started container bbox-pod
```

These commands will be run as bootstrapping the container.

```text
/bin/sh -c touch /tmp/healthy; sleep 30; rm -rf /tmp/healthy; sleep 600
```

The liveness probe is looking for the file `/tmp/healthy`

```text
Liveness:     exec [cat /tmp/healthy] delay=5s timeout=1s period=5s #success=1 #failure=3
```

Check for the file if it exists while the container sleeps.

```text
> k exec pod/pod-bbox-lp -- ls -als /tmp/healthy

0 -rw-r--r--    1 root     root             0 Aug 22 11:02 /tmp/healthy
```

Let us run `describe` after the sleep delay - 30 seconds.

```text
> k describe pod/pod-bbox-lp
```

```text
Name:         pod-bbox-lp
Namespace:    default
Priority:     0
Node:         docker-desktop/192.168.65.3
Start Time:   Sat, 22 Aug 2020 16:30:52 +0530
Labels:       name=liveness-probe-pod
Annotations:  kubectl.kubernetes.io/last-applied-configuration:
                {"apiVersion":"v1","kind":"Pod","metadata":{"annotations":{},"labels":{"name":"liveness-probe-pod"},"name":"pod-bbox-lp","namespace":"defa...
Status:       Running
IP:           10.1.0.92
IPs:
  IP:  10.1.0.92
Containers:
  bbox-pod:
    Container ID:  docker://302120c0b732718491733e9073830d40375df47c26e1b7df9cdd09391d74602f
    Image:         busybox:latest
    Image ID:      docker-pullable://busybox@sha256:4f47c01fa91355af2865ac10fef5bf6ec9c7f42ad2321377c21e844427972977
    Port:          <none>
    Host Port:     <none>
    Args:
      /bin/sh
      -c
      touch /tmp/healthy; sleep 30; rm -rf /tmp/healthy; sleep 600
    State:          Running
      Started:      Sat, 22 Aug 2020 16:32:17 +0530
    Last State:     Terminated
      Reason:       Error
      Exit Code:    137
      Started:      Sat, 22 Aug 2020 16:31:00 +0530
      Finished:     Sat, 22 Aug 2020 16:32:11 +0530
    Ready:          True
    Restart Count:  1
    Limits:
      cpu:     500m
      memory:  128Mi
    Requests:
      cpu:        500m
      memory:     128Mi
    Liveness:     exec [cat /tmp/healthy] delay=5s timeout=1s period=5s #success=1 #failure=3
    Environment:  <none>
    Mounts:
      /var/run/secrets/kubernetes.io/serviceaccount from default-token-ksbmz (ro)
Conditions:
  Type              Status
  Initialized       True 
  Ready             True 
  ContainersReady   True 
  PodScheduled      True 
Volumes:
  default-token-ksbmz:
    Type:        Secret (a volume populated by a Secret)
    SecretName:  default-token-ksbmz
    Optional:    false
QoS Class:       Guaranteed
Node-Selectors:  <none>
Tolerations:     node.kubernetes.io/not-ready:NoExecute for 300s
                 node.kubernetes.io/unreachable:NoExecute for 300s
Events:
  Type     Reason     Age                  From                     Message
  ----     ------     ----                 ----                     -------
  Normal   Scheduled  <unknown>            default-scheduler        Successfully assigned default/pod-bbox-lp to docker-desktop
  Normal   Pulling    57s (x2 over 2m17s)  kubelet, docker-desktop  Pulling image "busybox:latest"
  Normal   Pulled     52s (x2 over 2m9s)   kubelet, docker-desktop  Successfully pulled image "busybox:latest"
  Normal   Created    52s (x2 over 2m9s)   kubelet, docker-desktop  Created container bbox-pod
  Normal   Started    52s (x2 over 2m9s)   kubelet, docker-desktop  Started container bbox-pod
  Warning  Unhealthy  8s (x6 over 98s)     kubelet, docker-desktop  Liveness probe failed: cat: can't open '/tmp/healthy': No such file or directory
  Normal   Killing    8s (x2 over 88s)     kubelet, docker-desktop  Container bbox-pod failed liveness probe, will be restarted
```

Notice the error

```text
 Last State:     Terminated
      Reason:       Error
      Exit Code:    137
      Started:      Sat, 22 Aug 2020 16:31:00 +0530
      Finished:     Sat, 22 Aug 2020 16:32:11 +0530
```

```text
desktop  Started container bbox-pod
  Warning  Unhealthy  8s (x6 over 98s)     kubelet, docker-desktop  Liveness probe failed: cat: can't open '/tmp/healthy': No such file or directory
```

You can also use an `httpGet` liveness probe as well.

```text
--- # Livenessprobe example for HTTP endpoint
apiVersion: v1
kind: Pod
metadata:
  name: liveness-probe-example
  labels:
    name: liveness-probe-app
spec:
  containers:
    - name: liveness-probe-pod
      image: samarthya/epserver:1.0
      livenessProbe:
        httpGet:
          path: /hello
          port: 8090
          httpHeaders:
            - name: CustomHeader
              value: Awesome
        initialDelaySeconds: 5
        periodSeconds: 3
      resources:
        limits:
          memory: "128Mi"
          cpu: "500m"
      ports:
        - containerPort: 8090
```

If you look at the logs you can see the endpoint being called regularly

```text
> k logs pod/liveness-probe-example
2020/08/22 18:20:52 My Simple Http Server
2020/08/22 18:20:52  DBG: Accepting traffic for /hello
 -------- Welcome to my server ------- 
2020/08/22 18:20:59  DBG: Method -  GET
2020/08/22 18:20:59  DBG: Body -  {}
2020/08/22 18:20:59  DBG: URL -  /hello
2020/08/22 18:20:59     { 
2020/08/22 18:20:59      DBG: Hello World!
2020/08/22 18:20:59      DBG: 2020-08-22 18:20:59.6744393 +0000 UTC
2020/08/22 18:20:59     } 
2020/08/22 18:20:59  DBG: {"message":"Hello World!","timestamp":"2020-08-22T18:20:59.6744393Z"}
2020/08/22 18:21:02  DBG: Method -  GET
2020/08/22 18:21:02  DBG: Body -  {}
2020/08/22 18:21:02  DBG: URL -  /hello
2020/08/22 18:21:02     { 
2020/08/22 18:21:02      DBG: Hello World!
2020/08/22 18:21:02      DBG: 2020-08-22 18:21:02.6743863 +0000 UTC
2020/08/22 18:21:02     } 
2020/08/22 18:21:02  DBG: {"message":"Hello World!","timestamp":"2020-08-22T18:21:02.6743863Z"}
```

![From the official K8S documentation.](https://d33wubrfki0l68.cloudfront.net/cc38b0f3c0fd94e66495e3a4198f2096cdecd3d5/ace10/docs/tutorials/kubernetes-basics/public/images/module_04_services.svg "From the official K8S documentation.")

## Readiness Probe

- It is used to decide when the pod is ready to accept the incoming traffic.

## Startup Probe

- The `kubelet` uses startup probes to know when a container application has started.

## References

- https://kubernetes.io/docs/reference/command-line-tools-reference/kubelet/
- https://hub.docker.com/repository/docker/samarthya/epserver
