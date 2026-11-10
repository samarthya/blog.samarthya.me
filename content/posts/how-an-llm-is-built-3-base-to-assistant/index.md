---
title: "How an LLM is built, part 3: from base model to assistant"
date: 2026-11-10T10:43:00-05:00
description: "How a base model becomes an assistant that answers, uses tools and behaves: supervised fine-tuning, Kimi K2's synthetic agent data, reinforcement learning with verifiable and rubric rewards, evaluation, open-weight release and serving, and what each stage looks like at our own scale."
featureimage: "feature.png"
categories: ["technical"]
tags: ["ai", "llm", "ml", "agents", "tools"]
series: ["How an LLM is built"]
series_order: 3
draft: false
---

{{< lead >}}
A base model is a well-read graduate with no job experience: it knows a lot, but ask it a question and it may
reply with another question. Post-training is the apprenticeship. First it watches good work, then it does the
work itself and gets graded, until it is reliable enough to be let loose.
{{< /lead >}}

![Post-training Kimi K2 in four stages: supervised fine-tuning (demonstrations, and agent conversations built from 3,000+ real and 20,000+ synthetic tools, filtered by an LLM judge), reinforcement learning (a loop of try, grade, update, with verifiable rewards from 10,000+ sandboxes and self-critique rubric rewards, plus guard rails: token budget, PTX loss, temperature decay), evaluation (SWE-bench Verified 65.8, LiveCodeBench 53.7, GPQA-Diamond 75.1, AIME 2025 49.5) and release (base and instruct weights in block-FP8, about 1 TB, modified MIT licence).](overview.svg "From a base model to an assistant you can download")

