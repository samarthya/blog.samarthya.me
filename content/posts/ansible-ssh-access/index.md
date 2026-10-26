---
title: "Ansible: SSH Access"
date: "2023-02-08T12:00:00Z"
slug: "ansible-ssh-access"
description: "To set up SSH access for inventory hosts in Ansible, follow these steps:"
categories: ["technical"]
tags: ["ansible", "ssh"]
aliases: ["/wps/2023/02/08/ansible-ssh-access/"]
recovered: "Internet Archive snapshot 2026-03-13"
---

To set up SSH access for inventory hosts in `Ansible`, follow these steps:

1. Generate an SSH key pair
   - `ssh-keygen -t rsa`
2. Copy the public key to the remote host
   - `ssh-copy-id user@hostname`
3. Test the connection to the remote host:
   - `ssh user@hostname`
4. Modify the `ansible.cfg` file to set the remote user, if necessary.
5. Add the remote host to the Ansible inventory file.
6. Run the Ansible playbook to execute the desired tasks on the remote host.

Note: If you need to access multiple remote hosts, repeat steps 2-5 for each host.
