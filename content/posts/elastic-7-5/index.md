---
title: "Elastic 7.5"
date: "2020-01-06"
slug: "elastic-7-5"
categories: ["personal"]
tags: ["technical"]
aliases: ["/wps/2020/01/06/elastic-7-5/", "/wps/2026/10/23/elastic-7-5/"]
wp_id: 227
---

## Installing

### Step 1: Using docker

```sh
yum install docker
docker pull docker.elastic.co/elasticsearch/elasticsearch:7.5.1
```

```text
systemctl list-units --type=service
```

```text
docker version
Client:
 Version:         1.13.1
 API version:     1.26
 Package version:
```

```text
Cannot connect to the Docker daemon at unix:///var/run/docker.sock. Is the docker daemon running?
```

```text
sudo systemctl start docker
```

```text
docker version
Client:
 Version:         1.13.1
 API version:     1.26
 Package version: docker-1.13.1-103.git7f2769b.el7.centos.x86_64
 Go version:      go1.10.3
 Git commit:      7f2769b/1.13.1
 Built:           Sun Sep 15 14:06:47 2019
 OS/Arch:         linux/amd64

Server:
 Version:         1.13.1
 API version:     1.26 (minimum version 1.12)
 Package version: docker-1.13.1-103.git7f2769b.el7.centos.x86_64
 Go version:      go1.10.3
 Git commit:      7f2769b/1.13.1
 Built:           Sun Sep 15 14:06:47 2019
 OS/Arch:         linux/amd64
 Experimental:    false
```

```text
docker pull docker.elastic.co/elasticsearch/elasticsearch:7.5.1
Trying to pull repository docker.elastic.co/elasticsearch/elasticsearch ... 
7.5.1: Pulling from docker.elastic.co/elasticsearch/elasticsearch
c808caf183b6: Pull complete 
05ff3f896999: Pull complete 
82fb7fb0a94e: Pull complete 
c4d0024708f4: Pull complete 
136650a16cfe: Pull complete 
968db096c092: Pull complete 
42547e91692f: Pull complete 
Digest: sha256:b0960105e830085acbb1f9c8001f58626506ce118f33816ea5d38c772bfc7e6c
Status: Downloaded newer image for docker.elastic.co/elasticsearch/elasticsearch:7.5.1
```

```txt
docker pull docker.elastic.co/kibana/kibana:7.5.1
```
