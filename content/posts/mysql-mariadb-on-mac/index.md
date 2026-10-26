---
title: "MySQL/MariaDB on MAC"
date: "2019-11-01T12:00:00Z"
slug: "mysql-mariadb-on-mac"
description: "While trying to troubleshoot an inhouse application I had to setup a quick MySQL instance which led me to install my first instance of MariaDB on my local MAC machine."
categories: ["others"]
aliases: ["/wps/2019/11/01/mysql-mariadb-on-mac/"]
recovered: "Internet Archive snapshot 2026-03-13"
---

> Challenges are plenty but outcome is always one – Learning!

While trying to troubleshoot an inhouse application I had to setup a quick MySQL instance which led me to install my first instance of MariaDB on my local MAC machine.

BREW is my poison. You need to open a terminal and issue

> brew install mariadb

It helped me get the binaries on my system.

The challenge shifted from getting the binaries to starting the server.

> brew services –help

It lists out the commands you can utilize to start stop and list all the services running at that moment.

To start your MYSQL Daemon you just need to issue

> brew services start mariadb

And to validate the status you can issue

> brew services list

It should give an output like under

![](brew-list-services.png)

Time to login

> sudo mysql -u root

If you issue the command without sudo you wont be able to, as by default the root has no password for the local installation.

You can set the password using

> SET Password=PASSWORD(‘mypassword’)

You can validate the output by issuing

> select host, user, authentication\_string, password from mysql.user;
