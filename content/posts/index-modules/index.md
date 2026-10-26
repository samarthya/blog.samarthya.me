---
title: "Index Modules"
date: "2020-04-23T12:00:00Z"
slug: "index-modules"
description: "Index modules are a complex subject; they are defined per index and control every aspect of an index."
categories: ["technical"]
aliases: ["/wps/2020/04/23/index-modules/"]
recovered: "Internet Archive snapshot 2026-05-18"
---

Index modules are a complex subject; they are defined per index and control every aspect of an index.

There are two types of settings for an index

1. Static: Can usually be defined at the creation time **or** when the index is closed.
   - index can be closed by invoking the \_close api.
   - E.g. index.number\_of\_shards, index.shard.check\_on\_startup etc.
2. Dynamic: Can be changed on the live index using [index settings](https://www.elastic.co/guide/en/elasticsearch/reference/master/indices-update-settings.html) api.
   - E.g. index.number\_of\_replicas, index.refresh\_interval etc.

More details available [here](https://www.elastic.co/guide/en/elasticsearch/reference/master/index-modules.html#dynamic-index-settings).

## Example

> GET `samarthya-dummy/_settings`

Output looks like

> {  
> “samarthya-dummy” : {  
> “settings” : {  
> “index” : {  
> “creation\_date” : “1586159619660”,  
> “number\_of\_shards” : “1”,  
> “number\_of\_replicas” : “1”,  
> “uuid” : “aGtxZ-FSRNKUgObjpQKhtA”,  
> “version” : {  
> “created” : “7060299”  
> },  
> “provided\_name” : “samarthya-dummy”  
> }  
> }  
> }  
> }
