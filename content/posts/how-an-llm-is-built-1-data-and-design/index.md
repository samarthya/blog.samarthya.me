---
title: "How an LLM is built, part 1: the plan, the data and the design"
date: 2026-11-10T08:44:00-05:00
description: "The nine stages that turn raw text into a large language model, then the first three in detail (data, tokenizer and architecture), followed through the published recipe of Kimi K2, a 1-trillion-parameter open-weight model."
featureimage: "feature.png"
categories: ["technical"]
tags: ["ai", "llm", "ml", "transformers"]
series: ["How an LLM is built"]
series_order: 1
draft: false
---

{{< lead >}}
An LLM is raised in two stages. First it reads a library far bigger than anyone could read in many lifetimes and
learns to guess the next word. Then it does an apprenticeship: it is shown how to answer, made to practise, and
graded until it is useful. Before either can start, someone has to build the library and design the student.
{{< /lead >}}

![The nine stages of building Kimi K2, left to right: data (15.5T tokens), tokenizer (160K vocabulary), architecture (1.04T parameters, 32.6B active), pre-training (MuonClip, no loss spikes), long context (4K to 128K), supervised fine-tuning (23,000+ tools), reinforcement learning (verifiable rewards and self-critique), evaluation (SWE-bench Verified 65.8) and release (block-FP8, modified MIT). Stages 1 to 3 are highlighted as part 1, 4 and 5 as part 2, 6 to 9 as part 3.](overview.svg "Kimi K2's pipeline; this part covers the first three stages")

