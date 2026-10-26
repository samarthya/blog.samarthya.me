---
title: "Docker"
date: "2020-07-11T12:00:00Z"
slug: "docker-ubuntu-a-refresher"
description: "Usually I use Centos, but this time I wanted to try out docker swarm and ubuntu was the preferred option due to the options and supporting blogs available."
categories: ["others", "technical"]
tags: ["docker", "linux", "swarm", "ubuntu"]
aliases: ["/wps/2020/07/11/docker-ubuntu-a-refresher/"]
recovered: "Internet Archive snapshot 2026-05-17"
---

Usually I use Centos, but this time I wanted to try out docker swarm and ubuntu was the preferred option due to the options and supporting blogs available.

> Do read – https://docs.docker.com/get-started/#containers-and-virtual-machines
>
> docker.com

### ![](https://docs.docker.com/images/Container%402x.png)

### Step 1

Updating the system and installing required dependencies

```text
sudo apt-get update

sudo apt-get -y install \
  apt-transport-https \
  ca-certificates \
  curl \
  gnupg-agent \
  software-properties-common
```

The version of Ubuntu I am using is as under

```text
> cat /etc/issue
Ubuntu 18.04.4 LTS \n \l
```

Add the GPG key and repository. Finally install docker `community edition`

```text
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -

sudo apt-key fingerprint 0EBFCD88

sudo add-apt-repository \
   "deb [arch=amd64] https://download.docker.com/linux/ubuntu \
   $(lsb_release -cs) \
   stable"

sudo apt-get update

sudo apt-get install -y docker-ce=5:18.09.5~3-0~ubuntu-bionic docker-ce-cli=5:18.09.5~3-0~ubuntu-bionic containerd.io
```

```text
docker info
Containers: 0
 Running: 0
 Paused: 0
 Stopped: 0
Images: 0
Server Version: 18.09.5
Storage Driver: overlay2
 Backing Filesystem: extfs
 Supports d_type: true
 Native Overlay Diff: true
Logging Driver: json-file
Cgroup Driver: cgroupfs
Plugins:
 Volume: local
 Network: bridge host macvlan null overlay
 Log: awslogs fluentd gcplogs gelf journald json-file local logentries splunk syslog
Swarm: inactive
Runtimes: runc
Default Runtime: runc
Init Binary: docker-init
containerd version: 7ad184331fa3e55e52b890ea95e65ba581ae3429
runc version: dc9208a3303feef5b3839f4323d9beb36df0a9dd
init version: fec3683
Security Options:
 apparmor
 seccomp
  Profile: default
Kernel Version: 5.3.0-1023-aws
Operating System: Ubuntu 18.04.4 LTS
OSType: linux
Architecture: x86_64
CPUs: 2
Total Memory: 3.798GiB
Name: samarthya2c.mylabserver.com
ID: R4OG:F2YR:VRTY:XFRM:4QXX:JWN6:Y2YS:OA5M:7YCJ:OMFR:BXP5:HKXO
Docker Root Dir: /var/lib/docker
Debug Mode (client): false
Debug Mode (server): false
Registry: https://index.docker.io/v1/
Labels:
Experimental: false
Insecure Registries:
 127.0.0.0/8
Live Restore Enabled: false
Product License: Community Engine

WARNING: No swap limit support
```

## `docker version`

Now time to check the version. `docker version`

```text

Client:
 Version:           18.09.5
 API version:       1.39
 Go version:        go1.10.8
 Git commit:        e8ff056
 Built:             Thu Apr 11 04:43:57 2019
 OS/Arch:           linux/amd64
 Experimental:      false

Server: Docker Engine - Community
 Engine:
  Version:          18.09.5
  API version:      1.39 (minimum version 1.12)
  Go version:       go1.10.8
  Git commit:       e8ff056
  Built:            Thu Apr 11 04:10:53 2019
  OS/Arch:          linux/amd64
  Experimental:     false
```

### Step 2

Time to install docker swarm.

```text
docker swarm init
```

On the machine that you use the command above it will be the designated swarm manager.

