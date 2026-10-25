---
title: "PlayGround: K8S"
date: "2020-08-31T09:39:33Z"
slug: "playground-k8s"
categories: ["technical"]
tags: ["plaground"]
aliases: ["/wps/2020/08/31/playground-k8s/"]
wp_id: 1003
---

I have been working on Kubernetes cluster and will soon plan to give a Kubernetes Certified Developer exam. In my quest, I will just record some commands that I found helpful or useful in this blog. It may be multi-part, as I will keep adding on a daily basis the commands that I will be learning.

## Labels

```text
> k get nodes
NAME             STATUS                     ROLES    AGE    VERSION
docker-desktop   Ready,SchedulingDisabled   master   105d   v1.16.6-beta.0
```

Adding a label to the node

```text
> k label node docker-desktop nodeName=docker-node
node/docker-desktop labeled
```

```text
> k get nodes --show-labels
NAME             STATUS                     ROLES    AGE    VERSION          LABELS
docker-desktop   Ready,SchedulingDisabled   master   105d   v1.16.6-beta.0   beta.kubernetes.io/arch=amd64,beta.kubernetes.io/os=linux,kubernetes.io/arch=amd64,kubernetes.io/hostname=docker-desktop,kubernetes.io/os=linux,node-role.kubernetes.io/master=,nodeName=docker-node
```

Notice the new label at the end `nodeName=docker-node`. You can also validate the label has been applied by using the selector

```text
>k get nodes -l nodeName=docker-node
NAME             STATUS                     ROLES    AGE    VERSION
docker-desktop   Ready,SchedulingDisabled   master   105d   v1.16.6-beta.0
```

I will create a nginx-pod on my local `Docker CE/Kubernetes` and validate the Scheduling.

| `nodeSelector` *object* | NodeSelector is a selector which must be true for the pod to fit on a node. Selector which must match a node's labels for the pod to be scheduled on that node. More info: https://kubernetes.io/docs/concepts/configuration/assign-pod-node/ |
| --- | --- |

```text
apiVersion: v1
kind: Pod
metadata:
  labels:
    run: nginx
    app: nginx-on-node
  name: nginx-node
spec:
  nodeSelector:
    nodeName: docker-node
  containers:
    - image: nginx
      name: nginx-container
      resources:
        limits:
          memory: 500Mi
          cpu: 500m
        requests:
          memory: 250Mi
          cpu: 500m
  dnsPolicy: ClusterFirst
  restartPolicy: Never
status: {}
```

What I have used is a `nodeSelector` that uses the label define in the section above. As the only node on my local machine is the `docker-desktop` and it has a setting as SchedulingDisabled the container will forever be in the Pending state.

```text
> k get nodes
NAME             STATUS                     ROLES    AGE    VERSION
docker-desktop   Ready,SchedulingDisabled   master   105d   v1.16.6-beta.0
```

```text
> k get all
NAME                        READY   STATUS    RESTARTS   AGE
pod/curl-69c656fd45-zwt8n   1/1     Running   0          7d
pod/nginx-node              0/1     Pending   0          15m
```

A quick describe on the pod

```text
> k describe pod/nginx-node

Name:         nginx-node
Namespace:    default
Priority:     0
Node:         <none>
Labels:       app=nginx-on-node
              run=nginx
Annotations:  kubectl.kubernetes.io/last-applied-configuration:
                {"apiVersion":"v1","kind":"Pod","metadata":{"annotations":{},"labels":{"app":"nginx-on-node","run":"nginx"},"name":"nginx-node","namespace...
Status:       Pending
IP:           
IPs:          <none>
Containers:
  nginx-container:
    Image:      nginx
    Port:       <none>
    Host Port:  <none>
    Limits:
      cpu:     500m
      memory:  500Mi
    Requests:
      cpu:        500m
      memory:     250Mi
    Environment:  <none>
    Mounts:
      /var/run/secrets/kubernetes.io/serviceaccount from default-token-ksbmz (ro)
Conditions:
  Type           Status
  PodScheduled   False 
Volumes:
  default-token-ksbmz:
    Type:        Secret (a volume populated by a Secret)
    SecretName:  default-token-ksbmz
    Optional:    false
QoS Class:       Burstable
Node-Selectors:  nodeName=docker-node
Tolerations:     node.kubernetes.io/not-ready:NoExecute for 300s
                 node.kubernetes.io/unreachable:NoExecute for 300s
Events:
  Type     Reason            Age        From               Message
  ----     ------            ----       ----               -------
  Warning  FailedScheduling  <unknown>  default-scheduler  0/1 nodes are available: 1 node(s) were unschedulable.
```

