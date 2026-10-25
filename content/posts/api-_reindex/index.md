---
title: "API _reindex"
date: "2020-04-06"
slug: "api-_reindex"
categories: ["technical"]
tags: ["elasticsearch"]
aliases: ["/wps/2020/04/06/api-_reindex/", "/wps/2026/10/23/api-_reindex/"]
wp_id: 499
---

I will extrapolating based on the original documentation available [here](https://www.elastic.co/guide/en/elasticsearch/reference/current/docs-reindex.html) and based on some of my experience using this API.

> It copies documents from one index to another.

Extracts the document source from the source index and indexes the documents into the destination index. You can copy all documents to the destination index, or reindex a subset of the documents.

```text
POST _reindex
{
"source": {
"index": "source-index"
},
"dest": {
"index": "samarthya-dest"
}
}
```

### What is the API above doing?

I am calling it to re-index the document from source-index to samarthya-dest. It is a point in time copy; i.e. It will copy all the documents as prescribed that exists at the time of executing this command.

> `_reindex` gets a snapshot of the source index

In case of successful operation it will return something like

```text
{
"took" : 3917,
"timed_out" : false,
"total" : 19,
"updated" : 0,
"created" : 19,
"deleted" : 0,
"batches" : 1,
"version_conflicts" : 0,
"noops" : 0,
"retries" : {
"bulk" : 0,
"search" : 0
},
"throttled_millis" : 0,
"requests_per_second" : -1.0,
"throttled_until_millis" : 0,
"failures" : [ ]
}
```

If there is too much of data it can be scheduled to run asynchronously

```text
POST _reindex?wait_for_completion=false
{
"source": {
"index": "profile",
"size": 10
},
"dest": {
"index": "samarthya-dummy"
}
}
```

This will output a NODE and ID something like mrTQQhMPQfWPF6q\_IGfs5Q:13445408 which can be used in the tasks [api](https://www.elastic.co/guide/en/elasticsearch/reference/current/tasks.html).

GET \_tasks/mrTQQhMPQfWPF6q\_IGfs5Q:13445408

It should return the status of the task executed.

```text
{
"completed" : true,
"task" : {
"node" : "mrTQQhMPQfWPF6q_IGfs5Q",
"id" : 13445408,
"type" : "transport",
"action" : "indices:data/write/reindex",
"status" : {
"total" : 19,
"updated" : 19,
"created" : 0,
"deleted" : 0,
"batches" : 2,
"version_conflicts" : 0,
"noops" : 0,
"retries" : {
"bulk" : 0,
"search" : 0
},
"throttled_millis" : 0,
"requests_per_second" : -1.0,
"throttled_until_millis" : 0
},
"description" : "reindex from [profile] to [samarthya-dummy][_doc]",
"start_time_in_millis" : 1586159310602,
"running_time_in_nanos" : 782641181,
"cancellable" : true,
"headers" : { }
},
"response" : {
"took" : 777,
"timed_out" : false,
"total" : 19,
"updated" : 19,
"created" : 0,
"deleted" : 0,
"batches" : 2,
"version_conflicts" : 0,
"noops" : 0,
"retries" : {
"bulk" : 0,
"search" : 0
},
"throttled" : "0s",
"throttled_millis" : 0,
"requests_per_second" : -1.0,
"throttled_until" : "0s",
"throttled_until_millis" : 0,
"failures" : [ ]
}
}
```

### Limiting the number of docs

You can limit the number of documents to be copied by supplying the max\_docs argument to the reindex api.

```text
POST _reindex?wait_for_completion=false
{
"max_docs": 1000,
"source": {
"index": "abcd-*",
"size": 10
 },
"dest": {
"index": "samarthya-dummy"
 }
}
```

Looking at the status it was still completing.

```text
{
"completed" : false,
"task" : {
"node" : "mrTQQhMPQfWPF6q_IGfs5Q",
"id" : 13455103,
"type" : "transport",
"action" : "indices:data/write/reindex",
"status" : {
"total" : 1000,
"updated" : 0,
"created" : 30,
"deleted" : 0,
"batches" : 4,
"version_conflicts" : 0,
"noops" : 0,
"retries" : {
"bulk" : 0,
"search" : 0
},
"throttled_millis" : 0,
"requests_per_second" : -1.0,
"throttled_until_millis" : 0
},
"description" : "reindex from [abcd-*] to [samarthya-dummy][_doc]",
"start_time_in_millis" : 1586159619084,
"running_time_in_nanos" : 9908523430,
"cancellable" : true,
"headers" : { }
}
}
```

After a while it showed up as

```text
{
"completed" : false,
"task" : {
"node" : "mrTQQhMPQfWPF6q_IGfs5Q",
"id" : 13455103,
"type" : "transport",
"action" : "indices:data/write/reindex",
"status" : {
"total" : 1000,
"updated" : 0,
"created" : 450,
"deleted" : 0,
"batches" : 45,
"version_conflicts" : 0,
"noops" : 0,
"retries" : {
"bulk" : 0,
"search" : 0
},
"throttled_millis" : 0,
"requests_per_second" : -1.0,
"throttled_until_millis" : 0
},
"description" : "reindex from [abcd-*] to [samarthya-dummy][_doc]",
"start_time_in_millis" : 1586159619084,
"running_time_in_nanos" : 141584516109,
"cancellable" : true,
"headers" : { }
}
}
```
