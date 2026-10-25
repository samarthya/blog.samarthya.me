---
title: "Upgrading K8S cluster"
date: "2022-01-05T07:05:30Z"
slug: "upgrading-k8s-cluster"
categories: ["kubernetes", "technical"]
tags: ["k8s", "kubeadm", "upgrade"]
aliases: ["/wps/2022/01/05/upgrading-k8s-cluster/"]
wp_id: 1873
---

In this blog I will talk about how you can upgrade a node and the kubernetes cluster version to a specific version.

I have a 6 node local Kubernetes cluster like below

```text
root@master>k get nodes
NAME                           STATUS   ROLES                  AGE    VERSION
machinedev002687.samarthya.me  Ready    <none>                 41d    v1.22.4
machinedev003277.samarthya.me  Ready    <none>                 130d   v1.23.1
machinedev003278.samarthya.me  Ready    <none>                 130d   v1.23.1
machinedev003968.samarthya.me  Ready    <none>                 130d   v1.23.1
machineqa003969.samarthya.me   Ready    control-plane,master   130d   v1.23.1
machineqa003970.samarthya.me   Ready    <none>                 130d   v1.23.1
```

and as evident one of the node is having a different version than the others `1.22.4` which gave me the opportunity to apply what I learned for upgrading clusters using `kubeadm`.

> Refer to the official documentation for finding detailed steps
>
> https://kubernetes.io/docs/tasks/administer-cluster/kubeadm/kubeadm-upgrade/

## Step 1: `kubeadm upgrade plan`

First thing I tried as the documentation mandated was to plan for the upgrade

```text
root@master>kubeadm upgrade plan
```

The output was loads of useful information but in particular

```text
[upgrade/config] Making sure the configuration is correct:
[upgrade/config] Reading configuration from the cluster...
[upgrade/config] FYI: You can look at this config file with 'kubectl -n kube-system get cm kubeadm-config -o yaml'
[preflight] Running pre-flight checks.
[upgrade] Running cluster health checks
[upgrade] Fetching available versions to upgrade to
[upgrade/versions] Cluster version: v1.22.1
[upgrade/versions] kubeadm version: v1.23.1
[upgrade/versions] Target version: v1.23.1
[upgrade/versions] Latest version in the v1.22 series: v1.22.5
Components that must be upgraded manually after you have upgraded the control plane with 'kubeadm upgrade apply':
COMPONENT   CURRENT       TARGET
kubelet     1 x v1.22.4   v1.22.5
            5 x v1.23.1   v1.22.5

Upgrade to the latest version in the v1.22 series:

COMPONENT                 CURRENT   TARGET
kube-apiserver            v1.22.1   v1.22.5
kube-controller-manager   v1.22.1   v1.22.5
kube-scheduler            v1.22.1   v1.22.5
kube-proxy                v1.22.1   v1.22.5
CoreDNS                   v1.8.4    v1.8.6
etcd                      3.5.0-0   3.5.1-0

You can now apply the upgrade by executing the following command:

        kubeadm upgrade apply v1.22.5

_____________________________________________________________________

Components that must be upgraded manually after you have upgraded the control plane with 'kubeadm upgrade apply':
COMPONENT   CURRENT       TARGET
kubelet     1 x v1.22.4   v1.23.1
            5 x v1.23.1   v1.23.1

Upgrade to the latest stable version:

COMPONENT                 CURRENT   TARGET
kube-apiserver            v1.22.1   v1.23.1
kube-controller-manager   v1.22.1   v1.23.1
kube-scheduler            v1.22.1   v1.23.1
kube-proxy                v1.22.1   v1.23.1
CoreDNS                   v1.8.4    v1.8.6
etcd                      3.5.0-0   3.5.1-0

You can now apply the upgrade by executing the following command:

        kubeadm upgrade apply v1.23.1

_____________________________________________________________________

The table below shows the current state of component configs as understood by this version of kubeadm.
Configs that have a "yes" mark in the "MANUAL UPGRADE REQUIRED" column require manual config upgrade or
resetting to kubeadm defaults before a successful upgrade can be performed. The version to manually
upgrade to is denoted in the "PREFERRED VERSION" column.

API GROUP                 CURRENT VERSION   PREFERRED VERSION   MANUAL UPGRADE REQUIRED
kubeproxy.config.k8s.io   v1alpha1          v1alpha1            no
kubelet.config.k8s.io     v1beta1           v1beta1             no
_____________________________________________________________________
```

