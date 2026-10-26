---
title: "Installing K8S on Ubuntu"
date: "2020-12-14"
slug: "installing-k8s-on-ubuntu"
description: "Step by step: installing Docker, kubeadm, kubelet and kubectl on Ubuntu 18.04, initialising the control plane and joining worker nodes."
categories: ["docker", "technical"]
tags: ["k8s", "ubuntu"]
aliases: ["/wps/2020/12/14/installing-k8s-on-ubuntu/", "/wps/2026/10/23/installing-k8s-on-ubuntu/"]
wp_id: 1169
---

Install docker

```text
cat /etc/issue
Ubuntu 18.04.4 LTS \n \l
```

```text
sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu \
$(lsb_release -cs) \
stable"
```

```text
sudo apt-get update
```

```text
sudo apt-get install -y docker-ce=18.06.1~ce~3-0~ubuntu
```

```text
sudo apt-mark hold docker-ce
```

```text
apt-mark --help
apt 1.6.12ubuntu0.2 (amd64)
Usage: apt-mark [options] {auto|manual} pkg1 [pkg2 ...]

apt-mark is a simple command line interface for marking packages
as manually or automatically installed. It can also be used to
manipulate the dpkg(1) selection states of packages, and to list
all packages with or without a certain marking.
```

```text
lsb_release -c
Codename:       bionic
```

```text
lsb_release -cs
bionic
```

```text
systemctl status docker
● docker.service - Docker Application Container Engine
   Loaded: loaded (/lib/systemd/system/docker.service; enabled; vendor preset: enabled)
   Active: active (running) since Mon 2020-12-14 09:05:39 UTC; 45s ago
     Docs: https://docs.docker.com
 Main PID: 662 (dockerd)
    Tasks: 21
   CGroup: /system.slice/docker.service
           ├─662 /usr/bin/dockerd -H fd://
           └─685 docker-containerd --config /var/run/docker/containerd/containerd.toml

Dec 14 09:05:39 ip-10-0-1-101 dockerd[662]: time="2020-12-14T09:05:39.297237656Z" level=info msg="ClientConn switching balancer to \"pick_first\"" module=grpc
Dec 14 09:05:39 ip-10-0-1-101 dockerd[662]: time="2020-12-14T09:05:39.297281586Z" level=info msg="pickfirstBalancer: HandleSubConnStateChange: 0xc4201b7df0, CONNECTING" module=grpc
Dec 14 09:05:39 ip-10-0-1-101 dockerd[662]: time="2020-12-14T09:05:39.297797167Z" level=info msg="pickfirstBalancer: HandleSubConnStateChange: 0xc4201b7df0, READY" module=grpc
Dec 14 09:05:39 ip-10-0-1-101 dockerd[662]: time="2020-12-14T09:05:39.297852837Z" level=info msg="Loading containers: start."
Dec 14 09:05:39 ip-10-0-1-101 dockerd[662]: time="2020-12-14T09:05:39.596242360Z" level=info msg="Default bridge (docker0) is assigned with an IP address 172.17.0.0/16. Daemon option --bip can be used to set a preferred IP addres
Dec 14 09:05:39 ip-10-0-1-101 dockerd[662]: time="2020-12-14T09:05:39.753685539Z" level=info msg="Loading containers: done."
Dec 14 09:05:39 ip-10-0-1-101 dockerd[662]: time="2020-12-14T09:05:39.822291121Z" level=info msg="Docker daemon" commit=e68fc7a graphdriver(s)=overlay2 version=18.06.1-ce
Dec 14 09:05:39 ip-10-0-1-101 dockerd[662]: time="2020-12-14T09:05:39.822430053Z" level=info msg="Daemon has completed initialization"
Dec 14 09:05:39 ip-10-0-1-101 dockerd[662]: time="2020-12-14T09:05:39.853660664Z" level=info msg="API listen on /var/run/docker.sock"
Dec 14 09:05:39 ip-10-0-1-101 systemd[1]: Started Docker Application Container Engine.
```

```text
curl -s https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo apt-key add -
cat << EOF | sudo tee /etc/apt/sources.list.d/kubernetes.list
deb https://apt.kubernetes.io/ kubernetes-xenial main
EOF
```

```text
sudo apt-get update
sudo apt-get install -y kubelet=1.14.5-00 kubeadm=1.14.5-00 kubectl=1.14.5-00
sudo apt-mark hold kubelet kubeadm kubectl
```

```text
sudo kubeadm init --pod-network-cidr=10.244.0.0/16
```

