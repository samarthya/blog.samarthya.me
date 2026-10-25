---
title: "Docker Registry"
date: "2020-07-29T10:23:38Z"
slug: "docker-registry"
categories: ["docker"]
tags: ["registry"]
aliases: ["/wps/2020/07/29/docker-registry/"]
wp_id: 809
---

> A Docker registry is a stateless, highly scalable server side application that stores and lets you distribute Docker images.

Docker registry is a central location that stores and distributes docker images. E.g. hub.docker.com is the default registry used when you are using `docker pull`.

## Why use a docker registry?

The reason can be any, but primarily it is have tighter control over how you distribute your images, and who downloads them.

### How to Run a Registry?

It is a simple image that you can execute using `docker run`

```text
docker run -d -p 5000:5000 --name registry registry:latest
```

### Adding an image to your registry

### [Configuring registry](https://docs.docker.com/registry/configuration/#override-specific-configuration-options)

Registry configuration like other files in docker universe is a YAML file, and can be accessed (for specific options) by supplying `-e` option and creating an environment like `REGISTRY_variable` where `variable` is the name of the option.

```text
docker run -d -p 5000:5000 --restart=always --name registry -e REGISTRY_LOG_LEVEL=debug -e REGISTRY_HTTP_SECRET=abcdef12345 registry:2
```

The command outputs a hash.

```text
d50064a4bb16155711241ff14e0e94dfa17e5e3bbc9136d555dd63e3243cc5f
```

Let's see if it has been honored

```text
docker logs registry
```

```text
time="2020-07-29T10:20:02.676285386Z" level=info msg="redis not configured" go.version=go1.11.2 instance.id=a3eab61f-dfc3-481e-bff5-d5148bed033b service=registry version=v2.7.1 
time="2020-07-29T10:20:02.676607678Z" level=info msg="Starting upload purge in 20m0s" go.version=go1.11.2 instance.id=a3eab61f-dfc3-481e-bff5-d5148bed033b service=registry version=v2.7.1 
time="2020-07-29T10:20:02.68618669Z" level=info msg="using inmemory blob descriptor cache" go.version=go1.11.2 instance.id=a3eab61f-dfc3-481e-bff5-d5148bed033b service=registry version=v2.7.1 
time="2020-07-29T10:20:02.686740221Z" level=info msg="listening on [::]:5000" go.version=go1.11.2 instance.id=a3eab61f-dfc3-481e-bff5-d5148bed033b service=registry version=v2.7.1 
[root@mundev001685 ~]# docker logs registry
time="2020-07-29T10:20:02.676285386Z" level=info msg="redis not configured" go.version=go1.11.2 instance.id=a3eab61f-dfc3-481e-bff5-d5148bed033b service=registry version=v2.7.1 
time="2020-07-29T10:20:02.676607678Z" level=info msg="Starting upload purge in 20m0s" go.version=go1.11.2 instance.id=a3eab61f-dfc3-481e-bff5-d5148bed033b service=registry version=v2.7.1 
time="2020-07-29T10:20:02.68618669Z" level=info msg="using inmemory blob descriptor cache" go.version=go1.11.2 instance.id=a3eab61f-dfc3-481e-bff5-d5148bed033b service=registry version=v2.7.1 
time="2020-07-29T10:20:02.686740221Z" level=info msg="listening on [::]:5000" go.version=go1.11.2 instance.id=a3eab61f-dfc3-481e-bff5-d5148bed033b service=registry version=v2.7.1 
time="2020-07-29T10:20:12.687141013Z" level=debug msg="filesystem.Stat("/")" go.version=go1.11.2 instance.id=a3eab61f-dfc3-481e-bff5-d5148bed033b service=registry trace.duration=83.533µs trace.file="/go/src/github.com/docker/distribution/registry/storage/driver/base/base.go" trace.func="github.com/docker/distribution/registry/storage/driver/base.(*Base).Stat" trace.id=c5040120-f1fc-4ee2-9b42-9549e6e8535e trace.line=155 version=v2.7.1 
time="2020-07-29T10:20:22.687191951Z" level=debug msg="filesystem.Stat("/")" go.version=go1.11.2 instance.id=a3eab61f-dfc3-481e-bff5-d5148bed033b service=registry trace.duration=66.546µs trace.file="/go/src/github.com/docker/distribution/registry/storage/driver/base/base.go" trace.func="github.com/docker/distribution/registry/storage/driver/base.(*Base).Stat" trace.id=55c23278-9c49-4409-84fb-286a013d3fb1 trace.line=155 version=v2.7.1 
time="2020-07-29T10:20:32.687172108Z" level=debug msg="filesystem.Stat("/")" go.version=go1.11.2 instance.id=a3eab61f-dfc3-481e-bff5-d5148bed033b service=registry trace.duration=70.495µs trace.file="/go/src/github.com/docker/distribution/registry/storage/driver/base/base.go" trace.func="github.com/docker/distribution/registry/storage/driver/base.(*Base).Stat" trace.id=7fb56ccb-f9be-4727-bf78-0fb43283f5da trace.line=155 version=v2.7.1 
time="2020-07-29T10:20:42.687180724Z" level=debug msg="filesystem.Stat("/")" go.version=go1.11.2 instance.id=a3eab61f-dfc3-481e-bff5-d5148bed033b service=registry trace.duration=75.809µs trace.file="/go/src/github.com/docker/distribution/registry/storage/driver/base/base.go" trace.func="github.com/docker/distribution/registry/storage/driver/base.(*Base).Stat" trace.id=6ad9561c-d1f2-4ab6-bd19-3cbd5e58eaca trace.line=155 version=v2.7.1
```

