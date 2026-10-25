---
title: "PV, PVC"
date: "2020-07-15"
slug: "pv-pvc"
categories: ["technical"]
tags: ["k8s"]
aliases: ["/wps/2020/07/15/pv-pvc/", "/wps/2026/10/23/pv-pvc/"]
wp_id: 805
---

## PV and PVC: PersistentVolume and PersistentVolumeClaim

PV - Defines the structure for provisioning storage for use. They have a defined lifecycle, independent of any individual Pod that uses the PV.

> A *PersistentVolume* (PV) is a piece of storage in the cluster that has been provisioned by an administrator or dynamically provisioned using [Storage Classes](https://kubernetes.io/docs/concepts/storage/storage-classes/).

A related concept of Storage Classes - describes the `profile` of the type of storage. Each storage class contains

- provisioner
- parameter
- reclaimPolicy

Once the name and other parameters of a storage class are defined while creating the objects, it cannot be updated once they are created.

```text
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: esdatadir
provisioner: kubernetes.io/no-provisioner
volumeBindingMode: WaitForFirstConsumer
```

PVC - Defines the structure for using the provisioned storage.

> A *PersistentVolumeClaim* (PVC) is a request for storage by a user.

## References

- https://kubernetes.io/docs/concepts/storage/storage-classes/
- https://kubernetes.io/docs/concepts/storage/storage-classes/#provisioner
