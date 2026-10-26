---
title: "Adding Node to a cluster"
date: "2022-01-06T06:58:31Z"
slug: "adding-node-to-a-cluster"
categories: ["kubernetes", "technical"]
tags: ["cluster", "k8s", "new", "node"]
aliases: ["/wps/2022/01/06/adding-node-to-a-cluster/"]
wp_id: 1881
---

In this blog, I will try add a new node to the already running cluster.

## My Cluster

```text

root@master>k get nodes
NAME                              STATUS   ROLES                  AGE     VERSION
mydevmachine001830.samarthya.me   Ready    <none>                 22h     v1.23.1
mydevmachine002687.samarthya.me   Ready    <none>                 41d     v1.23.1
mydevmachine003277.samarthya.me   Ready    <none>                 131d    v1.23.1
mydevmachine003278.samarthya.me   Ready    <none>                 131d    v1.23.1
mydevmachine003417.samarthya.me   Ready    <none>                 4m55s   v1.23.1
mydevmachine003968.samarthya.me   Ready    <none>                 131d    v1.23.1
mydevmachine003969.samarthya.me   Ready    control-plane,master   131d    v1.23.1
mydevmachine003970.samarthya.me   Ready    <none>                 131d    v1.23.1
mydevmachine003979.samarthya.me   Ready    <none>                 29m     v1.23.1
```

## Steps to follow

- Install `docker`
- Install `kubeadm`, `kubectl` & `kubelet`
- Join the cluster using the token
- Check the node has joined the cluster

### Step 1: Install docker

```text
sudo yum install -y yum-utils
sudo yum-config-manager \
    --add-repo \
    https://download.docker.com/linux/centos/docker-ce.repo
```

When adding repo make sure the repo has been added successfully to the machine

```text
Loaded plugins: fastestmirror, langpacks
adding repo from: https://download.docker.com/linux/centos/docker-ce.repo
grabbing file https://download.docker.com/linux/centos/docker-ce.repo to /etc/yum.repos.d/docker-ce.repo
repo saved to /etc/yum.repos.d/docker-ce.repo
```

### Install the docker

```text
sudo yum install docker-ce docker-ce-cli containerd.io
```

You may see the output as under

```text
Total                                                                                                                                                                                                    14 MB/s |  93 MB  00:00:06     
Retrieving key from https://download.docker.com/linux/centos/gpg
Importing GPG key 0x621E9F35:
 Userid     : "Docker Release (CE rpm) <docker@docker.com>"
 Fingerprint: 060a 61c5 1b55 8a7f 742b 77aa c52f eb6b 621e 9f35
 From       : https://download.docker.com/linux/centos/gpg
Is this ok [y/N]: y
Running transaction check
Running transaction test
Transaction test succeeded
Running transaction
  Installing : docker-scan-plugin-0.12.0-3.el7.x86_64                                                                                                                                                                               1/9 
  Installing : 1:docker-ce-cli-20.10.12-3.el7.x86_64                                                                                                                                                                                2/9 
  Installing : 2:container-selinux-2.119.2-1.911c772.el7_8.noarch                                                                                                                                                                   3/9 
  Installing : containerd.io-1.4.12-3.1.el7.x86_64                                                                                                                                                                                  4/9 
  Installing : slirp4netns-0.4.3-4.el7_8.x86_64                                                                                                                                                                                     5/9 
  Installing : fuse3-libs-3.6.1-4.el7.x86_64                                                                                                                                                                                        6/9 
  Installing : fuse-overlayfs-0.7.2-6.el7_8.x86_64                                                                                                                                                                                  7/9 
  Installing : 3:docker-ce-20.10.12-3.el7.x86_64                                                                                                                                                                                    8/9 
  Installing : docker-ce-rootless-extras-20.10.12-3.el7.x86_64                                                                                                                                                                      9/9 
  Verifying  : fuse3-libs-3.6.1-4.el7.x86_64                                                                                                                                                                                        1/9 
  Verifying  : 1:docker-ce-cli-20.10.12-3.el7.x86_64                                                                                                                                                                                2/9 
  Verifying  : fuse-overlayfs-0.7.2-6.el7_8.x86_64                                                                                                                                                                                  3/9 
  Verifying  : docker-scan-plugin-0.12.0-3.el7.x86_64                                                                                                                                                                               4/9 
  Verifying  : slirp4netns-0.4.3-4.el7_8.x86_64                                                                                                                                                                                     5/9 
  Verifying  : 2:container-selinux-2.119.2-1.911c772.el7_8.noarch                                                                                                                                                                   6/9 
  Verifying  : docker-ce-rootless-extras-20.10.12-3.el7.x86_64                                                                                                                                                                      7/9 
  Verifying  : containerd.io-1.4.12-3.1.el7.x86_64                                                                                                                                                                                  8/9 
  Verifying  : 3:docker-ce-20.10.12-3.el7.x86_64                                                                                                                                                                                    9/9 

Installed:
  containerd.io.x86_64 0:1.4.12-3.1.el7                                         docker-ce.x86_64 3:20.10.12-3.el7                                         docker-ce-cli.x86_64 1:20.10.12-3.el7                                        

Dependency Installed:
  container-selinux.noarch 2:2.119.2-1.911c772.el7_8    docker-ce-rootless-extras.x86_64 0:20.10.12-3.el7    docker-scan-plugin.x86_64 0:0.12.0-3.el7    fuse-overlayfs.x86_64 0:0.7.2-6.el7_8    fuse3-libs.x86_64 0:3.6.1-4.el7   
  slirp4netns.x86_64 0:0.4.3-4.el7_8                   

Complete!
```