Voila you can see a debug message at the bottom

```text
time="2020-07-29T10:20:32.687172108Z" level=debug msg="filesystem.Stat("/")" go.version=go1.11.2 instance.id=a3eab61f-dfc3-481e-bff5-d5148bed033b service=registry trace.duration=70.495µs trace.file="/go/src/github.com/docker/distribution/registry/storage/driver/base/base.go" trace.func="github.com/docker/distribution/registry/storage/driver/base.(*Base).Stat" trace.id=7fb56ccb-f9be-4727-bf78-0fb43283f5da trace.line=155 version=v2.7.1 
time="2020-07-29T10:20:42.687180724Z" level=debug msg="filesystem.Stat("/")" go.version=go1.11.2 instance.id=a3eab61f-dfc3-481e-bff5-d5148bed033b service=registry trace.duration=75.809µs trace.file="/go/src/github.com/docker/distribution/registry/storage/driver/base/base.go" trace.func="github.com/docker/distribution/registry/storage/driver/base.(*Base).Stat" trace.id=6ad9561c-d1f2-4ab6-bd19-3cbd5e58eaca trace.line=155 version=v2.7.1
```

### TLS security

Let's add some SSL security to the docker registry. `Step - 1`, let's generate the certificate.

```text
openssl req -newkey rsa:4096 -nodes -sha256 -keyout certs/domain.key -x509 -days 365 -out certs/domain.crt
```

Now let's use this cert to supply to the `docker run` command

```text
docker run -d -p 443:443 --restart=always --name registry   -v /root/docker/certs:/certs  -e REGISTRY_HTTP_ADDR=0.0.0.0:443   -e REGISTRY_HTTP_TLS_CERTIFICATE=/certs/domain.crt   -e REGISTRY_HTTP_TLS_KEY=/certs/domain.key registry:2
```

As always it should show a has representation of the container spawned.

```text
476848e839e456a750a1869373d2b34d14654ed6b18772292324bbc9d4621150
```

Look at the logs by calling `docker logs registry`

```text
time="2020-07-29T10:31:57.015857606Z" level=warning msg="No HTTP secret provided - generated random secret. This may cause problems with uploads if multiple registries are behind a load-balancer. To provide a shared secret, fill in http.secret in the configuration file or set the REGISTRY_HTTP_SECRET environment variable." go.version=go1.11.2 instance.id=37c25acb-a673-458b-9f40-5632b2ccb6c2 service=registry version=v2.7.1 
time="2020-07-29T10:31:57.015945659Z" level=info msg="redis not configured" go.version=go1.11.2 instance.id=37c25acb-a673-458b-9f40-5632b2ccb6c2 service=registry version=v2.7.1 
time="2020-07-29T10:31:57.016037915Z" level=info msg="Starting upload purge in 31m0s" go.version=go1.11.2 instance.id=37c25acb-a673-458b-9f40-5632b2ccb6c2 service=registry version=v2.7.1 
time="2020-07-29T10:31:57.025659641Z" level=info msg="using inmemory blob descriptor cache" go.version=go1.11.2 instance.id=37c25acb-a673-458b-9f40-5632b2ccb6c2 service=registry version=v2.7.1 
time="2020-07-29T10:31:57.027103156Z" level=info msg="listening on [::]:443, tls" go.version=go1.11.2 instance.id=37c25acb-a673-458b-9f40-5632b2ccb6c2 service=registry version=v2.7.1
```

