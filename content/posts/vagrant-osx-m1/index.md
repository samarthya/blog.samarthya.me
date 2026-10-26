---
title: "Vagrant OSX"
date: "2022-08-18T12:00:00Z"
slug: "vagrant-osx-m1"
description: "Having just bought an M1 – MacBook Pro the issue are mounting. The premier challenge was to get my Vagrant boxes configured with provider virtualbox to run."
categories: ["technical"]
tags: ["docker"]
aliases: ["/wps/2022/08/18/vagrant-osx-m1/"]
recovered: "Internet Archive snapshot 2025-08-07"
---

Having just bought an M1 – MacBook Pro the issue are mounting. The premier challenge was to get my Vagrant boxes configured with provider `virtualbox` to run.

Since VirtualBox clearly calls it out “no support”

> 💬 VirtualBox is a powerful x86 and AMD64/Intel64 [virtualization](https://www.virtualbox.org/wiki/Virtualization) product for enterprise as well as home use.

The challenge was to find out what can work in the shortest time. I am keen to explore the `qemu` and `KVM's` but that is for another day as Docker seems to be the convenient solution for me.

```text
> vagrant version
Installed Version: 2.3.0
Latest Version: 2.3.0
 
You're running an up-to-date version of Vagrant!
```

Let’s create our first working version before targeting complex `Vagrantfile's`.

```text
> vagrant init 
A `Vagrantfile` has been placed in this directory. You are now
ready to `vagrant up` your first virtual environment! Please read
the comments in the Vagrantfile as well as documentation on
`vagrantup.com` for more information on using Vagrant.
```

The command above generates a template Vagrantfile that I will use to sequentially edit and get a centos machine up and running.

```text
# -*- mode: ruby -*-
# vi: set ft=ruby :

# All Vagrant configuration is done below. The "2" in Vagrant.configure
# configures the configuration version (we support older styles for
# backwards compatibility). Please don't change it unless you know what
# you're doing.
Vagrant.configure("2") do |config|
  # The most common configuration options are documented and commented below.
  # For a complete reference, please see the online documentation at
  # https://docs.vagrantup.com.

  # Every Vagrant development environment requires a box. You can search for
  # boxes at https://vagrantcloud.com/search.
  config.vm.box = "base"

  # Disable automatic box update checking. If you disable this, then
  # boxes will only be checked for updates when the user runs
  # `vagrant box outdated`. This is not recommended.
  # config.vm.box_check_update = false

  # Create a forwarded port mapping which allows access to a specific port
  # within the machine from a port on the host machine. In the example below,
  # accessing "localhost:8080" will access port 80 on the guest machine.
  # NOTE: This will enable public access to the opened port
  # config.vm.network "forwarded_port", guest: 80, host: 8080

  # Create a forwarded port mapping which allows access to a specific port
  # within the machine from a port on the host machine and only allow access
  # via 127.0.0.1 to disable public access
  # config.vm.network "forwarded_port", guest: 80, host: 8080, host_ip: "127.0.0.1"

  # Create a private network, which allows host-only access to the machine
  # using a specific IP.
  # config.vm.network "private_network", ip: "192.168.33.10"

  # Create a public network, which generally matched to bridged network.
  # Bridged networks make the machine appear as another physical device on
  # your network.
  # config.vm.network "public_network"

  # Share an additional folder to the guest VM. The first argument is
  # the path on the host to the actual folder. The second argument is
  # the path on the guest to mount the folder. And the optional third
  # argument is a set of non-required options.
  # config.vm.synced_folder "../data", "/vagrant_data"

  # Provider-specific configuration so you can fine-tune various
  # backing providers for Vagrant. These expose provider-specific options.
  # Example for VirtualBox:
  #
  # config.vm.provider "virtualbox" do |vb|
  #   # Display the VirtualBox GUI when booting the machine
  #   vb.gui = true
  #
  #   # Customize the amount of memory on the VM:
  #   vb.memory = "1024"
  # end
  #
  # View the documentation for the provider you are using for more
  # information on available options.

  # Enable provisioning with a shell script. Additional provisioners such as
  # Ansible, Chef, Docker, Puppet and Salt are also available. Please see the
  # documentation for more information about their specific syntax and use.
  # config.vm.provision "shell", inline: <<-SHELL
  #   apt-get update
  #   apt-get install -y apache2
  # SHELL
end
```

{{< lead >}}
[Official Vagrant Documentation](https://www.vagrantup.com/docs/providers/docker/basics)
— https://www.vagrantup.com/docs/providers/docker/basics
{{< /lead >}}

`Docker` provider behaves like just any other provider, but in comparison to Virtualbox it has specific options like `config.vm.box` that do NOT WORK.

Let’s add first box for docker to run

```text
config.vm.provider "docker" do |d|
    d.image = "centos:latest"
end
```

For my setup I get the following error.

```text
vagrant up --provider=docker
Bringing machine 'default' up with 'docker' provider...
==> default: Creating and configuring docker networks...
==> default: Creating the container...
    default:   Name: qemu-test_default_1660850922
    default:  Image: centos:latest
    default: Volume: /Users/samarthya/sourcebox/github.com/qemu-test:/vagrant
A Docker command executed by Vagrant didn't complete successfully!
The command run along with the output from the command is shown
below.

Command: ["docker", "run", "--name", "qemu-test_default_1660850922", "-d", "-v", "/Users/samarthya/sourcebox/github.com/qemu-test:/vagrant", "centos7:latest", {:notify=>[:stdout, :stderr]}]

Stderr: Unable to find image 'centos:latest' locally
docker: Error response from daemon: pull access denied for centos7, repository does not exist or may require 'docker login': denied: requested access to the resource is denied.
See 'docker run --help'.

Stdout:
```

Once you login `docker login` it should be able to pull the image (can be confirmed with `docker images` command)

The error I am stuck at is

```text
==> default: Starting container...
Guest-specific operations were attempted on a machine that is not
ready for guest communication. This should not happen and a bug
should be reported.
```