This marks docker installation as complete. Time to enable the docker, and run it.

```text
> systemctl enable docker
Created symlink from /etc/systemd/system/multi-user.target.wants/docker.service to /usr/lib/systemd/system/docker.service.
```

I am going to configure `systemd` as the `cgroupdriver` so will configure the `daemon.json` for the same; first lets start the docker and then configure the file `/etc/docker/daemon.json` as under

```text
{
  "exec-opts": ["native.cgroupdriver=systemd"]
}
```

Restart the docker and check the `docker info` status

```text
Client:
 Context:    default
 Debug Mode: false
 Plugins:
  app: Docker App (Docker Inc., v0.9.1-beta3)
  buildx: Docker Buildx (Docker Inc., v0.7.1-docker)
  scan: Docker Scan (Docker Inc., v0.12.0)

Server:
 Containers: 20
  Running: 8
  Paused: 0
  Stopped: 12
 Images: 6
 Server Version: 20.10.12
 Storage Driver: overlay2
  Backing Filesystem: xfs
  Supports d_type: true
  Native Overlay Diff: true
  userxattr: false
 Logging Driver: json-file
 Cgroup Driver: systemd
```

### Step 2: Install `Kubeadm` & others

Configure the repository first

```text
cat <<EOF > /etc/yum.repos.d/kubernetes.repo
[kubernetes]
name=Kubernetes
baseurl=https://packages.cloud.google.com/yum/repos/kubernetes-el7-x86_64
enabled=1
gpgcheck=1
repo_gpgcheck=1
gpgkey=https://packages.cloud.google.com/yum/doc/yum-key.gpg https://packages.cloud.google.com/yum/doc/rpm-package-key.gpg
EOF
```

### Install `kubeadm`

```text
yum install -y kubeadm-1.23.1
```

It will show an output as under

```text
Running transaction
  Installing : libnetfilter_cthelper-1.0.0-11.el7.x86_64                                                                                                                                                                           1/10 
  Installing : socat-1.7.3.2-2.el7.x86_64                                                                                                                                                                                          2/10 
  Installing : libnetfilter_cttimeout-1.0.0-7.el7.x86_64                                                                                                                                                                           3/10 
  Installing : kubectl-1.23.1-0.x86_64                                                                                                                                                                                             4/10 
  Installing : libnetfilter_queue-1.0.2-2.el7_2.x86_64                                                                                                                                                                             5/10 
  Installing : conntrack-tools-1.4.4-7.el7.x86_64                                                                                                                                                                                  6/10 
  Installing : kubernetes-cni-0.8.7-0.x86_64                                                                                                                                                                                       7/10 
  Installing : kubelet-1.23.1-0.x86_64                                                                                                                                                                                             8/10 
  Installing : cri-tools-1.19.0-0.x86_64                                                                                                                                                                                           9/10 
  Installing : kubeadm-1.23.1-0.x86_64                                                                                                                                                                                            10/10 
  Verifying  : cri-tools-1.19.0-0.x86_64                                                                                                                                                                                           1/10 
  Verifying  : kubeadm-1.23.1-0.x86_64                                                                                                                                                                                             2/10 
  Verifying  : kubelet-1.23.1-0.x86_64                                                                                                                                                                                             3/10 
  Verifying  : conntrack-tools-1.4.4-7.el7.x86_64                                                                                                                                                                                  4/10 
  Verifying  : kubernetes-cni-0.8.7-0.x86_64                                                                                                                                                                                       5/10 
  Verifying  : libnetfilter_queue-1.0.2-2.el7_2.x86_64                                                                                                                                                                             6/10 
  Verifying  : kubectl-1.23.1-0.x86_64                                                                                                                                                                                             7/10 
  Verifying  : libnetfilter_cttimeout-1.0.0-7.el7.x86_64                                                                                                                                                                           8/10 
  Verifying  : socat-1.7.3.2-2.el7.x86_64                                                                                                                                                                                          9/10 
  Verifying  : libnetfilter_cthelper-1.0.0-11.el7.x86_64                                                                                                                                                                          10/10 

Installed:
  kubeadm.x86_64 0:1.23.1-0                                                                                                                                                                                                             

Dependency Installed:
  conntrack-tools.x86_64 0:1.4.4-7.el7          cri-tools.x86_64 0:1.19.0-0                 kubectl.x86_64 0:1.23.1-0      kubelet.x86_64 0:1.23.1-0   kubernetes-cni.x86_64 0:0.8.7-0   libnetfilter_cthelper.x86_64 0:1.0.0-11.el7  
  libnetfilter_cttimeout.x86_64 0:1.0.0-7.el7   libnetfilter_queue.x86_64 0:1.0.2-2.el7_2   socat.x86_64 0:1.7.3.2-2.el7  

Complete!
```

