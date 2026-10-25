---
title: "Elastic: _security API"
date: "2020-05-21"
slug: "elastic-_security-api"
categories: ["technical"]
tags: ["elastic", "security"]
aliases: ["/wps/2020/05/21/elastic-_security-api/", "/wps/2026/10/23/elastic-_security-api/"]
wp_id: 696
---

Kibana is an effective way of managing users; but as a programmer you always need an API.

- It helps to integrate with other applications you are building
- Quick and clean way without any cosmetics

```text
> GET /_security/_authenticate HTTP/1.1
> Host: myserver.elastic.node:9200
> Authorization: Basic ABCDEFGHIJKLMNOP==
> User-Agent: insomnia/7.1.1
> Accept: */*

< HTTP/1.1 200 OK
< content-type: application/json; charset=UTF-8
< content-length: 236

* Received 236 B chunk
* Connection #2 to host myserver.elastic.node left intact
```

```text
GET https://myserver.elastic.node:9200/_security/_authenticate
```

I have added basic authentication to quickly check

```text
{
  "username": "kibana",
  "roles": [
    "kibana_system"
  ],
  "full_name": null,
  "email": null,
  "metadata": {
    "_reserved": true
  },
  "enabled": true,
  "authentication_realm": {
    "name": "reserved",
    "type": "reserved"
  },
  "lookup_realm": {
    "name": "reserved",
    "type": "reserved"
  }
}
```

```text
GET https://myserver.elastic.node:9200/_security/user/samarthya
```

```text
{
  "error": {
    "root_cause": [
      {
        "type": "security_exception",
        "reason": "missing authentication credentials for REST request [/_security/user/samarthya]",
        "header": {
          "WWW-Authenticate": [
            "Bearer realm=\"security\"",
            "ApiKey",
            "Basic realm=\"security\" charset=\"UTF-8\""
          ]
        }
      }
    ],
    "type": "security_exception",
    "reason": "missing authentication credentials for REST request [/_security/user/samarthya]",
    "header": {
      "WWW-Authenticate": [
        "Bearer realm=\"security\"",
        "ApiKey",
        "Basic realm=\"security\" charset=\"UTF-8\""
      ]
    }
  },
  "status": 401
}
```

User credentials are cached in memory on each node to avoid connecting to a remote authentication service or hitting the disk for every incoming request.

```text
POST https://myserver.elastic.node:9200/_security/realm/default_file/_clear_cache
```

```text
{
  "_nodes": {
    "total": 3,
    "successful": 3,
    "failed": 0
  },
  "cluster_name": "abcd_user",
  "nodes": {
    "mrTQQhMPQfWPF6q_IGf5s5Q": {
      "name": "node3.elasticsearch.node"
    },
    "8P5-I2yKQEu0Sbxtq0J0QDg": {
      "name": "node2.elasticsearch.node"
    },
    "hEkSDlSxQoKw94WS7c-T0xw": {
      "name": "master.elasticsearch.node"
    }
  }
}
```

```text
POST https://myserver.elastic.node:9200/_security/api_key
{
  "name": "blog-key",
  "expiration": "1d"
}
```

```text
{
  "id": "RKoiMnIBLGvMX-heXl-O",
  "name": "blog-key",
  "expiration": 1590065412726,
  "api_key": "NODL7y_TSkinR1GIitRGFQ"
}
```

Points out

- id - A unique id
- name - Name we gave for the key
- expiration - in ms
- api\_key - API key to be used
