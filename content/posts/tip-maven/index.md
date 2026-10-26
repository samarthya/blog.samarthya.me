---
title: "Tip #Maven"
date: "2022-10-19T12:00:00Z"
slug: "tip-maven"
description: "A decent developer trick is to ensure your maven points to the right JAVA version, and if you have freshly installed maven it will be pointing to the default available."
categories: ["technical"]
tags: ["maven", "tip"]
aliases: ["/wps/2022/10/19/tip-maven/"]
recovered: "Internet Archive snapshot 2026-04-21"
---

A decent developer trick is to ensure your `maven` points to the right `JAVA` version, and if you have freshly installed maven it will be pointing to the default available.

On my system’s dev or otherwise I normally take the help of the `profile.d` directory to allow me set the custom version.

This directory defines a system-wide behavior.

I created a `maven.sh` in this folder & put the contents as below

```text
export JAVA_HOME=/usr/lib/jvm/java-11-openjdk-11.0.16.1.1-1.el7_9.x86_64
export M2_HOME=/usr/share/maven
export MAVEN_HOME=/usr/share/maven
export PATH=${M2_HOME}/bin:${PATH}
```

Then source it `source /etc/profile.d/maven.sh`

Once you do that you can validate the `mvn --version`

```text
Apache Maven 3.0.5 (Red Hat 3.0.5-17)
Maven home: /usr/share/maven
Java version: 11.0.16.1, vendor: Red Hat, Inc.
Java home: /usr/lib/jvm/java-11-openjdk-11.0.16.1.1-1.el7_9.x86_64
Default locale: en_US, platform encoding: UTF-8
OS name: "linux", version: "3.10.0-1160.76.1.el7.x86_64", arch: "amd64", family: "unix"
```