As the output suggested I had two options to choose from and I went with `v1.23.1` and application was pretty simple

```text
root@master> kubeadm upgrade apply v1.23.1
```

The output was very verbose and it helped me understand what all it was doing. It is plain & simple steps that it was following. (If you are trying it out in your cluster the output might be little different)

```text
[upgrade/config] Making sure the configuration is correct:
[upgrade/config] Reading configuration from the cluster...
[upgrade/config] FYI: You can look at this config file with 'kubectl -n kube-system get cm kubeadm-config -o yaml'
[preflight] Running pre-flight checks.
[upgrade] Running cluster health checks
[upgrade/version] You have chosen to change the cluster version to "v1.23.1"
[upgrade/versions] Cluster version: v1.22.1
[upgrade/versions] kubeadm version: v1.23.1
[upgrade/confirm] Are you sure you want to proceed with the upgrade? [y/N]: y
[upgrade/prepull] Pulling images required for setting up a Kubernetes cluster
[upgrade/prepull] This might take a minute or two, depending on the speed of your internet connection
[upgrade/prepull] You can also perform this action in beforehand using 'kubeadm config images pull'
[upgrade/apply] Upgrading your Static Pod-hosted control plane to version "v1.23.1"...
Static pod: kube-apiserver-machineqa003969.samarthya.me hash: d4b824139c7c46f146c89d485f786b82
Static pod: kube-controller-manager-machineqa003969.samarthya.me hash: 7b04fc1bdfe67b074090ed91e434e5e8
Static pod: kube-scheduler-machineqa003969.samarthya.me hash: 0d03ef8ddb9b9c950d546a2993ef7aa0
[upgrade/etcd] Upgrading to TLS for etcd
Static pod: etcd-machineqa003969.samarthya.me hash: b6988bee4d945836d19e723256d23d35
[upgrade/staticpods] Preparing for "etcd" upgrade
[upgrade/staticpods] Renewing etcd-server certificate
[upgrade/staticpods] Renewing etcd-peer certificate
[upgrade/staticpods] Renewing etcd-healthcheck-client certificate
[upgrade/staticpods] Moved new manifest to "/etc/kubernetes/manifests/etcd.yaml" and backed up old manifest to "/etc/kubernetes/tmp/kubeadm-backup-manifests-2022-01-05-06-32-29/etcd.yaml"
[upgrade/staticpods] Waiting for the kubelet to restart the component
[upgrade/staticpods] This might take a minute or longer depending on the component/version gap (timeout 5m0s)
Static pod: etcd-machineqa003969.samarthya.me hash: b6988bee4d945836d19e723256d23d35
Static pod: etcd-machineqa003969.samarthya.me hash: b6988bee4d945836d19e723256d23d35
Static pod: etcd-machineqa003969.samarthya.me hash: 0112495d26c7c568eeca87d0bd40d695
[apiclient] Found 1 Pods for label selector component=etcd
[upgrade/staticpods] Component "etcd" upgraded successfully!
[upgrade/etcd] Waiting for etcd to become available
[upgrade/staticpods] Writing new Static Pod manifests to "/etc/kubernetes/tmp/kubeadm-upgraded-manifests3925365806"
[upgrade/staticpods] Preparing for "kube-apiserver" upgrade
[upgrade/staticpods] Renewing apiserver certificate
[upgrade/staticpods] Renewing apiserver-kubelet-client certificate
[upgrade/staticpods] Renewing front-proxy-client certificate
[upgrade/staticpods] Renewing apiserver-etcd-client certificate
[upgrade/staticpods] Moved new manifest to "/etc/kubernetes/manifests/kube-apiserver.yaml" and backed up old manifest to "/etc/kubernetes/tmp/kubeadm-backup-manifests-2022-01-05-06-32-29/kube-apiserver.yaml"
[upgrade/staticpods] Waiting for the kubelet to restart the component
[upgrade/staticpods] This might take a minute or longer depending on the component/version gap (timeout 5m0s)
Static pod: kube-apiserver-machineqa003969.samarthya.me hash: d4b824139c7c46f146c89d485f786b82
Static pod: kube-apiserver-machineqa003969.samarthya.me hash: d4b824139c7c46f146c89d485f786b82
Static pod: kube-apiserver-machineqa003969.samarthya.me hash: d4b824139c7c46f146c89d485f786b82
Static pod: kube-apiserver-machineqa003969.samarthya.me hash: 0cda1c6b70fd6f80c894dde50147f924
[apiclient] Found 1 Pods for label selector component=kube-apiserver
[upgrade/staticpods] Component "kube-apiserver" upgraded successfully!
[upgrade/staticpods] Preparing for "kube-controller-manager" upgrade
[upgrade/staticpods] Renewing controller-manager.conf certificate
[upgrade/staticpods] Moved new manifest to "/etc/kubernetes/manifests/kube-controller-manager.yaml" and backed up old manifest to "/etc/kubernetes/tmp/kubeadm-backup-manifests-2022-01-05-06-32-29/kube-controller-manager.yaml"
[upgrade/staticpods] Waiting for the kubelet to restart the component
[upgrade/staticpods] This might take a minute or longer depending on the component/version gap (timeout 5m0s)
Static pod: kube-controller-manager-machineqa003969.samarthya.me hash: 7b04fc1bdfe67b074090ed91e434e5e8
Static pod: kube-controller-manager-machineqa003969.samarthya.me hash: 7b04fc1bdfe67b074090ed91e434e5e8
Static pod: kube-controller-manager-machineqa003969.samarthya.me hash: 7b04fc1bdfe67b074090ed91e434e5e8
Static pod: kube-controller-manager-machineqa003969.samarthya.me hash: 7b04fc1bdfe67b074090ed91e434e5e8
Static pod: kube-controller-manager-machineqa003969.samarthya.me hash: 7b04fc1bdfe67b074090ed91e434e5e8
Static pod: kube-controller-manager-machineqa003969.samarthya.me hash: 7b04fc1bdfe67b074090ed91e434e5e8
Static pod: kube-controller-manager-machineqa003969.samarthya.me hash: 7b04fc1bdfe67b074090ed91e434e5e8
Static pod: kube-controller-manager-machineqa003969.samarthya.me hash: 7b04fc1bdfe67b074090ed91e434e5e8
Static pod: kube-controller-manager-machineqa003969.samarthya.me hash: 7b04fc1bdfe67b074090ed91e434e5e8
Static pod: kube-controller-manager-machineqa003969.samarthya.me hash: 7b04fc1bdfe67b074090ed91e434e5e8
Static pod: kube-controller-manager-machineqa003969.samarthya.me hash: 7b04fc1bdfe67b074090ed91e434e5e8
Static pod: kube-controller-manager-machineqa003969.samarthya.me hash: 7b04fc1bdfe67b074090ed91e434e5e8
Static pod: kube-controller-manager-machineqa003969.samarthya.me hash: 7b04fc1bdfe67b074090ed91e434e5e8
Static pod: kube-controller-manager-machineqa003969.samarthya.me hash: 7b04fc1bdfe67b074090ed91e434e5e8
Static pod: kube-controller-manager-machineqa003969.samarthya.me hash: 7b04fc1bdfe67b074090ed91e434e5e8
Static pod: kube-controller-manager-machineqa003969.samarthya.me hash: 7b04fc1bdfe67b074090ed91e434e5e8
Static pod: kube-controller-manager-machineqa003969.samarthya.me hash: 7b04fc1bdfe67b074090ed91e434e5e8
Static pod: kube-controller-manager-machineqa003969.samarthya.me hash: 7b04fc1bdfe67b074090ed91e434e5e8
Static pod: kube-controller-manager-machineqa003969.samarthya.me hash: 7b04fc1bdfe67b074090ed91e434e5e8
Static pod: kube-controller-manager-machineqa003969.samarthya.me hash: 7b04fc1bdfe67b074090ed91e434e5e8
Static pod: kube-controller-manager-machineqa003969.samarthya.me hash: 7b04fc1bdfe67b074090ed91e434e5e8
Static pod: kube-controller-manager-machineqa003969.samarthya.me hash: 7b04fc1bdfe67b074090ed91e434e5e8
Static pod: kube-controller-manager-machineqa003969.samarthya.me hash: 7b04fc1bdfe67b074090ed91e434e5e8
Static pod: kube-controller-manager-machineqa003969.samarthya.me hash: 7b04fc1bdfe67b074090ed91e434e5e8
Static pod: kube-controller-manager-machineqa003969.samarthya.me hash: 7b04fc1bdfe67b074090ed91e434e5e8
Static pod: kube-controller-manager-machineqa003969.samarthya.me hash: 7b04fc1bdfe67b074090ed91e434e5e8
Static pod: kube-controller-manager-machineqa003969.samarthya.me hash: 7b04fc1bdfe67b074090ed91e434e5e8
Static pod: kube-controller-manager-machineqa003969.samarthya.me hash: 7b04fc1bdfe67b074090ed91e434e5e8
Static pod: kube-controller-manager-machineqa003969.samarthya.me hash: f2e4c6777f4c0675b3987cadd9e82c16
[apiclient] Found 1 Pods for label selector component=kube-controller-manager
[upgrade/staticpods] Component "kube-controller-manager" upgraded successfully!
[upgrade/staticpods] Preparing for "kube-scheduler" upgrade
[upgrade/staticpods] Renewing scheduler.conf certificate
[upgrade/staticpods] Moved new manifest to "/etc/kubernetes/manifests/kube-scheduler.yaml" and backed up old manifest to "/etc/kubernetes/tmp/kubeadm-backup-manifests-2022-01-05-06-32-29/kube-scheduler.yaml"
[upgrade/staticpods] Waiting for the kubelet to restart the component
[upgrade/staticpods] This might take a minute or longer depending on the component/version gap (timeout 5m0s)
Static pod: kube-scheduler-machineqa003969.samarthya.me hash: 0d03ef8ddb9b9c950d546a2993ef7aa0
Static pod: kube-scheduler-machineqa003969.samarthya.me hash: 0d03ef8ddb9b9c950d546a2993ef7aa0
Static pod: kube-scheduler-machineqa003969.samarthya.me hash: 0d03ef8ddb9b9c950d546a2993ef7aa0
Static pod: kube-scheduler-machineqa003969.samarthya.me hash: 0d03ef8ddb9b9c950d546a2993ef7aa0
Static pod: kube-scheduler-machineqa003969.samarthya.me hash: 0d03ef8ddb9b9c950d546a2993ef7aa0
Static pod: kube-scheduler-machineqa003969.samarthya.me hash: 0d03ef8ddb9b9c950d546a2993ef7aa0
Static pod: kube-scheduler-machineqa003969.samarthya.me hash: 0d03ef8ddb9b9c950d546a2993ef7aa0
Static pod: kube-scheduler-machineqa003969.samarthya.me hash: 0d03ef8ddb9b9c950d546a2993ef7aa0
Static pod: kube-scheduler-machineqa003969.samarthya.me hash: 0d03ef8ddb9b9c950d546a2993ef7aa0
Static pod: kube-scheduler-machineqa003969.samarthya.me hash: 0d03ef8ddb9b9c950d546a2993ef7aa0
Static pod: kube-scheduler-machineqa003969.samarthya.me hash: 0d03ef8ddb9b9c950d546a2993ef7aa0
Static pod: kube-scheduler-machineqa003969.samarthya.me hash: 0d03ef8ddb9b9c950d546a2993ef7aa0
Static pod: kube-scheduler-machineqa003969.samarthya.me hash: 0d03ef8ddb9b9c950d546a2993ef7aa0
Static pod: kube-scheduler-machineqa003969.samarthya.me hash: 0d03ef8ddb9b9c950d546a2993ef7aa0
Static pod: kube-scheduler-machineqa003969.samarthya.me hash: 0d03ef8ddb9b9c950d546a2993ef7aa0
Static pod: kube-scheduler-machineqa003969.samarthya.me hash: 0d03ef8ddb9b9c950d546a2993ef7aa0
Static pod: kube-scheduler-machineqa003969.samarthya.me hash: 0d03ef8ddb9b9c950d546a2993ef7aa0
Static pod: kube-scheduler-machineqa003969.samarthya.me hash: 0d03ef8ddb9b9c950d546a2993ef7aa0
Static pod: kube-scheduler-machineqa003969.samarthya.me hash: 0d03ef8ddb9b9c950d546a2993ef7aa0
Static pod: kube-scheduler-machineqa003969.samarthya.me hash: 0d03ef8ddb9b9c950d546a2993ef7aa0
Static pod: kube-scheduler-machineqa003969.samarthya.me hash: 0d03ef8ddb9b9c950d546a2993ef7aa0
Static pod: kube-scheduler-machineqa003969.samarthya.me hash: 0d03ef8ddb9b9c950d546a2993ef7aa0
Static pod: kube-scheduler-machineqa003969.samarthya.me hash: 0d03ef8ddb9b9c950d546a2993ef7aa0
Static pod: kube-scheduler-machineqa003969.samarthya.me hash: 0d03ef8ddb9b9c950d546a2993ef7aa0
Static pod: kube-scheduler-machineqa003969.samarthya.me hash: 15a674e5b7a122f1e55f639ad88f1cbe
[apiclient] Found 1 Pods for label selector component=kube-scheduler
[upgrade/staticpods] Component "kube-scheduler" upgraded successfully!
[upgrade/postupgrade] Applying label node-role.kubernetes.io/control-plane='' to Nodes with label node-role.kubernetes.io/master='' (deprecated)
[upload-config] Storing the configuration used in ConfigMap "kubeadm-config" in the "kube-system" Namespace
[kubelet] Creating a ConfigMap "kubelet-config-1.23" in namespace kube-system with the configuration for the kubelets in the cluster
NOTE: The "kubelet-config-1.23" naming of the kubelet ConfigMap is deprecated. Once the UnversionedKubeletConfigMap feature gate graduates to Beta the default name will become just "kubelet-config". Kubeadm upgrade will handle this transition transparently.
[kubelet-start] Writing kubelet configuration to file "/var/lib/kubelet/config.yaml"
[bootstrap-token] configured RBAC rules to allow Node Bootstrap tokens to get nodes
[bootstrap-token] configured RBAC rules to allow Node Bootstrap tokens to post CSRs in order for nodes to get long term certificate credentials
[bootstrap-token] configured RBAC rules to allow the csrapprover controller automatically approve CSRs from a Node Bootstrap Token
[bootstrap-token] configured RBAC rules to allow certificate rotation for all node client certificates in the cluster
[addons] Applied essential addon: CoreDNS
[addons] Applied essential addon: kube-proxy

[upgrade/successful] SUCCESS! Your cluster was upgraded to "v1.23.1". Enjoy!

[upgrade/kubelet] Now that your control plane is upgraded, please proceed with upgrading your kubelets if you haven't already done so.
```

