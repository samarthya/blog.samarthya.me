---
title: "Docker network"
date: "2020-08-04T12:10:49Z"
slug: "docker-network"
categories: ["technical"]
tags: ["docker", "network"]
aliases: ["/wps/2020/08/04/docker-network/"]
wp_id: 892
---

## Learn by example

In this blog let's learn how to create a bridge network. By definition - Bridge networks are usually used when your applications run in standalone containers that need to communicate

> A bridge network is a Link Layer device which forwards traffic between network segments.
>
> docker.com

When you create a network, Docker engine creates a non-overlapping sub-network for the network by default and for a bridge network you can only have one subnet.

```text
docker network
```

{{< lead >}}
When you create a network, Engine creates a non-overlapping subnetwork for the network by default.
{{< /lead >}}

```text
Usage:	docker network COMMAND

Manage networks

Commands:
  connect     Connect a container to a network
  create      Create a network
  disconnect  Disconnect a container from a network
  inspect     Display detailed information on one or more networks
  ls          List networks
  prune       Remove all unused networks
  rm          Remove one or more networks

Run 'docker network COMMAND --help' for more information on a command.
```

{{< lead >}}
In terms of Docker, a bridge network uses a software bridge which allows containers connected to the same bridge network to communicate, while providing isolation from containers which are not connected to that bridge network.
{{< /lead >}}

```text
docker network create --help

Usage:	docker network create [OPTIONS] NETWORK

Create a network

Options:
      --attachable           Enable manual container attachment
      --aux-address map      Auxiliary IPv4 or IPv6 addresses used by Network driver (default map[])
      --config-from string   The network from which copying the configuration
      --config-only          Create a configuration only network
  -d, --driver string        Driver to manage the Network (default "bridge")
      --gateway strings      IPv4 or IPv6 Gateway for the master subnet
      --ingress              Create swarm routing-mesh network
      --internal             Restrict external access to the network
      --ip-range strings     Allocate container ip from a sub-range
      --ipam-driver string   IP Address Management Driver (default "default")
      --ipam-opt map         Set IPAM driver specific options (default map[])
      --ipv6                 Enable IPv6 networking
      --label list           Set metadata on a network
  -o, --opt map              Set driver specific options (default map[])
      --scope string         Control the network's scope
      --subnet strings       Subnet in CIDR format that represents a network segment
```

```text
docker network create --driver bridge my-nw
69b3024142339bb32fcf960de3175e3db3aeeca727ec653a27819549ee278e41
```

The command above will allow to define a network `my-nw` of type `--driver bridge` for the containers to connect-to and use.

```text
docker network ls
NETWORK ID          NAME                DRIVER              SCOPE
a97c7c66f4fd        bridge              bridge              local
d39ea265c531        host                host                local
efe4bfd141fe        none                null                local
69b302414233        my-nw               bridge              local
```

For a container to use this network one can specify the `--network` option with the value `my-nw` for it to utilize

{{< lead >}}
The Docker bridge driver automatically installs rules in the host machine so that containers on different bridge networks cannot communicate directly with each other.
{{< /lead >}}

```text
docker run --network my-nw --name using-nw samarthya/mydummycontainer:1
```

Please note `Bridge networks apply to containers running on the same Docker daemon host.`

{{< lead >}}
When you create or remove a user-defined bridge or connect or disconnect a container from a user-defined bridge, Docker uses tools specific to the operating system to manage the underlying network infrastructure (such as adding or removing bridge devices or configuring `iptables` rules on Linux).
{{< /lead >}}

## References

- https://success.docker.com/article/networking
- https://docs.docker.com/network/bridge/
