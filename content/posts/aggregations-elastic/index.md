---
title: "Aggregations: Elastic"
date: "2020-06-09"
slug: "aggregations-elastic"
categories: ["technical"]
tags: ["elasticsearch"]
aliases: ["/wps/2020/06/09/aggregations-elastic/", "/wps/2026/10/23/aggregations-elastic/"]
wp_id: 716
---

Aggregation works on a group of documents and can be categorized

1. Metric
2. Pipeline
3. Bucket
4. Matrix

## Metric Aggregation

Computes a single or multiple values

E.g. Average, Sum, Min, Max, Stats etc.

Stats computes multiple values Min, Max, Average, Sum and Count in a single request

Bucket aggregation computes metric on each bucket, something like a by clause in SQL

```text
GET network_sample/_search
{
  "size": 0, 
  "aggs": {
    "agg_count": {
      "max": {
        "field": "client.port"
      }
    }
  }
}
```

```text
{
  "took" : 3067,
  "timed_out" : false,
  "_shards" : {
    "total" : 3,
    "successful" : 3,
    "skipped" : 0,
    "failed" : 0
  },
  "hits" : {
    "total" : {
      "value" : 10000,
      "relation" : "gte"
    },
    "max_score" : null,
    "hits" : [ ]
  },
  "aggregations" : {
    "agg_count" : {
      "value" : 65535.0
    }
  }
}
```

```text
GET network_sample/_search
{
  "size": 0, 
  "aggs": {
    "agg_count": {
      "min": {
        "field": "client.port"
      }
    }
  }
}
```

```text
{
  "took" : 2319,
  "timed_out" : false,
  "_shards" : {
    "total" : 3,
    "successful" : 3,
    "skipped" : 0,
    "failed" : 0
  },
  "hits" : {
    "total" : {
      "value" : 10000,
      "relation" : "gte"
    },
    "max_score" : null,
    "hits" : [ ]
  },
  "aggregations" : {
    "agg_count" : {
      "value" : 0.0
    }
  }
}
```

Bucket aggregation example for the same network example.

```text
GET network_sample/_search
{
  "size": 0, 
  "aggs": {
    "example_buckets": {
      "terms": {
        "field": "source.geo.continent_name",
        "size": 10
      }
    }
  }
}
```

The `key` below is basically the unique values in the field specified. In our case we have specified `source.geo.continent_name` which has those values and the size specified limits it to maximum - 10

```text
{
  "took" : 2239,
  "timed_out" : false,
  "_shards" : {
    "total" : 3,
    "successful" : 3,
    "skipped" : 0,
    "failed" : 0
  },
  "hits" : {
    "total" : {
      "value" : 10000,
      "relation" : "gte"
    },
    "max_score" : null,
    "hits" : [ ]
  },
  "aggregations" : {
    "example_buckets" : {
      "doc_count_error_upper_bound" : 0,
      "sum_other_doc_count" : 0,
      "buckets" : [
        {
          "key" : "North America",
          "doc_count" : 4466179
        },
        {
          "key" : "Europe",
          "doc_count" : 2278900
        },
        {
          "key" : "Asia",
          "doc_count" : 217142
        },
        {
          "key" : "South America",
          "doc_count" : 7550
        },
        {
          "key" : "Africa",
          "doc_count" : 5954
        },
        {
          "key" : "Oceania",
          "doc_count" : 855
        }
      ]
    }
  }
}
```

If I change the size to 3, the other results will be excluded.

```text
{
  "took" : 1914,
  "timed_out" : false,
  "_shards" : {
    "total" : 3,
    "successful" : 3,
    "skipped" : 0,
    "failed" : 0
  },
  "hits" : {
    "total" : {
      "value" : 10000,
      "relation" : "gte"
    },
    "max_score" : null,
    "hits" : [ ]
  },
  "aggregations" : {
    "example_buckets" : {
      "doc_count_error_upper_bound" : 0,
      "sum_other_doc_count" : 14366,
      "buckets" : [
        {
          "key" : "North America",
          "doc_count" : 4467239
        },
        {
          "key" : "Europe",
          "doc_count" : 2280093
        },
        {
          "key" : "Asia",
          "doc_count" : 217223
        }
      ]
    }
  }
}
```

```text
GET network_sample/_search
{
  "size": 0, 
  "aggs": {
    "example_buckets": {
      "terms": {
        "field": "source.geo.continent_name",
        "size": 3
      },
      "aggs": {
        "country": {
          "terms": {
            "field": "source.geo.country_iso_code",
            "size": 10
          },
          "aggs": {
            "Total_Unique_IP": {
              "cardinality": {
                "field": "destination.ip"
              }
            }
          }
        }
      }
    }
  }
}
```

