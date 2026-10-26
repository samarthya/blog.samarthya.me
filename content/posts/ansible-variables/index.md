---
title: "Ansible: Variables"
date: "2023-02-08T12:00:00Z"
slug: "ansible-variables"
description: "Ansible Variables are used to store values that can be reused throughout an Ansible playbook."
categories: ["technical"]
tags: ["ansible", "variables"]
aliases: ["/wps/2023/02/08/ansible-variables/"]
recovered: "Internet Archive snapshot 2026-06-10"
---

Ansible Variables are used to store values that can be reused throughout an Ansible playbook. They can be set in a number of ways, including being passed as command-line options, defined in an inventory file, or defined in a playbook itself. Variables can be used to store values such as file paths, user-defined parameters, and results of tasks.

Ansible System Variables, on the other hand, are predefined variables provided by Ansible. These variables contain information about the host, such as the host name, operating system, IP address, etc. These variables are automatically available in playbooks and can be accessed using the “hostvars” dictionary. For example, the hostname of a target host can be accessed using the variable “ansible\_hostname”.

System Variables can be useful in writing more dynamic playbooks that adapt to the target host’s characteristics.

### Example

```text
---
- name: Example Playbook with Variables and System Variables
  hosts: all
  gather_facts: true
  tasks:
    - name: Print IP and FQDN
      debug:
        msg: "The IP address is {{ ansible_default_ipv4.address }} and the FQDN is {{ ansible_fqdn }}"
    - name: Print a custom variable
      debug:
        msg: "The custom message is: {{ custom_message }}"
  vars:
    custom_message: "Hello from the playbook!"
```

## System Variables

Ansible system variables are special variables that are used to represent information about the system, such as the hostname, architecture, IP address, and others. These variables are set by the Ansible control node and are available to all playbooks, tasks, and roles. Some of the common system variables in Ansible include:

- `ansible_hostname`: hostname of the system
- `ansible_os_family`: family of the operating system (e.g. RedHat, Debian, etc.)
- `ansible_distribution`: distribution of the operating system (e.g. CentOS, Ubuntu, etc.)
- `ansible_distribution_version`: version of the operating system distribution
- `ansible_architecture`: architecture of the system (e.g. x86\_64, aarch64, etc.)
- `ansible_all_ipv4_addresses`: list of all IPv4 addresses of the system
- `ansible_default_ipv4`: default IPv4 address of the system

These variables can be used in tasks and playbooks to conditionally execute tasks based on system information, customize the behavior of tasks and playbooks, and more.

```text
- name: Get IP and FQDN of Host
  hosts: all
  gather_facts: yes
  tasks:
    - name: Debug print host IP
      debug:
        msg: "Host IP: {{ ansible_default_ipv4.address }}"

    - name: Debug print host FQDN
      debug:
        msg: "Host FQDN: {{ ansible_fqdn }}"
```
