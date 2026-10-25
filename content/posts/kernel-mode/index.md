---
title: "Kernel Mode"
date: "2020-10-17T14:58:39Z"
slug: "kernel-mode"
categories: ["technical"]
tags: ["linux", "refresher", "tips"]
aliases: ["/wps/2020/10/17/kernel-mode/"]
wp_id: 1096
---

The CPU operates in two modes in Linux

1. User mode (non privileged mode)
2. Kernel mode (System mode)

When operating in Kernel mode it has un-restricted access to resources like memory and input output devices.

{{< lead >}}
Kernel is a trusted software and all other programs are treated as untrusted softwares.
{{< /lead >}}

## Mode switch

All processes start execution in the user mode, and they switch to kernel mode only when obtaining a service provided by the kernel. This change in mode is termed a *mode switch*.

{{< lead >}}
A *system call*, sometimes referred to as a *kernel call*
— system call
{{< /lead >}}

## How does the interaction happen?

Ever so often the user mode program needs to access a privileged resource and that happens via system calls.

{{< lead >}}
A system call is a request to the kernel by an *active process* for a service performed by the kernel.
{{< /lead >}}

When a user process runs a portion of the kernel code via a system call, the process temporarily shifts into the kernel mode.

## Preemptive vs non-preemptive

A preemptive task can be interrupted before it completes its function whereas a non preemptive task cannot be interrupted before it completes its task.

Process in kernel mode can be interrupted by an *interrupt* or an *exception*.

{{< lead >}}
A process in kernel mode cannot be arbitrarily suspended and replaced by another process for the duration of its *time slice*
— Preempted
{{< /lead >}}
