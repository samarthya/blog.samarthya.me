---
title: "A Maintainable Ansible Playbook Structure"
date: "2024-09-14"
description: "A small project layout for turning a working Ansible playbook into reusable roles without losing clarity."
categories: ["technical"]
tags: ["ansible", "devops"]
series: ["Back to basics"]
draft: false
---

My first Ansible playbook was a single file. It installed packages, created users, copied configuration, and restarted services. It was a reasonable starting point. The problem began when every change required editing the same file, which had quietly become a miniature operating system.

That was my signal to introduce structure, but not to turn a small playbook into a framework.

{{< alert "circle-info" >}}
Written up in October 2026 from my notes at the time. The check-mode result below is illustrative rather than a capture from the original run.
{{< /alert >}}

## Start with a clear boundary

One workable layout is:

```text
ansible/
  ansible.cfg
  inventories/
    lab/hosts.ini
    production/hosts.ini
  playbooks/
    site.yml
  roles/
    common/
      defaults/main.yml
      handlers/main.yml
      tasks/main.yml
      templates/
    kafka/
      defaults/main.yml
      handlers/main.yml
      tasks/main.yml
      templates/
```

The playbook should compose roles. A role should expose a small set of variables and own the files it manages.

```yaml
---
- name: Configure the Kafka platform
  hosts: kafka_brokers
  become: true
  roles:
    - common
    - kafka
```

## Defaults are the public interface

Put safe, documented defaults in `roles/kafka/defaults/main.yml`:

```yaml
---
kafka_user: kafka
kafka_data_dir: /var/lib/kafka
kafka_service_name: kafka
```

Variables that must change by environment belong in inventory or an encrypted variable file. Keep role tasks independent of a particular hostname or IP address.

## Handlers describe consequences

Configuration changes should notify a handler rather than restarting a service unconditionally:

```yaml
- name: Install broker configuration
  ansible.builtin.template:
    src: server.properties.j2
    dest: /etc/kafka/server.properties
    owner: root
    group: kafka
    mode: "0640"
  notify: Restart Kafka
```

```yaml
- name: Restart Kafka
  ansible.builtin.service:
    name: "{{ kafka_service_name }}"
    state: restarted
```

Handlers run once at the end of the play, even if several tasks notify the same handler. That reduces unnecessary restarts.

## Use tags sparingly

Tags are useful for focused operations such as `--tags config` or `--tags packages`. They become confusing when every task has several tags. Prefer role boundaries and `--limit` first; add tags only for a repeatable operational workflow.

## Validate the role

Before applying a role to a cluster:

```bash
ansible-playbook -i inventories/lab/hosts.ini playbooks/site.yml --syntax-check
ansible-playbook -i inventories/lab/hosts.ini playbooks/site.yml --check --diff
```

Illustrative second-run summary:

```text
PLAY RECAP **********************************************************
kafka01                    : ok=7  changed=0  unreachable=0  failed=0
```

Molecule or a disposable virtual machine can test service startup and idempotence. The most useful test is often simple: run the role twice and confirm that the second run reports no changes.

Good structure is not about creating more directories. It is about defining ownership: inventories describe environments, playbooks describe orchestration, and roles describe reusable capabilities.
