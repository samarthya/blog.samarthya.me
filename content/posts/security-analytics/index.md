---
title: "Security Analytics"
date: "2020-01-13"
slug: "security-analytics"
categories: ["others", "technical"]
tags: ["elastic", "security", "siem"]
aliases: ["/wps/2020/01/13/security-analytics/", "/wps/2026/10/23/security-analytics/"]
wp_id: 277
---

```text
* Header image from Elastic.co
```

As we move towards the micro-service/container economy where there are heaps of products available in form of applications to be downloaded & installed on primarily two platforms Android and IOS, we just cant underline the security implications enough.

> SIEM - Security information and Events management.

In this blog, I will walk through the enabling-platform that elastic is. Elastic enables data ingestion from multiple sources, and identifying/predicting threats.

![Data sources](screenshot-2020-01-13-at-4.54.30-pm.png "Data sources")

## Data generators

The source of truth is always the activity information from an application

## ECS

Elastic common schema allows to normalize the data from multiple sources. Which allows correlation much easier and eventually more convenient searches for data retrieval and enrichment.

In version 7.2 SIEM was made available.

![](screenshot-2020-01-13-at-4.42.06-pm.png)

```text
* Image above is from from Elastic.co
```