It took me around 2 minutes for the process to complete, but eventually it was success

`SUCCESS! Your cluster was upgraded to "v1.23.1". Enjoy!`

## Step 2: Check the nodes

```text
root@master>k get nodes -o wide
NAME                            STATUS   ROLES                  AGE    VERSION   INTERNAL-IP     EXTERNAL-IP   OS-IMAGE                KERNEL-VERSION                CONTAINER-RUNTIME
machinedev002687.samarthya.me   Ready    <none>                 41d    v1.22.4   10.80.120.188   <none>        CentOS Linux 7 (Core)   3.10.0-1127.13.1.el7.x86_64   docker://20.10.12
machinedev003277.samarthya.me   Ready    <none>                 130d   v1.23.1   10.80.120.148   <none>        CentOS Linux 7 (Core)   3.10.0-1160.45.1.el7.x86_64   docker://20.10.12
machinedev003278.samarthya.me   Ready    <none>                 130d   v1.23.1   10.80.120.149   <none>        CentOS Linux 7 (Core)   3.10.0-1160.45.1.el7.x86_64   docker://20.10.12
machinedev003968.samarthya.me   Ready    <none>                 130d   v1.23.1   10.80.241.70    <none>        CentOS Linux 7 (Core)   3.10.0-1160.45.1.el7.x86_64   docker://20.10.12
machineqa003969.samarthya.me    Ready    control-plane,master   130d   v1.23.1   10.80.241.78    <none>        CentOS Linux 7 (Core)   3.10.0-1160.45.1.el7.x86_64   docker://20.10.12
machineqa003970.samarthya.me    Ready    <none>                 130d   v1.23.1   10.80.241.80    <none>        CentOS Linux 7 (Core)   3.10.0-1160.45.1.el7.x86_64   docker://20.10.12
```