## Options – For Init

```text
docker swarm init --help

Usage:	docker swarm init [OPTIONS]

Initialize a swarm

Options:
      --advertise-addr string                  Advertised address (format: <ip|interface>[:port])
      --autolock                               Enable manager autolocking (requiring an unlock key to start a stopped manager)
      --availability string                    Availability of the node ("active"|"pause"|"drain") (default "active")
      --cert-expiry duration                   Validity period for node certificates (ns|us|ms|s|m|h) (default 2160h0m0s)
      --data-path-addr string                  Address or interface to use for data path traffic (format: <ip|interface>)
      --default-addr-pool ipNetSlice           default address pool in CIDR format (default [])
      --default-addr-pool-mask-length uint32   default address pool subnet mask length (default 24)
      --dispatcher-heartbeat duration          Dispatcher heartbeat period (ns|us|ms|s|m|h) (default 5s)
      --external-ca external-ca                Specifications of one or more certificate signing endpoints
      --force-new-cluster                      Force create a new cluster from current state
      --listen-addr node-addr                  Listen address (format: <ip|interface>[:port]) (default 0.0.0.0:2377)
      --max-snapshots uint                     Number of additional Raft snapshots to retain
      --snapshot-interval uint                 Number of log entries between Raft snapshots (default 10000)
      --task-history-limit int                 Task history retention limit (default 5)
```

If you are deploying it on a cloud or a hosted VM, you need to be cautious of which ports are accessible to the nodes who will be joining in the swarm.

For my case I have a `public` and `private` **ip** that my machine has, and I will be using the private ip for the option `--advertise-addr` and that has no restrictions in terms of port.

```text
docker swarm init --advertise-addr 172.31.0.1
Swarm initialized: current node (a0zuhhhc0mjnm322gadntwsrwe) is now a manager.

To add a worker to this swarm, run the following command:

    docker swarm join --token SWMTKN-1-417pmtvy5vtzui4lmf023jhr4q50tekzzgsf8evgy4emtykvs4-exobuyup2mro23r32aursfzxw 172.31.0.1:2377

To add a manager to this swarm, run 'docker swarm join-token manager' and follow the instructions.
```

`docker info` should return some information about the swarm

```text
Swarm: active
 NodeID: a0zuhhhc0mjnm322gadntwsrwe
 Is Manager: true
 ClusterID: uym09dgerjhhkasf
 Managers: 1
 Nodes: 1
 Default Address Pool: 100.0.0.0/8
```

> Namespace isolation provides a secure environment.
>
> linux

`docker node ls` is another command that can be used to see the nodes in the swarm.

Once the docker swarm manager is ready you can add slave nodes to the swarm.

In the slave nodes wherever we have deployed docker and is supposed to work as the slave node, you need to fire the command.

```text
docker swarm join --token SWMTKN-1-417pmtvy5vtzui4lmf023jhr4q50tekzzgsf8evgy4emtykvs4-exobuyup2mro23r32aursfzxw 172.31.0.1:2377
```

If it is successful, the following output will be shown.

```text
This node joined a swarm as a worker
```

If you run `docker node ls` again, you will be see the nodes in the swarm

```text
docker node ls
ID                            HOSTNAME                      STATUS              AVAILABILITY        MANAGER STATUS      ENGINE VERSION
mauqklyumsaqs     samarthya1c.samarthya.com   Ready               Active                                  18.09.5
kilop2sdhc0m *   samarthya2c.samarthya.com   Ready               Active              Leader              18.09.5
vg890hdgd333     samarthya3c.samarthya.com   Ready               Active                                  18.09.5
csl8igcknj28c     samarthya4c.samarthya.com   Ready               Active                                  18.09.5
```

You can see the designated leader in the swarm. The leader assigns work to the worker nodes.

You can output the join token in master/manager node using

```text
docker swarm join-token worker
```

```text
root@master>docker swarm join-token worker
To add a worker to this swarm, run the following command:

    docker swarm join \
    --token SWMTKN-1-21wvlfoixago56zx0dbpznq8la36he9blrdyoyhosm4u02kvzk-bltrqgg1qiyrnr48xs1g5sybn \
    172.31.0.1:2377
```

