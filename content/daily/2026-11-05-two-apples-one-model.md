---
title: "Two apples, one model"
date: 2026-11-05T19:33:00-05:00
slug: "two-apples-one-model"
description: "A day of running the same 30B coding model through Ollama and Colibri, on my desktop and on my Linux server."
categories: ["daily"]
tags: ["ai", "llm", "ollama", "colibri"]
---

Spent the day comparing two ways of running a model locally: Ollama, which I know, and Colibri, which I installed
last night. Same model on both, Qwen3-Coder 30B.

- **Fell:** the 19 GB Colibri download stalled overnight, and the Ollama one stalled at the very end and started
  again from 2%. My desktop ran out of memory twice with both tools and a browser open.
- **Got up:** moved the test to my Linux server. The model arrived in five minutes there, and the engine built
  in 25 seconds.
- **Learned:** on the same machine the two were close, about 10 tokens a second each. On my busy desktop one
  Colibri flag, `--cap 128`, made it 4.5 times faster.

Wrote it up: [Ollama or Colibri? A beginner's comparison]({{< relref "/posts/ollama-vs-colibri-beginners-guide" >}}).
Next: point a coding agent at Colibri and see whether it keeps up.
