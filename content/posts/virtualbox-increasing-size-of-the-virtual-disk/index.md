---
title: "VirtualBox: Increasing size of the virtual disk."
date: "2021-02-05T08:15:41Z"
slug: "virtualbox-increasing-size-of-the-virtual-disk"
categories: ["technical"]
tags: ["disk", "increase", "space", "vbox"]
aliases: ["/wps/2021/02/05/virtualbox-increasing-size-of-the-virtual-disk/"]
wp_id: 1314
---

I am using Virtual Box 6.1 and will use it to expand the disk space for one my VBox Ubuntu image which was almost full.

![](screenshot-2021-02-05-at-1.15.28-pm.png)

Click on **File** > **Virtual Media Manager**

![](screenshot-2021-02-05-at-1.17.44-pm-1.png)

You can see the `linux mint vdi` this is the disk which I increased size for using simple steps.

## Step-1 : Clone the disk

It is always recommended to ensure you have a copy that you can maintain in case of any irrecoverable failures.

- Click on Copy
- Follow the steps in the wizard

![](screenshot-2021-02-05-at-1.21.50-pm.png)

## Step - 2 Modify the attributes

Select the copy of the disk you just created and

![](screenshot-2021-02-05-at-1.23.53-pm-1.png)

![](screenshot-2021-02-05-at-1.24.06-pm.png)

I will increase by 2 GB

![](screenshot-2021-02-05-at-1.41.53-pm-1.png)

## Step 3: Resize

Boot up the machine and you can see some free space which you can adjust using any disk tool of you choice

![](screenshot-2021-02-05-at-1.39.34-pm.png)

You can click the gear for selected filesystem and increase the size.

![](screenshot-2021-02-05-at-1.39.59-pm.png)