## Step 3: Upgrade the node

### Step 3.1 Drain the node `machinedev002687.samarthya.me` for upgrade

```text
root@master>k drain machinedev002687.samarthya.me --ignore-daemonsets
node/machinedev002687.samarthya.me cordoned
WARNING: ignoring DaemonSet-managed Pods: default/kubernetes-ingress-z6m8x, ingress/haproxy-kubernetes-ingress-6jfnn, kube-system/calico-node-6nx7r, kube-system/kube-proxy-n6mgh
evicting pod kube-system/coredns-64897985d-tvr5s
evicting pod cert-manager/cert-manager-webhook-9cb88bd6d-lsh8f
evicting pod cert-manager/cert-manager-57d89b9548-shqzc
evicting pod ingress/haproxy-kubernetes-ingress-default-backend-7c55f74d7f-5pcwj
evicting pod ingress/haproxy-kubernetes-ingress-default-backend-7c55f74d7f-7vgr8
pod/haproxy-kubernetes-ingress-default-backend-7c55f74d7f-5pcwj evicted
pod/cert-manager-webhook-9cb88bd6d-lsh8f evicted
pod/cert-manager-57d89b9548-shqzc evicted
pod/haproxy-kubernetes-ingress-default-backend-7c55f74d7f-7vgr8 evicted
pod/coredns-64897985d-tvr5s evicted
node/machinedev002687.samarthya.me drained
```

