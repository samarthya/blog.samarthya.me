---
title: "ConfigMaps: K8S - 2"
date: "2020-08-21T12:24:01Z"
slug: "configmaps-k8s-2"
categories: ["technical"]
tags: ["configmap", "k8s"]
aliases: ["/wps/2020/08/21/configmaps-k8s-2/"]
wp_id: 932
---

We looked at using the environment variables using the configmap in the last [blog]({{< relref "/posts/configmap-k8s" >}}).

The config map remains the same but now in YAML.

```text
apiVersion: v1
kind: ConfigMap
metadata:
  name: happy-faces-mnt
data:
  data.values: |-
    my.name=samarthya
    my.profession=engineer
```

I will use this to mount it to a container and then see the contents of the file.

```text
apiVersion: v1
kind: Pod
metadata:
  name: happy-pod
spec:
  containers:
  - name: bbox-pod
    image: busybox:latest
    command: ['sh','-c',"echo hello world! && sleep 3600"]
    volumeMounts:
    - name: my-volume
      mountPath: /etc/values
      readOnly: true
  volumes:
  - name: my-volume
    configMap:
      name: happy-faces-mnt
```

Have added a `volume` and `mount`.

```text
volumes:
  - name: my-volume
    configMap:
      name: happy-faces-mnt
```

configMap listing for my machine is as under

```text
k get cm
NAME              DATA   AGE
happy-faces-mnt   1      36m
```

```text
k describe cm

Name:         happy-faces-mnt
Namespace:    default
Labels:       <none>
Annotations:  
Data
====
data.values:
----
my.name=samarthya
my.profession=engineer
Events:  <none>
```

Run the pod

```text
k get pods
NAME        READY   STATUS    RESTARTS   AGE
happy-pod   1/1     Running   0          8m21s
```

Check the mounted volume using

```text
k exec pod/happy-pod -- cat /etc/values/data.values
my.name=samarthya
my.profession=engineer
```

The content of the file are shown.