## Flattening the layers – Docker

In this section we will be using `directives` instructions used in `Dockerfile` to create an image and flatten it to a single image instead of multiple.

> Docker can build images automatically by reading the instructions from a `Dockerfile`.

Consider a small docker container created as under

```text
FROM golang:1.13.11 AS builder
WORKDIR /helloworld
COPY goworld.go .
RUN GOOS=linux go build -a -installsuffix cgo -o goworld .

FROM alpine:3.9.3
WORKDIR /root
COPY --from=builder /helloworld/goworld .
CMD ["./goworld"]
```

It just creates compiles a hello world go lang program and then executes it to print the output

```text
package main
import ("fmt")

func main() {
  fmt.Println(" Hello World!")
}
```

If I look at the layers of the image

```text
[
    {
        "Id": "sha256:2be60e641422227cd8caeb65894f66c63d08c514019e296dc32aae7f935f3076",
        "RepoTags": [
            "efficient:latest"
        ],
        "RepoDigests": [],
        "Parent": "sha256:192c03c1f3fa07ed20b20b2b4f73a60fcb42dc6d910e47b13b2cd0e060961452",
        "Comment": "",
        "Created": "2020-07-11T18:35:55.800402558Z",
        "Container": "b0a931821260361263ce15240238476813e7a84d3a32b9e773dcab24f956ce3f",
        "ContainerConfig": {
            "Hostname": "b0a931821260",
            "Domainname": "",
            "User": "",
            "AttachStdin": false,
            "AttachStdout": false,
            "AttachStderr": false,
            "Tty": false,
            "OpenStdin": false,
            "StdinOnce": false,
            "Env": [
                "PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"
            ],
            "Cmd": [
                "/bin/sh",
                "-c",
                "#(nop) ",
                "CMD [\"./goworld\"]"
            ],
            "Image": "sha256:192c03c1f3fa07ed20b20b2b4f73a60fcb42dc6d910e47b13b2cd0e060961452",
            "Volumes": null,
            "WorkingDir": "/root",
            "Entrypoint": null,
            "OnBuild": null,
            "Labels": {}
        },
        "DockerVersion": "19.03.12",
        "Author": "",
        "Config": {
            "Hostname": "",
            "Domainname": "",
            "User": "",
            "AttachStdin": false,
            "AttachStdout": false,
            "AttachStderr": false,
            "Tty": false,
            "OpenStdin": false,
            "StdinOnce": false,
            "Env": [
                "PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"
            ],
            "Cmd": [
                "./goworld"
            ],
            "Image": "sha256:192c03c1f3fa07ed20b20b2b4f73a60fcb42dc6d910e47b13b2cd0e060961452",
            "Volumes": null,
            "WorkingDir": "/root",
            "Entrypoint": null,
            "OnBuild": null,
            "Labels": null
        },
        "Architecture": "amd64",
        "Os": "linux",
        "Size": 7541995,
        "VirtualSize": 7541995,
        "GraphDriver": {
            "Data": {
                "LowerDir": "/var/lib/docker/overlay2/2f6641cf733d78bc0ad8d6f0bad7c4436f01bf978bed3f1a9b41d7ec06af0244/diff",
                "MergedDir": "/var/lib/docker/overlay2/3d38a55e5cd0e6dc257dd9ef2aa90b5d2b8a98ae55937a6ce37edf821c893e95/merged",
                "UpperDir": "/var/lib/docker/overlay2/3d38a55e5cd0e6dc257dd9ef2aa90b5d2b8a98ae55937a6ce37edf821c893e95/diff",
                "WorkDir": "/var/lib/docker/overlay2/3d38a55e5cd0e6dc257dd9ef2aa90b5d2b8a98ae55937a6ce37edf821c893e95/work"
            },
            "Name": "overlay2"
        },
        "RootFS": {
            "Type": "layers",
            "Layers": [
                "sha256:a464c54f93a9e88fc1d33df1e0e39cca427d60145a360962e8f19a1dbf900da9",
                "sha256:7bf030eb44f162731c1d17a4a3d5af128818f938997709309c13653780c15cd6"
            ]
        },
        "Metadata": {
            "LastTagTime": "2020-07-12T08:28:11.850260882Z"
        }
    }
]
```

