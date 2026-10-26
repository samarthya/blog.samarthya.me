---
title: "UMASK: What is it?"
date: "2024-07-31T12:00:00Z"
slug: "umask-what-is-it"
description: "In Unix-like operating systems, file permissions play a critical role in ensuring system security and proper access control."
categories: ["technical"]
tags: ["linux"]
aliases: ["/wps/2024/07/31/umask-what-is-it/"]
recovered: "Internet Archive snapshot 2026-03-12"
---

![](random.jpg)

## Introduction

In Unix-like operating systems, file `permissions` play a critical role in ensuring system security and proper access control. One of the key tools for managing file permissions is the `umask` (user file creation mode mask). This blog post explores the history, purpose, and best practices for using `umask`.

{{< lead >}}
Umask (short for “user mask” or “user file creation mask”) is a concept in Unix and Unix-like operating systems that determines the default permissions for newly created files and directories. It essentially sets the default restrictions on file permissions when new files or directories are created.
{{< /lead >}}

## The History of Umask

The concept of `umask` traces its origins back to the early days of Unix in the 1970s. Unix, designed as a multi-user system, needed a robust way to manage file permissions to protect user data and ensure appropriate access control. The `umask` command was introduced as part of the Unix operating system to allow users to specify default permissions for newly created files and directories.

## Purpose of Umask

The primary purpose of `umask` is to set default file permissions for new files and directories. When a new file or directory is created, the system assigns it a set of default permissions, which are then modified by the `umask` value. The `umask` essentially acts as a filter, removing certain permissions based on its value.

## Understanding File Permissions

In Unix-like systems, file permissions are represented by three types of access:

- **Read (r)**: Ability to read the contents of the file.
- **Write (w)**: Ability to modify the contents of the file.
- **Execute (x)**: Ability to execute the file (for files) or access the directory contents (for directories).

Permissions are assigned to three categories of users:

- **Owner (u)**: The user who owns the file.
- **Group (g)**: Users who are members of the file’s group.
- **Others (o)**: All other users.

These permissions are represented by a three-digit octal number, where each digit corresponds to one of the user categories.

## How Umask Works

The `umask` value is also represented as a three-digit octal number, with each digit corresponding to one of the user categories (owner, group, others). The `umask` value is subtracted from the system’s default permissions to determine the final permissions for a new file or directory.

The default permissions for new files are typically `666` (read and write for all) and for directories `777` (read, write, and execute for all). The `umask` value modifies these defaults by “masking” certain permissions.

For example, consider a `umask` value of `022`:

- The first digit `0` means no permissions are masked for the owner.
- The second digit `2` means write permissions are masked for the group.
- The third digit `2` means write permissions are masked for others.

If a new file is created with the default permissions `666`, the final permissions will be `644` (`666 - 022`), meaning the owner has read and write permissions, while the group and others have read-only permissions.

### Setting and Viewing Umask

To view the current `umask` value, you can use the `umask` command without any arguments:

```text
umask
```

To set a new `umask` value, use the `umask` command followed by the desired value:

```text
umask 027
```

In this example, the `umask` value `027` means that new files will have `640` permissions, and new directories will have `750` permissions.

## Recommendations for Using Umask

1. **Understand Your Environment**: Determine the appropriate default permissions based on your system’s security requirements and user needs.
2. **Use Least Privilege**: Set the `umask` to ensure that new files and directories have the least permissions necessary. For example, a `umask` of `027` provides a good balance by allowing the owner full control while restricting group and others’ access.
3. **Configure System-Wide Umask**: In multi-user environments, configure a default `umask` in system-wide configuration files like `/etc/profile` or `/etc/bash.bashrc` to ensure consistent security practices.
4. **Review and Adjust**: Periodically review and adjust the `umask` settings as needed, especially when security policies or user requirements change.