It validates the `un-scedulable` node. To overcome this handicap, I will use the `uncordon`

```text
k uncordon -h
Mark node as schedulable.

Examples:
  # Mark node "foo" as schedulable.
  $ kubectl uncordon foo

Options:
      --dry-run=false: If true, only print the object that would be sent, without sending it.
  -l, --selector='': Selector (label query) to filter on

Usage:
  kubectl uncordon NODE [options]
```

```text
> k uncordon docker-desktop
node/docker-desktop uncordoned
```

```text
> k get all
NAME                        READY   STATUS              RESTARTS   AGE
pod/curl-69c656fd45-zwt8n   1/1     Running             0          7d
pod/nginx-node              0/1     ContainerCreating   0          7m12s
```

The moment I mark it as `schedulable` the state changes and I can see the Container creating. A quick describe will show the events

```text
 Type     Reason            Age        From                     Message
  ----     ------            ----       ----                     -------
  Warning  FailedScheduling  <unknown>  default-scheduler        0/1 nodes are available: 1 node(s) were unschedulable.
  Warning  FailedScheduling  <unknown>  default-scheduler        0/1 nodes are available: 1 node(s) were unschedulable.
  Warning  FailedScheduling  <unknown>  default-scheduler        0/1 nodes are available: 1 node(s) had taints that the pod didn't tolerate.
  Normal   Scheduled         <unknown>  default-scheduler        Successfully assigned default/nginx-node to docker-desktop
  Normal   Pulling           6m11s      kubelet, docker-desktop  Pulling image "nginx"
  Normal   Pulled            6m6s       kubelet, docker-desktop  Successfully pulled image "nginx"
  Normal   Created           6m6s       kubelet, docker-desktop  Created container nginx-container
  Normal   Started           6m6s       kubelet, docker-desktop  Started container nginx-container
```

## Annotations

```text
> k annotate pods nginx-node description='My nginx-node on a specific node'
pod/nginx-node annotated
```

A describe call for the pod `nginx-node` can reveal the annotation.

```text
Annotations:  description: My nginx-node on a specific node
```

## Create

`k create -h`

```text
Available Commands:
  clusterrole         Create a ClusterRole.
  clusterrolebinding  Create a ClusterRoleBinding for a particular ClusterRole
  configmap           Create a configmap from a local file, directory or literal value
  cronjob             Create a cronjob with the specified name.
  deployment          Create a deployment with the specified name.
  job                 Create a job with the specified name.
  namespace           Create a namespace with the specified name
  poddisruptionbudget Create a pod disruption budget with the specified name.
  priorityclass       Create a priorityclass with the specified name.
  quota               Create a quota with the specified name.
  role                Create a role with single rule.
  rolebinding         Create a RoleBinding for a particular Role or ClusterRole
  secret              Create a secret using specified subcommand
  service             Create a service using specified subcommand.
  serviceaccount      Create a service account with the specified name
```

Lets create a deployment

```text
k create deploy bbdeploy --image=busybox --dry-run=true -o yaml
```

