---
title: "The Core Divide"
date: "2025-10-10T12:00:00Z"
slug: "the-core-divide"
description: "At the heart of machine learning, algorithms learn from data. The key distinction between supervised and unsupervised learning is the type of data used for training."
categories: ["technical"]
tags: ["ml", "data"]
aliases: ["/wps/2025/10/10/the-core-divide/"]
recovered: "Internet Archive snapshot 2026-05-17"
---

![](ml-1.png)

At the heart of machine learning, algorithms learn from data. The key distinction between supervised and unsupervised learning is the **type of data** used for training.

## Supervised Learning: Learning with a Teacher

Supervised learning algorithms are trained using a dataset that is **labeled**. This means for every input, there is a known, correct output (the “answer” or “label”). The algorithm’s job is to learn the mapping function from the input features to the output label.

| Characteristic | Description | Analogy |
| --- | --- | --- |
| **Data** | **Labeled Data** (Input Features + Correct Output/Label) | A student practicing math problems where they have the **answer key**. |
| **Goal** | **Predictive:** Predict a known outcome on new, unseen data. | Predict the price of a house or whether an email is spam. |
| **Main Tasks** | 1. **Classification** (predict a discrete category)  2. **Regression** (predict a continuous value) |

{{< lead >}}
When a machine learning algorithm is “trained” on data, it transforms from a **generic mathematical blueprint** into a **specific, highly tuned statistical model**.
— – Google
{{< /lead >}}

## Unsupervised Learning: Learning by Observation

Unsupervised learning algorithms are trained using a dataset that is **unlabeled**. There is no “answer key.” The algorithm’s job is to explore the data, find hidden patterns, and infer intrinsic structures or natural groupings without any guidance.

| Characteristic | Description | Analogy |
| --- | --- | --- |
| **Data** | **Unlabeled Data** (Input Features only) | A student given a collection of different objects and asked to **group them** based on their characteristics. |
| **Goal** | **Descriptive:** Discover patterns, structures, or natural groupings within the data. | Segment customers into groups with similar buying habits. |
| **Main Tasks** | 1. **Clustering** (grouping similar data points)  2. **Dimensionality Reduction** (simplifying data) |  |

## Note

> The algorithm itself is the **logic** or the blueprint.

### Example: **Linear Regression**

- When you first define this `algorithm`, the weights (wi) and the bias (b) are **unknown** (or randomly initialized).
- **Algorithm (Blueprint):** The logic is the formula `y=w1​x1​+w2​x2​+⋯+b`.
- It defines a relationship where the output (y) is a sum of inputs (xi​) multiplied by certain numbers called **weights** (wi​), plus a constant **bias** (b).

This logic (the formula) is what the programmer writes. It’s an empty shell waiting to be filled.

> “`Training`” is the process of using data to find the optimal values for these unknown numbers (the weights and the bias) so that the formula y=… gives the most accurate output (y) for the given inputs (xi​).

| Step | What the Algorithm Does | What is Stored (The “Learning”) |
| --- | --- | --- |
| **Input** | Reads a batch of labeled training data (e.g., x1​=2, x2​=5, True Answer y=12). | *Nothing yet—just processing data.* |
| **Prediction** | Uses the current (random) weights to calculate an output: ypred​=w1​x1​+w2​x2​+b. | *Nothing yet—just making a guess.* |
| **Error/Loss** | Compares its prediction (ypred​) to the true answer (ytrue​) and calculates the **error** (or “loss”). | *The calculated error value.* |
| **Adjustment** | Uses an optimization function (like Gradient Descent) to calculate *how much* each weight (wi​) needs to be adjusted to reduce the error. | **New values for w1​,w2​,…,b** (The core of the learned model). |

This four-step cycle repeats, potentially thousands or millions of times, using the entire dataset. With each iteration, the weights and bias are slightly adjusted to reduce the overall error.

Once the training process is complete (the error is minimized), the algorithm’s job is done. The result is the **Model**.

> **Model (The Application):** This is the **saved set of final, optimized numerical values** for all the internal parameters (weights and bias).

The trained PySpark `LogisticRegressionModel`, for example, is just an object that holds an array of final coefficients (`weights`) and an intercept (`bias`).

When you use the model to make predictions on new data, it **no longer learns**. It simply takes the new input data, plugs it into the original formula (the blueprint), and uses the **saved, learned weights** to calculate the final prediction.

In summary, the algorithm is the **potential** for a mathematical relationship, and the model is the **realized version** of that relationship, represented by a set of final numbers learned from the data.

![](ml-3.png)