```text
I1214 09:10:37.236647    3055 version.go:240] remote version is much newer: v1.20.0; falling back to: stable-1.14
[init] Using Kubernetes version: v1.14.10
[preflight] Running pre-flight checks
        [WARNING IsDockerSystemdCheck]: detected "cgroupfs" as the Docker cgroup driver. The recommended driver is "systemd". Please follow the guide at https://kubernetes.io/docs/setup/cri/
[preflight] Pulling images required for setting up a Kubernetes cluster
[preflight] This might take a minute or two, depending on the speed of your internet connection
[preflight] You can also perform this action in beforehand using 'kubeadm config images pull'
[kubelet-start] Writing kubelet environment file with flags to file "/var/lib/kubelet/kubeadm-flags.env"
[kubelet-start] Writing kubelet configuration to file "/var/lib/kubelet/config.yaml"
[kubelet-start] Activating the kubelet service
[certs] Using certificateDir folder "/etc/kubernetes/pki"
[certs] Generating "etcd/ca" certificate and key
[certs] Generating "etcd/server" certificate and key
[certs] etcd/server serving cert is signed for DNS names [ip-10-0-1-101 localhost] and IPs [10.0.1.101 127.0.0.1 ::1]
[certs] Generating "etcd/peer" certificate and key
[certs] etcd/peer serving cert is signed for DNS names [ip-10-0-1-101 localhost] and IPs [10.0.1.101 127.0.0.1 ::1]
[certs] Generating "apiserver-etcd-client" certificate and key
[certs] Generating "etcd/healthcheck-client" certificate and key
[certs] Generating "ca" certificate and key
[certs] Generating "apiserver-kubelet-client" certificate and key
[certs] Generating "apiserver" certificate and key
[certs] apiserver serving cert is signed for DNS names [ip-10-0-1-101 kubernetes kubernetes.default kubernetes.default.svc kubernetes.default.svc.cluster.local] and IPs [10.96.0.1 10.0.1.101]
[certs] Generating "front-proxy-ca" certificate and key
[certs] Generating "front-proxy-client" certificate and key
[certs] Generating "sa" key and public key
[kubeconfig] Using kubeconfig folder "/etc/kubernetes"
[kubeconfig] Writing "admin.conf" kubeconfig file
[kubeconfig] Writing "kubelet.conf" kubeconfig file
[kubeconfig] Writing "controller-manager.conf" kubeconfig file
[kubeconfig] Writing "scheduler.conf" kubeconfig file
[control-plane] Using manifest folder "/etc/kubernetes/manifests"
[control-plane] Creating static Pod manifest for "kube-apiserver"
[control-plane] Creating static Pod manifest for "kube-controller-manager"
[control-plane] Creating static Pod manifest for "kube-scheduler"
[etcd] Creating static Pod manifest for local etcd in "/etc/kubernetes/manifests"
[wait-control-plane] Waiting for the kubelet to boot up the control plane as static Pods from directory "/etc/kubernetes/manifests". This can take up to 4m0s
[apiclient] All control plane components are healthy after 16.001809 seconds
[upload-config] storing the configuration used in ConfigMap "kubeadm-config" in the "kube-system" Namespace
[kubelet] Creating a ConfigMap "kubelet-config-1.14" in namespace kube-system with the configuration for the kubelets in the cluster
[upload-certs] Skipping phase. Please see --experimental-upload-certs
[mark-control-plane] Marking the node ip-10-0-1-101 as control-plane by adding the label "node-role.kubernetes.io/master=''"
[mark-control-plane] Marking the node ip-10-0-1-101 as control-plane by adding the taints [node-role.kubernetes.io/master:NoSchedule]
[bootstrap-token] Using token: xtpkvj.e81gaeg0v18shctg
[bootstrap-token] Configuring bootstrap tokens, cluster-info ConfigMap, RBAC Roles
[bootstrap-token] configured RBAC rules to allow Node Bootstrap tokens to post CSRs in order for nodes to get long term certificate credentials
[bootstrap-token] configured RBAC rules to allow the csrapprover controller automatically approve CSRs from a Node Bootstrap Token
[bootstrap-token] configured RBAC rules to allow certificate rotation for all node client certificates in the cluster
[bootstrap-token] creating the "cluster-info" ConfigMap in the "kube-public" namespace
[addons] Applied essential addon: CoreDNS
[addons] Applied essential addon: kube-proxy

Your Kubernetes control-plane has initialized successfully!

To start using your cluster, you need to run the following as a regular user:

  mkdir -p $HOME/.kube
  sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
  sudo chown $(id -u):$(id -g) $HOME/.kube/config

You should now deploy a pod network to the cluster.
Run "kubectl apply -f [podnetwork].yaml" with one of the options listed at:
  https://kubernetes.io/docs/concepts/cluster-administration/addons/

Then you can join any number of worker nodes by running the following on each as root:

kubeadm join 10.0.1.101:6443 --token xtpkvj.e81gaeg0v18shctg \
    --discovery-token-ca-cert-hash sha256:6c79fda4db86da060f083b35def6c39790c47f6533ab8f7ebb6ea30c2c2af6a3
```
