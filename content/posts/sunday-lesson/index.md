---
title: "Sunday Lesson"
date: "2026-02-08"
slug: "sunday-lesson"
categories: ["technical"]
aliases: ["/wps/2026/02/08/sunday-lesson/", "/wps/2026/10/23/sunday-lesson/"]
wp_id: 2956
---

![Illustration of a person in a blanket with a coffee mug watching a machine learning dashboard by a snowy window](machine1.png)

After finishing the assignment late Saturday night, I took a moment to reflect on my progress. It was a valuable opportunity to document the key concepts and insights I gained from the experience.

## The Machine learning journey: From Raw to Predictions

The two quests, or rather two parallel journeys I embarked on; while trying to solve the assignment.

1. Classification: Predict if someone earns > 5-K ( Yes/No) [A binary decison]
2. Regression: Predict exact property values; a continuous number.

Look at the blog I wrote [here]({{< relref "/posts/data-mining-essentials" >}}).

## Act 1: Gathering the data

It started off with using [UCIML Repo](https://archive.ics.uci.edu/dataset/2/adult), to get the adult dataset.

```text
from ucimlrepo import fetch_ucirepo
adult = fetch_ucirepo(name="adult")
```

`fetch_ucirepo()` is your librarian, fetching the exact dataset you need

Sample data showed the contents besides what I could gather from the official documentation.