{{< alert "circle-info" >}}
New terms are explained in plain words in
[Keywords](/posts/how-an-llm-is-built-3-base-to-assistant/#keywords) at the end.
{{< /alert >}}

[Part 1]({{< relref "/posts/how-an-llm-is-built-1-data-and-design" >}}) built the data and the design, and
[part 2]({{< relref "/posts/how-an-llm-is-built-2-pre-training" >}}) trained **Kimi-K2-Base** on 15.5 trillion
tokens. This part turns it into **Kimi-K2-Instruct**, the model people actually chat with, following the
[Kimi K2 technical report](https://arxiv.org/abs/2507.20534).

## The recipe in one picture

The [InstructGPT paper](https://arxiv.org/abs/2203.02155) set the pattern most models still follow:

1. **Show it**: fine-tune on demonstrations of the behaviour you want.
2. **Grade it**: collect judgments of which answers are better.
3. **Practise**: use reinforcement learning to make the better answers more likely.

Its headline result explains why this stage matters: people preferred the answers of a **1.3B** model trained this
way over the raw **175B** GPT-3, a model a hundred times larger. Post-training is a small fraction of the compute,
but it decides how the model behaves.

## Stage 6: supervised fine-tuning (SFT)

### What a training example looks like

Fine-tuning uses the same next-token objective as pre-training (part 2), but on **conversations** written in a
fixed format, the *chat template*, with roles marked:

```json
{"messages": [
  {"role": "system",    "content": "You are a helpful assistant."},
  {"role": "user",      "content": "How do I list the pods in the my-app namespace?"},
  {"role": "assistant", "content": "kubectl get pods -n my-app"}
]}
```

The model learns to produce the assistant's turn given everything before it. SFT data is tiny next to the
trillions of pre-training tokens, and it still changes the model's habits, because the knowledge is already
there: SFT teaches the format and the manners.

K2's examples came from earlier Kimi models and in-house expert models, and each response was checked by LLM or
human judges before it was kept. The report also notes that SFT used the same Muon optimiser as pre-training.

### Teaching it to use tools, at scale

The most interesting part of K2's SFT is **tool use**. Hand-writing thousands of conversations in which an agent
plans, calls tools, reads results and recovers from errors is slow, so Moonshot built a pipeline to synthesise
them:

1. **Collect tools.** 3,000+ real MCP tools from GitHub (MCP is the tool protocol from
   [AI in practice, part 5]({{< relref "/posts/ai-in-practice-5-mcp" >}})), plus **20,000+ synthetic tools**
   evolved from them to cover more domains.
2. **Create agents.** Thousands of them, each with its own system prompt and a different set of tools.
3. **Write tasks with rubrics.** Every task comes with an explicit description of what success looks like.
4. **Play it out.** The agent works on the task with an LLM playing the user (each with its own persona and
   style) and a tool simulator that executes the calls and keeps track of state, like a small model of the world.
   For coding, real sandboxes run real code.
5. **Keep only the good runs.** An LLM judge checks each conversation against its rubric and keeps those that
   succeed.

The output is tens of thousands of worked examples, and it is a big part of why K2 is strong at agent tasks.

## Stage 7: reinforcement learning (RL)

### Why copying is not enough

SFT can only teach what the examples show. **Reinforcement learning** lets the model try for itself: it writes
several answers, each is scored by a **reward**, and training makes the higher-scoring answers more likely. The
model can then discover approaches nobody wrote down. The whole difficulty is the reward: whatever you score is
what you get.

### Two kinds of grader

| Reward | How it scores | Used for |
|---|---|---|
| **Verifiable** | A program checks the answer | Maths and logic answers, following format instructions, code that must pass tests, faithfulness to sources, safety |
| **Self-critique rubric** | The model compares pairs of its own answers against written rubrics | Helpfulness, clarity, style: anything no program can check |

The verifiable side needs serious infrastructure: K2's coding setup runs **more than 10,000 sandboxes at once**.
The rubric side uses three layers of rules: core values, prescriptive rules written to stop reward hacking (one
says a response "must not begin with compliments directed at the user or the question", so no "Good question!"),
and guidance written by people. The critic itself is kept honest: during RL it is refined with the verifiable
signals, where the right answer is known.

### Guard rails against gaming the grader

Left alone, RL finds shortcuts. K2 adds three guard rails:

| Risk | Guard rail |
|---|---|
| Answers grow longer and longer because length farms reward | A **token budget** per task; anything over it is cut off and penalised |
| The model forgets what it learnt before | An extra loss on hand-picked high-quality data (**PTX loss**) mixed into every step |
| It settles on one way of answering too early | **Temperature decay**: varied, exploratory answers at first, more focused ones later |

### Keeping the loop fast

RL alternates between *generating* answers and *training* on them, so weights move back and forth constantly.
K2's **checkpoint engine** pushes new weights to the generation workers in **under 30 seconds**, and very long
attempts are paused and resumed in the next round instead of holding everyone up.

## Stage 8: evaluation, did it work?

Benchmarks are imperfect, but they are how models are compared and how teams find weaknesses. A few of
K2-Instruct's published scores, all without long step-by-step "thinking":

| Benchmark | What it tests | K2-Instruct |
|---|---|---|
| SWE-bench Verified | Fixing real GitHub issues as an agent | 65.8 (single attempt), 71.6 (multiple) |
| LiveCodeBench v6 | Competitive programming | 53.7 |
| GPQA-Diamond | Graduate-level science questions | 75.1 |
| AIME 2025 | A maths competition | 49.5 |
| ACEBench | Tool use | 76.5 |

People's votes matter too: on the LMSYS Arena leaderboard of 17 July 2025, K2 ranked first among open models and
fifth overall, from more than 3,000 votes.

The report is just as useful for what it admits. On hard reasoning or unclear tool definitions, K2 can produce too
many tokens or get cut off, and it sometimes reaches for tools it does not need. A good model card tells you
where it breaks.

## Stage 9: release and serving

### What was published

Moonshot released both **Kimi-K2-Base** and **Kimi-K2-Instruct** on
[Hugging Face](https://huggingface.co/moonshotai/Kimi-K2-Instruct). The weights are stored in **block-FP8**, about
one byte per parameter, so roughly a **terabyte** for the full model, with a 128K-token context. The model card
recommends a temperature of 0.6 and lists four serving engines: vLLM, SGLang, KTransformers and TensorRT-LLM.

The [licence](https://huggingface.co/moonshotai/Kimi-K2-Instruct/blob/main/LICENSE) is a modified MIT. You can use,
change and sell it, with one condition: a commercial product with more than 100 million monthly active users, or
more than 20 million US dollars in monthly revenue, must show "Kimi K2" prominently in its interface.

### What it takes to run

| Item | Rough size |
|---|---|
| Weights (1.04T parameters × 1 byte) | about 1 TB |
| Memory per 80 GB GPU | so at least 13 GPUs for the weights alone, before the KV cache |
| Work per token | 32.6B active parameters, like a mid-size dense model |

MoE is cheap to *compute* but expensive to *hold*: the whole terabyte must sit in memory even though only 3% of it
works on each token. That is why open-weight giants are mostly run by cloud providers and by teams with a GPU
cluster, while the rest of us use them through an API.

### The next step: Kimi K2 Thinking

The later [Kimi-K2-Thinking](https://huggingface.co/moonshotai/Kimi-K2-Thinking) shows where post-training went
next. It reasons step by step between tool calls, keeps tool use stable across **200–300 sequential calls**, and
reads up to **256K tokens**. It was also trained to work with **INT4** weights (*quantisation-aware training*),
which the card says roughly doubles generation speed, and all its benchmark scores are reported at that precision.

## What this means at our scale

Very few teams will ever pre-train a model like this. But every stage of this series has a small version that an
ordinary engineering team can use:

| Stage | Your version |
|---|---|
| Data (part 1) | Clean, deduplicated documents for retrieval ([RAG]({{< relref "/posts/building-a-practical-retrieval-augmented-personal-assistant-rag" >}})) |
| Pre-training (part 2) | Usually skip it: start from an open base or instruct model |
| Fine-tuning | **LoRA** adapters on an open model: [LoRA](https://arxiv.org/abs/2106.09685) trains small add-on matrices, cutting trainable parameters by up to 10,000× |
| Reinforcement learning | Graders and rubrics to compare prompts and models automatically |
| Evaluation | Your own test set of real questions; it matters more than any leaderboard |
| Release and serving | Run an open model locally with [Ollama]({{< relref "/posts/ollama-revolutionizing-language-models" >}}) or vLLM |

## Takeaways

- **Post-training sets the behaviour.** A 1.3B model with it beat a 175B model without it.
- **SFT teaches format and manners;** the knowledge is already there from pre-training.
- **Agent skill can be synthesised:** 23,000+ tools, thousands of agents, and a judge that keeps only the
  successful runs.
- **Rewards decide what you get.** Verifiable checks where possible, rubrics where not, and guard rails against
  gaming them.
- **Open weights are a terabyte:** cheap per token, expensive to hold. The small versions of each stage are the
  ones most of us will use.

## Keywords

| Term | What it means |
|---|---|
| **Post-training** | Everything after pre-training that turns a base model into an assistant. |
| **SFT** | Supervised fine-tuning: training on example conversations. |
| **Chat template** | The fixed format that marks system, user and assistant turns. |
| **Instruct model** | A model after post-training, ready to follow instructions. |
| **MCP** | Model Context Protocol: a standard way for models to use tools. |
| **Synthetic data** | Training examples generated by models rather than written by people. |
| **LLM judge** | A model used to grade other models' outputs. |
| **Rubric** | A written description of what a good answer must do. |
| **Reinforcement learning (RL)** | The model tries, gets a score, and is pushed towards higher scores. |
| **Reward** | The score for one attempt. |
| **Verifiable reward** | A reward a program can compute, such as "the tests pass". |
| **Sandbox** | An isolated environment where generated code can run safely. |
| **Token budget** | A cap on answer length during RL. |
| **PTX loss** | An extra loss on good pre-training-style data that stops the model forgetting. |
| **Temperature** | How random sampling is: higher means more varied answers. |
| **Benchmark** | A standard test set used to compare models. |
| **Open weights** | The trained parameters are downloadable, so anyone can run the model. |
| **Block-FP8 / INT4** | Number formats with 8 or 4 bits per weight; smaller and faster than 16-bit. |
| **Quantisation-aware training** | Training a model to keep its quality when run at low precision. |
| **LoRA** | Low-rank adaptation: fine-tuning a few small add-on matrices instead of the whole model. |

## References

- [Kimi K2: Open Agentic Intelligence](https://arxiv.org/abs/2507.20534): Kimi Team, Moonshot AI (arXiv, v2); SFT data, the agentic tool-use pipeline, the RL framework (verifiable and self-critique rewards, budget control, PTX loss, temperature decay), RL infrastructure, benchmark results and limitations
- [Kimi-K2-Instruct model card](https://huggingface.co/moonshotai/Kimi-K2-Instruct): Moonshot AI on Hugging Face; released checkpoints, block-FP8 weights, 128K context, serving engines, recommended temperature
- [Kimi K2 licence](https://huggingface.co/moonshotai/Kimi-K2-Instruct/blob/main/LICENSE): Moonshot AI; the modified MIT condition
- [Kimi-K2-Thinking model card](https://huggingface.co/moonshotai/Kimi-K2-Thinking): Moonshot AI on Hugging Face; INT4 quantisation-aware training, 256K context, 200–300 sequential tool calls
- [Training language models to follow instructions with human feedback](https://arxiv.org/abs/2203.02155): Ouyang et al., OpenAI (arXiv); the three-step recipe and the 1.3B vs 175B result
- [LoRA: Low-Rank Adaptation of Large Language Models](https://arxiv.org/abs/2106.09685): Hu et al. (arXiv); low-rank adapters and the 10,000× reduction in trainable parameters

Related: [AI in practice, part 4: from RAG to tools and agents]({{< relref "/posts/ai-in-practice-4-tools-and-agents" >}}).
