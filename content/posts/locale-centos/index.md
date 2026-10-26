---
title: "Locale"
date: "2019-04-05T12:00:00Z"
slug: "locale-centos"
description: "Did you ever see a warning printed on your console the moment you log into your Linux machine and did that warning ever complaned to you about the benign locale?"
categories: ["others"]
tags: ["centos", "linux", "locale", "warning"]
aliases: ["/wps/2019/04/05/locale-centos/"]
recovered: "Internet Archive snapshot 2026-06-10"
---

Did you ever see a warning printed on your console the moment you log into your Linux machine and did that warning ever complaned to you about the benign locale?

If you are always troubled by these statements as you log in your CentOs machine

> -bash: warning: setlocale: LC\_CTYPE: cannot change locale (UTF-8): No such file or directory  
> -bash: warning: setlocale: LC\_CTYPE: cannot change locale (UTF-8): No such file or directory

and badly wished to do away with them. I have a solution for you.

Just need to add below entries into /etc/environment and you are good to go.

> LANG=en\_US.utf-8  
> LC\_ALL=en\_US.utf-8

Also the other way you check and set information of locale on a CentOS system is via **localectl** command.

> localectl –help

This command will show some information around what all options you can play with while dealing with the locale information

## Some experiments

### localectl status

> **System Locale: LANG=en\_US.UTF-8  
> VC Keymap: us  
> X11 Layout: us**

### cat /etc/locale.conf

> LANG=”en\_US.UTF-8″

### localectl list-locales

This will dump a long list of locales supported in your system.

### localectl set-locale LANG=en\_IN.utf8

I tried using this and if I verify the locale status I get the desired information available to me.
