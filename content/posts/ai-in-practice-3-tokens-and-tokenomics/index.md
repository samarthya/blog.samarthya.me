---
title: "AI in practice, part 3: Tokens and tokenomics"
date: 2026-10-26T18:20:00-04:00
description: "What a token is, why context windows have limits, how language-model bills are calculated, and practical ways to spend fewer tokens without getting worse answers."
categories: ["technical"]
tags: ["ai", "llm", "tokens", "tokenomics", "cost"]
series: ["AI in practice"]
series_order: 3
draft: false
---

{{< katex >}}

{{< lead >}}
Language models don't read words, and they don't bill by the request. They read and charge in tokens. Once you
can count them, both the model's limits and the monthly invoice stop being surprises.
{{< /lead >}}

## What a token is

Before a model sees your text, a **tokenizer** cuts it into pieces from a fixed vocabulary, typically tens of
thousands to a few hundred thousand entries. Common words are one token; rarer words are split into
pieces; spaces and punctuation are tokens too. Most modern tokenizers use variants of *byte-pair encoding*,
which learns the most frequent fragments from training text.

Rules of thumb for English prose: **one token is about four characters, or three-quarters of a word**, so
1,000 tokens is roughly 750 words. Code, numbers, URLs and most non-English languages need **more** tokens per
word. Different model families use different tokenizers, so the same text has a different count on each.

In [The Probability Engine](/posts/the-probability-engine/) the model picks the next token by weighted dice.
Tokens are the faces of those dice.

## The context window

Everything a model considers in one call has to fit in its **context window**: the system prompt, the
conversation so far, any retrieved documents, tool definitions and results, *and* the answer it writes.
Windows have grown from a few thousand tokens to hundreds of thousands, and to a million or more on some models.

Two reasons not to fill them just because you can:

1. **Cost and speed.** Every token in the window is processed on every call. Attention compares tokens with each
   other, so long inputs take more compute and time ([why GPUs matter](/posts/matrix-multiplication-to-gpus/)).
2. **Quality.** Models can lose track of details buried in very long contexts. Relevant beats long.

## How the bill is calculated

Hosted models charge per token, usually quoted **per million tokens**, with separate prices for input and output:

$$
\text{cost} = \frac{\text{input tokens} \times p_{in} + \text{output tokens} \times p_{out}}{1\,000\,000}
$$

Output tokens typically cost several times more than input tokens, because they are generated one at a time.
Prices differ by model size and change often, so the numbers below are **made up to show the arithmetic**,
not any vendor's price list:

| Assumption | Value |
|---|---|
| Input price \(p_{in}\) | $3 per million tokens |
| Output price \(p_{out}\) | $15 per million tokens |
| Requests per day | 1,000 |
| Tokens per request | 2,000 in (prompt + history + documents), 500 out |

Per day: 2 million input tokens cost $6, and 0.5 million output tokens cost $7.50, so **$13.50 a day, about
$400 a month**. Notice that the 500-token answers cost more than the 2,000-token prompts.

## Where tokens hide

| Source | Why it grows |
|---|---|
| **Conversation history** | Chat apps resend the whole conversation on every turn: turn 20 pays for turns 1–19 again |
| **RAG context** | Each retrieved chunk is input; five 800-token chunks add 4,000 tokens to every question ([my RAG build](/posts/building-a-practical-retrieval-augmented-personal-assistant-rag/)) |
| **Tool definitions** | Every tool's name, description and schema is sent with each call ([part 4](/posts/ai-in-practice-4-tools-and-agents/)) |
| **Agent loops** | An agent that takes ten steps makes ten calls, each carrying the growing context |
| **Reasoning** | Models that "think" before answering produce reasoning tokens, usually billed as output |
| **System prompt** | A long instruction block is paid for on every single request |

## Spending fewer tokens

1. **Measure first.** Count tokens with the model's own tokenizer or the provider's counting tools, and log
   input and output tokens per request. You can't optimise what you don't see.
2. **Cache the stable part.** Many providers offer *prompt caching*: a repeated prefix (system prompt, tool
   definitions, a long document) is billed at a steep discount on later calls. Put stable content first and
   changing content last.
3. **Retrieve less, better.** Fewer, more relevant chunks beat many loosely related ones, both for cost and for answers.
4. **Summarise long histories** instead of resending every turn verbatim.
5. **Cap the output.** Set a maximum number of output tokens, and ask for the format you need: a list, not an essay.
6. **Use the smallest model that does the job.** Route simple tasks (classification, extraction) to small,
   cheap models; save the large ones for hard reasoning.
7. **Batch what isn't urgent.** Batch APIs process requests asynchronously at a discount, often around half price.
8. **Run it locally when it fits.** A model on your own hardware ([Ollama](/posts/ollama-revolutionizing-language-models/))
   costs electricity and hardware instead of per-token fees: good for experiments, private data and steady workloads.

## Tokenomics beyond the invoice

Tokens also set **latency** (output arrives at a fairly steady number of tokens per second, so long answers take
longer) and **rate limits** (providers cap tokens per minute). Designing for fewer tokens makes an application
cheaper, faster and less likely to hit limits all at once.

## Takeaways

- A token is a fragment of text; about ¾ of an English word, often less for code and other languages.
- The context window holds *everything*, including the answer. Fill it with what's relevant, not what's available.
- Output tokens are the expensive ones. History, retrieval, tools and agent loops quietly multiply input.
- Measure, cache, retrieve less, cap output, and pick the smallest model that works.

## Further reading

- [OpenAI's tokenizer playground](https://platform.openai.com/tokenizer): paste text and see the tokens.

Previous: [part 2, Vertex AI pipelines](/posts/ai-in-practice-2-vertex-ai-pipelines/). Next:
[part 4](/posts/ai-in-practice-4-tools-and-agents/), from RAG to tools and agents.
