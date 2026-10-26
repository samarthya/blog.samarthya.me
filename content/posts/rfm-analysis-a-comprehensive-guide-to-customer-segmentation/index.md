---
title: "RFM Analysis: A Comprehensive Guide to Customer Segmentation"
date: "2025-01-24T12:00:00Z"
slug: "rfm-analysis-a-comprehensive-guide-to-customer-segmentation"
description: "RFM (Recency, Frequency, Monetary) Analysis is a customer segmentation technique that uses three key metrics:"
categories: ["technical"]
tags: ["data-analytics"]
aliases: ["/wps/2025/01/24/rfm-analysis-a-comprehensive-guide-to-customer-segmentation/"]
recovered: "Internet Archive snapshot 2026-03-12"
---

![](bin-3.jpg)

## What is RFM Analysis?

RFM (Recency, Frequency, Monetary) Analysis is a customer segmentation technique that uses three key metrics:

1. Recency: How recently a customer made a purchase
2. Frequency: How often they purchase
3. Monetary: Total amount spent

### Statistical Approach to Binning in RFM

Binning is critical in RFM to categorize customers:

- Divide each metric into quartiles (4 equal segments)
- Assign scores 1-4 for each dimension
- Create customer segments based on combined scores

## Python Example:

```text
import pandas as pd
import numpy as np

def rfm_segmentation(df):
    # Calculate RFM metrics
    rfm = df.groupby('customer_id').agg({
        'order_date': lambda x: (df['order_date'].max() - x.max()).days,
        'order_id': 'count',
        'total_amount': 'sum'
    })
    
    # Rename columns
    rfm.columns = ['Recency', 'Frequency', 'Monetary']
    
    # Create quartile-based scoring
    rfm['R_rank'] = pd.qcut(rfm['Recency'], q=4, labels=[4,3,2,1])
    rfm['F_rank'] = pd.qcut(rfm['Frequency'], q=4, labels=[1,2,3,4])
    rfm['M_rank'] = pd.qcut(rfm['Monetary'], q=4, labels=[1,2,3,4])
    
    return rfm
```

## R Example

```text
library(dplyr)

rfm_analysis <- function(data) {
  rfm_result <- data %>%
    group_by(customer_id) %>%
    summarise(
      Recency = as.numeric(max(max_date) - max(order_date)),
      Frequency = n_distinct(order_id),
      Monetary = sum(total_amount)
    ) %>%
    mutate(
      R_rank = ntile(Recency, 4),
      F_rank = ntile(Frequency, 4),
      M_rank = ntile(Monetary, 4)
    )
  
  return(rfm_result)
}
```

## Customer Segments Created

1. Champions: High scores across R, F, M
2. At Risk: High historical value but haven’t purchased recently
3. Hibernating: Low scores in all dimensions
4. New Customers: High recency, low frequency/monetary

## References

- Specifically referenced from:
  - Blattberg, R. C., & Deighton, J. (1996). Customer Equity Framework
  - Kumar, V., & Reinartz, W. (2016). Customer Engagement Marketing