We will flatten it to

```text
[
    {
        "Id": "sha256:b9038e8380fe786207d091bd9e313e867198d44f985d149685bcb6c6fbbf333b",
        "RepoTags": [
            "flat:latest"
        ],
        "RepoDigests": [],
        "Parent": "",
        "Comment": "Imported from -",
        "Created": "2020-07-12T09:04:40.856766368Z",
        "Container": "",
        "ContainerConfig": {
            "Hostname": "",
            "Domainname": "",
            "User": "",
            "AttachStdin": false,
            "AttachStdout": false,
            "AttachStderr": false,
            "Tty": false,
            "OpenStdin": false,
            "StdinOnce": false,
            "Env": null,
            "Cmd": null,
            "Image": "",
            "Volumes": null,
            "WorkingDir": "",
            "Entrypoint": null,
            "OnBuild": null,
            "Labels": null
        },
        "DockerVersion": "19.03.12",
        "Author": "",
        "Config": {
            "Hostname": "",
            "Domainname": "",
            "User": "",
            "AttachStdin": false,
            "AttachStdout": false,
            "AttachStderr": false,
            "Tty": false,
            "OpenStdin": false,
            "StdinOnce": false,
            "Env": null,
            "Cmd": null,
            "Image": "",
            "Volumes": null,
            "WorkingDir": "",
            "Entrypoint": null,
            "OnBuild": null,
            "Labels": null
        },
        "Architecture": "amd64",
        "Os": "linux",
        "Size": 7541906,
        "VirtualSize": 7541906,
        "GraphDriver": {
            "Data": {
                "MergedDir": "/var/lib/docker/overlay2/efd29f53d69a47bc7b983c9da58a7985afaf3b354800c13da8fd3ef0e7f8dea6/merged",
                "UpperDir": "/var/lib/docker/overlay2/efd29f53d69a47bc7b983c9da58a7985afaf3b354800c13da8fd3ef0e7f8dea6/diff",
                "WorkDir": "/var/lib/docker/overlay2/efd29f53d69a47bc7b983c9da58a7985afaf3b354800c13da8fd3ef0e7f8dea6/work"
            },
            "Name": "overlay2"
        },
        "RootFS": {
            "Type": "layers",
            "Layers": [
                "sha256:3aa6e339ec7bf27f61646f33b8532bff0de532c8072847f7e1d268ad51e0e358"
            ]
        },
        "Metadata": {
            "LastTagTime": "2020-07-12T09:04:40.859989787Z"
        }
    }
]
```

### Docker Service

To deploy an image when docker is in swarm mode you can use `docker service`. When service is created, you specify which container image to use and which commands to execute inside running containers.

