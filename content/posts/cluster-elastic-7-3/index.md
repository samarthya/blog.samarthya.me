---
title: "Cluster: Elastic 7.3"
date: "2020-04-14"
slug: "cluster-elastic-7-3"
categories: ["technical"]
tags: ["elastic"]
aliases: ["/wps/2020/04/14/cluster-elastic-7-3/", "/wps/2026/10/23/cluster-elastic-7-3/"]
wp_id: 572
---

What is intriguing about elastic stack is that; it can do so many things that it simplifies the life of a security analyst. The uphill task is to learn the technology itself, but once you have mastered it, things are much easier.

I will walk you through some of the learning that I got while experimenting for my Product to do some Security Analysis.

`GET _cat/nodes`

I have a set of three nodes running

172.18.0.2 35 74 37 1.26 1.26 0.66 dim \* node1  
172.18.0.3 36 74 34 1.26 1.26 0.66 dim - node2  
172.18.0.4 22 74 26 1.26 1.26 0.66 dim - node3

Creating an index can be as simple as

PUT myindex1

which returns response

{  
"acknowledged" : true,  
"shards\_acknowledged" : true,  
"index" : "denormalized\_blogs"  
}

\_bulk endpoint

POST denormalized\_blogs/\_bulk  
{"index":{"\_id":1}}  
{"id":"1","title":"Time Series with Kibana","authors":[{"name":"Alex Francoeur","company":{"country":{"code":"FR","name":"France"},"name":"ACME"}},{"name":"Chris Cowan","company":{"country":{"code":"NI","name":"Nigeria"},"name":"Elastic"}}]}

You cannot delete a mapping once it has been created without deleting the index.

Adding a temporary mapping for my document

POST temp1/\_doc  
{  
"id": "someid",  
"title": "My Blog Title",  
"products": [ "logstash", "beats" ],  
"authors": [  
{  
"name": "Author1",  
"company": {  
"name": "Company1",  
"country": {  
"name": "Country1",  
"code": "C1"  
}  
}  
}  
]  
}

Response for the index creation (temporary)

{  
"\_index" : "temp1",  
"\_type" : "\_doc",  
"\_id" : "GAvPeXEBkZu4d5ikkzZF",  
"\_version" : 1,  
"result" : "created",  
"\_shards" : {  
"total" : 2,  
"successful" : 1,  
"failed" : 0  
},  
"\_seq\_no" : 0,  
"\_primary\_term" : 1  
}

If you seek mapping

{  
"temp1" : {  
"mappings" : {  
"properties" : {  
"authors" : {  
"properties" : {  
"company" : {  
"properties" : {  
"country" : {  
"properties" : {  
"code" : {  
"type" : "text",  
"fields" : {  
"keyword" : {  
"type" : "keyword",  
"ignore\_above" : 256  
}  
}  
},  
"name" : {  
"type" : "text",  
"fields" : {  
"keyword" : {  
"type" : "keyword",  
"ignore\_above" : 256  
}  
}  
}  
}  
},  
"name" : {  
"type" : "text",  
"fields" : {  
"keyword" : {  
"type" : "keyword",  
"ignore\_above" : 256  
}  
}  
}  
}  
},  
"name" : {  
"type" : "text",  
"fields" : {  
"keyword" : {  
"type" : "keyword",  
"ignore\_above" : 256  
}  
}  
}  
}  
},  
"id" : {  
"type" : "text",  
"fields" : {  
"keyword" : {  
"type" : "keyword",  
"ignore\_above" : 256  
}  
}  
},  
"products" : {  
"type" : "text",  
"fields" : {  
"keyword" : {  
"type" : "keyword",  
"ignore\_above" : 256  
}  
}  
},  
"title" : {  
"type" : "text",  
"fields" : {  
"keyword" : {  
"type" : "keyword",  
"ignore\_above" : 256  
}  
}  
}  
}  
}  
}  
}
