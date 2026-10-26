---
title: "Kafka Cluster Fundamentals: Brokers, Topics, and Partitions"
date: "2025-01-18"
description: "A practical introduction to how Kafka distributes records across brokers and why partition planning matters."
categories: ["technical"]
tags: ["kafka", "streams", "devops"]
series: ["Back to basics"]
draft: false
---

I spent a fair amount of time looking at Kafka command output before the vocabulary settled in my head. Once I understood the difference between a broker, a topic, and a partition, the cluster stopped looking like one large mysterious system.

Kafka becomes easier to operate when its vocabulary is clear. A **broker** is a Kafka server. A **topic** is a logical stream name. A **partition** is an ordered append-only log inside a topic.

{{< alert "circle-info" >}}
Written up in October 2026 from my notes at the time. The topic description and command output are illustrative examples, not a current cluster capture.
{{< /alert >}}

## Partitions are the unit of scale

A topic with three partitions can distribute writes and reads across brokers. Records within one partition retain order. Records in different partitions do not have a single global order.

The producer chooses a partition using a partitioner. A message key commonly determines the partition, so all records for the same key can remain ordered:

```text
partition = hash(key) % number_of_partitions
```

The exact partitioner behavior is client-specific, but the design consequence is general: changing keys or partition counts can affect record placement.

## Replication and leaders

Each partition has a leader and replicas. Producers and consumers normally communicate with the leader. Replication protects availability when a broker fails, but it does not replace backups or a recovery plan.

A healthy cluster aims for replicas to remain in sync. If a replica falls behind, it may leave the in-sync replica set. Durability settings such as `acks=all` are meaningful only when the cluster's replica and minimum in-sync replica settings support the required guarantee.

## Consumer groups

A consumer group shares work. Within a group, one partition is assigned to one consumer at a time. Adding consumers helps only while there are unassigned partitions.

If a topic has three partitions and a group has five consumers, at least two consumers will be idle. If a consumer leaves, Kafka rebalances the group. Rebalances are normal, but frequent rebalances indicate instability, slow processing, or unsuitable timeout settings.

## Start with the workload

Before selecting partition counts, estimate:

- peak write rate;
- record size;
- required ordering key;
- consumer parallelism;
- retention duration;
- expected growth.

Partitions are not free. They add metadata, file handles, recovery work, and operational complexity. Choose enough to support growth, but do not use a large number as a substitute for capacity planning.

## A useful test

For a learning cluster, create a topic with three partitions and replication factor three, then observe:

```bash
kafka-topics.sh --bootstrap-server broker.example:9092 \
  --create --topic events --partitions 3 --replication-factor 3
```

Illustrative result:

```text
Created topic events.
Topic: events  PartitionCount: 3  ReplicationFactor: 3
```

Use documentation-only hostnames in examples and replace them with controlled infrastructure in practice. The most valuable Kafka skill is not memorizing commands; it is connecting each setting to an explicit durability, ordering, or throughput requirement.