Check for `https` request `curl -k https://localhost:443`

```text
docker logs registry
```

```text
time="2020-07-29T10:31:57.015857606Z" level=warning msg="No HTTP secret provided - generated random secret. This may cause problems with uploads if multiple registries are behind a load-balancer. To provide a shared secret, fill in http.secret in the configuration file or set the REGISTRY_HTTP_SECRET environment variable." go.version=go1.11.2 instance.id=37c25acb-a673-458b-9f40-5632b2ccb6c2 service=registry version=v2.7.1 
time="2020-07-29T10:31:57.015945659Z" level=info msg="redis not configured" go.version=go1.11.2 instance.id=37c25acb-a673-458b-9f40-5632b2ccb6c2 service=registry version=v2.7.1 
time="2020-07-29T10:31:57.016037915Z" level=info msg="Starting upload purge in 31m0s" go.version=go1.11.2 instance.id=37c25acb-a673-458b-9f40-5632b2ccb6c2 service=registry version=v2.7.1 
time="2020-07-29T10:31:57.025659641Z" level=info msg="using inmemory blob descriptor cache" go.version=go1.11.2 instance.id=37c25acb-a673-458b-9f40-5632b2ccb6c2 service=registry version=v2.7.1 
time="2020-07-29T10:31:57.027103156Z" level=info msg="listening on [::]:443, tls" go.version=go1.11.2 instance.id=37c25acb-a673-458b-9f40-5632b2ccb6c2 service=registry version=v2.7.1 
172.17.0.1 - - [29/Jul/2020:10:32:20 +0000] "GET / HTTP/1.1" 200 0 "" "curl/7.29.0"
```

Look at the last line.

```text
172.17.0.1 - - [29/Jul/2020:10:32:20 +0000] "GET / HTTP/1.1" 200 0 "" "curl/7.29.0"
```

Let's add some basic authentication to the registry as well. I am working on a Centos 7.6 VM, so first requirement was to add the `htpasswd` dependency.

```text
yum install httpd-tools
```

```text
> htpasswd
Usage:
        htpasswd [-cimB25dpsDv] [-C cost] [-r rounds] passwordfile username
        htpasswd -b[cmB25dpsDv] [-C cost] [-r rounds] passwordfile username password

        htpasswd -n[imB25dps] [-C cost] [-r rounds] username
        htpasswd -nb[mB25dps] [-C cost] [-r rounds] username password
 -c  Create a new file.
 -n  Don't update file; display results on stdout.
 -b  Use the password from the command line rather than prompting for it.
 -i  Read password from stdin without verification (for script usage).
 -m  Force MD5 encryption of the password (default).
 -2  Force SHA-256 crypt() hash of the password (secure).
 -5  Force SHA-512 crypt() hash of the password (secure).
 -B  Force bcrypt aencryption of the password (very secure).
 -C  Set the computing time used for the bcrypt algorithm
     (higher is more secure but slower, default: 5, valid: 4 to 31).
 -r  Set the number of rounds used for the SHA-256, SHA-512 algorithms
     (higher is more secure but slower, default: 5000).
 -d  Force CRYPT encryption of the password (8 chars max, insecure).
 -s  Force SHA-1 encryption of the password (insecure).
 -p  Do not encrypt the password (plaintext, insecure).
 -D  Delete the specified user.
 -v  Verify password for the specified user.
On other systems than Windows and NetWare the '-p' flag will probably not work.
The SHA-1 algorithm does not use a salt and is less secure than the MD5 algorithm.
```

make a `auth` directory

```text
mkdir auth
```

Use the following command to generate password

```text
docker run --entrypoint htpasswd registry -Bbn admin password > auth/htpasswd
```

A catch with changes to registry image if you simply use the above command you may get an error like below

```text
docker: Error response from daemon: OCI runtime create failed: container_linux.go:349: starting container process caused "exec: \"htpasswd\": executable file not found in $PATH": unknown.
ERRO[0000] error waiting for container: context canceled
```

This error can be circumvented by using the version `2.7.0`

