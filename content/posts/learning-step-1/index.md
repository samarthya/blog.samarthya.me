---
title: "Learning Step - 1"
date: "2019-02-27"
slug: "learning-step-1"
categories: ["others"]
tags: ["technical"]
aliases: ["/wps/2019/02/27/learning-step-1/", "/wps/2026/10/23/learning-step-1/"]
wp_id: 65
---

The best way to learn a technology is to create something from scratch and as my ever wandering brain hops from one framework to another I am starting out on a new conquest of learning something that professionally I have never tried. Not just a scripting technology but learning the new enabler platforms as well.

What I am using

Vagrant - Virtual environment provider and management.

> Vagrant provides easy to configure, reproducible, and portable work environments built on top of industry-standard technology and controlled by a single consistent workflow to help maximize the productivity and flexibility of you and your team.

Laravel ecosystem (Homestead)

> Laravel Homestead is an official, pre-packaged Vagrant box that provides you a wonderful development environment without requiring you to install PHP, a web server, and any other server software on your local machine.

Few commands that I have used.

1. To create a new project

> laravel new myblog --force

After doing the recommended setup commands of vagrant, and issuing the up command.

2. To create a new route

artisan make:auth

3. Added the is\_admin column in the migrate scripts

artisan migrate

mailtrap.io To create a dummy SMTP mail account for testing

laravel mix

Laravel Mix provides a clean, fluent API for defining basic [webpack](http://github.com/webpack/webpack) build steps for your Laravel application. Mix supports several common CSS and JavaScript pre-processors.

Composer - https://getcomposer.org/doc/00-intro.md
