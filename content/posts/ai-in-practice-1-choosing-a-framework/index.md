---
title: "AI in practice, part 1: Choosing the right framework"
date: 2026-10-26T18:00:00-04:00
description: "PyTorch, Hugging Face, scikit-learn, LangChain, vector stores, Ollama, MLflow: what each layer of the AI stack does, and how to pick the right tool for the job."
categories: ["technical"]
tags: ["ai", "ml", "llm", "python", "frameworks"]
series: ["AI in practice"]
series_order: 1
draft: false
---

{{< lead >}}
"Which AI framework should I use?" has no single answer, because the names people throw around do
completely different jobs. Put them on a map first, and the choice usually makes itself.
{{< /lead >}}

This series picks up where my earlier posts left off. Those covered the ideas: [what generative AI
is](/posts/genai/), [how transformers pay attention](/posts/language-model/), [why GPUs matter](/posts/matrix-multiplication-to-gpus/),
and two hands-on builds ([LangChain with Ollama](/posts/building-a-minimal-langchain-ollama-demo/) and a
[RAG assistant](/posts/building-a-practical-retrieval-augmented-personal-assistant-rag/)). This part is the map
that connects them.

## The stack, bottom to top

| Layer | What it does | Names you'll meet |
|---|---|---|
| **Hardware** | Does the arithmetic: mostly matrix multiplication | GPUs (CUDA), TPUs, Apple silicon |
| **Tensor frameworks** | Tensors, automatic gradients, training loops | PyTorch, TensorFlow/Keras, JAX |
| **Classic ML** | Models that aren't neural networks, and the data work around them | scikit-learn, pandas, PySpark |
| **Model libraries** | Ready-made architectures and pretrained weights | Hugging Face Transformers, Datasets, Tokenizers, PEFT |
| **Serving / runtimes** | Run a trained model and answer requests | Ollama, llama.cpp, vLLM, managed APIs |
| **Orchestration** | Chain prompts, retrieval and tools into an application | LangChain/LangGraph, LlamaIndex |
| **Retrieval** | Store embeddings and find similar text | Chroma, FAISS, pgvector |
| **MLOps / platforms** | Pipelines, tracking, registries, deployment | MLflow, Kubeflow, Vertex AI |

Most confusion comes from comparing tools on different rows. "LangChain or PyTorch?" is like asking "Flask or
the Linux kernel?": you will often use both, at different layers.

## Tensor frameworks: where models are built

**PyTorch** is the default for research and for most open-weight language models. Code reads like ordinary
Python, and debugging works the way you expect. **TensorFlow** with **Keras** remains common in older production
systems; Keras 3 can also run on top of PyTorch or JAX. **JAX** is NumPy with automatic differentiation and a
compiler, popular in research and on Google's TPUs.

If you are not training or fine-tuning models yourself, you may never write code at this layer, but it is
underneath everything above it.

## Classic ML: still the right tool surprisingly often

Not every problem needs a neural network. [K-nearest neighbours](/posts/k-nearest-neighbors/),
[linear regression](/posts/the-core-divide/), [TF-IDF](/posts/mastering-tf-idf-a-gamified-journey/) and
[forecasting models](/posts/forecasting-methods/) live in **scikit-learn** and friends. They train in seconds,
explain themselves, and run anywhere. Data preparation sits here too: **pandas** on one machine,
**PySpark** when the data outgrows it (I compared the two [here](/posts/pyspark-vs-pandas-choosing-right/)).

## Model libraries: standing on shoulders

**Hugging Face Transformers** gives you thousands of pretrained models behind a common interface: download a
model, tokenize text, run it. **Datasets** and **Tokenizers** handle the data side, and **PEFT** makes
fine-tuning affordable by training small adapter layers instead of the whole model.

## Serving: making a model answer

Two very different options:

- **Run it yourself.** [Ollama](/posts/ollama-revolutionizing-language-models/) and llama.cpp make local models
  easy on a laptop; vLLM serves them efficiently to many users on GPU servers. You pay for hardware, not per
  token, and your data never leaves your machine.
- **Call a managed API.** Hosted models (Claude, GPT, Gemini and others) are the most capable and need no
  hardware, but you pay per token. [Part 3](/posts/ai-in-practice-3-tokens-and-tokenomics/) is about exactly that bill.

## Orchestration and retrieval: from model to application

A model alone just completes text. Applications need prompts kept in files, retrieved documents, memory,
tools and error handling. **LangChain** (and **LangGraph** for multi-step flows) and **LlamaIndex** (strongest
on document retrieval) provide those pieces. **Vector stores** such as Chroma, FAISS or pgvector hold embeddings
so you can find the passages relevant to a question: the "R" in RAG.

A word of caution from building with them: these frameworks change quickly. Keep your own code thin around
them, and pin versions.

## MLOps: making it repeatable

Once a model matters, you need to know which data and code produced it, and to rebuild it on demand.
**MLflow** tracks experiments and models; **Kubeflow Pipelines** describes training as a graph of steps; cloud
platforms such as **Vertex AI** run those pipelines for you. [Part 2](/posts/ai-in-practice-2-vertex-ai-pipelines/)
walks through one.

## Picking, in one table

| You want to… | Start with |
|---|---|
| Classify, cluster or forecast tabular data | scikit-learn (+ pandas or PySpark) |
| Use a pretrained language or vision model | Hugging Face Transformers |
| Train or fine-tune a neural network | PyTorch (+ PEFT for fine-tuning) |
| Chat with a model privately on your laptop | Ollama |
| Build a chatbot over your own documents | LangChain or LlamaIndex + a vector store |
| Give a model access to tools and data | MCP ([part 5](/posts/ai-in-practice-5-mcp/)) |
| Retrain and deploy on a schedule | Kubeflow Pipelines / Vertex AI Pipelines + a model registry |

## Takeaways

- **Name the layer before you compare tools.** Most "X vs Y" debates compare different rows of the stack.
- **Prefer boring tools where they fit.** scikit-learn beats a neural network on many small, tabular problems.
- **Keep framework glue thin.** The model and your data last longer than any orchestration library's API.

## Further reading

- [PyTorch](https://pytorch.org/) · [scikit-learn](https://scikit-learn.org/) · [Hugging Face Transformers](https://huggingface.co/docs/transformers)
- The whole AI shelf on this site: [AI on this blog: a reading map](/posts/ai-reading-map/)

Next: [part 2](/posts/ai-in-practice-2-vertex-ai-pipelines/), ML pipelines on Google Vertex AI.
