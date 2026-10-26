---
title: "Elasticsearch v7.6"
date: "2020-02-24T12:00:00Z"
slug: "elasticsearch-v7-6-2"
description: "In the previous blog we searched for a match\\all, and sorted it by age. In this we will improve upon the query we are writing and look for other options."
categories: ["technical"]
tags: ["elasticsearch", "v7-6"]
aliases: ["/wps/2020/02/24/elasticsearch-v7-6-2/"]
recovered: "Internet Archive snapshot 2026-03-13"
---

In the previous blog we searched for a match\_all, and sorted it by age. In this we will improve upon the query we are writing and look for other options.

```text
GET profile/_search 
  {
    "query": {
      "match": {
        "title": "Mr. Ms."
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

The command executed above, uses `match` which allows to search for specific terms within a field `title` and the terms we are looking for are `Mr.` or `Mrs.`

The response as received is as under

```text
{
   "took" : 0,
   "timed_out" : false,
   "_shards" : {
     "total" : 1,
     "successful" : 1,
     "skipped" : 0,
     "failed" : 0
   },
   "hits" : {
     "total" : {
       "value" : 10,
       "relation" : "eq"
     },
     "max_score" : null,
     "hits" : [
       {
         "_index" : "profile",
         "_type" : "_doc",
         "_id" : "4",
         "_score" : null,
         "_source" : {
           "name" : "Deepa G",
           "age" : 22,
           "title" : "Ms.",
           "role" : "QA",
           "org" : "Security"
         },
         "sort" : [
           22
         ]
       },
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
       }
     ]
   }
 }
```

### match\_phrase

```text
GET profile/_search 
  {
    "query": {
      "match_phrase": {
        "name": "G"
      }
    },
    "sort": [
      {
        "age": "asc"
      }
    ],
    "size": 2
  }
```

In the example above I am trying to look for a phrase `G` rather than individual term.

```text
{
   "took" : 0,
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
         "_id" : "4",
         "_score" : null,
         "_source" : {
           "name" : "Deepa G",
           "age" : 22,
           "title" : "Ms.",
           "role" : "QA",
           "org" : "Security"
         },
         "sort" : [
           22
         ]
       },
       {
         "_index" : "profile",
         "_type" : "_doc",
         "_id" : "5",
         "_score" : null,
         "_source" : {
           "name" : "Reepa G",
           "age" : 24,
           "title" : "Mrs.",
           "role" : "QA",
           "org" : "Security"
         },
         "sort" : [
           24
         ]
       }
     ]
   }
 }
```

I have limited the size to 2 and hence even though it matched more than 2 documents, the result size was limited to 2.

## Complex Query

Creating a complex query is equally intuitive.

### Bool – Query

Let’s look for all the users who are between the age group of `>= 30 && <= 50`.

```text
GET profile/_search 
  {
    "query": {
      "bool": {
        "must": [
          { "range": {
            "age": {
              "gte": 30,
              "lte": 50
            }
          }}
        ]
      }
    },
    "sort": [
      {
        "age": "asc"
      }
    ],
    "size": 2
  }
```

The response as expected is

```text
{
   "took" : 3,
   "timed_out" : false,
   "_shards" : {
     "total" : 1,
     "successful" : 1,
     "skipped" : 0,
     "failed" : 0
   },
   "hits" : {
     "total" : {
       "value" : 3,
       "relation" : "eq"
     },
     "max_score" : null,
     "hits" : [
       {
         "_index" : "profile",
         "_type" : "_doc",
         "_id" : "11",
         "_score" : null,
         "_source" : {
           "name" : "Veronica G",
           "age" : 37,
           "title" : "Ms.",
           "role" : "Engineering",
           "org" : "Security"
         },
         "sort" : [
           37
         ]
       },
       {
         "_index" : "profile",
         "_type" : "_doc",
         "_id" : "10",
         "_score" : null,
         "_source" : {
           "name" : "Pranav G",
           "age" : 47,
           "title" : "Mr.",
           "role" : "Engineering",
           "org" : "Security"
         },
         "sort" : [
           47
         ]
       }
     ]
   }
 }
