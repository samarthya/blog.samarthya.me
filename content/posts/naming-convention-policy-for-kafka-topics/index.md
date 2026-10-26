---
title: "Naming Convention Policy for Kafka topics"
date: "2022-07-13T12:00:00Z"
slug: "naming-convention-policy-for-kafka-topics"
description: "Creating a Topic in a kafka-cluster is easy and well documented for the kafka-topics.sh or even the official API documentation."
categories: ["java", "technical"]
tags: ["kafka", "topics"]
aliases: ["/wps/2022/07/13/naming-convention-policy-for-kafka-topics/"]
recovered: "Internet Archive snapshot 2026-03-13"
---

Creating a **Topic** in a kafka-cluster is easy and well documented for the `kafka-topics.sh` or even the official API documentation.

```text
 bin/kafka-topics.sh --help
```

The complexity arises, when you are trying to enforce a standard way of defining topic naming. There are many ways to identify the **right convention** based on your need, but to enforce such a topic convention while you are creating one is explained in this 5 steps blog.

> There is no right *convention* it is always determined based on what your business needs.

For my example, I wish to define to define a topic convention that follows the semantics as under

```text
<organizationname>.<productname>
```

It is simple enough to get started, and can be easily extended as you will observe as you follow along.

From the [official documentation](https://kafka.apache.org/documentation/#brokerconfigs_create.topic.policy.class.name), if you wish to define a custom topic policy creation you will have to define property as under

Properties files

```text
create.topic.policy.class.name=mypackage.className
```

The className should implement the interface

```text
 org.apache.kafka.server.policy.CreateTopicPolicy
```

## Step 1: Building Project

With these two building blocks let’s define a maven project

![Project Space](https://dz2cdn1.dzone.com/storage/temp/16042395-screen-shot-2022-07-13-at-93700-am.png "Project Space")

## Step 2: Define the dependency

Let’s define a package `me.samarthya` and also add dependency of the kafka-clients in the `pom.xml`

```text
 <dependency>
   <groupId>org.apache.kafka</groupId>
   <artifactId>kafka-clients</artifactId>
   <version>3.2.0</version>
   <scope>compile</scope>
</dependency>
```

## Step 3: Implementation

Lets define the main class Topic Policy as under

```text
public class TopicPolicy implements CreateTopicPolicy {
    private final Logger logger = Logger.getLogger(TopicPolicy.class.toString());

    private final static String TopicPattern = "\\w+\\.{1}\\w+";

    @Override
    public void validate(RequestMetadata requestMetadata) throws PolicyViolationException {
        StringBuilder bd = new StringBuilder().append(" Topic Name=").append(requestMetadata.topic());
        logger.info(bd.toString());
        if ( requestMetadata.topic().isEmpty() || !Pattern.matches(TopicPattern, requestMetadata.topic())) {
            throw new PolicyViolationException("Topic name " + requestMetadata.topic() + " should match the pattern " + TopicPattern);
        }
    }

    @Override
    public void close() throws Exception {
        logger.info(" Close & release.");
    }

    @Override
    public void configure(Map<String, ?> configs) {
        if (configs != null) {
            for( String k: configs.keySet()) {
                logger.info(configs.get(k).toString());
            }
        }
    }
}
```

With the class defined the main thing to observe is, the **TopicPattern**that has been defined as the format that will be matched for the name, and if it is not found a PolicyViolationException will be thrown.

## **Step 4: Repeat for each broker in the cluster**

Package the jar and it has to be placed under the `lib` folder of the kafka (classpath).

PowerShell

```text
  4 -rw-r--r--. 1 vagrant vagrant     3881 Jul 12 06:28 topic-policy-1.0-SNAPSHOT.jar
```

also, in the `server.properties` you can define two properties

```text
create.topic.policy.class.name=me.samarthya.TopicPolicy
auto.create.topics.enable=false
```

Restart your cluster.

## Step 5: Test your `Topics`

Let’s go back to the kafka binary folder (local machine) and issue the topic creation command again

```text
 bin/kafka-topics.sh --bootstrap-server mybroker.test:9092  --topic invalid_topic --create
```

If the jar has been loaded successfully you should see an error reported as below

```text
WARNING: Due to limitations in metric names, topics with a period ('.') or underscore ('_') could collide. To avoid issues it is best to use either, but not both.
Error while executing topic command : Topic name invalid_topic should match the pattern \w+\.{1}\w+
[2022-07-13 09:49:21,805] ERROR org.apache.kafka.common.errors.PolicyViolationException: Topic name invalid_topic should match the pattern \w+\.{1}\w+
 (kafka.admin.TopicCommand$)
```

You can modify the pattern now as per your convenience and re-deploy the jar to check the new custom topic policies.

### Example:

```text
bin/kafka-topics.sh --bootstrap-server mybroker.test.test:9092  --topic invalid.valid --create
```

```text
WARNING: Due to limitations in metric names, topics with a period ('.') or underscore ('_') could collide. To avoid issues it is best to use either, but not both.
Created topic invalid.valid
```

## Note:

Since the auto-topic creation has been disabled if you try and create an invalid topic through producer it will not work (below).

PowerShell

```text
 bin/kafka-console-producer.sh --bootstrap-server mybroker.test:9092 --topic test
```

Will result in following error

```text
[2022-07-13 09:54:21,196] WARN [Producer clientId=console-producer] Error while fetching metadata with correlation id 4 : {test=UNKNOWN_TOPIC_OR_PARTITION} (org.apache.kafka.clients.NetworkClient)
```

For an existing topic `invalid.valid` it should work

```text
bin/kafka-console-producer.sh --bootstrap-server mybrokers.test:9092 --topic invalid.valid
```
