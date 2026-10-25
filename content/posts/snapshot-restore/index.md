---
title: "Snapshot & Restore"
date: "2020-02-26T08:58:21Z"
slug: "snapshot-restore"
categories: ["technical"]
tags: ["devops", "elastic", "restore", "snapshot"]
aliases: ["/wps/2020/02/26/snapshot-restore/"]
wp_id: 454
---

If you have a production grade elastic cluster it is always recommended to do a regular backup as a standard practice.

> Snapshot is a backup of information, that can be be used to restore the last known good state of the system

In the context of elasticsearch you can take snapshot of an individual index or the whole cluster and it be either stored on local file system or on remote repositories like google cloud.

![Snapshot and Restore](screenshot-2020-02-26-at-1.03.51-pm.png "Snapshot and Restore")

If you navigate to Snapshot and Restore in Kibana-Management you are presented the UI to execute the backup.

<img src="screenshot-2020-02-26-at-1.05.31-pm.png" alt="" class="grid-w100" />

## Points to remember

- Snapshots are incremental in nature, delta of data not available in the previous snapshot is only stored.
- Can restore snapshots to running clusters.
- Rest [Restore](https://www.elastic.co/guide/en/elasticsearch/reference/7.5/snapshots-restore-snapshot.html) - API interface can be used.
- All indices restore is the default option.
- Selective restore is also available.

## Snapshot repository

A snapshot repository is required before, any snapshot can be taken.

> It is always recommended to create a new snapshot for each major build version

{{< alert "circle-info" >}}
**Note:** Snapshots written by one version may not be visible to the other and the repository could be corrupted.
{{< /alert >}}

### Example

{{< alert "circle-info" >}}
GET \_snapshot
{{< /alert >}}

{{< alert "circle-info" >}}
{  
  
 "repo\_elastic7\_5" : {  
  
 "type" : "source",  
  
 "settings" : {  
  
 "compress" : "true",  
  
 "delegate\_type" : "fs",  
  
 "location" : "/home/elasticsearch/backup"  
  
 }  
  
 }  
  
}
{{< /alert >}}

In the example above you can see the GET request returns the Snapshot repo Name and information about the location.

![Repository](screenshot-2020-02-26-at-2.06.47-pm.png "Repository")

The information that the Rest API showed can also be viewed from Kibana by clicking the repo-name.

![](screenshot-2020-02-26-at-2.25.26-pm.png)

### Details

#### "type" : "fs"

FS is the shared file system to store the snapshots. The location is the exact location on system.

## New Repo

Let's try and add a new repo.

![](screenshot-2020-02-26-at-3.25.16-pm.png)

- In step one you need to click the register the Repository button on the top left and the dialog as above should be displayed.
- Specify a name and select the `Shared File System` and press next

<img src="screenshot-2020-02-26-at-3.26.01-pm.png" alt="" class="grid-w100" />

- Add the location name - this location has to be present in the `path.repo`

In my example I have two paths set

{{< alert "circle-info" >}}
ath.repo: ["/home/elasticsearch/backup","/mnt/nfs/var/nfsshare/es"]
{{< /alert >}}

In case you do not have the path set when you register it might fail like below

![](screenshot-2020-02-26-at-3.26.14-pm.png)

Otherwise

![Step 3](screenshot-2020-02-26-at-3.29.56-pm.png "Step 3")

-- THE - END --
