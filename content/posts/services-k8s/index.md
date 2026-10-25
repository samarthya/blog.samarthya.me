---
title: "Services: K8S"
date: "2020-08-21T17:34:29Z"
slug: "services-k8s"
categories: ["technical"]
tags: ["k8s", "service"]
aliases: ["/wps/2020/08/21/services-k8s/"]
wp_id: 936
---

There are multiple `Kubernetes` objects we will be talking about in this blog. Mainly Services, Selectors and Labels.

- Service is an abstraction which defines a logical set of Pods and a policy by which to access them.
- A Service in Kubernetes is a REST object, similar to a Pod.
- Service tags the pods, logically grouping them using selectors.
- Pods have a lifecycle, they are born, they live, process and then they die. The pods (desired state) can be managed using deployment.
- A label is an identifying attribute of an object, and can be defined at the creation time, and subsequently modified and added at any time.
- Label selector is a grouping primitive in Kubernetes and allows client/user to identify a set of objects. There are two sets of selectors
  - *equality-based* and
  - *set-based*.

{{< lead >}}
An abstract way to expose an application running on a set of [Pods](https://kubernetes.io/docs/concepts/workloads/pods/) as a network service.
{{< /lead >}}

The set of Pods targeted by a Service is usually determined by a selector.

{{< lead >}}
*Labels* are key/value pairs that are attached to objects, such as pods at the time of creation.
{{< /lead >}}

Labels allow for efficient queries and watches. Let's learn by example. I will try and crate a NGINX pod and expose the port using a service. A simple exercise?

## Step - 1: Define the Pod

```text
apiVersion: v1
kind: Pod
metadata:
  name: nginx-pod
  labels:
    app: my-pod
    author: samarthya
spec:
  containers:
  - name: nginx-pod-container
    image: nginx:latest
```

The above definition has labels applied to the pod, which will be used while creating a service and will be used in the selector.

```text
k describe pod nginx-pod
Name:               nginx-pod
Namespace:          default
Priority:           0
PriorityClassName:  <none>
Node:               ip-10-0-1-103/10.0.1.103
Start Time:         Fri, 21 Aug 2020 16:49:20 +0000
Labels:             app=my-pod
                    author=samarthya
Annotations:        kubectl.kubernetes.io/last-applied-configuration:
                      {"apiVersion":"v1","kind":"Pod","metadata":{"annotations":{},"labels":{"app":"my-pod","author":"samarthya"},"name":"nginx-pod","namespace":"...
Status:             Running
IP:                 10.244.2.3
```

You can use the labels for selectors as under

```text
k get pods -lapp=my-pod
NAME        READY   STATUS    RESTARTS   AGE
nginx-pod   1/1     Running   0          14m
```

you can combine labels as well

```text
k get pods -lapp=my-pod,author=samarthya
NAME        READY   STATUS    RESTARTS   AGE
nginx-pod   1/1     Running   0          15m
```

```text
k get pods -l 'app in (my-pod,my-name)'
NAME        READY   STATUS    RESTARTS   AGE
nginx-pod   1/1     Running   0          16m
```

{{< lead >}}
Each object in your cluster has a *Name* that is unique for that type of resource. Every Kubernetes object also has a *UID* that is unique across your whole cluster.
{{< /lead >}}

## Step - 2: Define the service

Let's create the service to expose the pod.

```text
apiVersion: v1
kind: Service
metadata:
  name: my-svc
spec:
  type: NodePort
  selector:
    app: my-pod
  ports:
  - protocol: TCP
    port: 8080
    targetPort: 80
```

{{< lead >}}
A Service can map *any* incoming `port` to a `targetPort`. By default and for convenience, the `targetPort` is set to the same value as the `port` field.
{{< /lead >}}

```text
k describe svc my-svc
Name:              my-svc
Namespace:         default
Labels:            <none>
Annotations:       kubectl.kubernetes.io/last-applied-configuration:
                     {"apiVersion":"v1","kind":"Service","metadata":{"annotations":{},"name":"my-svc","namespace":"default"},"spec":{"ports":[{"port":8080,"tar...
Selector:          app=my-pod
Type:              ClusterIP
IP:                10.102.126.164
Port:              <unset>  8080/TCP
TargetPort:        80/TCP
Endpoints:         10.244.2.4:80
Session Affinity:  None
Events:            <none>
```

You can validate the service for endpoints

```text
k get ep
NAME         ENDPOINTS                                 AGE
my-svc       10.244.2.4:80                             6m37s
```

I can also define the type of Service

```text

apiVersion: v1
kind: Service
metadata:
  name: my-svc
spec:
  type: NodePort
  selector:
    app: my-pod
  ports:
    - port: 8080
      targetPort: 80
```

and recreate the service.

```text
NAME         TYPE        CLUSTER-IP       EXTERNAL-IP   PORT(S)          AGE
my-svc       NodePort    10.110.6.32      <none>        8080:31676/TCP   2m50s
```

## References

- https://kubernetes.io/docs/concepts/overview/working-with-objects/labels/
- https://kubernetes.io/docs/concepts/overview/components/#kube-apiserver
- https://kubernetes.io/docs/concepts/services-networking/service/#virtual-ips-and-service-proxies
- https://kubernetes.io/docs/concepts/services-networking/service/#publishing-services-service-types
