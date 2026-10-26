---
title: "Ansible Variables"
date: "2023-03-15T12:00:00Z"
slug: "ansible-variables-2"
description: "Variables are a crucial part of Ansible and are used to store values that can be used across playbooks, roles, and tasks."
categories: ["technical"]
tags: ["ansible"]
aliases: ["/wps/2023/03/15/ansible-variables-2/"]
recovered: "Internet Archive snapshot 2026-05-17"
---

*[image unavailable: ans-vars.png]*

Ansible Variables

Variables are a crucial part of `Ansible` and are used to store values that can be used across `playbooks`, `roles`, and `tasks`. Understanding how variables work and their precedence is crucial to writing efficient and reliable playbooks.

`Ansible` provides a number of ways to define and use variables. Some of the common ways are:

1. `Inline variables`: Variables can be defined inline using the `vars` keyword in the task definition.

```text
- name: Example task
  debug:
    var: my_var
  vars:
    my_var: "my value"
```

2. `Playbook variables`: Variables can be defined at the playbook level using the `vars` keyword

```text
- name: Example playbook
  hosts: all
  vars:
    my_var: "my value"
  tasks:
    - name: Example task
      debug:
        var: my_var
```

3. `Role variables`: Variables can be defined at the role level using the `vars` directory in the role directory structure.

```text
my_role/
├── tasks/
└── vars/
    └── main.yml
```

The variables defined in this directory can be accessed using the `vars` keyword.

```text
- name: Example role
  hosts: all
  roles:
    - my_role
  tasks:
    - name: Example task
      debug:
        var: my_role_var
```

4. `Inventory variables`: Variables can be defined in the inventory file using the `host_vars` and `group_vars` directories.

```text
inventory/
├── host_vars/
│   └── my_host.yml
├── group_vars/
│   └── my_group.yml
└── hosts
```

The variables defined in these directories can be accessed using the `hostvars` and `group_vars` keywords respectively.

```text
- name: Example playbook
  hosts: all
  tasks:
    - name: Example task
      debug:
        var: hostvars['my_host']['my_var']
```

The order of precedence of variables in `Ansible` is as follows:

1. Role variables
2. Playbook variables
3. Inventory variables
4. Registered variables
5. Set facts
6. Extra variables (`--extra-vars` or `-e` command line argument)

It is important to keep this order in mind when defining variables to ensure that the correct value is used. For example, if a variable is defined in both the playbook and role variables, the role variable will take precedence.

In addition to the order of precedence, Ansible also provides the ability to override variables using tags. Tags are used to selectively execute tasks based on the tags defined in the playbook. By default, all tasks are executed unless a tag is specified. However, tags can be used to specify which tasks to execute.

```text
- name: Example playbook
  hosts: all
  tasks:
    - name: Example task
      debug:
        var: my_var
      tags:
        - my_tag
```

In this example, the task will only be executed if the `my_tag` tag is specified when running the playbook.

In summary, variables are a powerful feature of `Ansible` and are used to store values that can be used across playbooks, roles, and tasks. Understanding the order of precedence and how to use tags to override variables is crucial to writing efficient and reliable playbooks.
