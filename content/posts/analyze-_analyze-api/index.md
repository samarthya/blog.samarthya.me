---
title: "Analyze: _analyze api"
date: "2020-05-02T10:21:09Z"
slug: "analyze-_analyze-api"
categories: ["technical"]
tags: ["analyze", "elasticsearch"]
aliases: ["/wps/2020/05/02/analyze-_analyze-api/"]
wp_id: 637
---

Text is a key data in most of the information that is ingested in the **elasticsearch**, and whether it is type `text` or `keyword` it requires careful consideration to choose which analyzer to use.

What is Analyzer?

An *analyzer*  which can be either builtin or custom, is just a package which contains three lower-level building blocks

1. *character filters*,
2. *tokenizers*, and
3. *token filters*.

Main documentation [here](https://www.elastic.co/guide/en/elasticsearch/reference/7.4/_testing_analyzers.html)

> NOTE: The analysis settings are non dynamic and can’t be updated while the index is open.

```text
GET _analyze
{
"text": "My simple text!",
"explain": true
}
```

Look at the output to understand which analyzer has been used and how it processes.

```text
{
"detail" : {
"custom_analyzer" : false,
"analyzer" : {
"name" : "standard",
"tokens" : [
{
"token" : "my",
"start_offset" : 0,
"end_offset" : 2,
"type" : "<ALPHANUM>",
"position" : 0,
"bytes" : "[6d 79]",
"positionLength" : 1,
"termFrequency" : 1
},
{
"token" : "simple",
"start_offset" : 3,
"end_offset" : 9,
"type" : "<ALPHANUM>",
"position" : 1,
"bytes" : "[73 69 6d 70 6c 65]",
"positionLength" : 1,
"termFrequency" : 1
},
{
"token" : "text",
"start_offset" : 10,
"end_offset" : 14,
"type" : "<ALPHANUM>",
"position" : 2,
"bytes" : "[74 65 78 74]",
"positionLength" : 1,
"termFrequency" : 1
}
]
}
}
}
```

Look at the STANDARD analyzer being used and how it breaks the original text from

```text
My simple text!
```

to

```text
"tokens" : [
{
"token" : "my",
"start_offset" : 0,
"end_offset" : 2,
"type" : "",
"position" : 0,
"bytes" : "[6d 79]",
"positionLength" : 1,
"termFrequency" : 1
},
{
"token" : "simple",
"start_offset" : 3,
"end_offset" : 9,
"type" : "",
"position" : 1,
"bytes" : "[73 69 6d 70 6c 65]",
"positionLength" : 1,
"termFrequency" : 1
},
{
"token" : "text",
"start_offset" : 10,
"end_offset" : 14,
"type" : "",
"position" : 2,
"bytes" : "[74 65 78 74]",
"positionLength" : 1,
"termFrequency" : 1
}
]
```

Look at every space the input is broken and even the punctuation has been removed - `text` instead of `text!`.

### Changing the analyzer to - Whitespace

```text
GET _analyze
{
"text": "My simple text!",
"explain": true,
"analyzer": "whitespace"
}
```

The output is something like

```text
{
"detail" : {
"custom_analyzer" : false,
"analyzer" : {
"name" : "whitespace",
"tokens" : [
{
"token" : "My",
"start_offset" : 0,
"end_offset" : 2,
"type" : "word",
"position" : 0,
"bytes" : "[4d 79]",
"positionLength" : 1,
"termFrequency" : 1
},
{
"token" : "simple",
"start_offset" : 3,
"end_offset" : 9,
"type" : "word",
"position" : 1,
"bytes" : "[73 69 6d 70 6c 65]",
"positionLength" : 1,
"termFrequency" : 1
},
{
"token" : "text!",
"start_offset" : 10,
"end_offset" : 15,
"type" : "word",
"position" : 2,
"bytes" : "[74 65 78 74 21]",
"positionLength" : 1,
"termFrequency" : 1
}
]
}
}
}
```

Look at how the output is similar except the punctuation has not been removed and the the case has been retained.

`My` instead of `my` as in the previous example.

### Other Analyzer: Stop, Keyword, English

#### Stop

```text
GET _analyze
{
"text": "My simple and sweet text!",
"explain": true,
"analyzer": "stop"
}
```

The stop words will be removed (Look at no and below)

```text
{
"detail" : {
"custom_analyzer" : false,
"analyzer" : {
"name" : "stop",
"tokens" : [
{
"token" : "my",
"start_offset" : 0,
"end_offset" : 2,
"type" : "word",
"position" : 0,
"bytes" : "[6d 79]",
"positionLength" : 1,
"termFrequency" : 1
},
{
"token" : "simple",
"start_offset" : 3,
"end_offset" : 9,
"type" : "word",
"position" : 1,
"bytes" : "[73 69 6d 70 6c 65]",
"positionLength" : 1,
"termFrequency" : 1
},
{
"token" : "sweet",
"start_offset" : 14,
"end_offset" : 19,
"type" : "word",
"position" : 3,
"bytes" : "[73 77 65 65 74]",
"positionLength" : 1,
"termFrequency" : 1
},
{
"token" : "text",
"start_offset" : 20,
"end_offset" : 24,
"type" : "word",
"position" : 4,
"bytes" : "[74 65 78 74]",
"positionLength" : 1,
"termFrequency" : 1
}
]
}
}
}
```

#### English: Analyzer

```text
GET _analyze
{
"text": "My simple and sweet text! by working.",
"explain": true,
"analyzer": "english"
}
```

Look at the output as under

```text
{
"detail" : {
"custom_analyzer" : false,
"analyzer" : {
"name" : "english",
"tokens" : [
{
"token" : "my",
"start_offset" : 0,
"end_offset" : 2,
"type" : "",
"position" : 0,
"bytes" : "[6d 79]",
"keyword" : false,
"positionLength" : 1,
"termFrequency" : 1
},
{
"token" : "simpl",
"start_offset" : 3,
"end_offset" : 9,
"type" : "",
"position" : 1,
"bytes" : "[73 69 6d 70 6c]",
"keyword" : false,
"positionLength" : 1,
"termFrequency" : 1
},
{
"token" : "sweet",
"start_offset" : 14,
"end_offset" : 19,
"type" : "",
"position" : 3,
"bytes" : "[73 77 65 65 74]",
"keyword" : false,
"positionLength" : 1,
"termFrequency" : 1
},
{
"token" : "text",
"start_offset" : 20,
"end_offset" : 24,
"type" : "",
"position" : 4,
"bytes" : "[74 65 78 74]",
"keyword" : false,
"positionLength" : 1,
"termFrequency" : 1
},
{
"token" : "work",
"start_offset" : 29,
"end_offset" : 36,
"type" : "",
"position" : 6,
"bytes" : "[77 6f 72 6b]",
"keyword" : false,
"positionLength" : 1,
"termFrequency" : 1
}
]
}
}
}
```

#### Keyword

```text
GET _analyze
{
"text": "My simple and sweet text! by working.",
"explain": true,
"analyzer": "keyword"
}
```

The output will change as under

```text
{
"detail" : {
"custom_analyzer" : false,
"analyzer" : {
"name" : "keyword",
"tokens" : [
{
"token" : "My simple and sweet text! by working.",
"start_offset" : 0,
"end_offset" : 37,
"type" : "word",
"position" : 0,
"bytes" : "[4d 79 20 73 69 6d 70 6c 65 20 61 6e 64 20 73 77 65 65 74 20 74 65 78 74 21 20 62 79 20 77 6f 72 6b 69 6e 67 2e]",
"positionLength" : 1,
"termFrequency" : 1
}
]
}
}
}
```

## Tokenizer and filters

How about playing with the some examples of tokenizer and filters.

```text
GET _analyze
{
"tokenizer": "standard",
"filter": ["lowercase"],
"text": "My simple and sweet exmple at work(ing)!"
}
```

I am using the `standard` as tokenizer and `lowercase` as filter. Look at how it tokenizes the information.

```text
{
"tokens" : [
{
"token" : "my",
"start_offset" : 0,
"end_offset" : 2,
"type" : "",
"position" : 0
},
{
"token" : "simple",
"start_offset" : 3,
"end_offset" : 9,
"type" : "",
"position" : 1
},
{
"token" : "and",
"start_offset" : 10,
"end_offset" : 13,
"type" : "",
"position" : 2
},
{
"token" : "sweet",
"start_offset" : 14,
"end_offset" : 19,
"type" : "",
"position" : 3
},
{
"token" : "exmple",
"start_offset" : 20,
"end_offset" : 26,
"type" : "",
"position" : 4
},
{
"token" : "at",
"start_offset" : 27,
"end_offset" : 29,
"type" : "",
"position" : 5
},
{
"token" : "work",
"start_offset" : 30,
"end_offset" : 34,
"type" : "",
"position" : 6
},
{
"token" : "ing",
"start_offset" : 35,
"end_offset" : 38,
"type" : "",
"position" : 7
}
]
}
```

adding snowball to the filter list now, and adding the missing `a` in `example` for the text.

```text
{
"tokens" : [
{
"token" : "my",
"start_offset" : 0,
"end_offset" : 2,
"type" : "",
"position" : 0
},
{
"token" : "simpl",
"start_offset" : 3,
"end_offset" : 9,
"type" : "",
"position" : 1
},
{
"token" : "and",
"start_offset" : 10,
"end_offset" : 13,
"type" : "",
"position" : 2
},
{
"token" : "sweet",
"start_offset" : 14,
"end_offset" : 19,
"type" : "",
"position" : 3
},
{
"token" : "exampl",
"start_offset" : 20,
"end_offset" : 27,
"type" : "",
"position" : 4
},
{
"token" : "at",
"start_offset" : 28,
"end_offset" : 30,
"type" : "",
"position" : 5
},
{
"token" : "work",
"start_offset" : 31,
"end_offset" : 35,
"type" : "",
"position" : 6
},
{
"token" : "ing",
"start_offset" : 36,
"end_offset" : 39,
"type" : "",
"position" : 7
}
]
}
```

look how it removed the `e` in the example other than other things.

### Defining a new analyzer

```text
PUT myIndex
{
  "settings": {
     "analysis": {
       "char_filter": {
        },
       "filter": {
        },
       "analyzer": {
           "new_analyzer": {}
        }
     }
   }
}
```
