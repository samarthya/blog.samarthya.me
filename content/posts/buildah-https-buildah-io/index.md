---
title: "Buildah: https://buildah.io/"
date: "2023-03-07T12:00:00Z"
slug: "buildah-https-buildah-io"
description: "Buildah is a command-line tool used for building and managing OCI-compliant images. It is an alternative to Docker Build that provides greater flexibility and control over the image building process."
categories: ["docker", "technical"]
tags: ["buildah", "docker"]
aliases: ["/wps/2023/03/07/buildah-https-buildah-io/"]
recovered: "Internet Archive snapshot 2026-05-18"
---

![](https://buildah.io/images/buildah.png)

Buildah is a command-line tool used for building and managing OCI-compliant images. It is an alternative to Docker Build that provides greater flexibility and control over the image building process.

In this blog, we will explore what Buildah is and how to use it.

### What is Buildah?

`Buildah` is a container image builder that uses standard container images as its build output format. `Buildah` can be used as a standalone tool or as a library in larger applications. It is part of the larger Podman project, which is an open-source container engine that runs as a rootless user.

`Buildah` is different from Docker Build because it does not require a daemon to be running, making it an ideal tool for building images in a `containerized environment`. Instead, `Buildah` uses the `Buildah` `Buildah container` to build the images, providing a more secure and isolated environment for building images.

### How to use `Buildah`?

`Buildah` is a command-line tool, and it can be used to build images in a few simple steps.

#### Step 1: Installing Buildah

To use `Buildah`, you need to install it on your system. Buildah is available for most Linux distributions and can be installed using the package manager. For example, on Ubuntu, you can install Buildah using the following command:

```text
$ sudo apt-get install buildah
```

#### Step 2: Creating a Container Image

The first step in creating an image with Buildah is to create a container image. To create a new container image, use the `buildah from` command:

```text
$ buildah from centos
```

This command will create a new container image based on the CentOS image. You can then use the `buildah run` command to execute commands inside the container.

#### Step 3: Adding Packages

You can add packages to the container image using the `buildah run` command. For example, to install the Apache web server, use the following command:

```text
$ buildah run myimage yum -y install httpd
```

This command will install the Apache web server inside the container.

#### Step 4: Configuring the Image

You can configure the image by adding files or modifying configuration files using the `buildah copy` command. For example, to copy the `index.html` file to the web server’s document root directory, use the following command:

```text
$ buildah copy myimage index.html /var/www/html/
```

#### Step 5: Saving the Image

Once you have built and configured the image, you can save it to a file using the `buildah commit` command:

```text
$ buildah commit myimage myimage:v1.0
```

This command will save the container image as a new image called `myimage:v1.0`.

#### Step 6: Pushing the Image to a Registry

Finally, you can push the image to a container registry using the `buildah push` command:

```text
$ buildah push myimage:v1.0 docker://registry.example.com/myimage:v1.0
```

This command will push the image to the `registry.example.com` container registry.
