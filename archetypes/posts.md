---
title: "{{ replace .File.ContentBaseName "-" " " | title }}"
date: {{ .Date }}
description: ""     # one line; shown on cards and in search results
categories: ["technical"]
tags: []            # reuse existing tags (k8s, golang, docker, ...) so the right cover and related posts show up
draft: true
---

<!-- Images: put them in this folder and use ![alt text](photo.jpg).
     The first image becomes the card picture; name one feature.jpg to pick it explicitly. -->
