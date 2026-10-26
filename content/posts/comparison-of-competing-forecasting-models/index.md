---
title: "Comparison of Competing Forecasting Models"
date: "2025-02-07T12:00:00Z"
slug: "comparison-of-competing-forecasting-models"
description: "How to tell which forecasting model is better: MAE, MSE, RMSE, MAPE, sMAPE, bias and Theil's U, explained with an ice-cream-sales example."
categories: ["technical"]
tags: ["ba", "data-analytics"]
aliases: ["/wps/2025/02/07/comparison-of-competing-forecasting-models/"]
recovered: "Internet Archive snapshot 2026-04-21"
---

| Performance Measure | Description | Interpretation | Advantages | Disadvantages |
| --- | --- | --- | --- | --- |
| Mean Absolute Error (MAE) | Average absolute difference between forecast and actual values. | Lower MAE indicates better accuracy. | Easy to understand and interpret. Robust to outliers. | Doesn’t penalize large errors more than small ones. |
| Mean Squared Error (MSE) | Average squared difference between forecast and actual values. | Lower MSE indicates better accuracy. | Penalizes larger errors more heavily. Mathematically convenient. | Sensitive to outliers. Units are squared. |
| Root Mean Squared Error (RMSE) | Square root of MSE. | Lower RMSE indicates better accuracy. | Same units as the original data. Penalizes larger errors more heavily. | Sensitive to outliers. |
| Mean Absolute Percentage Error (MAPE) | Average absolute percentage difference between forecast and actual values. | Lower MAPE indicates better accuracy. | Easy to understand and interpret. Scale-independent. | Undefined if actual values are zero. Can be biased if actual values are close to zero. |
| Symmetric Mean Absolute Percentage Error (sMAPE) | A variation of MAPE that handles zero or near-zero actual values better. | Lower sMAPE indicates better accuracy. | Handles zero or near-zero actual values better than MAPE. Scale-independent. | Can still be biased if forecasts are consistently over or under the actual values. |
| Mean Error (ME) or Bias | Average difference between forecast and actual values. | Closer to zero indicates less bias. Positive ME suggests over-forecasting. Negative ME suggests under-forecasting. | Detects systematic over or under-forecasting. | Doesn’t measure the magnitude of errors, only the direction. |
| Theil’s U | Compares the forecasting accuracy of the model to a naive forecast (e.g., assuming no change). | U < 1 indicates better performance than the naive forecast. U = 1 means equal performance. U > 1 means worse performance. | Useful for assessing the value added by the model compared to a simple benchmark. | Can be sensitive to outliers. |

**Imagine you’re predicting how many ice cream cones you’ll sell each day.** You have a model that makes these predictions, and you want to see how good it is. These measures help you do that.

- **Mean Absolute Error (MAE):** Think of this as the *average “oops” amount*. It’s how far off your predictions are *on average*, ignoring whether you predicted too high or too low. A lower MAE is better – it means your predictions are closer to the actual sales. *Significance:* Simple to understand, gives you a general sense of accuracy.
- **Mean Squared Error (MSE):** This is similar to MAE, but it *really punishes big “oops” amounts*. If you’re off by a lot on one day, MSE goes up a lot. A lower MSE is better. *Significance:* Useful if big errors are really bad for your business (e.g., running out of ice cream is much worse than having a little extra).
- **Root Mean Squared Error (RMSE):** This is just the square root of MSE. It’s helpful because it’s in the same units as your original data (number of ice cream cones). So, if your RMSE is 10, it means your predictions are *typically* off by about 10 cones. A lower RMSE is better. *Significance:* Easy to compare to your actual sales numbers.
- **Mean Absolute Percentage Error (MAPE):** This tells you how far off your predictions are *as a percentage*. If your MAPE is 5%, it means your predictions are *typically* off by 5% of the actual sales. A lower MAPE is better. *Significance:* Useful for comparing accuracy across different scales (e.g., comparing ice cream cone sales to t-shirt sales). *Important Note:* MAPE can be misleading if your actual sales are ever zero.
- **Symmetric Mean Absolute Percentage Error (sMAPE):** This is a slightly fancier version of MAPE that’s better behaved when actual sales are close to zero. Still measures error as a percentage. A lower sMAPE is better. *Significance:* A more reliable percentage error measure than MAPE in some situations.
- **Mean Error (ME) or Bias:** This tells you if you’re *consistently* over- or under-predicting. A positive ME means you tend to predict too high (you’re too optimistic), and a negative ME means you tend to predict too low (you’re too pessimistic). Ideally, you want ME to be close to zero. *Significance:* Helps you identify systematic biases in your predictions.
- **Theil’s U:** This is a bit more complex. It compares your model’s accuracy to a *really simple* prediction (like just assuming tomorrow’s sales will be the same as today’s). If your Theil’s U is less than 1, your model is doing better than that simple prediction. If it’s greater than 1, your model is actually doing *worse*! *Significance:* Tells you if your fancy model is actually adding value compared to a basic guess.
