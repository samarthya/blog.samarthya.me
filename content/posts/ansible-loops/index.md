---
title: "Ansible Loops"
date: "2024-08-28T12:00:00Z"
slug: "ansible-loops"
description: "Loops in Ansible allow you to repeat a task multiple times with different input values."
categories: ["technical"]
tags: ["ansible"]
aliases: ["/wps/2024/08/28/ansible-loops/"]
recovered: "Internet Archive snapshot 2026-05-17"
---

![](loop-1.jpg)

`Ansible` offers powerful looping mechanisms that can significantly enhance your playbooks’ efficiency and readability. In this blog post, we’ll dive deep into Ansible loops, exploring various elements and providing practical examples to help you master this essential feature.

## Table of Contents

1. [Introduction to Loops](#introduction-to-loops)
2. [Basic Loop Usage](#basic-loop-usage)
3. [loop\_control and loop\_var](#loop-control-and-loop_var)
4. [Looping Over Dictionaries](#looping-over-dictionaries)
5. [Nested Loops](#nested-loops)
6. [Using Loops with Include Statements](#using-loops-with-include-statements)
7. [Advanced Loop Techniques](#advanced-loop-techniques)
8. [Best Practices and Tips](#best-practices-and-tips)

## Introduction to Loops

Loops in `Ansible` allow you to repeat a task multiple times with different input values. This can dramatically reduce the amount of code you need to write and maintain, making your playbooks more efficient and easier to read.

## Basic Loop Usage

The most common way to use loops in `Ansible` is with the `loop` keyword. Here’s a simple example:

```text
- name: Ensure multiple users exist
  ansible.builtin.user:
    name: "{{ item }}"
    state: present
  loop:
    - john
    - jane
    - bob
```

In this example, the task will run three times, creating users named `john`, `jane`, and `bob`. The loop variable `item` takes on each value in the list.

## `loop_control` and `loop_var`

The `loop_control` directive allows you to fine-tune how your loops behave. One of its most useful features is `loop_var`, which lets you rename the loop variable:

```text
- name: Install multiple packages
  ansible.builtin.apt:
    name: "{{ package }}"
    state: present
  loop:
    - nginx
    - postgres
    - redis
  loop_control:
    loop_var: package
```

Here, we’ve used `loop_var: package` to rename the loop variable from `item` to `package`, making the playbook more readable.

## Looping Over Dictionaries

Loops become even more powerful when working with dictionaries:

```text
- name: Create multiple users with specific properties
  ansible.builtin.user:
    name: "{{ user.name }}"
    groups: "{{ user.groups }}"
    state: present
  loop:
    - { name: 'john', groups: 'admins' }
    - { name: 'jane', groups: 'developers' }
    - { name: 'bob', groups: 'support' }
  loop_control:
    loop_var: user
```

This example demonstrates how to loop over a list of dictionaries, creating users with specific properties.

## Nested Loops

Ansible supports nested loops, allowing you to iterate over multiple lists:

```text
---
# sample-loop.yml
- name: Print outer and inner items
  ansible.builtin.debug:
    msg: "outer item={{ outer_item }} inner item={{ item }}"
  loop:
    - a
    - b
    - c
```

```text
    - include_tasks: sample-loop.yml      loop:
        - 1
        - 2
        - 3
      loop_control:
        loop_var: outer_item
```

This loops through two loops

```text
ok: [localhost] => (item=a) => {
    "msg": "outer item=1 inner item=a"
}
ok: [localhost] => (item=b) => {
    "msg": "outer item=1 inner item=b"
}
ok: [localhost] => (item=c) => {
    "msg": "outer item=1 inner item=c"
}
ok: [localhost] => (item=a) => {
    "msg": "outer item=2 inner item=a"
}
ok: [localhost] => (item=b) => {
    "msg": "outer item=2 inner item=b"
}
ok: [localhost] => (item=c) => {
    "msg": "outer item=2 inner item=c"
}
ok: [localhost] => (item=a) => {
    "msg": "outer item=3 inner item=a"
}
ok: [localhost] => (item=b) => {
    "msg": "outer item=3 inner item=b"
}
ok: [localhost] => (item=c) => {
    "msg": "outer item=3 inner item=c"
}
```

## Using Loops with Include Statements

Loops can be used with `include_tasks` to dynamically include task files:

```text
- name: Include task file for each user
  include_tasks: user_setup.yml
  loop:
    - { name: 'john', role: 'admin' }
    - { name: 'jane', role: 'developer' }
  loop_control:
    loop_var: current_user
```

This includes and executes the `user_setup.yml` task file for each user in the loop.

## Advanced Loop Techniques

Ansible offers several advanced looping techniques:

1. **with\_items**: An older syntax, still supported but `loop` is preferred.
2. **with\_dict**: For iterating over dictionary key-value pairs.
3. **with\_fileglob**: For looping over files matching a pattern.
4. **with\_sequence**: For generating a sequence of items to iterate over.

Example of `with_sequence`:

```text
- name: Create multiple directories
  ansible.builtin.file:
    path: "/tmp/dir{{ item }}"
    state: directory
  with_sequence: start=1 end=5 format="%02d"
```

This creates directories named dir01 through dir05.

## Best Practices and Tips

1. Use meaningful names for your loop variables with `loop_var`.
2. Keep your loops simple and readable. If a loop becomes too complex, consider breaking it into separate tasks.
3. Use `loop` instead of `with_items` for better performance and consistency.
4. Be mindful of the performance impact when looping over large datasets.
5. Use `loop_control: label` to customize the output of your loops for better readability in Ansible output.

## Happy looping!
