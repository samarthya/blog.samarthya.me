---
title: "Containers: A brief take"
date: "2024-05-17T12:00:00Z"
slug: "containers-a-brief-take"
description: "The story of Linux containers is a tale of innovation and collaboration, with roots surprisingly deep in the history of the Linux operating system itself."
categories: ["technical"]
tags: ["container", "docker", "history", "linux"]
aliases: ["/wps/2024/05/17/containers-a-brief-take/"]
recovered: "Internet Archive snapshot 2026-01-16"
---

![](dock12.jpg)

The story of Linux containers is a tale of innovation and collaboration, with roots surprisingly deep in the history of the Linux operating system itself.

Let’s explore this fascinating journey, starting with a simple tool called `chroot`.

## **Chroot: A Stepping Stone**

Developed in the 1970s, `chroot` (ch-root) allows you to confine a process to a specific directory structure. This creates a limited environment, useful for security or running specific programs. While offering isolation, `chroot` has drawbacks.

It doesn’t manage resources or provide true process isolation, making it a rudimentary solution.

## **Namespaces: A Vision of Isolation**

The concept of `namespaces` emerged in the late 1990s. Namespaces isolate processes from seeing system resources used by other processes.

Imagine separate “universes” within the same kernel – processes in one namespace wouldn’t be aware of processes in another. This isolation paved the way for more **advanced containerization**.

## **`cgroups`: Resource Management Takes Center Stage**

Around 2006, Google introduced `cgroups` (control groups). **Cgroups** allow for resource allocation and control at the process level. You can define CPU, memory, and other resource limits for groups of processes, ensuring fairness and preventing runaway applications.

## **LXC: The First Container Champion**

In 2008, Linux Containers (LXC) arrived, combining the power of namespaces and cgroups. `LXC` provided a complete container management solution, allowing users to create isolated Linux environments on a single kernel. LXC was a significant step forward, but it still relied on a full Linux environment within each container, making them relatively heavyweight.

## **Docker: Democratizing Containers**

Docker, launched in 2013, revolutionized the container landscape. Docker containers are lightweight and share the underlying Linux kernel, making them faster and more efficient. Docker also introduced a user-friendly interface and a registry for sharing container images, making containerization accessible to a wider audience. Docker’s open-source approach and focus on developer experience fueled a meteoric rise in container adoption.

## **Podman: A Container Runtime for the Future**

While Docker dominates the container world, other players are emerging. Podman is a container runtime focused on security and compliance. It utilizes the same container engine (libcontainer) as Docker but offers a simpler and more lightweight solution. `Podman` is gaining traction, particularly in security-conscious environments.

The evolution from Docker to OCI (Open Container Initiative) and Podman is a story of standardization, flexibility, and fostering a healthy container ecosystem.

Let’s delve into the timeline:

## Docker: The Rise of a Container Kingpin

Docker, launched in 2013, exploded in popularity with its user-friendly approach to containerization. It offered a complete solution – building, running, and managing containers – all wrapped in a convenient interface. Docker also popularized container registries, making it easier to share containerized applications.

However, Docker’s dominance came with a caveat: vendor lock-in. With a tightly integrated ecosystem, users became reliant on Docker for every aspect of containerization. This lack of flexibility raised concerns about long-term sustainability and innovation.

While Docker offered a user-friendly experience, it relied on a central daemon process that always ran in the background. This daemon required elevated privileges, increasing the system’s attack surface. Additionally, managing the daemon could be cumbersome for some users.

## Enter OCI: Standardization for the Masses

In 2015, industry leaders recognized the need for open standards in container technology. This led to the formation of the `Open Container Initiative (OCI)`. `OCI` aimed to define open specifications for container `formats`, `runtimes`, and `images`.

The arrival of OCI marked a turning point. By establishing standards, OCI ensured that container images could run on any OCI-compliant runtime, not just Docker. This fostered competition and innovation in the container runtime space.

## **Podman Emerges: A Lightweight Challenger**

`Podman`, launched in 2017, is a prime example of OCI’s impact. Built on top of the same container engine (libcontainer) as Docker, Podman offers a more lightweight and security-focused alternative. It leverages OCI standards, allowing it to run Docker images seamlessly.

Here’s why Podman gained traction:

- **Security:** `Podman` focuses on security by running as an unprivileged user, reducing the attack surface.
- **Simplicity:** `Podman` offers a command-line interface similar to Docker but with a smaller footprint.
- **Flexibility:** OCI compliance allows `Podman` to integrate with various container orchestration tools.
- **No Daemon Needed:** Podman operates without a background daemon. This simplifies container management and reduces the attack surface as Podman itself runs with minimal privileges.
