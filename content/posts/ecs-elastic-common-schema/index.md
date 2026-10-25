---
title: "ECS: Elastic common schema"
date: "2020-04-02"
slug: "ecs-elastic-common-schema"
categories: ["technical"]
tags: ["ecs", "elasticsearch"]
aliases: ["/wps/2020/04/02/ecs-elastic-common-schema/", "/wps/2026/10/23/ecs-elastic-common-schema/"]
wp_id: 497
---

Open specification for document fields for data ingested in Elasticsearch. It brings uniformity to certain common fields that are used across data sources.

ECS defines two field levels

1. Core fields: Represent the fields that are most common across all use cases.
2. Extended fields: That are not part of the core and specific to cases.

## Field sets

Field sets are multiple groups of related fields defined by ECS. More information [here](https://www.elastic.co/guide/en/ecs/current/ecs-field-reference.html).

### Base fields

Common across all event, and are at the top level. E.g. @timestamp, tags etc. More details available [here](https://www.elastic.co/guide/en/ecs/current/ecs-base.html).

### Agent fields

As the name indicates it about the software entity like FileBeat agent. Details [here](https://www.elastic.co/guide/en/ecs/current/ecs-agent.html). E.g. agent.name, agent.id etc.

### Error fields

Represents errors of any kind in ECS. E.g. error.code, error.message etc. More details available [here](https://www.elastic.co/guide/en/ecs/current/ecs-error.html).

### Event fields

It provides for the context information of the log or the metric event. More details [here](https://www.elastic.co/guide/en/ecs/current/ecs-event.html). E.g. event.created, event.code etc.

### Host fields

It populates the information about the host on which the event happened. E.g. host.ip, host.mac etc.

More details available [here](https://www.elastic.co/guide/en/ecs/current/ecs-host.html).
