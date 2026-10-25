---
title: "Text - Elastic"
date: "2020-03-29T17:37:33Z"
slug: "text-elastic"
categories: ["technical"]
tags: ["elasticsearch"]
aliases: ["/wps/2020/03/29/text-elastic/"]
wp_id: 490
---

If you are not aware of mapping, it might be a little confusing but I would try my best.

Every document that gets indexed in elastic has fields, every field that is accessible has an associated type with it (Inverted Index) which helps elastic organize data for quick retrieval.

I create a sample index my\_index with a field `country_name` that was auto-mapped as I added the value.

```text
POST my_index/_doc/1
 {
   "country_name": "The United States of America"
 }

GET my_index/_mapping

{
   "my_index" : {
     "mappings" : {
       "properties" : {
         "country_name" : {
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

## Text

As evident the default type provided to the `country_name` is TEXT, and another something called `fields` (Multi-fields which I will touch upon later).

From the official documentation

> A field to index full-text values, such as the body of an email or the description of a product. These fields are `analyzed`, that is they are passed through an [analyzer](https://www.elastic.co/guide/en/elasticsearch/reference/master/analysis.html) to convert the string into a list of individual terms before being indexed.
>
> @elastic.co

If you need to index structured content it is better to use Keyword (the one in the fields as shown above)

Keyword is typically used for Filtering, like show all the movies of category comedy.

### What is the difference?

One is for full text search and the other for aggregations and sorting.

A simple search request

```text
GET my_index/_search
```

Since there is only one document currently it should return something like

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
       "value" : 1,
       "relation" : "eq"
     },
     "max_score" : 1.0,
     "hits" : [
       {
         "_index" : "my_index",
         "_type" : "_doc",
         "_id" : "1",
         "_score" : 1.0,
         "_source" : {
           "country_name" : "The United States of America"
         }
       }
     ]
   }
 }
```

Let us run an aggregation to highlight the difference

```text
GET my_index/_search
 {
   "aggs": {
     "Top Country": {
       "terms": {
         "field": "country_name",
         "size": 10
       }
     }
   }
 }
```

What do you guess the response will be? I am running a `terms` aggregation on `country_name`.

You should get an error like below

```text
"error": {
     "root_cause": [
       {
         "type": "illegal_argument_exception",
         "reason": "Fielddata is disabled on text fields by default. Set fielddata=true on [country_name] in order to load fielddata in memory by uninverting the inverted index. Note that this can however use significant memory. Alternatively use a keyword field instead."
       }
     ],
```

If it is simple `TEXT` it will be broken down to be indexed, to make the following query possible

```text
GET my_index/_search
 {
   "size": 0, 
   "query": {
     "match": {
       "country_name": "America"
     }
   }
 }
```

It should respond as under

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
       "value" : 1,
       "relation" : "eq"
     },
     "max_score" : null,
     "hits" : [ ]
   }
 }
```

But if I aggregate and since it is broken down it wont work, and hence the error as seen above. If I want that `agg` to work, I will simply modify the query as under.

```text
GET my_index/_search
 {
   "aggs": {
     "Top Country": {
       "terms": {
         "field": "country_name.keyword",
         "size": 10
       }
     }
   }
 }
```

and when executed it shall return something like

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

      "value" : 1,

      "relation" : "eq"

    },

    "max_score" : 1.0,

    "hits" : [

      {

        "_index" : "my_index",

        "_type" : "_doc",

        "_id" : "1",

        "_score" : 1.0,

        "_source" : {

          "country_name" : "The United States of America"

        }

      }

    ]

  },

  "aggregations" : {

    "Top Country" : {

      "doc_count_error_upper_bound" : 0,

      "sum_other_doc_count" : 0,

      "buckets" : [

        {

          "key" : "The United States of America",

          "doc_count" : 1

        }

      ]

    }

  }

}
```

Simple yet effective.

Helpful links

- https://www.elastic.co/guide/en/elasticsearch/reference/master/keyword.html
- https://www.elastic.co/guide/en/elasticsearch/reference/master/text.html
- https://www.elastic.co/guide/en/elasticsearch/reference/master/doc-values.html

### Multi Fields

It is often useful to index the same field in different ways for different
purposes. For instance, a `string` field could be mapped as
a `text` field for full-text search, and as a `keyword` field for
sorting or aggregations. Alternatively, you could index a text field with
the [`standard` analyzer](https://www.elastic.co/guide/en/elasticsearch/reference/master/analysis-standard-analyzer.html), the
[`english`](https://www.elastic.co/guide/en/elasticsearch/reference/master/analysis-lang-analyzer.html#english-analyzer) analyzer, and the
[`french` analyzer](https://www.elastic.co/guide/en/elasticsearch/reference/master/analysis-lang-analyzer.html#french-analyzer).

Most datatypes support multi-fields via the [`fields`](https://www.elastic.co/guide/en/elasticsearch/reference/master/multi-fields.html) parameter.

## -- THE - END --
