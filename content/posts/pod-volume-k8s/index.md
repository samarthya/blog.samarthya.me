---
title: "Pod & Volume: K8S"
date: "2021-01-22T10:19:46Z"
slug: "pod-volume-k8s"
categories: ["docker", "technical"]
tags: ["k8s", "pv", "pvc"]
aliases: ["/wps/2021/01/22/pod-volume-k8s/"]
wp_id: 1264
---

Everything in the same file

```text
apiVersion: v1
kind: Pod
metadata:
  name: redispod
spec:
  containers:
  - image: redis
    name: redisdb
    volumeMounts:
    - name: redis-data
      mountPath: /data
    ports:
    - containerPort: 6379
      protocol: TCP
  volumes:
  - name: redis-data
    persistentVolumeClaim:
      claimName: redisdb-pvc
---
apiVersion: v1
kind: PersistentVolume
metadata:
  name: redis-pv
spec:
  storageClassName: ""
  capacity:
    storage: 1Gi
  accessModes:
    - ReadWriteOnce
  hostPath:
    path: "/mnt/data"
---
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: redisdb-pvc
spec:
  storageClassName: ""
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 1Gi
```

If you deploy you will get something like

```text
k apply -f redis.yaml 
pod/redispod created
persistentvolume/redis-pv created
persistentvolumeclaim/redisdb-pvc created
```
