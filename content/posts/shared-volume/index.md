---
title: "Shared Volume"
date: "2020-07-31T07:10:03Z"
slug: "shared-volume"
categories: ["docker"]
tags: ["volumes"]
aliases: ["/wps/2020/07/31/shared-volume/"]
wp_id: 832
---

[![](https://docs.docker.com/storage/images/types-of-mounts-volume.png)](https://docs.docker.com/storage/images/types-of-mounts-volume.png)

Volumes are managed by Docker and is the preferred way of persisting, sharing data.

## Key Points

- Volume drivers allows to
  1. Store volumes on remote hosts or cloud providers,
  2. Encrypt the contents of volumes.
- Volumes does not increase the size of the containers using it.
- Volume’s contents exist outside the lifecycle of a given container.

```text
root@docker>docker volume ls
DRIVER              VOLUME NAME
local               c9ad85b13e22062f4eeefd9b65ae102c19856bea73622189f1a3393727c9b3e7
```

## Options to define volumes

One an define a volume using either `-v` or `--mount`.

### `--mount`

Option `--mount` is more explicit and allows one to avoid mistakes.

> It consists of multiple key-value pairs, separated by commas and each consisting of a `<key>=<value>` tuple.

The option `type` can be either of

1. volume
2. bind
3. tempfs

### `-v` or `--volume`

The order of information provided is very important for this option.

> `-v` or `--volume` Consists of three fields, separated by colon characters (`:`).

```text
root@docker>docker volume

Usage:  docker volume COMMAND

Manage volumes

Commands:
  create      Create a volume
  inspect     Display detailed information on one or more volumes
  ls          List volumes
  prune       Remove all unused local volumes
  rm          Remove one or more volumes

Run 'docker volume COMMAND --help' for more information on a command.
```

### Experiment time

You can simply create a volume without specifying any name

```text
root@docker>docker volume create
502f4ffc940ead1fc8cfaed65a9829b17aac322f9b4125b57e3a2e66f113a658
```

`docker volume ls` will return the listing which will show the volume just created.

You can give name to volumes too.

```text
root@docker>docker volume create my-volume
my-volume
```

```text
root@docker>docker volume ls
DRIVER              VOLUME NAME
local               my-volume
```

```text
root@docker>docker volume inspect my-volume
[
    {
        "CreatedAt": "2020-07-31T07:06:07Z",
        "Driver": "local",
        "Labels": {},
        "Mountpoint": "/var/lib/docker/volumes/my-volume/_data",
        "Name": "my-volume",
        "Options": {},
        "Scope": "local"
    }
]
```

deleting a volume is equally simple

```text
root@docker>docker volume rm my-volume
my-volume
```

How about attaching a volume to a container?

#### Step 1: Create a volume

```text
root@docker>docker volume create myvol
myvol
root@docker>docker volume ls
DRIVER              VOLUME NAME
local               myvol
```

#### Step 2: Refer to the volume

```text
docker run -d --mount src=myvol,dst=/app --name my_nginx nginx:latest
```

```text
Unable to find image 'nginx:latest' locally
latest: Pulling from library/nginx
6ec8c9369e08: Pull complete 
d3cb09a117e5: Pull complete 
7ef2f1459687: Pull complete 
e4d1bf8c9482: Pull complete 
795301d236d7: Pull complete 
Digest: sha256:0e188877aa60537d1a1c6484b8c3929cfe09988145327ee47e8e91ddf6f76f5c
Status: Downloaded newer image for nginx:latest
cee753ad7a48ccd4b1039391f7c10e8b710404472fce82e474319760e65bc89f
```

Inspecting the image can show the mount

```text
root@docker>docker container inspect my_nginx
```

```text
"Mounts": [
            {
                "Type": "volume",
                "Name": "myvol",
                "Source": "/var/lib/docker/volumes/myvol/_data",
                "Destination": "/app",
                "Driver": "local",
                "Mode": "z",
                "RW": true,
                "Propagation": ""
            }
        ]
```

If you look carefully there is a `RW` property which can be defined as false if you use the option `ro`, `readonly` in the option.

```text
root@docker>ls -als /var/lib/docker/volumes/myvol/_data
total 0
0 drwxr-xr-x. 2 root root  6 Jul 31 07:12 .
0 drwxr-xr-x. 3 root root 19 Jul 31 07:12 ..
```

Inspecting the volume `myvol`

```text
root@docker>docker inspect myvol
[
    {
        "CreatedAt": "2020-07-31T07:12:00Z",
        "Driver": "local",
        "Labels": {},
        "Mountpoint": "/var/lib/docker/volumes/myvol/_data",
        "Name": "myvol",
        "Options": {},
        "Scope": "local"
    }
]
```

The syntax in the `--mount` can be simplified by using `--volume`

```text
docker run -d -v myvol:/app --name my_nginx nginx:latest
```

Please note if you are creating service you have to use the `--mount` option as the `-v` is not supported for `docker service create`

{{< lead >}}
None of the containers can share the data if you use the `local` volume driver
{{< /lead >}}

## References

- https://docs.docker.com/storage/volumes/#share-data-among-machines
