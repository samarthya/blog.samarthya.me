---
title: "Quick: Cheat Sheet"
date: "2021-01-08T11:04:34Z"
slug: "quick-cheat-sheet"
categories: ["docker", "technical"]
tags: ["cluster", "k8s", "kubeadm", "ubuntu"]
aliases: ["/wps/2021/01/08/quick-cheat-sheet/"]
wp_id: 1221
---

A cheat sheet for Installing K8S cluster.

## Step1:

```text
Check your OS?
```

- `cat /etc/issue`
- `lsb_release -a`

## Step 2:

Add the GPG key as described [here](https://docs.docker.com/engine/install/ubuntu/)

```text
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
```

## Step 3:

Add repository

```text
sudo add-apt-repository \
   "deb [arch=amd64] https://download.docker.com/linux/ubuntu \
   $(lsb_release -cs) \
   stable"
```

## Step 4:

GPG for K8S as mentioned [here](https://kubernetes.io/docs/setup/production-environment/tools/kubeadm/install-kubeadm/)

```text
curl -s https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo apt-key add -
```

add the repostiory too

```text
cat <<EOF | sudo tee /etc/apt/sources.list.d/kubernetes.list
deb https://apt.kubernetes.io/ kubernetes-xenial main
EOF
```

## Step 5:

Run apt update

`sudo apt-get update`

## Step 6:

Installing latest can be accomplished by using

```text
sudo apt-get install -y kubelet kubeadm kubectl
sudo apt-mark hold kubelet kubeadm kubectl
```

I did a specific version

```text
sudo apt install -y docker-ce=5:19.03.10~3-0~ubuntu-focal kubelet=1.18.5-00 kubeadm=1.18.5-00 kubectl=1.18.5-00
```

## Step 7:

Depending on which third-party provider you choose, you might need to set the `--pod-network-cidr` to a provider-specific value. See [Installing a Pod network add-on](https://kubernetes.io/docs/setup/production-environment/tools/kubeadm/create-cluster-kubeadm/#pod-network).

{{< lead >}}
Choose a Pod network add-on, and verify whether it requires any arguments to be passed to `kubeadm init`.
{{< /lead >}}

```text
sudo kubeadm init --pod-network-cidr=10.244.0.0/16
```

It might give an output at the end like this

```text
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

kubeadm join 10.0.1.101:6443 --token 0s94g0.l7q69nvf7jwa2vxm \
    --discovery-token-ca-cert-hash sha256:559f153599b382e2a4551b15360e111cca40bde56889448eedce0c6ae733b0e4
```

## Step 8:

Follow the steps before you can use cluster as mentioned in output and keep not of the join command

```text
mkdir -p $HOME/.kube
sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
sudo chown $(id -u):$(id -g) $HOME/.kube/config
```

Do not issue the join command on the master node, as it is meant for nodes.

Follow `Step 1 - 6` on the machines that you want to be part of the cluster

```text
kubeadm join 10.0.1.101:6443 --token 0s94g0.l7q69nvf7jwa2vxm \
    --discovery-token-ca-cert-hash sha256:559f153599b382e2a4551b15360e111cca40bde56889448eedce0c6ae733b0e4
```

## Step 9:

Install network-add on.

{{< lead >}}
**Note:** Currently Calico is the only CNI plugin that the kubeadm project performs e2e tests against. If you find an issue related to a CNI plugin you should log a ticket in its respective issue tracker instead of the kubeadm or kubernetes issue trackers.
{{< /lead >}}

```text
 kubectl apply -f https://docs.projectcalico.org/v3.14/manifests/calico.yaml
```

## Step 10:

On node machines use the join command to join the cluster. It would show an output at the end like below

```text
[kubelet-start] Downloading configuration for the kubelet from the "kubelet-config-1.18" ConfigMap in the kube-system namespace
[kubelet-start] Writing kubelet configuration to file "/var/lib/kubelet/config.yaml"
[kubelet-start] Writing kubelet environment file with flags to file "/var/lib/kubelet/kubeadm-flags.env"
[kubelet-start] Starting the kubelet
[kubelet-start] Waiting for the kubelet to perform the TLS Bootstrap...

This node has joined the cluster:
* Certificate signing request was sent to apiserver and a response was received.
* The Kubelet was informed of the new secure connection details.

Run 'kubectl get nodes' on the control-plane to see this node join the cluster.
```

## Conclusion

Check for the nodes joining the cluster using

```text
kubectl get nodes
NAME            STATUS   ROLES    AGE   VERSION
ip-10-0-1-101   Ready    master   28m   v1.18.5
ip-10-0-1-102   Ready    <none>   26m   v1.18.5
ip-10-0-1-103   Ready    <none>   26m   v1.18.5
```

You can also follow it up by creating a quick deployment using the NGINX image as below

```text
kubectl create deployment nginx --image=nginx
```

```text
kubectl get deploy
NAME    READY   UP-TO-DATE   AVAILABLE   AGE
nginx   1/1     1            1           29m
```

```text
kubectl get pods
NAME                    READY   STATUS    RESTARTS   AGE
nginx-f89759699-hqvcm   1/1     Running   0          30m
```

Try exposing the port

```text
kubectl expose --help
```
