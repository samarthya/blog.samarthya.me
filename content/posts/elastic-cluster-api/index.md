---
title: "Elastic Cluster API"
date: "2020-02-06"
slug: "elastic-cluster-api"
categories: ["technical"]
tags: ["apis", "cluster", "elastic"]
aliases: ["/wps/2020/02/06/elastic-cluster-api/", "/wps/2026/10/23/elastic-cluster-api/"]
wp_id: 369
---

> Elastic Stack Monitoring Service is available with XPack only.

GET \_cluster/settings

{  
"persistent" : {  
"xpack" : {  
"monitoring" : {  
"elasticsearch" : {  
"collection" : {  
"enabled" : "false"  
}  
},  
"collection" : {  
"enabled" : "true"  
}  
}  
}  
},  
"transient" : { }  
}
