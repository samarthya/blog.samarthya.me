---
title: "Performance Tweaks: Kibana"
date: "2020-08-07T13:23:55Z"
slug: "performance-tweaks-kibana"
categories: ["technical"]
tags: ["nginx", "performance"]
aliases: ["/wps/2020/08/07/performance-tweaks-kibana/"]
wp_id: 901
---

The performance I was getting after deploying `Elasticsearch` 7.6.2 and `Kibana` in my local VM's was not satisfactory, so I thought of deploying a front proxy `Nginx` in front and enabling static resources caching.

The journey starts at installing NGINX the steps are very much simple and covered [here](https://www.nginx.com/resources/wiki/start/topics/tutorials/install/) in detail.

My `/etc/yum.repos.d/nginx.repo` looks like below

```text
[nginx-stable]
name=nginx stable repo
baseurl=http://nginx.org/packages/centos/$releasever/$basearch/
gpgcheck=1
enabled=1
gpgkey=https://nginx.org/keys/nginx_signing.key
module_hotfixes=true

[nginx-mainline]
name=nginx mainline repo
baseurl=http://nginx.org/packages/mainline/centos/$releasever/$basearch/
gpgcheck=1
enabled=1
gpgkey=https://nginx.org/keys/nginx_signing.key
module_hotfixes=true
```

```text
nginx -v
nginx version: nginx/1.19.1
```

```text
nginx -V
nginx version: nginx/1.19.1
built by gcc 4.8.5 20150623 (Red Hat 4.8.5-39) (GCC) 
built with OpenSSL 1.0.2k-fips  26 Jan 2017
TLS SNI support enabled
configure arguments: --prefix=/etc/nginx --sbin-path=/usr/sbin/nginx --modules-path=/usr/lib64/nginx/modules --conf-path=/etc/nginx/nginx.conf --error-log-path=/var/log/nginx/error.log --http-log-path=/var/log/nginx/access.log --pid-path=/var/run/nginx.pid --lock-path=/var/run/nginx.lock --http-client-body-temp-path=/var/cache/nginx/client_temp --http-proxy-temp-path=/var/cache/nginx/proxy_temp --http-fastcgi-temp-path=/var/cache/nginx/fastcgi_temp --http-uwsgi-temp-path=/var/cache/nginx/uwsgi_temp --http-scgi-temp-path=/var/cache/nginx/scgi_temp --user=nginx --group=nginx --with-compat --with-file-aio --with-threads --with-http_addition_module --with-http_auth_request_module --with-http_dav_module --with-http_flv_module --with-http_gunzip_module --with-http_gzip_static_module --with-http_mp4_module --with-http_random_index_module --with-http_realip_module --with-http_secure_link_module --with-http_slice_module --with-http_ssl_module --with-http_stub_status_module --with-http_sub_module --with-http_v2_module --with-mail --with-mail_ssl_module --with-stream --with-stream_realip_module --with-stream_ssl_module --with-stream_ssl_preread_module --with-cc-opt='-O2 -g -pipe -Wall -Wp,-D_FORTIFY_SOURCE=2 -fexceptions -fstack-protector-strong --param=ssp-buffer-size=4 -grecord-gcc-switches -m64 -mtune=generic -fPIC' --with-ld-opt='-Wl,-z,relro -Wl,-z,now -pie'
```

My Kibana is deployed on the same host and listening on `5601`

- Handy commands
  1. `nginx -t` to test the changes are syntactically correct before loading the nginx.
  2. `systemctl reload nginx` reloads the nginx configurations.

Let's get started with the configuration definition and I will explain as I do it. The default configuration for me looks like below

```text
user  nginx;
worker_processes  1;

error_log  /var/log/nginx/error.log warn;
pid        /var/run/nginx.pid;

events {
    worker_connections  1024;
}

http {
    include       /etc/nginx/mime.types;
    default_type  application/octet-stream;

    log_format  main  '$remote_addr - $remote_user [$time_local] "$request" '
                      '$status $body_bytes_sent "$http_referer" '
                      '"$http_user_agent" "$http_x_forwarded_for"';

    access_log  /var/log/nginx/access.log  main;

    sendfile        on;
    #tcp_nopush     on;

    keepalive_timeout  65;

    #gzip  on;

    include /etc/nginx/conf.d/*.conf;
}
```

- **Notice** the line `include /etc/nginx/conf.d/*.conf;` this allows you to define multiple configurations within the http context.
- [Server](http://nginx.org/en/docs/http/ngx_http_core_module.html#server) block has a scope context of http and sets the configuration for a virtual server hence you will notice in the configuration files we defined in `conf.d` we usually have only `server` blocks

```text
systemctl status nginx
```

```text

● nginx.service - nginx - high performance web server
   Loaded: loaded (/usr/lib/systemd/system/nginx.service; enabled; vendor preset: disabled)
   Active: active (running) since Fri 2020-08-07 11:53:24 UTC; 9s ago
     Docs: http://nginx.org/en/docs/
  Process: 224365 ExecStart=/usr/sbin/nginx -c /etc/nginx/nginx.conf (code=exited, status=0/SUCCESS)
 Main PID: 224366 (nginx)
    Tasks: 2
   CGroup: /system.slice/nginx.service
           ├─224366 nginx: master process /usr/sbin/nginx -c /etc/nginx/nginx.conf
           └─224367 nginx: worker process
```

Let's make some changes

{{< lead >}}
Syntax:

`worker_processes number | auto;`
— http://nginx.org/en/docs/ngx_core_module.html#worker_processes
{{< /lead >}}

The default value of 1 not going to suffice for my case so bump it up to `auto` which should be ideal. Please note the `auto` parameter is supported starting from versions 1.3.8 and 1.2.5 only.

```text
worker_processes  auto;
```

It allows to create a more conducive environment and in my case since the VM has 16 cores the number of workers launched when I enabled Nginx it is pushed to 16 (+1 master).

To allow more information in case of [errors](http://nginx.org/en/docs/ngx_core_module.html#error_log), let me add the debug log information as well

```text
error_log /var/log/nginx/error.log debug;
```

{{< lead >}}
Syntax:

`error_log file [level];`
{{< /lead >}}

Time to reload the configuration and see if the number of worker thread changes

```text
systemctl status nginx
● nginx.service - nginx - high performance web server
   Loaded: loaded (/usr/lib/systemd/system/nginx.service; enabled; vendor preset: disabled)
   Active: active (running) since Fri 2020-08-07 11:53:24 UTC; 42s ago
     Docs: http://nginx.org/en/docs/
  Process: 224398 ExecReload=/bin/sh -c /bin/kill -s HUP $(/bin/cat /var/run/nginx.pid) (code=exited, status=0/SUCCESS)
  Process: 224365 ExecStart=/usr/sbin/nginx -c /etc/nginx/nginx.conf (code=exited, status=0/SUCCESS)
 Main PID: 224366 (nginx)
    Tasks: 17
   CGroup: /system.slice/nginx.service
           ├─224366 nginx: master process /usr/sbin/nginx -c /etc/nginx/nginx.conf
           ├─224402 nginx: worker process
           ├─224403 nginx: worker process
           ├─224404 nginx: worker process
           ├─224405 nginx: worker process
           ├─224406 nginx: worker process
           ├─224407 nginx: worker process
           ├─224408 nginx: worker process
           ├─224409 nginx: worker process
           ├─224410 nginx: worker process
           ├─224411 nginx: worker process
           ├─224412 nginx: worker process
           ├─224413 nginx: worker process
           ├─224414 nginx: worker process
           ├─224415 nginx: worker process
           ├─224416 nginx: worker process
           └─224417 nginx: worker process
```

The `default.conf` defined in `/etc/nginx/conf.d` looks like

```text
server {
    listen       80;
    server_name  localhost;

    location / {
        root   /usr/share/nginx/html;
        index  index.html index.htm;
    }
}
```

- [listen](http://nginx.org/en/docs/http/ngx_http_core_module.html#listen) directive sets the `address` and `port` for IP. An `address` may also be a hostname
- `server_name` sets names of a virtual server, for example

```text
server_name example.com www.example.com;
```

If you browse to `http://machine.host:80` you will be presented the Nginx welcome page, now lets tweak it a little to validate if our changes do work.

```text
listen      [::]:8989 default_server;
```

I changed the port and restarted the server. The same page is now presented when I hit `http://machine.host:8989`.

{{< lead >}}
The `default_server` parameter, if present, will cause the server to become the default server for the specified `address`:`port` pair.
{{< /lead >}}

Undo the port change to default to 80 again.

Let's have only SSL communication and we shall redirect all the incoming `http` communication to `https`.

### Generate SSL certificates

Step 1, requires generating certificates. Follow the steps below to generate `private.key` and `public.pem` at `/etc/nginx/ssl`

```text
mkdir /etc/nginx/ssl
```

```text
openssl req -x509 -nodes -days 365 \
>   -newkey rsa:2048 \
>   -keyout /etc/nginx/ssl/private.key \
>   -out /etc/nginx/ssl/public.pem
Generating a 2048 bit RSA private key
..........................+++
.........................+++
writing new private key to '/etc/nginx/ssl/private.key'
-----
You are about to be asked to enter information that will be incorporated
into your certificate request.
What you are about to enter is what is called a Distinguished Name or a DN.
There are quite a few fields but you can leave some blank
For some fields there will be a default value,
If you enter '.', the field will be left blank.
-----
Country Name (2 letter code) [XX]:IN
State or Province Name (full name) []:Telangana
Locality Name (eg, city) [Default City]:Hyderabad
Organization Name (eg, company) [Default Company Ltd]:Samarthya.me
Organizational Unit Name (eg, section) []:Security
Common Name (eg, your name or your server's hostname) []:localmachine.host
Email Address []:s.r@gmail.com
```

Let us redirect all the traffic to https by using `return`.

{{< lead >}}
`return code URL;`
{{< /lead >}}

```text
return 301 https://$host$request_uri;
```

Create a sample page

```text
echo "It Works" >/usr/share/nginx/html/ssltest.html
```

Add a new configuration called `ssl.conf` at `/etc/nginx`

```text
server {
        listen 443 ssl;
        server_name .host;

        ssl_certificate    /etc/nginx/ssl/public.pem;
        ssl_certificate_key /etc/nginx/ssl/private.key;

        location / {
                root   /usr/share/nginx/html;
                index   ssltest.html;
        }
}
```

Specify the certificate and key as specified above. Now, after you reload nginx and hit the default location `http://host` it should redirect you to `https://`.

```text
GET / HTTP/1.1
Host: machine.host
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:79.0) Gecko/20100101 Firefox/79.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate
DNT: 1
Connection: keep-alive
Upgrade-Insecure-Requests: 1
Pragma: no-cache
Cache-Control: no-cache
```

```text
HTTP/1.1 301 Moved Permanently
Server: nginx/1.19.1
Date: Fri, 07 Aug 2020 12:53:14 GMT
Content-Type: text/html
Content-Length: 169
Connection: keep-alive
Location: https://machine.host/
```

```text
https://machine.host/
GET / HTTP/1.1
Host: machine.host
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:79.0) Gecko/20100101 Firefox/79.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
DNT: 1
Connection: keep-alive
Upgrade-Insecure-Requests: 1
Pragma: no-cache
Cache-Control: no-cache
```

Finally it shows

## It Works

This was a simple http to https configuration the bigger question is enabling cache and forwarding the request to another server. Let's use the `proxy_cache` to define a zone.

{{< lead >}}
`proxy_cache` defines a shared memory zone used for caching.
{{< /lead >}}

```text
proxy_cache kibana;
proxy_cache_background_update on;
proxy_cache_valid 200 302 60m;
```

`proxy_cache_path` sets the path and other parameters of a cache.

```text
proxy_cache_path /var/cache/nginx/kibana levels=1:2 keys_zone=kibana:10m max_size=1g inactive=60m;
```

Mind you the `proxy_cache_path` context is `http` so we will be defining it at the top

Finally proxy to the kibanaserver using `proxy_pass`

```text
proxy_cache_path /var/cache/nginx/kibana levels=1:2 keys_zone=kibana:10m max_size=1g inactive=60m;

server {
        listen 443 ssl;
        server_name .host;

        ssl_certificate    /etc/nginx/ssl/public.pem;
        ssl_certificate_key /etc/nginx/ssl/private.key;

        location / {
                # root   /usr/share/nginx/html;
                # index   ssltest.html;
                proxy_cache kibana;
                proxy_cache_background_update on;
                proxy_cache_valid 200 302 60m;
                proxy_pass_request_headers on;
                proxy_pass_request_body on;

                proxy_set_header HOST $host;
                proxy_set_header X-Forwarded-Proto $scheme;
                proxy_set_header X-Real-IP $remote_addr;
                proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
                
                proxy_pass https://kibanaserver.net:5601/;
        }
}
```

A quick listing of cache on `fs` can be seen by doing a directory listing

```text
ls /var/cache/nginx/kibana/ -als
total 0
0 drwx------ 17 nginx root  141 Aug  7 13:16 .
0 drwxr-xr-x  8 root  root  112 Aug  7 13:05 ..
0 drwx------ 10 nginx nginx  86 Aug  7 13:17 0
0 drwx------ 10 nginx nginx  86 Aug  7 13:17 1
0 drwx------ 24 nginx nginx 226 Aug  7 13:18 2
0 drwx------ 13 nginx nginx 116 Aug  7 13:18 3
0 drwx------ 12 nginx nginx 106 Aug  7 13:17 4
0 drwx------  8 nginx nginx  66 Aug  7 13:18 5
0 drwx------  8 nginx nginx  66 Aug  7 13:17 6
0 drwx------ 12 nginx nginx 106 Aug  7 13:18 7
0 drwx------ 11 nginx nginx  96 Aug  7 13:17 8
0 drwx------ 16 nginx nginx 146 Aug  7 13:18 a
0 drwx------ 14 nginx nginx 126 Aug  7 13:18 b
0 drwx------ 15 nginx nginx 136 Aug  7 13:17 c
0 drwx------ 10 nginx nginx  86 Aug  7 13:17 d
0 drwx------  9 nginx nginx  76 Aug  7 13:17 e
0 drwx------  6 nginx nginx  46 Aug  7 13:16 f
```

## References

- https://www.nginx.com/resources/wiki/start/topics/tutorials/install/
- http://nginx.org/en/docs/
- http://nginx.org/en/docs/install.html
- http://nginx.org/en/docs/http/request\_processing.html
- http://nginx.org/en/docs/ngx\_core\_module.html#error\_log
- http://nginx.org/en/docs/http/ngx\_http\_core\_module.html#listen
- http://nginx.org/en/docs/http/ngx\_http\_core\_module.html#server
- http://nginx.org/en/docs/ngx\_core\_module.html#include
- http://nginx.org/en/docs/http/ngx\_http\_ssl\_module.html#ssl
- http://nginx.org/en/docs/http/ngx\_http\_proxy\_module.html#proxy\_cache
- http://nginx.org/en/docs/http/ngx\_http\_proxy\_module.html#proxy\_cache\_path
- http://nginx.org/en/docs/http/ngx\_http\_proxy\_module.html#proxy\_pass
- http://nginx.org/en/docs/http/ngx\_http\_core\_module.html#var\_request\_uri
