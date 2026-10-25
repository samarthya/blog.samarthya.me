---
title: "Dockeriz'd service"
date: "2020-08-13T05:51:34Z"
slug: "dockerizd-service"
categories: ["docker", "technical"]
tags: ["golang"]
aliases: ["/wps/2020/08/13/dockerizd-service/"]
wp_id: 910
---

Someone asked me to define a simple docker pod for the service I wrote in GOLang [here.]({{< relref "/posts/go-webservice-postget" >}}) I completely forgot about it, till today.

So here is my first attempt at getting a docker image for the service.

{{< lead >}}
The code is available [here](https://github.com/samarthya/gws.git).
{{< /lead >}}

My code space is organised as under, and I am using VS Code to write this docker file.

```text
├── Dockerfile
├── README.MD
├── gqs.code-workspace
└── src
    ├── counter
    │   ├── count.go
    │   └── count.service.go
    ├── go.mod
    ├── server.go
    ├── user
    │   ├── user.data.go
    │   ├── user.go
    │   └── user.service.go
    └── users.json
```

Let me first publish my `Dockerfile` and then I will explain it.

```text
# Building the container image for the image.
ARG VERSION=alpine

# Sets the base image
FROM golang:${VERSION} AS baseimage
RUN echo 'Building image...'

# Environment variable for the home directory
ENV home /server
WORKDIR ${home}

ADD ./src/counter/* ./counter/
ADD ./src/user/* ./user/
ADD ./src/server.go ./server.go
ADD ./src/go.mod ./go.mod
ADD ./src/users.json ./

RUN go build -o main server.go  

EXPOSE 8090
ENTRYPOINT [ "/server/main" ]
```

We start with the `FROM` using the `golang:alpine` image.

- The `ARG` instruction defines a variable that users can pass at build-time to the builder with the `docker build` command using the `--build-arg <varname>=<value>` flag. The default value is `alpine` in our case.
- The `FROM` instruction initialises a new build stage and sets the *Base Image* for subsequent instructions.
- The `RUN` instruction will execute any commands in a new layer on top of the current image and commit the results. The resulting committed image will be used for the next step in the `Dockerfile`. In our case it is a simple Text message `denoting build initiation`.
- The `ENV` instruction sets the environment variable `home` to the `/server`. This value will be in the environment for all subsequent instructions in the build stage and can be replaced inline in many as well.
- The `WORKDIR` instruction sets the working directory to `${home}`for any `RUN`, `CMD`, `ENTRYPOINT`, `COPY` and `ADD` instructions that follow it in the `Dockerfile`.
- The multiple `ADD` instructions used copies files, directories or remote file URLs from `<src>` and adds them to the filesystem of the image at the path `<dest>`.
- The `RUN` instruction used begins building the program binary.
- The `EXPOSE` instruction informs Docker that the container listens on the specified network ports at runtime. You can specify whether the port listens on TCP or UDP, and the default is TCP if the protocol is not specified.
- The final command `ENTRYPOINT` allows to configure a container that will run as an executable.

## Build image

```text
docker build -t samarthya/serviceingo:v1.0 .
```

Run the image

```text
docker run -d -p 9090:8090 --name smv samarthya/serviceingo:v1.0
```

```text
REPOSITORY                           TAG                                              IMAGE ID            CREATED             SIZE
samarthya/serviceingo                v1.0                                             10bc4a2e8183        15 hours ago        409MB
```

docker inspect can elaborate more in the image create.

```text
[
    {
        "Id": "sha256:10bc4a2e8183df14784a0ec97856559e1d8bf8c3f3dded73ece5b74a01da0f46",
        "RepoTags": [
            "samarthya/serviceingo:v1.0"
        ],
        "RepoDigests": [
            "samarthya/serviceingo@sha256:bac7"
        ],
        "Parent": "sha256:ba00",
        "Comment": "",
        "Created": "2020-08-12T14:33:20.916677548Z",
        "Container": "1af",
        "ContainerConfig": {
            "Hostname": "1afe36040e10",
            "Domainname": "",
            "User": "",
            "AttachStdin": false,
            "AttachStdout": false,
            "AttachStderr": false,
            "ExposedPorts": {
                "8090/tcp": {}
            },
            "Tty": false,
            "OpenStdin": false,
            "StdinOnce": false,
            "Env": [
                "PATH=/go/bin:/usr/local/go/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin",
                "GOLANG_VERSION=1.15",
                "GOPATH=/go",
                "home=/server"
            ],
            "Cmd": [
                "/bin/sh",
                "-c",
                "#(nop) ",
                "ENTRYPOINT [\"/server/main\"]"
            ],
            "Image": "sha256:ba0",
            "Volumes": null,
            "WorkingDir": "/server",
            "Entrypoint": [
                "/server/main"
            ],
            "OnBuild": null,
            "Labels": {}
        },
        "DockerVersion": "19.03.12",
        "Author": "",
        "Config": {
            "Hostname": "",
            "Domainname": "",
            "User": "",
            "AttachStdin": false,
            "AttachStdout": false,
            "AttachStderr": false,
            "ExposedPorts": {
                "8090/tcp": {}
            },
            "Tty": false,
            "OpenStdin": false,
            "StdinOnce": false,
            "Env": [
                "PATH=/go/bin:/usr/local/go/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin",
                "GOLANG_VERSION=1.15",
                "GOPATH=/go",
                "home=/server"
            ],
            "Cmd": null,
            "Image": "sha256:ba00f",
            "Volumes": null,
            "WorkingDir": "/server",
            "Entrypoint": [
                "/server/main"
            ],
            "OnBuild": null,
            "Labels": null
        },
        "Architecture": "amd64",
        "Os": "linux",
        "Size": 409358142,
        "VirtualSize": 409358142,
        "GraphDriver": {
            "Data": {
                "LowerDir": "/var/lib/docker/overlay2/ca784789ba90274d9bb7ea66d6fd88bb802f04a81117b33e271fbcf05a52f0ec/diff:/var/lib/docker/overlay2/3148cf2fd8b0c66a0609dfcdf19cad2e6434117379765f4329eca82d750e2b1b/diff:/var/lib/docker/overlay2/6ff4ab6c9f99471ca4d4c06fefdfa80fe95b2eda9505e55d2b2b7746d4a3070d/diff:/var/lib/docker/overlay2/756a454e35cf1dfcf450829ddd10f90a85b8b41e447a01d3a1c483a06b6a6e0d/diff:/var/lib/docker/overlay2/4e64169defbd603b6c390e9e2447a2a1d7596b46a516013e03e43b15d2e1e0fa/diff:/var/lib/docker/overlay2/c0f2ddbe44ea7b5fb17a3074ceae1478c08d0dce890c5d17b25c32b17fe0904a/diff:/var/lib/docker/overlay2/7af1b9667dc01775de4c71554e10e54e3cc424000dd1823f26682065c74fd7e4/diff:/var/lib/docker/overlay2/42c28bbea609cc637ca22830bd78a5a8b9f1f15385d21abd8ddd37bb12917304/diff:/var/lib/docker/overlay2/bb96c77843dbe71872b0b5368519eee56e5f13883c8fd1eb2184724ff93dba70/diff:/var/lib/docker/overlay2/db8152e75c500db9e23be1063f963527a685c61552a12b1c13d23d43af621ef9/diff:/var/lib/docker/overlay2/6f5/diff",
                "MergedDir": "/var/lib/docker/overlay2/c38/merged",
                "UpperDir": "/var/lib/docker/overlay2/c38/diff",
                "WorkDir": "/var/lib/docker/overlay2/c38/work"
            },
            "Name": "overlay2"
        },
        "RootFS": {
            "Type": "layers",
            "Layers": [
                "sha256:506",
                "sha256:0f7",
                "sha256:1ba1",
                "sha256:91f",
                "sha256:02d0",
                "sha256:1a7a",
                "sha256:5e95",
                "sha256:23a",
                "sha256:a3e",
                "sha256:4ea8",
                "sha256:ea8c",
                "sha256:dd2"
            ]
        },
        "Metadata": {
            "LastTagTime": "2020-08-12T14:33:20.942126827Z"
        }
    }
]
```

## References

- <https://docs.docker.com/engine/reference/builder/>
- <https://hub.docker.com/layers/golang/library/golang/alpine/images/sha256-660d670cbe7d9f5d183bc4ab8603cbd05a3436404475a5718876cb58c14e9a11?context=explore>
