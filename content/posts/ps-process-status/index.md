---
title: "PS: Process Status"
date: "2020-10-20T11:13:18Z"
slug: "ps-process-status"
categories: ["technical"]
tags: ["linux"]
aliases: ["/wps/2020/10/20/ps-process-status/"]
wp_id: 1102
---

MAN Pages are one source of truth for all curious queries.

```text
man ps
```

```text
Name
   ps - report a snapshot of the current processes.
```

It is used to display instant information about the active processes in the system.

It accepts multiple types of arguments

- **UNIX** options, which may be grouped and must be preceded by a dash.
- **BSD** options, which may be grouped and must not be used with a dash.
- **GNU** long options, which are preceded by two dashes.

## Examples

```text
ps aux
```

It lists out all the processes running. In my system

```text
ps aux|wc -l
```

```text
root@node1>ps aux|wc -l
244
```

`243` processes - excluding the heading.

The ps command reads the `/proc` filesystem which is RAM based or virtual file system.

```text
mount -l|grep proc
```

```text
proc on /proc type proc (rw,nosuid,nodev,noexec,relatime)
systemd-1 on /proc/sys/fs/binfmt_misc type autofs (rw,relatime,fd=31,pgrp=1,timeout=0,minproto=5,maxproto=5,direct,pipe_ino=29236)
proc on /run/docker/netns/ingress_sbox type proc (rw,nosuid,nodev,noexec,relatime)
proc on /run/docker/netns/default type proc (rw,nosuid,nodev,noexec,relatime)
proc on /run/docker/netns/1-k52v1yjsgr type proc (rw,nosuid,nodev,noexec,relatime)
proc on /run/docker/netns/e57f884c0d0f type proc (rw,nosuid,nodev,noexec,relatime)
```

To see the process tree

```text
ps -e --forest
```

```text
 PID TTY          TIME CMD
     2 ?        00:00:00 kthreadd
     4 ?        00:00:00  \_ kworker/0:0H
     6 ?        00:00:00  \_ ksoftirqd/0
     7 ?        00:00:01  \_ migration/0
     8 ?        00:00:00  \_ rcu_bh
     9 ?        00:30:31  \_ rcu_sched
    10 ?        00:00:00  \_ lru-add-drain
    11 ?        00:00:07  \_ watchdog/0
    12 ?        00:00:06  \_ watchdog/1
    13 ?        00:00:01  \_ migration/1
    14 ?        00:00:01  \_ ksoftirqd/1
    16 ?        00:00:00  \_ kworker/1:0H
    17 ?        00:00:05  \_ watchdog/2
    18 ?        00:00:04  \_ migration/2
    19 ?        00:00:00  \_ ksoftirqd/2
    21 ?        00:00:00  \_ kworker/2:0H
    22 ?        00:00:05  \_ watchdog/3
    23 ?        00:00:04  \_ migration/3
    24 ?        00:00:00  \_ ksoftirqd/3
    26 ?        00:00:00  \_ kworker/3:0H
    27 ?        00:00:05  \_ watchdog/4
    28 ?        00:00:03  \_ migration/4
```