```

A simple modifications to exclude `Veronica` is as under.

> must\_not clause is more of a filter.

```text
GET profile/_search 
  {
    "query": {
      "bool": {
        "must": [
          { "range": {
            "age": {
              "gte": 30,
              "lte": 50
            }
          }}
        ],
        "must_not": [
          {
            "match": {
              "name": "Veronica G"
            }
          }
        ]
      }
    },
    "sort": [
      {
        "age": "asc"
      }
    ],
    "size": 2
  }
```

## Aggregating

Let’s show aggregation

```text
GET profile/_search 
  {
    "aggs": {
      "Group-By-Age": {
        "terms": {
          "field": "title.keyword"
        }
      }
    }, 
    "size": 0
  }
```

and the results are

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
       "value" : 11,
       "relation" : "eq"
     },
     "max_score" : null,
     "hits" : [ ]
   },
   "aggregations" : {
     "Group-By-Age" : {
       "doc_count_error_upper_bound" : 0,
       "sum_other_doc_count" : 0,
       "buckets" : [
         {
           "key" : "Mr.",
           "doc_count" : 8
         },
         {
           "key" : "Ms.",
           "doc_count" : 2
         },
         {
           "key" : "Mrs.",
           "doc_count" : 1
         }
       ]
     }
   }
 }
```

What are these buckets?

```text
"buckets" : []
```

In our example we are aggregating for `title.keyword` and the `key` shows the unique values found and the `doc_count` is the total matches.

So for our response we have 8 `Mr.` , 2 `Ms.` and 1 `Mrs.`

If the `size` is not zero in the query all the responses that matched will also be returned in the `hits[]`

### Complexity increased

A little modifications to further aggregate and group by role.

```text
GET profile/_search 
  {
    "aggs": {
      "Group-By-Age": {
        "terms": {
          "field": "title.keyword"
        },
        "aggs": {
          "Group-By-Role": {
            "terms": {
              "field": "role.keyword"
            }
          }
        }
      }
    },
    "size": 0
  }
```

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
       "value" : 11,
       "relation" : "eq"
     },
     "max_score" : null,
     "hits" : [ ]
   },
   "aggregations" : {
     "Group-By-Age" : {
       "doc_count_error_upper_bound" : 0,
       "sum_other_doc_count" : 0,
       "buckets" : [
         {
           "key" : "Mr.",
           "doc_count" : 8,
           "Group-By-Role" : {
             "doc_count_error_upper_bound" : 0,
             "sum_other_doc_count" : 0,
             "buckets" : [
               {
                 "key" : "Program management",
                 "doc_count" : 2
               },
               {
                 "key" : "Engineering",
                 "doc_count" : 1
               },
               {
                 "key" : "Engineering management",
                 "doc_count" : 1
               },
               {
                 "key" : "Lead",
                 "doc_count" : 1
               },
               {
                 "key" : "Lead Engr",
                 "doc_count" : 1
               },
               {
                 "key" : "Manager",
                 "doc_count" : 1
               },
               {
                 "key" : "Product management",
                 "doc_count" : 1
               }
             ]
           }
         },
         {
           "key" : "Ms.",
           "doc_count" : 2,
           "Group-By-Role" : {
             "doc_count_error_upper_bound" : 0,
             "sum_other_doc_count" : 0,
             "buckets" : [
               {
                 "key" : "Engineering",
                 "doc_count" : 1
               },
               {
                 "key" : "QA",
                 "doc_count" : 1
               }
             ]
           }
         },
         {
           "key" : "Mrs.",
           "doc_count" : 1,
           "Group-By-Role" : {
             "doc_count_error_upper_bound" : 0,
             "sum_other_doc_count" : 0,
             "buckets" : [
               {
                 "key" : "QA",
                 "doc_count" : 1
               }
             ]
           }
         }
       ]
     }
   }
 }
```

### — THE – END —
