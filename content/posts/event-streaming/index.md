---
title: "Event Streaming"
date: "2022-01-20T08:06:56Z"
slug: "event-streaming"
categories: ["learn", "others", "technical"]
tags: ["kafka"]
aliases: ["/wps/2022/01/20/event-streaming/"]
wp_id: 1952
---

While reading Apache `Kafka` it was interesting analogy that they described

{{< lead >}}
Event streaming is the digital equivalent of the human body's central nervous system.
— Apache Kafka
{{< /lead >}}

It draws a great parallel between how the central nervous system allows for real time event generations and consumption in terms of reflex actions. The examples are well explained and captured [here](https://kafka.apache.org/powered-by).

The biggest advantage of using such a platform is that besides the obvious

- Distributed
- Secure
- Highly scalable & fault-tolerant

It can be deployed on bare-metal hardware and containers.

## Terminologies

The basic terms that you might often hear when talking about Kafka are as under.

## Server and Clients

Since it is distributed system it interacts over TCP via server and client system. It uses a binary protocol over TCP. (More details [here](https://kafka.apache.org/protocol.html#protocol_details))

Kafka cluster storage layer is termed as Broker.

## Events

These are essentially the information (a record) that is produced and read in the Kafka universe. They generally have a Key, Value and Timestamp. Events are organized and stored in `Topics`.

In `kafka` one can define for how long should the events should be retained through a per-topic configuration setting, after which old events will be discarded.

Topics are **partitioned**, meaning a topic is spread over a number of "buckets" located on different Kafka brokers.

## Producers

Applications that generates and publishes the information.

## Consumers

Applications that consume the information available in `Kafka` universe
