---
title: "Privilege Escalation: How a `remote_user` and a `become_user` works"
date: "2024-07-26T12:00:00Z"
slug: "ansible-privilege-escalation"
description: "One of its Ansible’s features is the ability to execute tasks with elevated privileges, often necessary for managing system configurations. This process is known as privilege escalation."
categories: ["ansible", "technical"]
tags: ["ansible"]
aliases: ["/wps/2024/07/26/ansible-privilege-escalation/"]
recovered: "Internet Archive snapshot 2026-03-13"
---

![](image-ansible.jpg)

One of its Ansible’s features is the ability to execute tasks with elevated privileges, often necessary for managing system configurations. This process is known as privilege escalation.

Let’s dive into the details of how privilege escalation works in `Ansible`, how to configure it using different variables, and the best practices for secure and effective use.

## Understanding Privilege Escalation

Privilege escalation in `Ansible` refers to the ability to run tasks with higher permissions than the user who initially connects to the remote system. This is crucial for operations that require root or administrator access, such as installing packages, modifying system configurations, or managing services.

{{< lead >}}
To see all configuration possibilities you can use the following command  
`ansible-config init --disabled -t all > ansible.cfg`
— Ansible documentation
{{< /lead >}}

### Users in `Ansible` Context

- `user`: This is the user account on the control machine running Ansible.
- `remote_user`: This is the user account on the managed nodes that Ansible connects to via SSH.
- `become_user`: This is the user account on the managed nodes to which Ansible escalates privileges.

### Key Variables for Privilege Escalation

Ansible uses several variables to control privilege escalation. Let’s explore each one:

1. `become`: This boolean variable enables or disables privilege escalation.
2. `become_method`: Specifies the privilege escalation method (e.g., sudo, su, pbrun).
3. `become_user`: Defines the user to become for privilege escalation.
4. `become_ask_pass`: Determines whether `Ansible` should prompt for a password.
5. `become_pass`: This defines the password for privilege escalation.
6. `become_pass_file`: This specifies a file containing the password for privilege escalation.
7. `become_flags`: This sets the flags to pass to the privilege escalation command.

Let’s look at how to configure each of these variables with examples.

#### 1. become

The `become` variable is the master switch for privilege escalation. When set to `true`, Ansible will attempt to escalate privileges for the specified tasks.

##### Example:

```text
- name: Install nginx
  apt:
    name: nginx
    state: present
  become: true
```

#### 2. become\_method

The `become_method` variable specifies how Ansible should escalate privileges. Common values include:

- sudo
- su
- pbrun
- pfexec
- doas
- dzdo
- ksu
- runas
- pmrun

##### Example:

```text
- name: Restart nginx service
  service:
    name: nginx
    state: restarted
  become: true
  become_method: sudo
```

#### 3. become\_user

The `become_user` variable allows you to specify which user Ansible should become when escalating privileges. This is particularly useful when you need to perform actions as a specific system user.

##### Example:

```text
- name: Create a directory as www-data
  file:
    path: /var/www/new_site
    state: directory
  become: true
  become_user: www-data
```

#### 4. become\_ask\_pass

When set to `true`, `become_ask_pass` prompts for a password for privilege escalation. This is useful when you can’t store the sudo password in plain text or when you need to enter it interactively.

##### Example:

```text
[privilege_escalation]
# (boolean) Toggle to prompt for privilege escalation password.
become_ask_pass=True
```

Once it is set and when you execute a playbook you should expect a prompt

```text
> ansible-playbook play-one.yml 
BECOME password:
```

### Combining Variables: Password and Password File Examples

Let’s look at two common scenarios for handling passwords:

#### 1. Interactive Password Prompt for the login user (SSH User, remote\_user)

Let’s configure `ansible.cfg` with the required properties

```text
# (boolean) This controls whether an Ansible playbook should prompt for a login password. If using SSH keys for authentication, you probably do not need to change this setting.
ask_pass=True

# (string) Sets the login user for the target machines
# When blank it uses the connection plugin's default, normally the user currently executing Ansible.
remote_user=ruser
```

```text
- hosts: all
  tasks:
    - name: Run a command as root
      command: whoami
      register: who
    - debug:
        var: who.stdout
```

Now when you run the playbook you should expect a password prompt

```text
> ansible-playbook play-two.yml
SSH password: 

PLAY [all] ***************************************************************************************************************************************************************************************************************************************************************************************************************************************************************

TASK [Gathering Facts] ***************************************************************************************************************************************************************************************************************************************************************************************************************************************************
ok: [localhost]

TASK [Run a command as root] *********************************************************************************************************************************************************************************************************************************************************************************************************************************************
changed: [localhost]

TASK [debug] *************************************************************************************************************************************************************************************************************************************************************************************************************************************************************
ok: [localhost] => {
    "who.stdout": "ruser"
}

PLAY RECAP ***************************************************************************************************************************************************************************************************************************************************************************************************************************************************************
localhost                  : ok=3    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
```

You can configure the password file as well

```text
# (boolean) This controls whether an Ansible playbook should prompt for a login password. If using SSH keys for authentication, you probably do not need to change this setting.
ask_pass=False

# (path) The password file to use for the connection plugin. --connection-password-file.
connection_password_file=./connection.yml
```

I added the password information in the local directory and now if you run you should be prompted for password

```text
> ansible-playbook play-two.yml

PLAY [all] ***************************************************************************************************************************************************************************************************************************************************************************************************************************************************************

TASK [Gathering Facts] ***************************************************************************************************************************************************************************************************************************************************************************************************************************************************
ok: [localhost]

TASK [Run a command as root] *********************************************************************************************************************************************************************************************************************************************************************************************************************************************
changed: [localhost]

TASK [debug] *************************************************************************************************************************************************************************************************************************************************************************************************************************************************************
ok: [localhost] => {
    "who.stdout": "ruser"
}

PLAY RECAP ***************************************************************************************************************************************************************************************************************************************************************************************************************************************************************
localhost                  : ok=3    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
```

Combining with become user now.

```text
- hosts: all
  become: true
  become_method: sudo
  tasks:
    - name: Run a command as root
      command: whoami
      register: who
    - debug:
        var: who.stdout
```

Now when I run with the configuration already defined in sections above.

```text
TASK [debug] *************************************************************************************************************************************************************************************************************************************************************************************************************************************************************
ok: [localhost] => {
    "who.stdout": "root"
}
```

Who is the ssh login user can be defined in two ways

- `remote_user`: Property in the ansible.cfg
- `ansible_user`: Property in the inventory for each host.