### Install the `kubelet` and `kubectl`

```text
yum install -y kubelet-1.23.1 kubectl-1.23.1
```

If the `kubeadm` was installed successfully it should already be installed.

### Enable the kubelet

```text
> systemctl enable kubelet

Created symlink from /etc/systemd/system/multi-user.target.wants/kubelet.service to /usr/lib/systemd/system/kubelet.service.
```

Now time to join the cluster using the `token`

```text
kubeadm join 10.80.241.78:6443 --token MYTOKENFROMKUBEMASTER  --discovery-token-ca-cert-hash sha256:HASHGENERATED
```

Most likely it should sail through but in case you see errors like under

```text
[preflight] Running pre-flight checks
[preflight] Reading configuration from the cluster...
[preflight] FYI: You can look at this config file with 'kubectl -n kube-system get cm kubeadm-config -o yaml'
[kubelet-start] Writing kubelet configuration to file "/var/lib/kubelet/config.yaml"
[kubelet-start] Writing kubelet environment file with flags to file "/var/lib/kubelet/kubeadm-flags.env"
[kubelet-start] Starting the kubelet
[kubelet-start] Waiting for the kubelet to perform the TLS Bootstrap...
[kubelet-check] Initial timeout of 40s passed.
[kubelet-check] It seems like the kubelet isn't running or healthy.
[kubelet-check] The HTTP call equal to 'curl -sSL http://localhost:10248/healthz' failed with error: Get "http://localhost:10248/healthz": dial tcp [::1]:10248: connect: connection refused.
[kubelet-check] It seems like the kubelet isn't running or healthy.
[kubelet-check] The HTTP call equal to 'curl -sSL http://localhost:10248/healthz' failed with error: Get "http://localhost:10248/healthz": dial tcp [::1]:10248: connect: connection refused.
[kubelet-check] It seems like the kubelet isn't running or healthy.
[kubelet-check] The HTTP call equal to 'curl -sSL http://localhost:10248/healthz' failed with error: Get "http://localhost:10248/healthz": dial tcp [::1]:10248: connect: connection refused.
[kubelet-check] It seems like the kubelet isn't running or healthy.
[kubelet-check] The HTTP call equal to 'curl -sSL http://localhost:10248/healthz' failed with error: Get "http://localhost:10248/healthz": dial tcp [::1]:10248: connect: connection refused.
[kubelet-check] It seems like the kubelet isn't running or healthy.
[kubelet-check] The HTTP call equal to 'curl -sSL http://localhost:10248/healthz' failed with error: Get "http://localhost:10248/healthz": dial tcp [::1]:10248: connect: connection refused.
error execution phase kubelet-start: error uploading crisocket: nodes "ibndev004518.bpc.broadcom.net" not found
To see the stack trace of this error execute with --v=5 or higher
```

You can refer to this [blog]({{< relref "/posts/calico-cni-failures" >}}) to how to allow it. In case you need to run the command again, first you will have to reset

using `kubeadm reset`

```text
kubeadm reset
[reset] WARNING: Changes made to this host by 'kubeadm init' or 'kubeadm join' will be reverted.
[reset] Are you sure you want to proceed? [y/N]: y
[preflight] Running pre-flight checks
W0106 06:29:42.289836  119690 removeetcdmember.go:80] [reset] No kubeadm config, using etcd pod spec to get data directory
[reset] No etcd config found. Assuming external etcd
[reset] Please, manually reset etcd to prevent further issues
[reset] Stopping the kubelet service
[reset] Unmounting mounted directories in "/var/lib/kubelet"
[reset] Deleting contents of config directories: [/etc/kubernetes/manifests /etc/kubernetes/pki]
[reset] Deleting files: [/etc/kubernetes/admin.conf /etc/kubernetes/kubelet.conf /etc/kubernetes/bootstrap-kubelet.conf /etc/kubernetes/controller-manager.conf /etc/kubernetes/scheduler.conf]
[reset] Deleting contents of stateful directories: [/var/lib/kubelet /var/lib/dockershim /var/run/kubernetes /var/lib/cni]

The reset process does not clean CNI configuration. To do so, you must remove /etc/cni/net.d

The reset process does not reset or clean up iptables rules or IPVS tables.
If you wish to reset iptables, you must do so manually by using the "iptables" command.

If your cluster was setup to utilize IPVS, run ipvsadm --clear (or similar)
to reset your system's IPVS tables.

The reset process does not clean your kubeconfig files and you must remove them manually.
Please, check the contents of the $HOME/.kube/config file.
```

