---
title: "Non root `podman` and `molecule`"
date: "2024-02-13T12:00:00Z"
slug: "non-root-podman-and-molecule"
description: "On my Centos8 I was facing issue when I was trying to run Molecule on a centos machine which is running podman as a non root user."
categories: ["ansible", "technical"]
tags: ["ansible", "docker", "molecule"]
aliases: ["/wps/2024/02/13/non-root-podman-and-molecule/"]
recovered: "Internet Archive snapshot 2026-05-18"
---

![](molecule.png "(thumbnail only — original image lost)")

On my `Centos8` I was facing issue when I was trying to run Molecule on a centos machine which is running `podman` as a non root user. Also, I am using the driver – `docker` and not `podman`, so to overcome the aliases and references issues I have installed `podman-docker`.

## What is Podman?

Podman is a powerful tool for managing containers and pods, but it doesn’t have the exact same command-line interface (CLI) as Docker. This can be a hurdle for users accustomed to Docker workflows.

That’s where **podman-docker** comes in. This package installs a script named docker that emulates the `Docker CLI`. It also creates links between all `Docker CLI` and `podman`.

**Podman-docker** is a **compatibility layer** that allows you to use familiar Docker commands directly with Podman. It translates Docker commands into Podman commands under the hood, essentially **bridging the gap between the two tools**.

## Error

With the compatibility layer `podman-docker`; I was facing multiple issues.

### Exception – 1

```text
docker.errors.DockerException: Error while fetching server API version: ('Connection aborted.', PermissionError(13, 'Permission denied'))
```

What I could gather looking at this error was that it is trying to reach out to docker service but since I have podman something in place.

## `podman.socket`

Podman.socket is a Unix socket file that allows communication with the Podman API. It functions in two main ways:

**1. Socket Activation:**

- In combination with `systemd`, Podman.socket can enable **on-demand service activation**. As soon as a client connects to the socket, systemd starts the Podman API service, eliminating unnecessary background processes. This optimizes resource usage and improves security.

**2. Docker Compatibility:**

- Podman.socket can be used to emulate the Docker API, allowing tools and scripts designed for Docker to work with Podman. This is achieved by translating Docker commands into Podman commands before execution. This compatibility layer is particularly useful for:
  - **Transitioning from Docker:** Users familiar with Docker can continue using existing workflows without significant changes.
  - **Team Collaboration:** Teams using Docker tools can continue working together even if individual members use Podman.
  - **Supporting existing scripts:** Scripts written for Docker can be used with Podman without modifications.

Enabling the `podman.socket` for the current user

```text
systemctl enable --now --user podman.socket
```

Check the status

```text
systemctl status --user podman.socket
● podman.socket - Podman API Socket
   Loaded: loaded (/usr/lib/systemd/user/podman.socket; enabled; vendor preset: enabled)
   Active: active (listening) since Tue 2024-02-13 18:44:17 UTC; 8s ago
     Docs: man:podman-system-service(1)
   Listen: /run/user/0000/podman/podman.sock (Stream)
   CGroup: /user.slice/user-0000.slice/user@0000.service/podman.socket
```

Once it was running it was still giving the same error

exporting `DOCKER_HOST`

We use `export DOCKER_HOST` to tell the Docker client where to find the Docker daemon it needs to communicate with. It’s particularly useful in specific scenarios, but it’s essential to understand its function and potential drawbacks.

```text
export DOCKER_HOST=unix:///run/user/0000/podman/podman.sock
```

Once this property was set molecule was able to communicate with the `docker`/`podman` and without errors.

### Error – 2

The next error I got when I executed my molecule test is as under

```text
UNREACHABLE! => {
    "changed": false,
    "msg": "Failed to create temporary directory. In some cases, you may have been able to authenticate and did not have permissions on the target directory. Consider changing the remote tmp path in ansible.cfg to a path rooted in \"/tmp\", for more error information use -vvv. Failed command was: ( umask 77 && mkdir -p \"` echo ~/.ansible/tmp `\"&& mkdir \"` echo ~/.ansible/tmp/ansible-tmp-1707932756.4075935-520325-234920630732299 `\" && echo ansible-tmp-1707932756.4075935-520325-234920630732299=\"` echo ~/.ansible/tmp/ansible-tmp-1707932756.4075935-520325-234920630732299 `\" ), exited with result 125",
    "unreachable": true
}
```

To resolve this you need to set the `PODMAN_SOCK` variable.

```text
export PODMAN_SOCK=/run/user/0000/podman/podman.sock
```

Once set I ran the `molecule test` again and voila! all was green.

### Versions

I have the following version of molecule and I am using `podman`

#### `molecule --version`

```text
molecule 6.0.3 using python 3.12 
    ansible:2.16.3
    azure:23.5.0 from molecule_plugins
    containers:23.5.0 from molecule_plugins requiring collections: ansible.posix>=1.3.0 community.docker>=1.9.1 containers.podman>=1.8.1
    default:6.0.3 from molecule
    docker:23.5.0 from molecule_plugins requiring collections: community.docker>=3.0.2 ansible.posix>=1.4.0
    ec2:23.5.0 from molecule_plugins
    gce:23.5.0 from molecule_plugins requiring collections: google.cloud>=1.0.2 community.crypto>=1.8.0
    podman:23.5.0 from molecule_plugins requiring collections: containers.podman>=1.7.0 ansible.posix>=1.3.0
    vagrant:23.5.0 from molecule_plugins
```

#### `ansible --version`

```text
ansible [core 2.16.3]
```

#### `podman --version`

```text
podman version 4.8.3

> rpm -qa "podman-docker"
podman-docker-4.8.3-1.module_el8+804+f131391c.noarch
```
