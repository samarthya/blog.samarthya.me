---
title: "Elasticsearch v7.6"
date: "2020-02-21T11:24:29Z"
slug: "elasticsearch-v7-6"
categories: ["technical"]
tags: ["elasticsearch", "v7.6"]
aliases: ["/wps/2020/02/21/elasticsearch-v7-6/"]
wp_id: 427
---

What I have been doing is evaluating Elasticsearch. The indexing, searching (Phrase, Similarity, Structured, Full Text, Complex), clustering etc. In this blog I will just try and simplify the learning curve.

## Q - 1 What is Elasticsearch?

- Distributed document store for complex datastore serialised as JSON
- Accessible from any of the member nodes.
- Uses Inverted index.
- Indexes all data in every field.
- Every field has a dedicated. optimised data store.
- Text is stored in inverted indexes.
- Numeric and Geo points in BKD trees.
- Based on Apache lucene.
- Can execute structured, full text and complex queries.

## Q- 2 What is an index?

- Index is a logical grouping of physical shards.
- Single document may be distributed across multiple shards.
- Shards can be primaries or replicas.
- Each document belongs to one primary shard.
- Number of primary shards are fixed at the time of index creation.
- Number of replicas shards can be changed anytime.

> [https://myserver.elastic.com:9200/\_cat/health?v](https://localhost:9200/_cat/health?v)
>
> Returns information about your cluster

```text
epoch                  1582199918   
timestamp              11:58:38
cluster                samarthya-cluster
status                 yellow
node.total             4
node.data              4
shards                 108
pri                    64
relo                   0
init                   0
unassign               17
pending_tasks          0
max_task_wait_time     -
active_shards_percent.  86.4%
```

## Action Time

1. Let's add a document into an index.

The most powerful aspect of elasticsearch is [Dynamic Mapping](http://One of the most important features of Elasticsearch is that it tries to get out of your way and let you start exploring your data as quickly as possible. To index a document, you don’t have to first create an index, define a mapping type, and define your fields — you can just index a document and the index, type, and fields will spring to life automatically:) (more details below) which allows you to explore your data as quickly as possible.

To index a document, you don’t have to first create an index, define a mapping type, and define your fields — you can just index a document and the index, type, and fields will spring to life automatically

In the command below I am trying to issue a request for a document with `_id` 1.

#### 1. GET /profile/\_doc/1

A sample request for an index `profile` which does not exists at the moment.

```text
 {
   "error" : {
     "root_cause" : [
       {
         "type" : "index_not_found_exception",
         "reason" : "no such index [profile]",
         "resource.type" : "index_expression",
         "resource.id" : "profile",
         "index_uuid" : "na",
         "index" : "profile"
       }
     ],
     "type" : "index_not_found_exception",
     "reason" : "no such index [profile]",
     "resource.type" : "index_expression",
     "resource.id" : "profile",
     "index_uuid" : "na",
     "index" : "profile"
   },
   "status" : 404
 }
```

One way to create a non existing index is by using `PUT`. Dynamically the mapping will be put in place and you can execute the `GET` above to see the details.

#### 2. PUT /profile/\_doc/1

```text
{
   "name": "Samarthya",
   "age": "60",
   "title": "Mr.",
   "role": "Tech lead",
   "org": "Security"
 }
```

In case of successful execution you should see an output like under

```text
{
   "_index" : "profile",
   "_type" : "_doc",
   "_id" : "1",
   "_version" : 1,
   "result" : "created",
   "_shards" : {
     "total" : 2,
     "successful" : 1,
     "failed" : 0
   },
   "_seq_no" : 0,
   "_primary_term" : 1
 }
```

The document that was passed as JSON body is now successfully indexed.

> The automatic detection and addition of new fields is called *dynamic mapping*.
>
> Dynamic Mapping

#### If no body is provided it might throw an error like below.

```text
{
   "error": {
     "root_cause": [
       {
         "type": "parse_exception",
         "reason": "request body is required"
       }
     ],
     "type": "parse_exception",
     "reason": "request body is required"
   },
   "status": 400
 }
```

If the GET is issued again. It will return the document indexed. You can look at the fields that have an `_` at the start like `_type`, `id`, `version` etc. These are called [metafields](https://www.elastic.co/guide/en/elasticsearch/reference/current/mapping-fields.html).

#### GET /profile/\_doc/1

```text
{
   "_index" : "profile",
   "_type" : "_doc",
   "_id" : "1",
   "_version" : 1,
   "_seq_no" : 0,
   "_primary_term" : 1,
   "found" : true,
   "_source" : {
     "name" : "Samarthya",
     "age" : "60",
     "title" : "Mr.",
     "role" : "Tech lead",
     "org" : "Security"
   }
 }
```

One can use the [BULK API](https://www.elastic.co/guide/en/elasticsearch/reference/7.6/docs-bulk.html), to ingest more than one document.

## Search

#### GET /profile/\_search

```text
{
   "query": { "match_all": {}},
   "sort": [
     {
       "age": "asc"
     }
   ]
 }
```

We hare looking for all the matches and sorting it by age in ascending order.

#### Result : Exception

```text
{
   "error": {
     "root_cause": [
       {
         "type": "illegal_argument_exception",
         "reason": "Fielddata is disabled on text fields by default. Set fielddata=true on [age] in order to load fielddata in memory by uninverting the inverted index. Note that this can however use significant memory. Alternatively use a keyword field instead."
       }
     ],
     "type": "search_phase_execution_exception",
     "reason": "all shards failed",
     "phase": "query",
     "grouped": true,
     "failed_shards": [
       {
         "shard": 0,
         "index": "profile",
         "node": "mrTQQhMPQfWPF6q_IGfs5Q",
         "reason": {
           "type": "illegal_argument_exception",
           "reason": "Fielddata is disabled on text fields by default. Set fielddata=true on [age] in order to load fielddata in memory by uninverting the inverted index. Note that this can however use significant memory. Alternatively use a keyword field instead."
         }
       }
     ],
     "caused_by": {
       "type": "illegal_argument_exception",
       "reason": "Fielddata is disabled on text fields by default. Set fielddata=true on [age] in order to load fielddata in memory by uninverting the inverted index. Note that this can however use significant memory. Alternatively use a keyword field instead.",
       "caused_by": {
         "type": "illegal_argument_exception",
         "reason": "Fielddata is disabled on text fields by default. Set fielddata=true on [age] in order to load fielddata in memory by uninverting the inverted index. Note that this can however use significant memory. Alternatively use a keyword field instead."
       }
     }
   },
   "status": 400
 }
```

If I look at the [mapping](https://www.elastic.co/guide/en/elasticsearch/reference/7.6/mapping.html) (Will discuss it later, what it is and how it helps)

#### GET profile/\_mapping

```text
{
   "profile" : {
     "mappings" : {
       "properties" : {
         "age" : {
           "type" : "text",
           "fields" : {
             "keyword" : {
               "type" : "keyword",
               "ignore_above" : 256
             }
           }
         },
         "name" : {
           "type" : "text",
           "fields" : {
             "keyword" : {
               "type" : "keyword",
               "ignore_above" : 256
             }
           }
         },
         "org" : {
           "type" : "text",
           "fields" : {
             "keyword" : {
               "type" : "keyword",
               "ignore_above" : 256
             }
           }
         },
         "role" : {
           "type" : "text",
           "fields" : {
             "keyword" : {
               "type" : "keyword",
               "ignore_above" : 256
             }
           }
         },
         "title" : {
           "type" : "text",
           "fields" : {
             "keyword" : {
               "type" : "keyword",
               "ignore_above" : 256
             }
           }
         }
       }
     }
   }
 }
```

The error that was thrown had the reason specified

```text
"Fielddata is disabled on text fields by default. Set fielddata=true on [age] in order to load fielddata in memory by uninverting the inverted index. Note that this can however use significant memory. Alternatively use a keyword field instead."
```

If I look at the [KEYWORD](https://www.elastic.co/guide/en/elasticsearch/reference/7.6/keyword.html) definition.

They are typically used for filtering (*Find me all blog posts where `status` is `published`*), for sorting, and for aggregations. Keyword fields are only searchable by their exact value.

Since the index already exists and if we try and modify the mappings

```text
PUT profile
 {
   "mappings":{
     "properties" : {
         "age" : {
           "type": "keyword"
         }
     }
   }
 }
```

It should throw a response as under.

```text
{
   "error": {
     "root_cause": [
       {
         "type": "resource_already_exists_exception",
         "reason": "index [profile/aXasR54rR6SvXk-GQd6mRQ] already exists",
         "index_uuid": "aXasR54rR6SvXk-GQd6mRQ",
         "index": "profile"
       }
     ],
     "type": "resource_already_exists_exception",
     "reason": "index [profile/aXasR54rR6SvXk-GQd6mRQ] already exists",
     "index_uuid": "aXasR54rR6SvXk-GQd6mRQ",
     "index": "profile"
   },
   "status": 400
 }
```

## How to resolve?

The [removal](https://www.elastic.co/guide/en/elasticsearch/reference/current/removal-of-types.html) of mappings is one way. The other as we un-intentionally used `age` as string when specifying value `20` implying we should delete the index recreate the value.

#### DELETE profile/

You will get an acknowledgment - True message implying the index has been deleted. If you try and delete it again you will get a message as under

```text
{
   "error" : {
     "root_cause" : [
       {
         "type" : "index_not_found_exception",
         "reason" : "no such index [profile]",
         "index_uuid" : "na",
         "resource.type" : "index_or_alias",
         "resource.id" : "profile",
         "index" : "profile"
       }
     ],
     "type" : "index_not_found_exception",
     "reason" : "no such index [profile]",
     "index_uuid" : "na",
     "resource.type" : "index_or_alias",
     "resource.id" : "profile",
     "index" : "profile"
   },
   "status" : 404
 }
```

Time to add mapping or use dynamic mapping by supplying right values for the `age` field.

```text
PUT /profile/_doc/1
 {
   "name": "Saptha b",
   "age": 50,
   "title": "Mr.",
   "role": "Manager",
   "org": "Security"
 }
```

It should return the acknowledgment of addition

```text
{
   "_index" : "profile",
   "_type" : "_doc",
   "_id" : "1",
   "_version" : 1,
   "result" : "created",
   "_shards" : {
     "total" : 2,
     "successful" : 1,
     "failed" : 0
   },
   "_seq_no" : 0,
   "_primary_term" : 1
 }
```

Once that has been established and if we execute the query again you should get the results as under.

```text
GET profile/_search 
 {
   "query": {
     "match_all": {}
   },
   "sort": [
     {
       "age": "asc"
     }
   ]
 }
```

#### Response

{  
"took" : 3,  
"timed\_out" : false,  
"\_shards" : {  
"total" : 1,  
"successful" : 1,  
"skipped" : 0,  
"failed" : 0  
},  
"hits" : {  
"total" : {  
"value" : 2,  
"relation" : "eq"  
},  
"max\_score" : null,  
"hits" : [  
{  
"\_index" : "profile",  
"\_type" : "\_doc",  
"\_id" : "1",  
"\_score" : null,  
"\_source" : {  
"name" : "Saptha b",  
"age" : 50,  
"title" : "Mr.",  
"role" : "Manager",  
"org" : "Security"  
},  
"sort" : [  
50  
]  
},  
{  
"\_index" : "profile",  
"\_type" : "\_doc",  
"\_id" : "2",  
"\_score" : null,  
"\_source" : {  
"name" : "Samarthya",  
"age" : 70,  
"title" : "Mr.",  
"role" : "Lead Engr",  
"org" : "Security"  
},  
"sort" : [  
70  
]  
}  
]  
}  
}

By default, the hits section includes the first 10 documents that match the search criteria.

### Specific search

```text
GET profile/_search 
  {
    "query": {
      "match": {
        "title": "Mr."
      }
    },
    "sort": [
      {
        "age": "asc"
      }
    ],
    "size": 3
  }
```

Here instead of `match_all`, I am using looking for people with specific title and limited the size as well.

```text
{
   "took" : 1,
   "timed_out" : false,
   "_shards" : {
     "total" : 1,
     "successful" : 1,
     "skipped" : 0,
     "failed" : 0
   },
   "hits" : {
     "total" : {
       "value" : 8,
       "relation" : "eq"
     },
     "max_score" : null,
     "hits" : [
       {
         "_index" : "profile",
         "_type" : "_doc",
         "_id" : "6",
         "_score" : null,
         "_source" : {
           "name" : "Smdie G",
           "age" : 24,
           "title" : "Mr.",
           "role" : "Program management",
           "org" : "Security"
         },
         "sort" : [
           24
         ]
       },
       {
         "_index" : "profile",
         "_type" : "_doc",
         "_id" : "7",
         "_score" : null,
         "_source" : {
           "name" : "Amdie G",
           "age" : 24,
           "title" : "Mr.",
           "role" : "Program management",
           "org" : "Security"
         },
         "sort" : [
           24
         ]
       },
       {
         "_index" : "profile",
         "_type" : "_doc",
         "_id" : "3",
         "_score" : null,
         "_source" : {
           "name" : "Deepak R",
           "age" : 25,
           "title" : "Mr.",
           "role" : "Lead",
           "org" : "Security"
         },
         "sort" : [
           25
         ]
       }
     ]
   }
 }
```

The element returned in the response have specific purpose like

- `took` - defines the time in milliseconds it took for the query to execute.
- `_shards` - specifies how many shards were searched, and its respective breakdown.
- `hits.total.value` - specifies the total matching documents found. (In example above it is 8)

## Q -3 What is Mapping?

Mapping defines how a document, and the fields it contains, are stored and indexed.

- Which fields are date fields
- Which string fields are to be used for full text searching
- Which are numeric

### .. to be continued.