```text
apiVersion: apps/v1
kind: Deployment
metadata:
  creationTimestamp: null
  labels:
    app: bbdeploy
  name: bbdeploy
spec:
  replicas: 1
  selector:
    matchLabels:
      app: bbdeploy
  strategy: {}
  template:
    metadata:
      creationTimestamp: null
      labels:
        app: bbdeploy
    spec:
      containers:
      - image: busybox
        name: busybox
        resources: {}
status: {}
```

Lets change the replicas to 2 and create the deployment

```text
k describe deploy
```

```text
Name:                   bbdeploy
Namespace:              default
CreationTimestamp:      Mon, 31 Aug 2020 16:14:00 +0530
Labels:                 app=bbdeploy
Annotations:            deployment.kubernetes.io/revision: 1
                        kubectl.kubernetes.io/last-applied-configuration:
                          {"apiVersion":"apps/v1","kind":"Deployment","metadata":{"annotations":{},"labels":{"app":"bbdeploy"},"name":"bbdeploy","namespace":"defaul...
Selector:               app=bbdeploy
Replicas:               2 desired | 2 updated | 2 total | 0 available | 2 unavailable
StrategyType:           RollingUpdate
MinReadySeconds:        0
RollingUpdateStrategy:  25% max unavailable, 25% max surge
Pod Template:
  Labels:  app=bbdeploy
  Containers:
   busybox:
    Image:      busybox
    Port:       <none>
    Host Port:  <none>
    Limits:
      cpu:     250m
      memory:  500Mi
    Requests:
      cpu:        250m
      memory:     500Mi
    Environment:  <none>
    Mounts:       <none>
  Volumes:        <none>
Conditions:
  Type           Status  Reason
  ----           ------  ------
  Available      False   MinimumReplicasUnavailable
  Progressing    True    ReplicaSetUpdated
OldReplicaSets:  <none>
NewReplicaSet:   bbdeploy-5797fdc756 (2/2 replicas created)
Events:
  Type    Reason             Age   From                   Message
  ----    ------             ----  ----                   -------
  Normal  ScalingReplicaSet  7s    deployment-controller  Scaled up replica set bbdeploy-5797fdc756 to 2
```

Similar example for Nginx

```text
--- # My deployment
apiVersion: apps/v1
kind: Deployment
metadata:
  labels:
    app: nginx-webserver
  name: deploy-nginx-deploy
spec:
  replicas: 2
  selector:
    matchLabels:
      app: nginx-webserver-pod
  template:
    metadata:
      labels:
        app: nginx-webserver-pod
    spec:
      containers:
        - image: nginx
          name: nginx
          resources:
            requests:
              cpu: 250m
              memory: 500Mi
            limits:
              cpu: 250m
              memory: 500Mi
```

```text
k get pods --show-labels
NAME                                   READY   STATUS    RESTARTS   AGE    LABELS
deploy-nginx-deploy-6d45895bf5-mv9wr   1/1     Running   0          21s    app=nginx-webserver-pod,pod-template-hash=6d45895bf5
deploy-nginx-deploy-6d45895bf5-vpt6p   1/1     Running   0          21s    app=nginx-webserver-pod,pod-template-hash=6d45895bf5
```

```text
k get deploy --show-labels
NAME                  READY   UP-TO-DATE   AVAILABLE   AGE    LABELS
deploy-nginx-deploy   2/2     2            2           32s    app=nginx-webserver
```

{{< lead >}}
Scaling to 3
{{< /lead >}}

```text
> k scale --replicas=3 deploy/deploy-nginx-deploy
deployment.apps/deploy-nginx-deploy scaled
```

```text
k get all
NAME                                       READY   STATUS              RESTARTS   AGE
pod/deploy-nginx-deploy-6d45895bf5-79kd7   0/1     ContainerCreating   0          4s
pod/deploy-nginx-deploy-6d45895bf5-mv9wr   1/1     Running             0          5m
pod/deploy-nginx-deploy-6d45895bf5-vpt6p   1/1     Running             0          5
```
