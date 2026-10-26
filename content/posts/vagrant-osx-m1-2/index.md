---
title: "Vagrant-OSX"
date: "2022-08-19T12:00:00Z"
slug: "vagrant-osx-m1-2"
description: "In the previous blog, I was left with the error that had little information for me to debug. I realized since I migrated most of the files from my previous laptop it might be causing an issue."
categories: ["technical"]
tags: ["docker"]
aliases: ["/wps/2022/08/19/vagrant-osx-m1-2/"]
recovered: "Internet Archive snapshot 2023-05-29"
---

In the previous [blog]({{< relref "/posts/vagrant-osx-m1" >}}), I was left with the error that had little information for me to debug. I realized since I migrated most of the files from my previous laptop it might be causing an issue.

So a shot in the dark helped me. In my home directory, I just moved the `.vagrant.d` to `.old_vagrant.d` and just reissued the commands and VOILA!

```text
> vagrant up --provider=docker
Bringing machine 'default' up with 'docker' provider...
==> default: Creating and configuring docker networks...
==> default: Image is already built from the Dockerfile. `vagrant reload` to rebuild.
==> default: Vagrant has noticed that the synced folder definitions have changed.
==> default: With Docker, these synced folder changes won't take effect until you
==> default: destroy the container and recreate it.
==> default: Enabling network interfaces...
==> default: Starting container...
```

A quick check for the docker image execution

```text
> docker ps -a
CONTAINER ID   IMAGE                  COMMAND                  CREATED        STATUS                      PORTS     NAMES
82a58adb9870   e6a0117ec169           "/bin/bash"              17 hours ago   Exited (0) 16 seconds ago             qemu-test_default_1660854015
```
