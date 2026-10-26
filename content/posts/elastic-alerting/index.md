---
title: "Elastic Alerting"
date: "2020-07-05"
slug: "elastic-alerting"
categories: ["technical"]
tags: ["alerting", "elasticsearch"]
aliases: ["/wps/2020/07/05/elastic-alerting/", "/wps/2026/10/23/elastic-alerting/"]
wp_id: 759
---

## Watcher

Watcher is an Elasticsearch feature that facilitates alerting and can be used to create actions based on conditions, which are periodically evaluated using queries on your data. There are two ways of creating a watcher

1. Watcher API
2. Kibana Watcher UI

Elastic Alerting is one of what are called stack features that are available as part of Gold subscription or higher. Elastic watcher has typically four components

<img src="alerting.png" alt="Elastic Watcher: a schedule triggers a check; if the condition is met an action runs, otherwise nothing happens" class="grid-w100" />

## Trigger - Schedule

A typically periodic trigger for data already available in Elasticsearch on a schedule basis.

## Query

## Condition

## Action

## Helpful links

- https://www.elastic.co/guide/en/kibana/current/watcher-ui.html
