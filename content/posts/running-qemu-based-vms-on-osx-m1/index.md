---
title: "Running QEMu based VM’s on OSX M1"
date: "2022-08-24T12:00:00Z"
slug: "running-qemu-based-vms-on-osx-m1"
description: "In this blog let’s try and look at some of the commands I used to build an RockyLinux machine on a MacPro M1."
categories: ["technical"]
tags: ["linux"]
aliases: ["/wps/2022/08/24/running-qemu-based-vms-on-osx-m1/"]
recovered: "Internet Archive snapshot 2025-08-07"
---

`A popular choice in the OSS QEMu is an open source machine emulator (system emulation/usermode emulation`) and virtualizer. Since I recently moved to Apple M1 silicone, I had not option of sticking to VirtualBox and was forced to relook at my options.

{{< lead >}}
The most recent version being `7.1.0-rc3` at the time of writing this blog.
— qemu.org
{{< /lead >}}

In this blog let’s try and look at some of the commands I used to build an RockyLinux machine on a MacPro M1.

> 💬 Look at the official man page [here](https://manpages.debian.org/testing/qemu-system-arm/qemu-system-aarch64.1.en.html).

> 💬 Another helpful [link](https://www.arthurkoziel.com/qemu-ubuntu-20-04/) that I used

Define the disk image

```text
> qemu-img create -f qcow2 centos4.brokers.test 15G
Formatting 'centos4.brokers.test', fmt=qcow2 cluster_size=65536 extended_l2=off compression_type=zlib size=16106127360 lazy_refcounts=off refcount_bits=16
```

You can look at the detailed help via

```text
> qemu-img --help
qemu-img version 7.0.0
Copyright (c) 2003-2022 Fabrice Bellard and the QEMU Project developers
usage: qemu-img [standard options] command [command options]
QEMU disk image utility

    '-h', '--help'       display this help and exit
    '-V', '--version'    output version information and exit
    '-T', '--trace'      [[enable=]<pattern>][,events=<file>][,file=<file>]
                         specify tracing options
```

The option we are interested in were

```text
create [--object objectdef] [-q] [-f fmt] [-b backing_file [-F backing_fmt]] [-u] [-o options] filename [size]
```

| Option | Description |
| --- | --- |
| -f | Defines the format. In our example qcow2 |
| centos2.brokers.test.qcow2 | File name on the disk |
| 15G | Size of the disk in bytes. Optional suffixes  “k” or “K” (kilobyte, 1024)  “M” (megabyte, 1024k) and  “G” (gigabyte, 1024M) and  “T” (terabyte, 1024G) are supported. |

https://linux.die.net/man/1/qemu-img

```text
> qemu-img check -f qcow2 centos4.brokers.test
No errors were found on the image.
Image end offset: 262144
```

{{< youtubeLite id="8K-jKdIm-Iw" label="How to enable KVM on a Mac for Qemu" >}}

Moving on; Once the disk has been defined let’s try and deploy the OS.

```text
> qemu-system-aarch64 --version
QEMU emulator version 7.0.0
Copyright (c) 2003-2022 Fabrice Bellard and the QEMU Project developers
```

Let me explain few arguments before I dive deeper into it.

-machine

```text
> qemu-system-aarch64 -machine help
```

You can look at the options you can supply by issuing the command above.

```text
Supported machines are:
virt                 QEMU 7.0 ARM Virtual Machine (alias of virt-7.0)
virt-7.0             QEMU 7.0 ARM Virtual Machine
```

**Sub-option**

`accel=` selects accelerator supported accelerators are kvm, xen, hax, hvf, nvmm, whpx or tcg (default: tcg)

```text
-accel [accel=]accelerator[,prop[=value][,...]]
                select accelerator (kvm, xen, hax, hvf, nvmm, whpx or tcg; use 'help' for a list)
                igd-passthru=on|off (enable Xen integrated Intel graphics passthrough, default=off)
                kernel-irqchip=on|off|split controls accelerated irqchip support (default=on)
                kvm-shadow-mem=size of KVM shadow MMU in bytes
                split-wx=on|off (enable TCG split w^x mapping)
                tb-size=n (TCG translation block cache size)
                dirty-ring-size=n (KVM dirty ring GFN count, default 0)
                thread=single|multi (enable multi-threaded TCG)
```

The other options are as under

```text
-machine [type=]name[,prop[=value][,...]]
                selects emulated machine ('-machine help' for list)
                property accel=accel1[:accel2[:...]] selects accelerator
                supported accelerators are kvm, xen, hax, hvf, nvmm, whpx or tcg (default: tcg)
                vmport=on|off|auto controls emulation of vmport (default: auto)
                dump-guest-core=on|off include guest memory in a core dump (default=on)
                mem-merge=on|off controls memory merge support (default: on)
                aes-key-wrap=on|off controls support for AES key wrapping (default=on)
                dea-key-wrap=on|off controls support for DEA key wrapping (default=on)
                suppress-vmdesc=on|off disables self-describing migration (default=off)
                nvdimm=on|off controls NVDIMM support (default=off)
                memory-encryption=@var{} memory encryption object to use (default=none)
                hmat=on|off controls ACPI HMAT support (default=off)
                memory-backend='backend-id' specifies explicitly provided backend for main RAM (default=none)
                sgx-epc.0.memdev=memid,sgx-epc.0.node=numaid
```

-smp

```text
> qemu-system-aarch64 -smp help
```

Allows you to specify specific cores and cpu values

```text
smp-opts options:
clusters=<num>
cores=<num>
cpus=<num>
dies=<num>
maxcpus=<num>
sockets=<num>
threads=<num>
```

```text
-smp [[cpus=]n][,maxcpus=maxcpus][,sockets=sockets][,dies=dies][,clusters=clusters][,cores=cores][,threads=threads]
                set the number of initial CPUs to 'n' [default=1]
                maxcpus= maximum number of total CPUs, including
                offline CPUs for hotplug, etc
                sockets= number of sockets on the machine board
                dies= number of dies in one socket
                clusters= number of clusters in one die
                cores= number of cores in one cluster
                threads= number of threads in one core
```

-drive

```text
> qemu-system-aarch64 -drive help
qemu-system-x86_64: -drive help: Must specify either driver or file
```

Look at the detailed options as below

```text
-drive [file=file][,if=type][,bus=n][,unit=m][,media=d][,index=i]
       [,cache=writethrough|writeback|none|directsync|unsafe][,format=f]
       [,snapshot=on|off][,rerror=ignore|stop|report]
       [,werror=ignore|stop|report|enospc][,id=name]
       [,aio=threads|native|io_uring]
       [,readonly=on|off][,copy-on-read=on|off]
       [,discard=ignore|unmap][,detect-zeroes=on|off|unmap]
       [[,bps=b]|[[,bps_rd=r][,bps_wr=w]]]
       [[,iops=i]|[[,iops_rd=r][,iops_wr=w]]]
       [[,bps_max=bm]|[[,bps_rd_max=rm][,bps_wr_max=wm]]]
       [[,iops_max=im]|[[,iops_rd_max=irm][,iops_wr_max=iwm]]]
       [[,iops_size=is]]
       [[,group=g]]
                use 'file' as a drive image
```

-boot

The sequence of boot. You can choose value based on CD-ROM “`d`” or hard-disk “`c`“.

```text
-boot [order=drives][,once=drives][,menu=on|off]
      [,splash=sp_name][,splash-time=sp_time][,reboot-timeout=rb_time][,strict=on|off]
                'drives': floppy (a), hard disk (c), CD-ROM (d), network (n)
                'sp_name': the file's name that would be passed to bios as logo picture, if menu=on
                'sp_time': the period that splash picture last if menu=on, unit is ms
                'rb_timeout': the timeout before guest reboot when boot failed, unit is ms
```

-m

Memory requirements for the guest system. My system has 32G so I can spare some for good quality VM’s (2048).

```text
-m [size=]megs[,slots=n,maxmem=size]
                configure guest RAM
                size: initial amount of guest memory
                slots: number of hotplug slots (default: none)
                maxmem: maximum amount of guest memory (default: none)
NOTE: Some architectures might enforce a specific granularity
```

-name

```text
-name string1[,process=string2][,debug-threads=on|off]
                set the name of the guest
                string1 sets the window title and string2 the process name.
```

-nographic

(Optional) disable graphical output and redirect serial I/Os to console

-vga

Display settings

```text
[std|cirrus|vmware|qxl|xenfb|tcx|cg3|virtio|none]
select video card type
```

Time to deploy the VM using the CDROM and boot preference for the ISO.

```text
> qemu-system-aarch64 -boot d -machine virt,highmem=off -accel hvf -bios QEMU_EFI.fd -cdrom ./Rocky-9.0-aarch64-dvd.iso -m 2G -hda centos4.brokers.test -cpu host -device virtio-gpu-pci -name centos4.brokers.test -display cocoa,show-cursor=on,full-grab=on -device qemu-xhci -device usb-tablet -device intel-hda -device usb-kbd
```

It should pop a window for you to follow the steps to install linux. Some of the reference images are attached below.

{{< gallery >}}
  <img src="screen-shot-2022-08-24-at-3.57.45-pm.png" alt="" class="grid-w33" />
  <img src="screen-shot-2022-08-24-at-3.59.07-pm.png" alt="" class="grid-w33" />
  <img src="screen-shot-2022-08-24-at-3.59.15-pm.png" alt="" class="grid-w33" />
  <img src="screen-shot-2022-08-24-at-3.59.24-pm.png" alt="" class="grid-w33" />
  <img src="screen-shot-2022-08-24-at-3.59.39-pm.png" alt="" class="grid-w33" />
  <img src="screen-shot-2022-08-24-at-3.59.54-pm.png" alt="" class="grid-w33" />
  <img src="screen-shot-2022-08-24-at-4.00.09-pm.png" alt="" class="grid-w33" />
  <img src="screen-shot-2022-08-24-at-4.00.34-pm.png" alt="" class="grid-w33" />
  <img src="screen-shot-2022-08-24-at-11.26.33-am.png" alt="" class="grid-w33" />
{{< /gallery >}}

Once installation is completed you will be prompted to reboot.

<img src="screen-shot-2022-08-24-at-4.06.32-pm.png" alt="" class="grid-w100" />

![Final steps](screen-shot-2022-08-24-at-4.07.25-pm.png "Final steps")

{{< gallery >}}
  <img src="screen-shot-2022-08-24-at-4.07.25-pm-1.png" alt="" class="grid-w33" />
  <img src="screen-shot-2022-08-24-at-4.08.39-pm.png" alt="" class="grid-w33" />
  <img src="screen-shot-2022-08-24-at-4.08.50-pm.png" alt="" class="grid-w33" />
  <img src="screen-shot-2022-08-24-at-4.08.57-pm-1.png" alt="" class="grid-w33" />
  <img src="screen-shot-2022-08-24-at-4.09.13-pm.png" alt="" class="grid-w33" />
  <img src="screen-shot-2022-08-24-at-4.09.43-pm.png" alt="" class="grid-w33" />
{{< /gallery >}}

Once you are done you can shut down the VM and change the option `-boot` to c from d and now it will boot from disk

```text
> qemu-system-aarch64 -boot c -machine virt,highmem=off -accel hvf -bios QEMU_EFI.fd -cdrom ./Rocky-9.0-aarch64-dvd.iso -m 2G -hda centos4.brokers.test -cpu host -device virtio-gpu-pci -name centos4.brokers.test -display cocoa,show-cursor=on,full-grab=on -device qemu-xhci -device usb-tablet -device intel-hda -device usb-kbd
```

![All done and machine is accessible](screen-shot-2022-08-24-at-4.19.24-pm-1.png "All done and machine is accessible")

### Help

- Raw format [example](https://adonis0147.github.io/post/qemu-macos-apple-silicon/)
- VDE [VMNET](https://github.com/lima-vm/vde_vmnet)
- [Bios](https://releases.linaro.org/components/kernel/uefi-linaro/16.02//release/qemu64/) from linaro.org
- [Libvirt](https://linuxconfig.org/how-to-use-bridged-networking-with-libvirt-and-kvm) and KVM
