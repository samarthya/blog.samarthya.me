---
title: "Apache Spark"
date: "2025-09-14T12:00:00Z"
slug: "apache-spark"
description: "So as part of the academic curriculum we just started re-exploring Apache Spark. It’s been one of the technology that I had long lost touch with."
categories: ["technical"]
tags: ["ai", "ml", "spark"]
aliases: ["/wps/2025/09/14/apache-spark/"]
recovered: "Internet Archive snapshot 2026-05-18"
---

![](big-data.png)

So as part of the academic curriculum we just started re-exploring Apache Spark. It’s been one of the technology that I had long lost touch with. Ironical but true, in this age of big data and speed Spark was left somewhere way behind in my past projects working for Pitney Bowes.

## History

Apache Spark was created in 2009 at UC Berkeley’s AMPLab as a research project led by Matei Zaharia. The goal was to overcome the limitations of **Hadoop’s MapReduce**, a popular but often slow data processing framework. MapReduce was designed for a linear workflow where each step reads data from a disk and writes the results back to a disk, which made it inefficient for tasks that require multiple passes over the same data, like machine learning algorithms.

Spark’s key innovation was the **Resilient Distributed Dataset (RDD)**, a fault-tolerant collection of elements that can be processed in parallel. RDDs can be cached in memory, which significantly speeds up iterative computations and interactive queries by avoiding constant disk reads and writes. This in-memory processing is what makes Spark much faster than MapReduce.

In 2013, the project was donated to the Apache Software Foundation, and it has since become a top-level project with a massive global community of developers.

## Purpose

The core purpose of Apache Spark is to provide a **fast and unified engine for big data workloads**. It can handle a wide variety of tasks, including:

- **Batch Processing:** Analyzing large amounts of static data (e.g., analyzing all sales data from the past year).
- **Real-time Stream Processing:** Analyzing data as it’s generated (e.g., monitoring a live feed of social media posts).
- **Machine Learning:** Training and running machine learning models on vast datasets.
- **SQL Queries:** Performing structured data analysis using a familiar language (SQL).
- **Graph Processing:** Analyzing network-like data, such as social connections.

Spark’s power lies in its ability to do all these things on a single, unified platform, eliminating the need to use separate tools for different tasks. It can run on a variety of cluster managers like Hadoop YARN, Apache Mesos, or Kubernetes, and can read data from a multitude of sources, including local files, Amazon S3, and HDFS.

## Example

```text
import requests
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, explode, split, lower, regexp_replace, length

# 1. Fetch the content from a URL using a separate library
url = "https://cloud.google.com/learn/what-is-artificial-intelligence"
try:
    response = requests.get(url, timeout=10)
    response.raise_for_status()  # This will raise an HTTPError if the response was an error
    url_content = response.text
except requests.exceptions.RequestException as e:
    print(f"Error fetching URL: {e}")
    url_content = ""

# 2. Create a SparkSession
spark = SparkSession.builder.appName("CountWordsFromURL").getOrCreate()

# 3. Create a DataFrame with the fetched content
data = [(url_content,)]
df = spark.createDataFrame(data, ["text_content"])

# 4. Use Spark to process the text
words = df.select(explode(split(df.text_content, "\\s+")).alias("word"))
cleaned_words = words.withColumn("word", col("word").cast("string")) \
    .withColumn("word", regexp_replace(col("word"), "[^a-zA-Z]", "")) \
    .filter(length(col("word")) > 0) \
    .withColumn("word", lower(col("word")))

# 5. Count the occurrences of "ai"
ai_count = cleaned_words.filter(col("word") == "ai").count()

# 6. Print the result
print(f"The word 'AI' appears {ai_count} times on the page.")

# 7. Stop the SparkSession
spark.stop()
```

Console output

```text
25/09/14 12:38:18 WARN Utils: Your hostname, Samarthya resolves to a loopback address: 127.0.1.1; using 10.255.255.254 instead (on interface lo)
25/09/14 12:38:18 WARN Utils: Set SPARK_LOCAL_IP if you need to bind to another address
Setting default log level to "WARN".
To adjust logging level use sc.setLogLevel(newLevel). For SparkR, use setLogLevel(newLevel).
25/09/14 12:38:18 WARN NativeCodeLoader: Unable to load native-hadoop library for your platform... using builtin-java classes where applicable
25/09/14 12:38:19 WARN Utils: Service 'SparkUI' could not bind on port 4040. Attempting port 4041.
25/09/14 12:38:22 WARN TaskSetManager: Stage 0 contains a task of very large size (1946 KiB). The maximum recommended task size is 1000 KiB.
The word 'AI' appears 228 times on the page.
```
