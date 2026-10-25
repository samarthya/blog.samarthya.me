---
title: "journalctl - Query the systemd journal"
date: "2020-10-17"
slug: "journalctl-query-the-systemd-journal"
categories: ["technical"]
tags: ["journalctl", "linux"]
aliases: ["/wps/2020/10/17/journalctl-query-the-systemd-journal/", "/wps/2026/10/23/journalctl-query-the-systemd-journal/"]
wp_id: 1090
---

`journald` is used to query the `systemd` journal contents.

### Example 1

Lets try and see the kubelet service logs in the `systemd` journal

Checking if the service exists

```text
systemctl list-units --show-types|grep kubelet
```

on my system the output is as below.

```text
kubelet.service                                                                                                   loaded active running   kubelet: The Kubernetes Node Agent
```

Time to get the log information

```text
journalctl -u kubelet -f -o json
```

Please note the options

- `-u`
  - Identifies the unit `kubelet` in our case
- `-f`
  - To follow the journal
- `-o`
  - Output formation

In my case output is as under

```text
{
   "__CURSOR":"s=4b762904ccb24ceeb1cfa518f498790c;i=cf33fa;b=5e07b79a1d1444ef9729bb834c352d1b;m=f1cfad0b04;t=5b18a9f763acf;x=db876470889c7586",
   "__REALTIME_TIMESTAMP":"1602583822482127",
   "__MONOTONIC_TIMESTAMP":"1038571342596",
   "_BOOT_ID":"5e07b79a1d1444ef9729bb834c352d1b",
   "_TRANSPORT":"stdout",
   "_STREAM_ID":"ffb8882786f14db1bcd227a42a088329",
   "PRIORITY":"6",
   "SYSLOG_FACILITY":"3",
   "SYSLOG_IDENTIFIER":"kubelet",
   "_PID":"1582",
   "_UID":"0",
   "_GID":"0",
   "_COMM":"kubelet",
   "_EXE":"/usr/bin/kubelet",
   "_CMDLINE":"/usr/bin/kubelet --bootstrap-kubeconfig=/etc/kubernetes/bootstrap-kubelet.conf --kubeconfig=/etc/kubernetes/kubelet.conf --config=/var/lib/kubelet/config.yaml --cgroup-driver=cgroupfs --network-plugin=cni --pod-infra-container-image=k8s.gcr.io/pause:3.2",
   "_CAP_EFFECTIVE":"1fffffffff",
   "_SYSTEMD_CGROUP":"/system.slice/kubelet.service",
   "_SYSTEMD_UNIT":"kubelet.service",
   "_SYSTEMD_SLICE":"system.slice",
   "_MACHINE_ID":"05cb8c7b39fe0f70e3ce97e5beab809d",
   "_HOSTNAME":"mymachine.net",
   "MESSAGE":"E1013 10:10:22.481755    1582 kubelet.go:2183] node \"mymachine.net\" not found"
}
```

Let's do a quick check using `systemd-cat` util.

From the official man page for `systemd-cat`

{{< lead >}}
systemd-cat - Connect a pipeline or program's output with the journal
— from man pages
{{< /lead >}}

Let's execute a dummy statement that has a timestamp added to the output which is connected to the journal using `systemd-cat`

```text
echo "My date is: `date`" | systemd-cat
```

If you now see the `journalctl` using either `-r` or may be use grep to look for

```text
journalctl |grep "My date is"
```

You will see an output as under

```text
Oct 13 13:43:42 mymachine.net cat[244214]: My date is: Tue Oct 13 13:43:42 UTC 2020
```

## Others

- `ps` is a useful utility to show the current active processes snapshot.
- `ps e` and `ps -e` are distinct
- [Man page](https://man7.org/linux/man-pages/man1/ps.1.html) - <https://man7.org/linux/man-pages/man1/ps.1.html>