### Step 3.2 Upgrade the `kubeadm` on the node

```text
[root@node5 ~]# yum install -y kubeadm-1.23.1 --disableexcludes=kubernetes
Loaded plugins: fastestmirror, langpacks, product-id, search-disabled-repos, subscription-manager

This system is not registered with an entitlement server. You can use subscription-manager to register.

Loading mirror speeds from cached hostfile
 * base: centos.excellmedia.net
 * epel: mirror.datto.com
 * extras: centos.excellmedia.net
 * updates: centos.excellmedia.net
Resolving Dependencies
--> Running transaction check
---> Package kubeadm.x86_64 0:1.22.4-0 will be updated
---> Package kubeadm.x86_64 0:1.23.1-0 will be an update
--> Finished Dependency Resolution

Dependencies Resolved

========================================================================================================================================================================================================================================
 Package                                                Arch                                                  Version                                                   Repository                                                 Size
========================================================================================================================================================================================================================================
Updating:
 kubeadm                                                x86_64                                                1.23.1-0                                                  kubernetes                                                9.0 M

Transaction Summary
========================================================================================================================================================================================================================================
Upgrade  1 Package

Total download size: 9.0 M
Downloading packages:
No Presto metadata available for kubernetes
0ec1322286c077c3dd975de1098d4c938b359fb59d961f0c7ce1b35bdc98a96c-kubeadm-1.23.1-0.x86_64.rpm                                                                                                                     | 9.0 MB  00:00:03     
Running transaction check
Running transaction test
Transaction test succeeded
Running transaction
  Updating   : kubeadm-1.23.1-0.x86_64                                                                                                                                                                                              1/2 
  Cleanup    : kubeadm-1.22.4-0.x86_64                                                                                                                                                                                              2/2 
  Verifying  : kubeadm-1.23.1-0.x86_64                                                                                                                                                                                              1/2 
  Verifying  : kubeadm-1.22.4-0.x86_64                                                                                                                                                                                              2/2 

Updated:
  kubeadm.x86_64 0:1.23.1-0                                                                                                                                                                                                             

Complete!
```