{{< alert "circle-info" >}}
New terms are explained in plain words in [Keywords](/posts/how-an-llm-is-built-1-data-and-design/#keywords)
at the end.
{{< /alert >}}

## Why follow one real model

Most "how LLMs work" articles stop at the transformer diagram. The hard part, and the part that decides whether a
model is any good, is everything around it: which data, how much compute, how to keep a months-long training run
from blowing up, and how to turn a text predictor into an assistant that can use tools.

So I followed one model from start to finish. **Kimi K2**, from the Beijing company Moonshot AI, was released in
July 2025 with downloadable weights and a [detailed technical report](https://arxiv.org/abs/2507.20534). That makes
it a rare case where the whole recipe is public, with real numbers. Moonshot's newer
[K3 line (July 2026)](https://fortune.com/2026/07/16/moonshots-kimi-k3-pushes-chinese-ai-into-fable-level-territory/)
is reported at 2.7 trillion parameters, but K2's report is the one I could read stage by stage.

This series has three parts:

1. **The plan, the data and the design** (this post): what goes in and what shape the model takes.
2. **Pre-training**: the months on GPUs that produce a *base model*.
3. **From base model to assistant**: fine-tuning, reinforcement learning, evaluation and release.

## The whole pipeline

| # | Stage | What happens | Kimi K2 |
|---|---|---|---|
| 1 | Data | Collect, clean, deduplicate and mix text | 15.5 trillion tokens: web, code, maths, knowledge |
| 2 | Tokenizer | Decide how text is cut into pieces | 160K-token vocabulary |
| 3 | Architecture | Choose the network's shape and size | Mixture-of-Experts: 1.04T parameters, 32.6B used per token |
| 4 | Pre-training | Learn to predict the next token | MuonClip optimiser, no loss spikes |
| 5 | Long context | Learn to read long inputs | 4K → 32K → 128K tokens |
| 6 | Fine-tuning | Learn from examples of good answers and tool use | Agent conversations built from 23,000+ tools |
| 7 | Reinforcement learning | Practise, get graded, improve | Verifiable rewards plus self-critique |
| 8 | Evaluation | Measure and find weaknesses | SWE-bench Verified 65.8 |
| 9 | Release | Package, license and serve | Block-FP8 weights, modified MIT licence |

Stages 1–5 make the **base model**, a brilliant autocomplete. Stages 6–9 turn it into an **assistant**.

## Stage 1: data, the library

A model can only know what it has read. Everything it will later "know" about Kubernetes, cooking or Hindi grammar
comes from this stage, so most of a model team's effort goes here.

### Where the text comes from

| Source | Why it is there |
|---|---|
| Web pages (mostly Common Crawl, a public crawl of the web) | Breadth: language, facts, opinions, styles |
| Code (public repositories) | Programming, and a strong dose of step-by-step logic |
| Maths (papers, textbooks, solutions) | Reasoning that can be checked |
| Knowledge (books, encyclopaedias, reference) | Dense, reliable facts |

K2 used exactly these four domains: web text, code, mathematics and knowledge.

### Turning a crawl into training text

Raw web pages are mostly menus, adverts and near-copies. Moonshot does not publish its filtering code, but the open
[FineWeb dataset](https://arxiv.org/abs/2406.17557) (15 trillion tokens from 96 Common Crawl snapshots, the same
size class as K2's data) documents every step:

1. **Block bad URLs** with a list of adult and spam sites.
2. **Extract the text** from the raw HTML, dropping navigation and boilerplate.
3. **Keep the right language** with a language classifier (FineWeb keeps English with a score of at least 0.65).
4. **Quality filters:** drop pages that are mostly short lines, repeated lines, lists of links or placeholder text.
5. **Deduplicate.** Near-identical pages are found with MinHash (a fast way to spot documents that share most of
   their phrases) and only one copy is kept. Repeated text teaches a model to memorise instead of understand.
6. **Remove personal data** such as email addresses before release.

A final step many teams now add is a **quality classifier**. FineWeb-Edu had a large model score 460,000 pages for
educational value from 0 to 5, trained a small classifier on those scores, and kept pages scoring 3 or more. That
cut 15 trillion tokens to 1.3 trillion, and models trained on the smaller set did much better on knowledge and
reasoning tests. Less, but better.

### How much text is enough?

The [Chinchilla paper](https://arxiv.org/abs/2203.15556) found that model size and data should grow together:
"for every doubling of model size the number of training tokens should also be doubled". Its 70B model, trained
on four times more data than the 280B Gopher with the same compute, beat it. K2 was trained on
**15.5 trillion tokens**.

### When good data runs out: rephrase it

There is only so much high-quality text in the world. The obvious move, showing the same good text many times,
makes the model memorise it. K2 did something smarter: an LLM **rewrote** knowledge documents in different styles
and from different perspectives, chunk by chunk, with checks that the facts survived.

The report's test on SimpleQA (short factual questions) shows the effect:

| Training data | SimpleQA score |
|---|---|
| Raw text, read 10 times | 23.76 |
| 10 different rephrasings, each read once | **28.94** |

Maths documents got the same treatment, rewritten in a "learning note" style, and good maths material in other
languages was translated into English. Each corpus was rephrased at most twice, to limit the risk of drifting
from the original.

### The mix

The last data decision is the **mix**: how much of each domain the model sees. More code makes a better
programmer; too much and its everyday writing suffers. Teams settle the mix with small test runs before the big
one, and often change it near the end of training to favour the best data (part 2 covers that).

## Stage 2: the tokenizer, cutting text into pieces

A model does not see letters or words. It sees **tokens**: pieces of text from a fixed list (the *vocabulary*),
each mapped to a number. Common words are one token; rare words are split into pieces.

Most tokenizers are built with **byte pair encoding (BPE)**, first used for
[translating rare words as subword units](https://arxiv.org/abs/1508.07909). The idea fits in a few lines:

1. Start with single characters (or bytes) as the vocabulary.
2. Count which pair of neighbours appears most often in the training text, say `t` + `h`.
3. Merge it into a new token `th` and add it to the vocabulary.
4. Repeat until the vocabulary is the size you want.

You can see the result with any tokenizer. This uses GPT-2's (not K2's, which needs the full model files), but the
idea is the same:

```python
# pip install transformers
from transformers import AutoTokenizer

tok = AutoTokenizer.from_pretrained("gpt2")
for text in ["Kubernetes", "the cat sat", "Fall. Get up. Build again."]:
    ids = tok.encode(text)                       # text -> token numbers
    pieces = [tok.decode([i]) for i in ids]      # each number back to its piece of text
    print(f"{text!r:30} {len(ids)} tokens: {pieces}")
```

On my machine (transformers 5.22) it prints:

```text
'Kubernetes'                   4 tokens: ['K', 'uber', 'net', 'es']
'the cat sat'                  3 tokens: ['the', ' cat', ' sat']
'Fall. Get up. Build again.'   8 tokens: ['Fall', '.', ' Get', ' up', '.', ' Build', ' again', '.']
```

Common words are one token each (the leading space is part of the token), while a rarer word like *Kubernetes*
is split into four pieces.

The trade-off is size. K2's vocabulary has [160K entries](https://huggingface.co/moonshotai/Kimi-K2-Instruct),
about three times GPT-2's 50K. A bigger vocabulary means fewer tokens per sentence, so text is cheaper to process
and more fits in the context window, especially for languages other than English. The price is a bigger table of
token meanings (the *embedding table*) for the model to learn. The tokenizer is fixed before training; changing
it later means starting again. [AI in practice, part 3]({{< relref "/posts/ai-in-practice-3-tokens-and-tokenomics" >}})
shows why token counts also drive the bill.

## Stage 3: the architecture, designing the student

### The transformer in one paragraph

Almost every modern LLM is a **transformer**, the design from
[Attention Is All You Need](https://arxiv.org/abs/1706.03762). Each token becomes a long list of numbers (a
*vector*). The vectors then pass through a stack of identical **layers**. In each layer:

1. **Attention:** every token looks back at the tokens before it and decides which ones matter. In "the cat sat
   on the mat because *it* was tired", attention is how *it* finds *cat*.
2. **Feed-forward network:** each token's vector goes through a small neural network on its own, where most of
   the model's stored knowledge lives.

At the top, the final vector is turned into a probability for every token in the vocabulary: the guess for the
next token. K2 has **61 layers**, and each token's vector has **7,168 numbers**.

### Mixture-of-Experts: a kitchen of specialists

The obvious way to make a model smarter is to make it bigger, but in a normal (*dense*) model every parameter
works on every token, so cost grows with size. K2 instead uses **Mixture-of-Experts (MoE)**.

Picture a restaurant kitchen with **384 specialist cooks** in each MoE layer. For every token, a small *router*
picks the **8** most suitable cooks, and **1** shared cook works on every dish. The kitchen holds the skill of all
384, but each dish costs only the time of nine.

| | Stored | Used per token |
|---|---|---|
| Parameters | 1.04 trillion | 32.6 billion |
| Experts per MoE layer | 384 | 8 + 1 shared |

That is a **sparsity of 48**: K2 stores 48 times more expertise than it pays for on each token. The catch is
memory: all 1.04 trillion parameters must still be loaded somewhere, even if only 3% are used at a time.

### Attention that remembers less

While generating, a model keeps a memory of every earlier token, the **KV cache**, so it does not recompute them.
For long inputs this cache becomes the main cost of serving. K2 uses **Multi-head Latent Attention (MLA)**, which
compresses that memory into a smaller form; in [DeepSeek-V2](https://arxiv.org/abs/2405.04434), where it was
introduced, MLA cut the cache by 93.3%. K2 also uses 64 attention *heads* (parallel ways of looking back) where
DeepSeek-V3 uses 128, which the report chose to make long inputs cheaper to run.

### The design in numbers

| Setting | Kimi K2 |
|---|---|
| Layers | 61 (1 dense, the rest MoE) |
| Hidden size (numbers per token) | 7,168 |
| Experts per MoE layer | 384, 8 active + 1 shared |
| Attention | MLA, 64 heads |
| Vocabulary | 160K |
| Parameters | 1.04T total, 32.6B active |

With the library built and the student designed, the expensive part can begin. Part 2 follows the training run
itself: 15.5 trillion tokens, thousands of GPUs, and the small trick that kept it from blowing up.

## Takeaways

- **Two halves:** stages 1–5 make a base model that predicts text; stages 6–9 make it an assistant.
- **Data is the product.** Filtering, deduplication and a quality classifier matter more than raw size.
- **Rephrasing beats repeating:** ten rewrites read once beat the same text read ten times.
- **Tokens are a design choice:** a bigger vocabulary means shorter inputs but a bigger model to train.
- **MoE buys knowledge cheaply:** 1.04 trillion parameters stored, 32.6 billion used per token.

## Keywords

| Term | What it means |
|---|---|
| **LLM** | Large language model: a network trained on huge amounts of text to predict the next token. |
| **Token** | A piece of text (a word, part of a word, a symbol) from a fixed list. |
| **Vocabulary** | The fixed list of tokens a model knows; 160K for K2. |
| **BPE** | Byte pair encoding: builds the vocabulary by repeatedly merging the most common pair of pieces. |
| **Parameter / weight** | One of the numbers inside the network that training adjusts. |
| **Common Crawl** | A free, public crawl of the web, the starting point of most training data. |
| **Deduplication** | Removing repeated or near-identical documents. |
| **MinHash** | A fast technique to find documents that share most of their phrases. |
| **Quality classifier** | A small model that scores pages so only good ones are kept. |
| **Rephrasing** | Rewriting good documents with an LLM to get more varied training text. |
| **Transformer** | The standard LLM design: layers of attention plus feed-forward networks. |
| **Attention** | How each token looks at earlier tokens to decide what matters. |
| **Layer** | One block of attention plus feed-forward network; models stack dozens. |
| **Dense model** | A model where every parameter works on every token. |
| **Mixture-of-Experts (MoE)** | Many specialist sub-networks; a router uses only a few per token. |
| **Active parameters** | The parameters actually used for one token (32.6B in K2). |
| **Sparsity** | Total experts divided by experts used; 48 for K2. |
| **KV cache** | The model's memory of earlier tokens while generating. |
| **MLA** | Multi-head Latent Attention: compresses the KV cache. |
| **Base model** | The model after pre-training: good at continuing text, not yet an assistant. |

## References

- [Kimi K2: Open Agentic Intelligence](https://arxiv.org/abs/2507.20534): Kimi Team, Moonshot AI (arXiv, v2); data domains, rephrasing and its SimpleQA results, architecture and design choices
- [Kimi-K2-Instruct model card](https://huggingface.co/moonshotai/Kimi-K2-Instruct): Moonshot AI on Hugging Face; vocabulary size
- [The FineWeb Datasets](https://arxiv.org/abs/2406.17557): Penedo et al., Hugging Face (arXiv); the open web-data pipeline (filters, MinHash deduplication) and the FineWeb-Edu classifier
- [Training Compute-Optimal Large Language Models](https://arxiv.org/abs/2203.15556): Hoffmann et al., DeepMind (arXiv); scaling data with model size (Chinchilla)
- [Neural Machine Translation of Rare Words with Subword Units](https://arxiv.org/abs/1508.07909): Sennrich et al. (arXiv); byte pair encoding for subwords
- [Attention Is All You Need](https://arxiv.org/abs/1706.03762): Vaswani et al. (arXiv); the transformer
- [DeepSeek-V2](https://arxiv.org/abs/2405.04434): DeepSeek-AI (arXiv); Multi-head Latent Attention and the 93.3% KV-cache reduction
- [Moonshot's Kimi K3 pushes Chinese AI into Fable-level territory](https://fortune.com/2026/07/16/moonshots-kimi-k3-pushes-chinese-ai-into-fable-level-territory/): Fortune, 16 July 2026; K3's release and reported size

Related: [Language Model]({{< relref "/posts/language-model" >}}) and
[AI in practice, part 3: tokens and tokenomics]({{< relref "/posts/ai-in-practice-3-tokens-and-tokenomics" >}}).