> Refer to more information [here](https://docs.docker.com/engine/reference/commandline/service/#child-commands)

Minimum version required to use `docker service` is 1.24.

![](https://docs.docker.com/engine/swarm/images/services-diagram.png)

```text
docker service create --help

Usage:  docker service create [OPTIONS] IMAGE [COMMAND] [ARG...]

Create a new service

Options:
      --config config                      Specify configurations to expose to the service
      --constraint list                    Placement constraints
      --container-label list               Container labels
      --credential-spec credential-spec    Credential spec for managed service account (Windows only)
  -d, --detach                             Exit immediately instead of waiting for the service to converge
      --dns list                           Set custom DNS servers
      --dns-option list                    Set DNS options
      --dns-search list                    Set custom DNS search domains
      --endpoint-mode string               Endpoint mode (vip or dnsrr) (default "vip")
      --entrypoint command                 Overwrite the default ENTRYPOINT of the image
  -e, --env list                           Set environment variables
      --env-file list                      Read in a file of environment variables
      --generic-resource list              User defined resources
      --group list                         Set one or more supplementary user groups for the container
      --health-cmd string                  Command to run to check health
      --health-interval duration           Time between running the check (ms|s|m|h)
      --health-retries int                 Consecutive failures needed to report unhealthy
      --health-start-period duration       Start period for the container to initialize before counting retries towards unstable (ms|s|m|h)
      --health-timeout duration            Maximum time to allow one check to run (ms|s|m|h)
      --host list                          Set one or more custom host-to-IP mappings (host:ip)
      --hostname string                    Container hostname
      --init                               Use an init inside each service container to forward signals and reap processes
      --isolation string                   Service container isolation mode
  -l, --label list                         Service labels
      --limit-cpu decimal                  Limit CPUs
      --limit-memory bytes                 Limit Memory
      --log-driver string                  Logging driver for service
      --log-opt list                       Logging driver options
      --mode string                        Service mode (replicated or global) (default "replicated")
      --mount mount                        Attach a filesystem mount to the service
      --name string                        Service name
      --network network                    Network attachments
      --no-healthcheck                     Disable any container-specified HEALTHCHECK
      --no-resolve-image                   Do not query the registry to resolve image digest and supported platforms
      --placement-pref pref                Add a placement preference
  -p, --publish port                       Publish a port as a node port
  -q, --quiet                              Suppress progress output
      --read-only                          Mount the container's root filesystem as read only
      --replicas uint                      Number of tasks
      --reserve-cpu decimal                Reserve CPUs
      --reserve-memory bytes               Reserve Memory
      --restart-condition string           Restart when condition is met ("none"|"on-failure"|"any") (default "any")
      --restart-delay duration             Delay between restart attempts (ns|us|ms|s|m|h) (default 5s)
      --restart-max-attempts uint          Maximum number of restarts before giving up
      --restart-window duration            Window used to evaluate the restart policy (ns|us|ms|s|m|h)
      --rollback-delay duration            Delay between task rollbacks (ns|us|ms|s|m|h) (default 0s)
      --rollback-failure-action string     Action on rollback failure ("pause"|"continue") (default "pause")
      --rollback-max-failure-ratio float   Failure rate to tolerate during a rollback (default 0)
      --rollback-monitor duration          Duration after each task rollback to monitor for failure (ns|us|ms|s|m|h) (default 5s)
      --rollback-order string              Rollback order ("start-first"|"stop-first") (default "stop-first")
      --rollback-parallelism uint          Maximum number of tasks rolled back simultaneously (0 to roll back all at once) (default 1)
      --secret secret                      Specify secrets to expose to the service
      --stop-grace-period duration         Time to wait before force killing a container (ns|us|ms|s|m|h) (default 10s)
      --stop-signal string                 Signal to stop the container
  -t, --tty                                Allocate a pseudo-TTY
      --update-delay duration              Delay between updates (ns|us|ms|s|m|h) (default 0s)
      --update-failure-action string       Action on update failure ("pause"|"continue"|"rollback") (default "pause")
      --update-max-failure-ratio float     Failure rate to tolerate during an update (default 0)
      --update-monitor duration            Duration after each task update to monitor for failure (ns|us|ms|s|m|h) (default 5s)
      --update-order string                Update order ("start-first"|"stop-first") (default "stop-first")
      --update-parallelism uint            Maximum number of tasks updated simultaneously (0 to update all at once) (default 1)
  -u, --user string                        Username or UID (format: <name|uid>[:<group|gid>])
      --with-registry-auth                 Send registry authentication details to swarm agents
  -w, --workdir string                     Working directory inside the container
```

Simply using `docker service create`

```text
docker service create --name mynginx nginx
```

the parameter `--name` defines the service name and the last param is the image to be used for the service.

```text
docker service ls
ID                  NAME                  MODE                REPLICAS            IMAGE                                         PORTS
tp2szq0s5hbi        mynginx               replicated          1/1                 nginx:latest
```

See I have not exposed any port, and replicas are also only one.

How can I scale it?

```text
docker service scale mynginx=3
mynginx scaled to 3
overall progress: 3 out of 3 tasks 
1/3: running   [==================================================>] 
2/3: running   [==================================================>] 
3/3: running   [==================================================>] 
verify: Service converged
```

How should I update to expose a port

```text
docker service update --help

Usage:  docker service update [OPTIONS] SERVICE

Update a service

Options:
      --args command                       Service command args
      --config-add config                  Add or update a config file on a service
      --config-rm list                     Remove a configuration file
      --constraint-add list                Add or update a placement constraint
      --constraint-rm list                 Remove a constraint
      --container-label-add list           Add or update a container label
      --container-label-rm list            Remove a container label by its key
      --credential-spec credential-spec    Credential spec for managed service account (Windows only)
  -d, --detach                             Exit immediately instead of waiting for the service to converge
      --dns-add list                       Add or update a custom DNS server
      --dns-option-add list                Add or update a DNS option
      --dns-option-rm list                 Remove a DNS option
      --dns-rm list                        Remove a custom DNS server
      --dns-search-add list                Add or update a custom DNS search domain
      --dns-search-rm list                 Remove a DNS search domain
      --endpoint-mode string               Endpoint mode (vip or dnsrr)
      --entrypoint command                 Overwrite the default ENTRYPOINT of the image
      --env-add list                       Add or update an environment variable
      --env-rm list                        Remove an environment variable
      --force                              Force update even if no changes require it
      --generic-resource-add list          Add a Generic resource
      --generic-resource-rm list           Remove a Generic resource
      --group-add list                     Add an additional supplementary user group to the container
      --group-rm list                      Remove a previously added supplementary user group from the container
      --health-cmd string                  Command to run to check health
      --health-interval duration           Time between running the check (ms|s|m|h)
      --health-retries int                 Consecutive failures needed to report unhealthy
      --health-start-period duration       Start period for the container to initialize before counting retries towards unstable (ms|s|m|h)
      --health-timeout duration            Maximum time to allow one check to run (ms|s|m|h)
      --host-add list                      Add a custom host-to-IP mapping (host:ip)
      --host-rm list                       Remove a custom host-to-IP mapping (host:ip)
      --hostname string                    Container hostname
      --image string                       Service image tag
      --init                               Use an init inside each service container to forward signals and reap processes
      --isolation string                   Service container isolation mode
      --label-add list                     Add or update a service label
      --label-rm list                      Remove a label by its key
      --limit-cpu decimal                  Limit CPUs
      --limit-memory bytes                 Limit Memory
      --log-driver string                  Logging driver for service
      --log-opt list                       Logging driver options
      --mount-add mount                    Add or update a mount on a service
      --mount-rm list                      Remove a mount by its target path
      --network-add network                Add a network
      --network-rm list                    Remove a network
      --no-healthcheck                     Disable any container-specified HEALTHCHECK
      --no-resolve-image                   Do not query the registry to resolve image digest and supported platforms
      --placement-pref-add pref            Add a placement preference
      --placement-pref-rm pref             Remove a placement preference
      --publish-add port                   Add or update a published port
      --publish-rm port                    Remove a published port by its target port
  -q, --quiet                              Suppress progress output
      --read-only                          Mount the container's root filesystem as read only
      --replicas uint                      Number of tasks
      --reserve-cpu decimal                Reserve CPUs
      --reserve-memory bytes               Reserve Memory
      --restart-condition string           Restart when condition is met ("none"|"on-failure"|"any")
      --restart-delay duration             Delay between restart attempts (ns|us|ms|s|m|h)
      --restart-max-attempts uint          Maximum number of restarts before giving up
      --restart-window duration            Window used to evaluate the restart policy (ns|us|ms|s|m|h)
      --rollback                           Rollback to previous specification
      --rollback-delay duration            Delay between task rollbacks (ns|us|ms|s|m|h)
      --rollback-failure-action string     Action on rollback failure ("pause"|"continue")
      --rollback-max-failure-ratio float   Failure rate to tolerate during a rollback
      --rollback-monitor duration          Duration after each task rollback to monitor for failure (ns|us|ms|s|m|h)
      --rollback-order string              Rollback order ("start-first"|"stop-first")
      --rollback-parallelism uint          Maximum number of tasks rolled back simultaneously (0 to roll back all at once)
      --secret-add secret                  Add or update a secret on a service
      --secret-rm list                     Remove a secret
      --stop-grace-period duration         Time to wait before force killing a container (ns|us|ms|s|m|h)
      --stop-signal string                 Signal to stop the container
  -t, --tty                                Allocate a pseudo-TTY
      --update-delay duration              Delay between updates (ns|us|ms|s|m|h)
      --update-failure-action string       Action on update failure ("pause"|"continue"|"rollback")
      --update-max-failure-ratio float     Failure rate to tolerate during an update
      --update-monitor duration            Duration after each task update to monitor for failure (ns|us|ms|s|m|h)
      --update-order string                Update order ("start-first"|"stop-first")
      --update-parallelism uint            Maximum number of tasks updated simultaneously (0 to update all at once)
  -u, --user string                        Username or UID (format: <name|uid>[:<group|gid>])
      --with-registry-auth                 Send registry authentication details to swarm agents
  -w, --workdir string                     Working directory inside the container
```

Adding `8082` as a published port to expose the port `80` of `nginx`.

```text
docker service update mynginx --publish-add 8082:80
mynginx
overall progress: 3 out of 3 tasks 
1/3: running   [==================================================>] 
2/3: running   [==================================================>] 
3/3: running   [==================================================>] 
verify: Service converged
```

```text
docker service ls
ID                  NAME                  MODE                REPLICAS            IMAGE                                         PORTS
tp2szq0s5hbi        mynginx               replicated          3/3                 nginx:latest                                  *:8082->80/tcp
```

Simple check

```text
curl localhost:8082
```

```text

<!DOCTYPE html>
<html>
<head>
<title>Welcome to nginx!</title>
<style>
    body {
        width: 35em;
        margin: 0 auto;
        font-family: Tahoma, Verdana, Arial, sans-serif;
    }
</style>
</head>
<body>
<h1>Welcome to nginx!</h1>
<p>If you see this page, the nginx web server is successfully installed and
working. Further configuration is required.</p>

<p>For online documentation and support please refer to
<a href="http://nginx.org/">nginx.org</a>.<br/>
Commercial support is available at
<a href="http://nginx.com/">nginx.com</a>.</p>

<p><em>Thank you for using nginx.</em></p>
</body>
</html>
```

When running Docker Engine in swarm mode, you can use `docker stack deploy` to deploy a complete application stack to the swarm. It accepts instructions form a compose file.

The Compose file is a [YAML](http://yaml.org/) file defining [services](https://docs.docker.com/compose/compose-file/#service-configuration-reference), [networks](https://docs.docker.com/compose/compose-file/#network-configuration-reference) and [volumes](https://docs.docker.com/compose/compose-file/#volume-configuration-reference).

```text
Supports version 3 and upwards.
```

> Docker services allows replication of a single service across nodes in a docker swarm, and Docker stack allows more deployment of more complex application of interrelated services and to be scaled as a unit.

## Helpful link

- <https://docs.docker.com/engine/swarm/how-swarm-mode-works/services/>
- <https://docs.docker.com/engine/swarm/admin_guide/#back-up-the-swarm>
- <https://docs.docker.com/get-started/swarm-deploy/>
- https://www.toptal.com/linux/separation-anxiety-isolating-your-system-with-linux-namespaces
- <https://docs.docker.com/get-started/#containers-and-virtual-machines>
- <https://docs.docker.com/engine/swarm/swarm-tutorial/add-nodes/>
- <https://docs.docker.com/engine/reference/builder/>
- <https://helm.sh/docs/topics/charts/>
- <https://docs.docker.com/compose/compose-file/>

Next, I might look into Helm.

> [Helm](https://helm.sh/) is the package manager for the **Kubernetes**  & in this approach, Kubernetes could be considered as an operating system.
