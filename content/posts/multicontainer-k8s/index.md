---
title: "MultiContainer: K8S"
date: "2020-08-27T11:18:17Z"
slug: "multicontainer-k8s"
categories: ["technical"]
tags: ["k8s", "multicontainer", "pods"]
aliases: ["/wps/2020/08/27/multicontainer-k8s/"]
wp_id: 976
---

## [POD](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.18/#pod-v1-core)

Smallest deployment unit you can manage in K8S, is a `Pod`. A pod may have one or more containers.

### Points to remember

- [Pod](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.18/#pod-v1-core) is a specification for container.
- Pods do not self-heal.
- In K8S, a `controller` is used to manage the `Pod` instances.
- Pod is a group of one or more containers
- It may share storage or other resources. (Storage and Networking)
- Pods can support multiple cooperating processes.
- Workload resources is used to manage the multiple pods. (DaemonSet, [Deployment](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/), [SatefulSet](https://kubernetes.io/docs/concepts/workloads/controllers/statefulset/))

![From the official documentation](https://d33wubrfki0l68.cloudfront.net/aecab1f649bc640ebef1f05581bfcc91a48038c4/728d6/images/docs/pod.svg "From the official documentation")

{{< lead >}}
Refer to [code](https://github.com/kubernetes/community/blob/master/contributors/devel/sig-architecture/api-conventions.md#resources)
{{< /lead >}}

### Basic Structure

| Field | Description |
| --- | --- |
| apiVersion | Versioned schema for representation of the object. |
| [kind](https://github.com/kubernetes/community/blob/master/contributors/devel/sig-architecture/api-conventions.md#types-kinds) | The object (Persistent entity) being represented. Typically categorised in three groups (details [here](https://github.com/kubernetes/community/blob/master/contributors/devel/sig-architecture/api-conventions.md#types-kinds)) 1. Objects 2. List 3. Simple |
| [metadata](https://github.com/kubernetes/community/blob/master/contributors/devel/sig-architecture/api-conventions.md#metadata) | Every object must have [metadata](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.18/#objectmeta-v1-meta) that can define 1. namespace 2. [name](https://kubernetes.io/docs/concepts/overview/working-with-objects/names/) 3. unique ID |
| [spec](https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#spec-and-status) | A complete description of the desired [state](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.18/#podspec-v1-core). |

#### Example

```text
apiVersion: v1
kind: Pod
metadata:
  creationTimestamp: null
  labels:
    app: my-pod
    author: samarthya
  name: myepserver
spec:
  containers:
  - env:
    - name: SERVERPORT
      value: "9090"
    image: samarthya/epserver:2.0
    name: myepserver
    ports:
    - containerPort: 9090
    resources: {}
  dnsPolicy: ClusterFirst
  restartPolicy: Always
status: {}
```

{{< lead >}}
k api-resources
— gives the complete list of resources supported
{{< /lead >}}

The YAML (from example above) in form of a command

```text
k run myepserver --image samarthya/epserver:2.0 --env SERVERPORT=9090 --port=9090 -l'app=my-pod,author=samarthya'
```

I could have generated the same YAML using

```text
k run myepserver --image samarthya/epserver:2.0 --env SERVERPORT=9090 --port=9090 -l'app=my-pod,author=samarthya' --dry-run=client -o yaml
```

{{< lead >}}
In terms of Docker concepts, a Pod is similar to a group of Docker containers with shared namespaces and shared filesystem volumes.
{{< /lead >}}

### Lifecycle of a POD

When we use `k get pods` to see the pods running the status field defined is the Phase associated with the `Pod` and can be either of `Pending`, `Running`, `Succeeded`, `Failed` or `Unknown`.

```text
k get pod myepserver -o=jsonpath="{range .status.conditions[*]}{'\n'}{.type}{'\t'}{.lastTransitionTime}{end}"
```

```text
Initialized 2020-08-27T08:41:06Z
Ready 2020-08-27T08:41:16Z
ContainersReady 2020-08-27T08:41:16Z
```

If you are wondering about the `jsonpath` used above; it is a very powerful way to parse and get the desired information bit.

Example: To get the host IP you can use a command like below.

```text
k get pod myepserver -o=jsonpath="{.status.hostIP}{'\n'}"
```

To get a restart policy

```text
k get pod myepserver -o=jsonpath="{.spec.restartPolicy}{'\n'}"
```

```text
k get pod myepserver -o=jsonpath="{range .status.conditions[*]}{'\n'}{.type}{'\t'}{.lastTransitionTime}{'\t'}{.lastProbeTime}{'->'}{.status}{end}{'\n'}"
```

```text
Initialized     2020-08-27T08:41:06Z    <nil>->True
Ready   2020-08-27T08:41:16Z    <nil>->True
ContainersReady 2020-08-27T08:41:16Z    <nil>->True
PodScheduled    2020-08-27T08:41:06Z    <nil>->True
```

{{< lead >}}
Like Pod, a container also has lifecycle and possible states: Waiting, Running, Terminated.
{{< /lead >}}

```text
NAME         READY   STATUS    RESTARTS   AGE
myepserver   1/1     Running   0          63m
```

## More..

- [Init containers](https://kubernetes.io/docs/concepts/workloads/pods/init-containers/)
- [Ephemeral containers.](https://kubernetes.io/docs/concepts/workloads/pods/ephemeral-containers/)
- [Container lifecycle hooks.](https://kubernetes.io/docs/concepts/containers/container-lifecycle-hooks/)