```text
docker run --entrypoint htpasswd registry:2.7.0 -Bbn admin password > auth/htpasswd
```

```text
cat auth/htpasswd 

admin:$2y$05$xxS3Jj8ZG1JFc7sipI5NQeAgfgJS9V80kbF7zDtFous.VjQe8vqNy
```

With some additions to the command with TLS configuration we are ready to launch

```text
docker run -d -p 443:443 --restart=always --name registry   -v /root/docker/certs:/certs -v /root/docker/auth:/auth  -e REGISTRY_HTTP_ADDR=0.0.0.0:443 -e REGISTRY_AUTH=htpasswd -e REGISTRY_AUTH_HTPASSWD_PATH=/auth/htpasswd -e "REGISTRY_AUTH_HTPASSWD_REALM=Registry Realm" -e REGISTRY_HTTP_TLS_CERTIFICATE=/certs/domain.crt   -e REGISTRY_HTTP_TLS_KEY=/certs/domain.key registry:2
```

```text
docker logs registry
```

time="2020-07-29T11:01:21.52091005Z" level=warning msg="No HTTP secret provided - generated random secret. This may cause problems with uploads if multiple registries are behind a load-balancer. To provide a shared secret, fill in http.secret in the configuration file or set the REGISTRY\_HTTP\_SECRET environment variable." go.version=go1.11.2 instance.id=6df183de-4a59-4465-baea-90d07ca4b1f8 service=registry version=v2.7.1  
time="2020-07-29T11:01:21.521019306Z" level=info msg="redis not configured" go.version=go1.11.2 instance.id=6df183de-4a59-4465-baea-90d07ca4b1f8 service=registry version=v2.7.1  
time="2020-07-29T11:01:21.521165669Z" level=info msg="Starting upload purge in 16m0s" go.version=go1.11.2 instance.id=6df183de-4a59-4465-baea-90d07ca4b1f8 service=registry version=v2.7.1  
time="2020-07-29T11:01:21.530893238Z" level=info msg="using inmemory blob descriptor cache" go.version=go1.11.2 instance.id=6df183de-4a59-4465-baea-90d07ca4b1f8 service=registry version=v2.7.1  
time="2020-07-29T11:01:21.53268731Z" level=info msg="listening on [::]:443, tls" go.version=go1.11.2 instance.id=6df183de-4a59-4465-baea-90d07ca4b1f8 service=registry version=v2.7.1

It is a self signed certificate and if you try `docker login`

```text
docker login myserver.local.net
```

You might get an error like below

```text
x509: certificate signed by unknown authority
```

It is because the local Docker `dameon` doesn't trust this certificate.

### How to go around it?

#### Disable Certificate Validation [Not recommended]

You can rely on defining `insecure-registries` option for `/etc/docker/daemon.json` file and restarting the daemon.

```text
{
  "insecure-registries" : ["myserver.local.net"]
}
```

```text
systemctl restart docker
```

```text
docker info
```

```text
.....
 Insecure Registries:
  myserver.local.net
  127.0.0.0/8
 Live Restore Enabled: false
```

Once the changes reflect you can do `docker login` for the server and you can see following message.

```text
Username: admin
Password: 
WARNING! Your password will be stored unencrypted in /root/.docker/config.json.
Configure a credential helper to remove this warning. See
https://docs.docker.com/engine/reference/commandline/login/#credentials-store

Login Succeeded
```

### Copy the public cert

Remember when we used `openssl` to generate the certificate `domain.crt` this is the cert we need to copy to a specific location.

```text
mkdir -p /etc/docker/certs.d/myserver.local.net/
```

```text
cp certs/domain.crt /etc/docker/certs.d/myserver.local.net/domain.crt
```

```text
docker login myserver.local.net
```

```text
Username: admin
Password: 
WARNING! Your password will be stored unencrypted in /root/.docker/config.json.
Configure a credential helper to remove this warning. See
https://docs.docker.com/engine/reference/commandline/login/#credentials-store
```

### Adding images

```text
docker tag ubuntu myserver.local.net/ubuntu:latest
```

```text
docker push myserver.local.net/ubuntu:latest
```

Remove the local images using `docker rm` `image name` and finally

```text
docker pull myserver.local.net/ubuntu
```

## References

- https://docs.docker.com/registry/insecure/
- https://docs.docker.com/registry/configuration
- https://docs.docker.com/engine/reference/commandline/search/
