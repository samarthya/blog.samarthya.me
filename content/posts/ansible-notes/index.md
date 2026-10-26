---
title: "Ansible: Notes"
date: "2022-03-04T12:00:00Z"
slug: "ansible-notes"
description: "Control node   Managed nodes   Inventory   Modules   Tasks   Playbooks"
categories: ["technical"]
tags: ["ansible"]
aliases: ["/wps/2022/03/04/ansible-notes/"]
recovered: "Internet Archive snapshot 2026-03-13"
---

{{< accordion >}}

{{< accordionItem title="Official documentation notes (Self Read)" >}}

{{< tabs >}}

{{< tab label="Getting Started" >}}

[Control node](https://docs.ansible.com/ansible/2.9/user_guide/basic_concepts.html#control-node)  
[Managed nodes](https://docs.ansible.com/ansible/2.9/user_guide/basic_concepts.html#managed-nodes)  
[Inventory](https://docs.ansible.com/ansible/2.9/user_guide/basic_concepts.html#inventory)  
[Modules](https://docs.ansible.com/ansible/2.9/user_guide/basic_concepts.html#modules)  
[Tasks](https://docs.ansible.com/ansible/2.9/user_guide/basic_concepts.html#tasks)  
[Playbooks](https://docs.ansible.com/ansible/2.9/user_guide/basic_concepts.html#playbooks)

Building blocks for Ansible.

{{< /tab >}}

{{< tab label="Playbooks" >}}

{{< lead >}}
A playbook is composed of one or more ‘plays’ in an ordered list.
— Official documentation
{{< /lead >}}

- Ordered lists of tasks, saved so you can run those tasks in that order repeatedly.
- Expressed in YAML format
- It offers a multi-machine configuration & deployment system for complex applications that is
  - Repeatable
  - Re-usable &
  - Simple

{{< /tab >}}

{{< tab label="Control Node" >}}

- Controller machine
- Has the Ansible executable installed (+Python)

{{< /tab >}}

{{< tab label="Managed Node" >}}

- List of nodes/hosts that will be managed by control node

{{< /tab >}}

{{< tab label="Inventory" >}}

- List of nodes
- Can specify information like IP address for each managed node.
- An inventory can also organise managed nodes in groups e.g. `[webserver]`

{{< /tab >}}

{{< tab label="Modules" >}}

- The units of code Ansible executes.

{{< /tab >}}

{{< tab label="Tasks" >}}

The units of action in Ansible

{{< /tab >}}

{{< /tabs >}}

{{< /accordionItem >}}

{{< /accordion >}}