and then run the `kubeadm join` again. If all goes well you should see a message like below

```text
[preflight] Running pre-flight checks
[preflight] Reading configuration from the cluster...
[preflight] FYI: You can look at this config file with 'kubectl -n kube-system get cm kubeadm-config -o yaml'
[kubelet-start] Writing kubelet configuration to file "/var/lib/kubelet/config.yaml"
[kubelet-start] Writing kubelet environment file with flags to file "/var/lib/kubelet/kubeadm-flags.env"
[kubelet-start] Starting the kubelet
[kubelet-start] Waiting for the kubelet to perform the TLS Bootstrap...

This node has joined the cluster:
* Certificate signing request was sent to apiserver and a response was received.
* The Kubelet was informed of the new secure connection details.

Run 'kubectl get nodes' on the control-plane to see this node join the cluster.
```

The cluster looks like below now

```text
root@master>k get nodes
NAME                              STATUS   ROLES                  AGE     VERSION
mydevmachine004518.samarthya.me   Ready    <none>                 55s     v1.23.1
mydevmachine001830.samarthya.me   Ready    <none>                 22h     v1.23.1
mydevmachine002687.samarthya.me   Ready    <none>                 41d     v1.23.1
mydevmachine003277.samarthya.me   Ready    <none>                 131d    v1.23.1
mydevmachine003278.samarthya.me   Ready    <none>                 131d    v1.23.1
mydevmachine003417.samarthya.me   Ready    <none>                 4m55s   v1.23.1
mydevmachine003968.samarthya.me   Ready    <none>                 131d    v1.23.1
mydevmachine003969.samarthya.me   Ready    control-plane,master   131d    v1.23.1
mydevmachine003970.samarthya.me   Ready    <none>                 131d    v1.23.1
mydevmachine003979.samarthya.me   Ready    <none>                 29m     v1.23.1
```

{{< lead >}}
Do lookout for `selinux` settings if it is enforcing you might have to change it before you try joining the cluster
{{< /lead >}}

In my case the selinux was enforcing so I had to do like below

```text
[root@mydevmachine004518 ~]# getenforce
Enforcing 
[root@mydevmachine004518 ~]# setenforce 0
[root@mydevmachine004518 ~]# getenforce 
Permissive

[root@mydevmachine004518 ~]# cat /etc/selinux/config 

# This file controls the state of SELinux on the system.
# SELINUX= can take one of these three values:
#     enforcing - SELinux security policy is enforced.
#     permissive - SELinux prints warnings instead of enforcing.
#     disabled - No SELinux policy is loaded.
SELINUX=enforcing
# SELINUXTYPE= can take one of three values:
#     targeted - Targeted processes are protected,
#     minimum - Modification of targeted policy. Only selected processes are protected. 
#     mls - Multi Level Security protection.
SELINUXTYPE=targeted

[root@mydevmachine004518 ~]# sed -i 's/^SELINUX=enforcing$/SELINUX=permissive/' /etc/selinux/config
[root@mydevmachine004518 ~]# cat /etc/selinux/config 

# This file controls the state of SELinux on the system.
# SELINUX= can take one of these three values:
#     enforcing - SELinux security policy is enforced.
#     permissive - SELinux prints warnings instead of enforcing.
#     disabled - No SELinux policy is loaded.
SELINUX=permissive
# SELINUXTYPE= can take one of three values:
#     targeted - Targeted processes are protected,
#     minimum - Modification of targeted policy. Only selected processes are protected. 
#     mls - Multi Level Security protection.
SELINUXTYPE=targeted
```

I also edited the `/etc/sysconfig/syslinux`

```text

# This file controls the state of SELinux on the system.
# SELINUX= can take one of these three values:
#     enforcing - SELinux security policy is enforced.
#     permissive - SELinux prints warnings instead of enforcing.
#     disabled - No SELinux policy is loaded.
SELINUX=disabled
# SELINUXTYPE= can take one of three values:
#     targeted - Targeted processes are protected,
#     minimum - Modification of targeted policy. Only selected processes are protected.
#     mls - Multi Level Security protection.
SELINUXTYPE=targeted
```

Reboot is recommended for a better success.

> 🎉 Finally!
