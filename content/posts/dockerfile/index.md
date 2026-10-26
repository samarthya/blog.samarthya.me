---
title: "Dockerfile"
date: "2020-07-15T12:00:00Z"
slug: "dockerfile"
description: "I would move in stages, like a good learning guide always recommends."
categories: ["technical"]
tags: ["docker"]
aliases: ["/wps/2020/07/15/dockerfile/"]
recovered: "Internet Archive snapshot 2026-06-10"
---

`docker build` builds a docker image by reading instructions (directives) from a text file called `Dockerfile`

> The build is run by the Docker daemon, not by the CLI

## Hello World!

I would move in stages, like a good learning guide always recommends.

```text
# Lesson 1 - Using basic Dockerfile to compose an image
FROM alpine:3.7 
# Using alpine 3.7 latest on the day.
CMD ["echo","Hello world!"]
```

The file above uses two directives and an image

### Format: directive

Every directive you write in your docker file would follow a template

```text
# INSTRUCTION arguments
FROM alpine:3.7
```

`FROM` directive identifies the parent image

### alpine

This is a 5mb image small and convenient to get started in our case. You can find more details on how to use it [here](https://hub.docker.com/_/alpine).

```text
docker build -t samarthya/ahello:1.0 .
```

```text
Sending build context to Docker daemon  2.048kB
Step 1/2 : FROM alpine:3.7
 ---> 6d1ef012b567
Step 2/2 : CMD ["echo","Hello world!"]
 ---> Running in 4c96833eaeb6
Removing intermediate container 4c96833eaeb6
 ---> 460a990ca06c
Successfully built 460a990ca06c
Successfully tagged samarthya/ahello:1.0
```

```text
docker image ls
REPOSITORY                           TAG                                              IMAGE ID            CREATED              SIZE
samarthya/ahello                     1.0                                              460a990ca06c        About a minute ago   4.21MB
```

```text
docker image history 460a990ca06c
IMAGE               CREATED              CREATED BY                                      SIZE                COMMENT
460a990ca06c        About a minute ago   /bin/sh -c #(nop)  CMD ["echo" "Hello world!…   0B                  
6d1ef012b567        16 months ago        /bin/sh -c #(nop)  CMD ["/bin/sh"]              0B                  
<missing>           16 months ago        /bin/sh -c #(nop) ADD file:aa17928040e31624c…   4.21MB
```

A simple execution allows to see the desired output.

```text
docker run --name hello samarthya/ahello:1.0
Hello world!
```

## Reference

- https://hub.docker.com/\_/alpine
- <https://docs.docker.com/engine/reference/builder/#format>