### Step 3.3 Upgrade `kubelet` & `kubectl`

```text
[root@node5 ~]# yum install -y kubelet-1.23.1 kubectl-1.23.1 --disableexcludes=kubernetes
Loaded plugins: fastestmirror, langpacks, product-id, search-disabled-repos, subscription-manager

This system is not registered with an entitlement server. You can use subscription-manager to register.

Loading mirror speeds from cached hostfile
 * base: centos.excellmedia.net
 * epel: mirror.datto.com
 * extras: centos.excellmedia.net
 * updates: centos.excellmedia.net
Resolving Dependencies
--> Running transaction check
---> Package kubectl.x86_64 0:1.22.4-0 will be updated
---> Package kubectl.x86_64 0:1.23.1-0 will be an update
---> Package kubelet.x86_64 0:1.22.4-0 will be updated
---> Package kubelet.x86_64 0:1.23.1-0 will be an update
--> Finished Dependency Resolution

Dependencies Resolved

========================================================================================================================================================================================================================================
 Package                                                Arch                                                  Version                                                   Repository                                                 Size
========================================================================================================================================================================================================================================
Updating:
 kubectl                                                x86_64                                                1.23.1-0                                                  kubernetes                                                9.5 M
 kubelet                                                x86_64                                                1.23.1-0                                                  kubernetes                                                 21 M

Transaction Summary
========================================================================================================================================================================================================================================
Upgrade  2 Packages

Total download size: 30 M
Downloading packages:
No Presto metadata available for kubernetes
(1/2): 8d4a11b0303bf2844b69fc4740c2e2f3b14571c0965534d76589a4940b6fafb6-kubectl-1.23.1-0.x86_64.rpm                                                                                                              | 9.5 MB  00:00:03     
(2/2): 7a203c8509258e0c79c8c704406b2d8f7d1af8ff93eadaa76b44bb8e9f9cbabd-kubelet-1.23.1-0.x86_64.rpm                                                                                                              |  21 MB  00:00:05     
----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
Total                                                                                                                                                                                                   5.8 MB/s |  30 MB  00:00:05     
Running transaction check
Running transaction test
Transaction test succeeded
Running transaction
  Updating   : kubectl-1.23.1-0.x86_64                                                                                                                                                                                              1/4 
  Updating   : kubelet-1.23.1-0.x86_64                                                                                                                                                                                              2/4 
  Cleanup    : kubectl-1.22.4-0.x86_64                                                                                                                                                                                              3/4 
  Cleanup    : kubelet-1.22.4-0.x86_64                                                                                                                                                                                              4/4 
  Verifying  : kubelet-1.23.1-0.x86_64                                                                                                                                                                                              1/4 
  Verifying  : kubectl-1.23.1-0.x86_64                                                                                                                                                                                              2/4 
  Verifying  : kubelet-1.22.4-0.x86_64                                                                                                                                                                                              3/4 
  Verifying  : kubectl-1.22.4-0.x86_64                                                                                                                                                                                              4/4 

Updated:
  kubectl.x86_64 0:1.23.1-0                                                                                          kubelet.x86_64 0:1.23.1-0                                                                                         

Complete!
```

reload & restart kubelet.

```text
[root@node5 ~]# sudo systemctl daemon-reload
[root@node5 ~]# sudo systemctl restart kubelet
```

### Step 3.4 Bring the node back online

```text
root@master>kubectl uncordon machinedev002687.samarthya.me
node/machinedev002687.samarthya.me uncordoned
```

## Step 4: Check the nodes `k get nodes -owide`

```text
root@master>k get nodes
NAME                           STATUS   ROLES                  AGE    VERSION
machinedev002687.samarthya.me  Ready    <none>                 41d    v1.23.1
machinedev003277.samarthya.me  Ready    <none>                 130d   v1.23.1
machinedev003278.samarthya.me  Ready    <none>                 130d   v1.23.1
machinedev003968.samarthya.me  Ready    <none>                 130d   v1.23.1
machineqa003969.samarthya.me   Ready    control-plane,master   130d   v1.23.1
machineqa003970.samarthya.me   Ready    <none>                 130d   v1.23.1
```
