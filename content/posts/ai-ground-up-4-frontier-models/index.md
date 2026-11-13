---
title: "AI from the ground up, part 4: what is a frontier model?"
date: 2026-11-12T20:32:00-05:00
description: "What 'frontier model' means to researchers, industry and lawmakers (state of the art, compute thresholds of 10^25 and 10^26 operations, dangerous capabilities), the frontier models of late 2026 from Anthropic, Google, OpenAI and Moonshot, and what the label should and should not mean when you pick a model."
featureimage: "feature.png"
categories: ["technical"]
tags: ["ai", "llm", "ml", "security"]
series: ["AI from the ground up"]
series_order: 4
draft: false
---

{{< lead >}}
"Frontier" is borrowed from maps: the edge of the explored territory. A frontier model is one at the edge of what
AI can currently do. The edge moves every few months, so the label is less a property of a model than a statement
about a date.
{{< /lead >}}

![What makes a frontier model, in three panels: definitions (state of the art per the Frontier Model Forum, top 5 by training compute per Epoch AI, dangerous capabilities per frontier AI regulation research), a compute ladder on a log scale (Kimi K2 estimated at about 3 × 10^24 operations, the EU AI Act systemic-risk presumption at 10^25, California SB 53's frontier model at 10^26, with compute growing 4 to 5 times a year), and late-2026 examples (Claude Fable 5.2, 9 Nov 2026; Gemini 4 Argon, 30 Sep; GPT-6 Astra, 3 Sep; Kimi K3 open weights, 16 Jul).](overview.svg "The edge of the map, as of November 2026")

{{< alert "circle-info" >}}
New terms are explained in plain words in [Keywords](/posts/ai-ground-up-4-frontier-models/#keywords) at the end.
{{< /alert >}}

The first three parts of this series covered the [maths]({{< relref "/posts/ai-ground-up-1-maths-behind-llms" >}}),
the [probability]({{< relref "/posts/ai-ground-up-2-probability" >}}) and the
[hardware]({{< relref "/posts/ai-ground-up-3-what-gpus-do" >}}) behind every LLM. This part looks at the models at
the very top: what makes them "frontier", who builds them, and why the term now appears in law.

## Three ways to define "frontier"

There is no single definition. Three groups use the word, each for its own purpose.

| Lens | Who | Definition |
|---|---|---|
| **Capability** | The [Frontier Model Forum](https://www.frontiermodelforum.org/about-us/), an industry body | "general purpose AI models that constitute the state of the art"; for membership, a general-purpose model that outperforms "all other models that have been widely deployed for at least 12 months" |
| **Compute** | [Epoch AI](https://epoch.ai/data/ai-models), which tracks AI models | Models "in the top 5 by training compute at the time of their release" |
| **Risk** | [Frontier AI Regulation](https://arxiv.org/abs/2307.03718), a 2023 policy paper | "highly capable foundation models that could possess dangerous capabilities sufficient to pose severe risks to public safety" |

They overlap in practice: the models with the most training compute tend to be the most capable, and the most
capable are the ones whose risks get studied. But each lens answers a different question: *is it the best?*, *is it
the biggest?*, *could it be dangerous?*

## The law draws a line in operations

Lawmakers needed something measurable, and settled on **training compute**: the total number of operations used to
train a model (part 1 explained them; the [How an LLM is built]({{< relref "/posts/how-an-llm-is-built-2-pre-training" >}})
series estimated one).

| Rule | Threshold | What happens above it |
|---|---|---|
| **EU AI Act, Article 51** | more than 10²⁵ operations | A general-purpose model is [presumed to have "high impact capabilities"](https://artificialintelligenceact.eu/article/51/) and so "systemic risk", which brings extra obligations; the Commission can change the number |
| **California SB 53** (signed 29 September 2025) | more than 10²⁶ operations, counting later fine-tuning | A ["frontier model"](https://fpf.org/blog/californias-sb-53-the-first-frontier-ai-law-explained/): its developer must publish a transparency report before deployment and report critical safety incidents within 15 days; developers with revenue above $500 million must also publish a yearly frontier AI framework |

To put the numbers on a scale: my estimate for [Kimi K2]({{< relref "/posts/how-an-llm-is-built-2-pre-training" >}}),
a 1-trillion-parameter open model from 2025, was about **3 × 10²⁴** operations, using the common 6 × parameters ×
tokens estimate on its active parameters. That is below the EU line and thirty times below California's. Training
compute for frontier models has been
[growing 4–5× per year](https://epoch.ai/blog/training-compute-of-frontier-ai-models-grows-by-4-5x-per-year)
(Epoch AI, 2010 to May 2024), so a fixed line that is far away today is close in two or three years. Both rules
expect to revise their thresholds for that reason.

Compute is an imperfect proxy. Developers do not always publish it, efficient training gets more capability per
operation every year, and a small model can be fine-tuned for a dangerous task. But it is measurable before a
model is released, which is why regulators use it.

## The frontier in November 2026

Here are the flagship releases of the last few months, from the companies' own announcements where I could read
them. Treat this table as a snapshot: it will be out of date within months.

| Model | Company | Announced | What stands out |
|---|---|---|---|
| **Claude Fable 5.2** (and Claude Mythos 5.2) | Anthropic | 9 Nov 2026 | Anthropic's [most capable models](https://www.anthropic.com/news), "for demanding reasoning and long-horizon agentic work"; 1M-token context; $8 / $40 per million input / output tokens |
| **Gemini 4 Argon** | Google | 30 Sep 2026 | [Aimed at](https://blog.google/innovation-and-ai/models-and-research/gemini-models/gemini-4-argon/) long-horizon coding, legal and finance work, and cyber defence; 77.9% on the DeepSWE coding benchmark (Google's figure); up to 1M output tokens; $2 / $10 at launch, rising to $4 / $20 |
| **GPT-6 Astra** | OpenAI | 3 Sep 2026 | [Reported](https://www.constellationr.com/insights/news/openai-launches-gpt-6-astra) as OpenAI's first model with "critical" cybersecurity capability, trained on more than 100,000 GPUs; focused on computer use and professional work; $10 / $50 |
| **Kimi K3** | Moonshot AI | 16 Jul 2026 | [Open weights](https://fortune.com/2026/07/16/moonshots-kimi-k3-pushes-chinese-ai-into-fable-level-territory/), reported at 2.7 trillion parameters, which Fortune called "the largest open-weight large language model available today" |

Below the flagship sits a range of cheaper models from the same companies. Anthropic's
[model overview](https://platform.claude.com/docs/en/about-claude/models/overview), for example, lists Claude Opus 5.5
($4 / $20) as the starting point "for most workloads", Sonnet 5.5 ($2 / $10) for speed and Haiku 5.5 (from
$0.10 / $0.50) for high-volume tasks such as classification. The frontier model is the top of a ladder, not the
whole product.

### Patterns worth noticing

1. **Gated launches.** Gemini 4 Argon rolled out first to "a set of trusted cyber defenders" through Google's
   Fairwind Program, and GPT-6 Astra reportedly first to customers in OpenAI's Daybreak programme. The most capable
   models now reach security defenders before everyone else.
2. **Safety frameworks are part of the launch.** Google's announcement describes refusing harmful cyber and
   chemical, biological, radiological and nuclear (CBRN) requests under its *Frontier Safety Framework*, plus
   monitoring of the model's reasoning. California's law now makes a published framework a legal duty for large
   developers.
3. **Agents are the target.** Every announcement above leads with long-running, multi-step work (coding, computer
   use, professional tasks), not chat.
4. **Open weights are close behind.** An open model, Kimi K3, is in the same conversation as the closed ones, which
   matters for anyone who needs to run a model themselves.
5. **Leaderboards disagree.** Each company reports the benchmarks it wins. Independent rankings change week to
   week and order the top models differently depending on the test.

## What "frontier" should mean to you

The label is about the edge of capability. Your question is usually different: which model does *my* job well
enough, fast enough and cheaply enough?

| If your task is | You probably need |
|---|---|
| Long, open-ended agent work, hard reasoning, large codebases | A frontier model, at a higher effort setting |
| Everyday coding, writing, analysis | The provider's recommended default model |
| Classification, extraction, routing at high volume | The smallest, fastest model that passes your tests |
| Data that must stay in-house | An open-weight model you run yourself (part 3 shows the hardware it takes) |

Price differences are large: in the Anthropic line-up above, the top model costs 80 times more per input token than
the smallest. The only reliable way to choose is to test candidate models on your own task, which is what part 5
is about.

## Takeaways

- **"Frontier" means the current state of the art,** and the edge moves every few months.
- **Three lenses:** capability (best), compute (biggest) and risk (potentially dangerous).
- **Law uses compute:** the EU presumes systemic risk above 10²⁵ operations; California's SB 53 defines frontier
  models above 10²⁶.
- **Late-2026 frontier:** Claude Fable 5.2, Gemini 4 Argon, GPT-6 Astra, and Kimi K3 among open models; launches
  are gated, framed by safety frameworks and aimed at agents.
- **The frontier is rarely the right default.** Test the cheapest model that does your job.

## Keywords

| Term | What it means |
|---|---|
| **Frontier model** | A model at the current edge of AI capability. |
| **Foundation model / general-purpose model** | A large model trained on broad data that can be adapted to many tasks. |
| **State of the art** | The best currently known result. |
| **Training compute** | Total operations used to train a model, usually written as a power of ten. |
| **10²⁵ / 10²⁶** | 1 followed by 25 or 26 zeros: the EU and California thresholds. |
| **Systemic risk** | The EU AI Act's term for risks from the most capable general-purpose models. |
| **Frontier AI framework** | A developer's published plan for finding and reducing catastrophic risks. |
| **Transparency report** | What a frontier developer must publish about a model before deploying it under SB 53. |
| **CBRN** | Chemical, biological, radiological and nuclear: the main catastrophic-misuse categories. |
| **Gated release** | Giving a model first to a vetted group (for example cyber defenders) before general access. |
| **Open weights** | The model's parameters are downloadable, so anyone can run it. |
| **Benchmark** | A standard test used to compare models. |

## References

- [About the Frontier Model Forum](https://www.frontiermodelforum.org/about-us/): Frontier Model Forum; the capability definition of frontier AI and the membership test
- [AI models database](https://epoch.ai/data/ai-models): Epoch AI; frontier as top 5 by training compute at release
- [Frontier AI Regulation: Managing Emerging Risks to Public Safety](https://arxiv.org/abs/2307.03718): Anderljung et al. (arXiv); the risk-based definition
- [EU AI Act, Article 51](https://artificialintelligenceact.eu/article/51/): Future of Life Institute's AI Act Explorer; classification of general-purpose models with systemic risk and the 10²⁵ presumption
- [California's SB 53: The First Frontier AI Law, Explained](https://fpf.org/blog/californias-sb-53-the-first-frontier-ai-law-explained/): Future of Privacy Forum; the 10²⁶ definition, signing date, $500 million threshold and obligations
- [Training compute of frontier AI models grows by 4-5x per year](https://epoch.ai/blog/training-compute-of-frontier-ai-models-grows-by-4-5x-per-year): Epoch AI; the growth rate, 2010 to May 2024
- [Anthropic news](https://www.anthropic.com/news): Anthropic; Claude Fable 5.2 and Claude Mythos 5.2 announcement date and description
- [Models overview](https://platform.claude.com/docs/en/about-claude/models/overview): Anthropic documentation; current Claude models, prices, context windows and guidance on choosing
- [Gemini 4 Argon: our next era of frontier intelligence](https://blog.google/innovation-and-ai/models-and-research/gemini-models/gemini-4-argon/): Google; date, focus, access programme, pricing, benchmark claims and safety measures
- [OpenAI launches GPT-6 Astra](https://www.constellationr.com/insights/news/openai-launches-gpt-6-astra): Constellation Research; launch date, Daybreak access, training scale and pricing (OpenAI's own site could not be read)
- [Moonshot's Kimi K3 pushes Chinese AI into Fable-level territory](https://fortune.com/2026/07/16/moonshots-kimi-k3-pushes-chinese-ai-into-fable-level-territory/): Fortune; K3's release date, size and open weights

Related: [How an LLM is built]({{< relref "/posts/how-an-llm-is-built-1-data-and-design" >}}) and
[AI in practice, part 3: tokens and tokenomics]({{< relref "/posts/ai-in-practice-3-tokens-and-tokenomics" >}}).