```text
{
  "took" : 5353,
  "timed_out" : false,
  "_shards" : {
    "total" : 3,
    "successful" : 3,
    "skipped" : 0,
    "failed" : 0
  },
  "hits" : {
    "total" : {
      "value" : 10000,
      "relation" : "gte"
    },
    "max_score" : null,
    "hits" : [ ]
  },
  "aggregations" : {
    "example_buckets" : {
      "doc_count_error_upper_bound" : 0,
      "sum_other_doc_count" : 14388,
      "buckets" : [
        {
          "key" : "North America",
          "doc_count" : 4470404,
          "country" : {
            "doc_count_error_upper_bound" : 0,
            "sum_other_doc_count" : 162,
            "buckets" : [
              {
                "key" : "US",
                "doc_count" : 4422865,
                "Total_Unique_IP" : {
                  "value" : 1025
                }
              },
              {
                "key" : "PA",
                "doc_count" : 21161,
                "Total_Unique_IP" : {
                  "value" : 528
                }
              },
              {
                "key" : "CA",
                "doc_count" : 20980,
                "Total_Unique_IP" : {
                  "value" : 531
                }
              },
              {
                "key" : "MX",
                "doc_count" : 2587,
                "Total_Unique_IP" : {
                  "value" : 123
                }
              },
              {
                "key" : "BZ",
                "doc_count" : 2198,
                "Total_Unique_IP" : {
                  "value" : 145
                }
              },
              {
                "key" : "GT",
                "doc_count" : 225,
                "Total_Unique_IP" : {
                  "value" : 170
                }
              },
              {
                "key" : "TT",
                "doc_count" : 64,
                "Total_Unique_IP" : {
                  "value" : 20
                }
              },
              {
                "key" : "DO",
                "doc_count" : 61,
                "Total_Unique_IP" : {
                  "value" : 38
                }
              },
              {
                "key" : "CR",
                "doc_count" : 57,
                "Total_Unique_IP" : {
                  "value" : 36
                }
              },
              {
                "key" : "HN",
                "doc_count" : 44,
                "Total_Unique_IP" : {
                  "value" : 35
                }
              }
            ]
          }
        },
        {
          "key" : "Europe",
          "doc_count" : 2282954,
          "country" : {
            "doc_count_error_upper_bound" : 254,
            "sum_other_doc_count" : 47199,
            "buckets" : [
              {
                "key" : "RU",
                "doc_count" : 1579851,
                "Total_Unique_IP" : {
                  "value" : 780
                }
              },
              {
                "key" : "NL",
                "doc_count" : 255431,
                "Total_Unique_IP" : {
                  "value" : 779
                }
              },
              {
                "key" : "LV",
                "doc_count" : 92544,
                "Total_Unique_IP" : {
                  "value" : 305
                }
              },
              {
                "key" : "CH",
                "doc_count" : 84128,
                "Total_Unique_IP" : {
                  "value" : 530
                }
              },
              {
                "key" : "EE",
                "doc_count" : 57542,
                "Total_Unique_IP" : {
                  "value" : 771
                }
              },
              {
                "key" : "RO",
                "doc_count" : 43722,
                "Total_Unique_IP" : {
                  "value" : 779
                }
              },
              {
                "key" : "DE",
                "doc_count" : 36094,
                "Total_Unique_IP" : {
                  "value" : 779
                }
              },
              {
                "key" : "MD",
                "doc_count" : 32729,
                "Total_Unique_IP" : {
                  "value" : 779
                }
              },
              {
                "key" : "LT",
                "doc_count" : 29318,
                "Total_Unique_IP" : {
                  "value" : 779
                }
              },
              {
                "key" : "GB",
                "doc_count" : 24284,
                "Total_Unique_IP" : {
                  "value" : 534
                }
              }
            ]
          }
        },
        {
          "key" : "Asia",
          "doc_count" : 217465,
          "country" : {
            "doc_count_error_upper_bound" : 103,
            "sum_other_doc_count" : 9081,
            "buckets" : [
              {
                "key" : "CN",
                "doc_count" : 116283,
                "Total_Unique_IP" : {
                  "value" : 780
                }
              },
              {
                "key" : "TW",
                "doc_count" : 25497,
                "Total_Unique_IP" : {
                  "value" : 288
                }
              },
              {
                "key" : "IN",
                "doc_count" : 20001,
                "Total_Unique_IP" : {
                  "value" : 332
                }
              },
              {
                "key" : "IR",
                "doc_count" : 14020,
                "Total_Unique_IP" : {
                  "value" : 530
                }
              },
              {
                "key" : "VN",
                "doc_count" : 8043,
                "Total_Unique_IP" : {
                  "value" : 542
                }
              },
              {
                "key" : "SG",
                "doc_count" : 6280,
                "Total_Unique_IP" : {
                  "value" : 68
                }
              },
              {
                "key" : "KR",
                "doc_count" : 5403,
                "Total_Unique_IP" : {
                  "value" : 136
                }
              },
              {
                "key" : "JP",
                "doc_count" : 4933,
                "Total_Unique_IP" : {
                  "value" : 480
                }
              },
              {
                "key" : "HK",
                "doc_count" : 4036,
                "Total_Unique_IP" : {
                  "value" : 486
                }
              },
              {
                "key" : "TR",
                "doc_count" : 2916,
                "Total_Unique_IP" : {
                  "value" : 64
                }
              }
            ]
          }
        }
      ]
    }
  }
}
```

Common buckets

- Histogram
- Date histogram
- Terms
- Filters
- Range

Watcher
