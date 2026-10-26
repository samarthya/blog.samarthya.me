---
title: "Failed to connect to bus: No medium found"
date: "2024-09-11T12:00:00Z"
slug: "failed-to-connect-to-bus-no-medium-found"
description: "If you have ever seen this error, you know the pain of a fellow linux user."
categories: ["technical"]
tags: ["docker", "linux"]
aliases: ["/wps/2024/09/11/failed-to-connect-to-bus-no-medium-found/"]
recovered: "Internet Archive snapshot 2026-03-13"
---

![](mg.jpg)

If you have ever seen this error, you know the pain of a fellow linux user.

```text
Failed to connect to bus: No medium found
```

This is message I get when I was trying to install `podman.socket`

```text
systemctl enable --now podman.socket --user -M samarthya@
```

**Why do we need Podman.socket?**

- **Communication with other applications:** `podman.socket` enables other applications, such as container orchestration tools or custom scripts, to interact with Podman without requiring direct access to the Podman binary. This provides a more secure and flexible way to manage containers.
- **Integration with other tools:** `podman.socket` can be used by tools like Docker Compose or Kubernetes to communicate with Podman and manage containers.
- **Custom scripts and automation:** Podman.socket can be used to create custom scripts or automation workflows that interact with Podman’s functionality.

In all googling I did I was able to see the problem boiling from `XDG_RUNTIME_DIR` which was empty on my host OS.

```text
> echo $XDG_RUNTIME_DIR
```

`XDG_RUNTIME_DIR` is an environment variable in Linux systems that specifies a directory for storing user-specific non-essential runtime files and other file objects. Its primary purposes include:

1. Providing a secure location for temporary runtime files.
2. Ensuring user-specific runtime data is cleaned up when the user logs out.
3. Offering a standardized location for applications to store runtime data.

The XDG\_RUNTIME\_DIR variable is part of the XDG Base Directory Specification, which was introduced by the `freedesktop.org` project (formerly X Desktop Group, hence XDG) in the early 2000s. This specification aimed to standardize file locations across different Linux distributions and desktop environments.

Key points in its history and development:

1. Early 2000s: The XDG Base Directory Specification was first proposed to address the lack of standardization in file locations across Linux systems.
2. 2010: XDG\_RUNTIME\_DIR was added to the specification in version 0.7. This addition was motivated by the need for a secure, user-specific location for runtime files that would be automatically cleaned up.
3. 2012: `systemd`, a system and service manager for Linux, began to create and manage XDG\_RUNTIME\_DIR, further standardizing its use across systems using `systemd`.
4. Over time: Various applications and services began relying on `XDG_RUNTIME_DIR` for storing temporary data, sockets, and other runtime objects.

The introduction of `XDG_RUNTIME_DIR` solved several problems:

1. `Security`: It provides a per-user directory with strict permissions, enhancing security for runtime data.
2. `Cleanup`: Unlike /tmp, which can accumulate files, XDG\_RUNTIME\_DIR is typically cleared when the user logs out.
3. `Standardization`: It offers a consistent location for applications to store runtime data across different Linux distributions.

Today, XDG\_RUNTIME\_DIR is widely used in modern Linux systems, particularly those using `systemd`. It plays a crucial role in managing user-specific runtime data and is an important part of the Linux filesystem hierarchy.

This is how I solved it.

```text
$ mkdir -p ~/.bashrc.d

$ cat << EOF > ~/.bashrc.d/systemd
export XDG_RUNTIME_DIR=/run/user/\$(id -u)
EOF
$ cat ~/.bashrc.d/systemd 
export XDG_RUNTIME_DIR=/run/user/$(id -u)
$ source ~/.bashrc.d/systemd

$ echo $XDG_RUNTIME_DIR
/run/user/59388

$ loginctl enable-linger $USER
$ systemctl --user daemon-reload
$ systemctl enable --now podman.socket --user -M samarthya@
$  systemctl status podman.socket --user
● podman.socket - Podman API Socket
     Loaded: loaded (/usr/lib/systemd/user/podman.socket; enabled; preset: disabled)
     Active: active (listening) since Wed 2024-09-11 15:21:32 UTC; 2min 1s ago
      Until: Wed 2024-09-11 15:21:32 UTC; 2min 1s ago
   Triggers: ● podman.service
       Docs: man:podman-system-service(1)
     Listen: /run/user/59388/podman/podman.sock (Stream)
     CGroup: /user.slice/user-59388.slice/user@59388.service/app.slice/podman.socket
```

I can see the session is lingering

```text
loginctl list-users
  UID USER    LINGER STATE    
59388 samarthya yes    lingering

1 users listed.
```

## What is `loginctl`?

`loginctl` was introduced as part of `systemd`, which was first released in 2010. It was developed by `Lennart Poettering` and `Kay Sievers`, initially for Fedora Linux, but has since been adopted by many other distributions.

### Significance

`loginctl` is a crucial tool in modern Linux systems that use `systemd`. It provides a way to introspect and control the login manager, which is responsible for keeping track of user sessions, seats (hardware setups like keyboards, mice, and monitors), and users.

### **Uses**

1. List active sessions, users, and seats
2. Show properties of users, sessions, and seats
3. Attach or detach devices to seats
4. Enable or disable multi-seat support
5. Terminate user sessions
6. Manage user linger state (more on this below)

Common commands:

- `loginctl list-sessions`: Lists all active sessions
- `loginctl list-users`: Lists all known users
- `loginctl show-user <username>`: Shows properties of a specific user
- `loginctl terminate-session <session-id>`: Terminates a specific session

### `loginctl enable-linger $USER`

The `loginctl enable-linger $USER` command is particularly interesting and relates to how `systemd` manages user sessions.

Let’s break it down:

**What it does**: This command enables “lingering” for the specified user. When lingering is enabled, `systemd` will maintain the user’s session even when they’re not logged in.

Why we need it:

1. Persistent User Services: It allows user-specific systemd services to run independently of user logins. This is crucial for users who want to run long-lived processes or services under their own user account.
2. Remote Management: It’s particularly useful in server environments where you want user services to continue running after SSH disconnections.
3. Scheduled Tasks: It enables user-specific timers (systemd’s version of cron jobs) to run even when the user is not logged in.
4. Container Management: For tools like Podman that run containers in user space, lingering allows these containers to keep running after logout.

**How it works**:

1. Without lingering, systemd typically terminates all of a user’s processes when they log out.
2. With lingering enabled, `systemd` maintains a user manager for that user even when they’re not logged in.
3. This user manager can then keep user services running persistently.
