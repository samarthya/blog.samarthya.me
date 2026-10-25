---
title: "Storage Drivers"
date: "2020-07-30T09:28:40Z"
slug: "storage-drivers"
categories: ["docker"]
tags: ["storage"]
aliases: ["/wps/2020/07/30/storage-drivers/"]
wp_id: 825
---

The storage driver allows your to create data in the writable layers of the container and it also controls how images and containers are stored and managed on the Docker host.

The files will not be persisted after the container is deleted, and performance wise it is relatively slower than native `fs` performance.

![](https://docs.docker.com/storage/storagedriver/images/container-layers.jpg)

E.g. Let's run a image `hello-world`

```text
docker run --name hello hello-world
```

```text
Hello from Docker!
This message shows that your installation appears to be working correctly.

To generate this message, Docker took the following steps:
 1. The Docker client contacted the Docker daemon.
 2. The Docker daemon pulled the "hello-world" image from the Docker Hub.
    (amd64)
 3. The Docker daemon created a new container from that image which runs the
    executable that produces the output you are currently reading.
 4. The Docker daemon streamed that output to the Docker client, which sent it
    to your terminal.

To try something more ambitious, you can run an Ubuntu container with:
 $ docker run -it ubuntu bash

Share images, automate workflows, and more with a free Docker ID:
 https://hub.docker.com/

For more examples and ideas, visit:
 https://docs.docker.com/get-started/
```

Let's inspect the container, and look for `GraphDriver`

```text
docker container inspect hello
```

```text
        "GraphDriver": {
            "Data": {
                "LowerDir": "/var/lib/docker/overlay2/228075bcce28b817db0857971a8da5209a5b4743fd2c2a462243bd8d793555ff-init/diff:/var/lib/docker/overlay2/39cd21c862ae937b5ac61b392f85dc65c04c7e0cabbf7a15408bf5cc14bd2232/diff",
                "MergedDir": "/var/lib/docker/overlay2/228075bcce28b817db0857971a8da5209a5b4743fd2c2a462243bd8d793555ff/merged",
                "UpperDir": "/var/lib/docker/overlay2/228075bcce28b817db0857971a8da5209a5b4743fd2c2a462243bd8d793555ff/diff",
                "WorkDir": "/var/lib/docker/overlay2/228075bcce28b817db0857971a8da5209a5b4743fd2c2a462243bd8d793555ff/work"
            },
            "Name": "overlay2"
        },
```

You can see the Name of the driver and some locations mentioned in `Data`

```text
"WorkDir": "/var/lib/docker/overlay2/228075bcce28b817db0857971a8da5209a5b4743fd2c2a462243bd8d793555ff/work"
```

If I do a listing in my docker host system I can see this directory

```text
ls -als /var/lib/docker/overlay2/228075bcce28b817db0857971a8da5209a5b4743fd2c2a462243bd8d793555ff/work
total 0
0 drwx------. 3 root root 18 Jul 30 09:32 .
0 drwx------. 4 root root 55 Jul 30 09:32 ..
0 d---------. 2 root root  6 Jul 30 09:32 work
```

How about the `image`?

```text
docker image inspect hello-world
```

Look for `GraphDriver` again

```text
"GraphDriver": {
            "Data": {
                "MergedDir": "/var/lib/docker/overlay2/39cd21c862ae937b5ac61b392f85dc65c04c7e0cabbf7a15408bf5cc14bd2232/merged",
                "UpperDir": "/var/lib/docker/overlay2/39cd21c862ae937b5ac61b392f85dc65c04c7e0cabbf7a15408bf5cc14bd2232/diff",
                "WorkDir": "/var/lib/docker/overlay2/39cd21c862ae937b5ac61b392f85dc65c04c7e0cabbf7a15408bf5cc14bd2232/work"
            },
            "Name": "overlay2"
        },
```

A quick directory listing can reveal the contents

```text
ls -als /var/lib/docker/overlay2/39cd21c862ae937b5ac61b392f85dc65c04c7e0cabbf7a15408bf5cc14bd2232
```

```text
total 12
0 drwx------.  3 root root   47 Jul 28 08:08 .
8 drwx------. 50 root root 4096 Jul 30 09:32 ..
0 -rw-------.  1 root root    0 Jul 30 09:32 committed
0 drwxr-xr-x.  2 root root   19 Jul 28 08:08 diff
4 -rw-r--r--.  1 root root   26 Jul 28 08:08 link
```

## Types of drivers

- overlay2
- aufs
- devicemapper
- btrfs
- vfs

> Read more [here](https://docs.docker.com/storage/storagedriver/select-storage-driver/).

- `overlay2` is the preferred storage driver for all currently supported Linux distributions.
- `aufs` is preferred for the kernels with no support for `overlay2` for Ubuntu 14.01 and older.
- `devicemapper` requires `direct-lvm` and is recommended storage driver for CentOS7 and earlier and RHEL. (The recent versions do support `overlay2`)

| Linux distribution | Recommended storage drivers | Alternative drivers |
| --- | --- | --- |
| Docker Engine - Community on Ubuntu | `overlay2` or `aufs` (for Ubuntu 14.04 running on kernel 3.13) | `overlay`, `devicemapper`, `zfs`, `vfs` |
| Docker Engine - Community on Debian | `overlay2` (Debian Stretch), `aufs` or `devicemapper` (older versions) | `overlay`, `vfs` |
| Docker Engine - Community on CentOS | `overlay2` | `overlay`, `devicemapper`, `zfs`, `vfs` |
| Docker Engine - Community on Fedora | `overlay2` | `overlay`, `devicemapper`, `zfs`, `vfs` |

### Supported backing filesystems

| Storage driver | Supported backing filesystems |
| --- | --- |
| `overlay2`, `overlay` | `xfs` with ftype=1, `ext4` |
| `aufs` | `xfs`, `ext4` |
| `devicemapper` | `direct-lvm` |
| `btrfs` | `btrfs` |
| `zfs` | `zfs` |
| `vfs` | any filesystem |

Data persistence is managed using several storage models

1. Filesystem storage
   - Used by `overlay2` and `aufs`, and is memory efficient.
2. Block storage
   - `devicemapper` uses it, and is useful for write heavy workloads.
3. Object storage
   - It is highly flexible and scalable object based store, e.g. A rest API that can push and pull data.

### Checking the storage driver

You can use `docker info` to check the driver on your `localhost`.

```text
 Server Version: 19.03.12
 Storage Driver: overlay2
  Backing Filesystem: xfs
  Supports d_type: true
  Native Overlay Diff: true
```

## References

- https://docs.docker.com/storage/storagedriver/select-storage-driver/#docker-engine---community
- https://rancher.com/block-object-file-storage-containers/
- https://docs.docker.com/storage/bind-mounts/
- https://docs.docker.com/storage/volumes/
