---
title: "Ansible: Building Inventory"
date: "2023-02-08T12:00:00Z"
slug: "ansible-building-inventory"
description: "An Ansible inventory is a file that defines the hosts and groups of hosts that Ansible will manage. Inventory files are used to define the nodes (hosts) that will be managed by Ansible."
categories: ["technical"]
tags: ["ansible", "inventory"]
aliases: ["/wps/2023/02/08/ansible-building-inventory/"]
recovered: "Internet Archive snapshot 2026-03-13"
---

![](an-inventory.png)

{{< lead >}}
The blog is adapted from the information available [here](https://docs.ansible.com/ansible/latest/getting_started/get_started_inventory.html#get-started-inventory).
— https://docs.ansible.com/ansible/
{{< /lead >}}

An Ansible inventory is a file that defines the hosts and groups of hosts that Ansible will manage. Inventory files are used to define the nodes (hosts) that will be managed by Ansible. These files can be in different formats, including INI and YAML.

{{< lead >}}
In `Ansible`, inventory refers to a file containing a list of hosts and their details (such as IP addresses, SSH credentials, etc.) that `Ansible` can interact with. Inventory variables are variables that are assigned to a specific host or group of hosts in the inventory file. These variables can be used to customize the behavior of `Ansible` playbooks and roles.
— ANSIBLE.com
{{< /lead >}}

The basic structure of an `Ansible` inventory file includes:

- `Hosts`: defined by their IP addresses or hostnames.
- `Groups`: a collection of hosts.
- `Variables`: data that can be associated with a host or group and used in playbooks.

To build an inventory, you need to decide on the following:

1. Hosts: List the IP addresses or hostnames of the nodes you want to manage.
2. Groups: Create groups based on your organizational structure. For example, you could have a group for web servers, another for databases, and another for applications.
3. Variables: Define variables for each host or group that you want to use in your playbooks.

Here’s a simple example of an Ansible inventory in the INI format:

```text
[webservers]
web1 ansible_host=192.168.1.10
web2 ansible_host=192.168.1.11

[dbservers]
db1 ansible_host=192.168.1.12
db2 ansible_host=192.168.1.13

[all:vars]
ansible_user=ansible
```

In this example, we have two groups: `webservers` and `dbservers`. Each group has two hosts defined by their IP addresses. Additionally, we have a `[all:vars]` section that defines a variable `ansible_user` for all hosts and groups.

## Variables

Variables can be defined in an inventory file, either at the group or host level, and can be used in playbooks to configure tasks.

Here’s an example of how variables can be defined in an inventory file:

```text
[web-server]
host1 ansible_host=192.168.1.100 http_port=80
host2 ansible_host=192.168.1.101 http_port=8080

[db-server]
host3 ansible_host=192.168.1.102 db_port=3306
host4 ansible_host=192.168.1.103 db_port=3306
```

In this example, the `web-server` and `db-server` groups have different variables defined for each host. These variables can then be referenced in a playbook to configure tasks specific to each group.

## Example of YAML

```text
virtualmachines:
  hosts:
    vm01:
      ansible_host: 192.0.2.50
    vm02:
      ansible_host: 192.0.2.51
    vm03:
      ansible_host: 192.0.2.52
```
