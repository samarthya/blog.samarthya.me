---
title: "Can a local 30B model write my blog? I fact-checked it"
date: 2026-11-05T21:41:00-05:00
description: "I gave one blog brief to Qwen3-Coder 30B running locally through Colibri and Ollama, and through Claude Code as an agent. Timings, every factual error I found, and what I will use local models for."
categories: ["technical"]
tags: ["ai", "llm", "ollama", "colibri"]
featureimage: "feature.png"
draft: false
---

{{< lead >}}
An intern who never says "I'm not sure" needs more checking than one who asks too many questions. I asked a local
model to write a blog post for me, told it to mark anything it was unsure of, and then checked every line.
{{< /lead >}}

![Three attempts at the same brief: the agent run read for 84 minutes and wrote nothing; Colibri wrote 975 words in 10 minutes with 12 errors and no warnings; Ollama wrote 1,153 words in 13.5 minutes with 10 errors, one warning and a page that breaks the site build](overview.svg "Fluent, fast enough, and wrong in a dozen places.")

After [comparing Ollama and Colibri]({{< relref "/posts/ollama-vs-colibri-beginners-guide" >}}) on speed, I
wanted to know whether a local model is good enough for real work. So I picked a job I do every week: writing a
post for this blog. The topic was one I had just covered myself, [what model weights are]({{< relref "/posts/what-model-weights-are" >}}),
so I had a researched, sourced version to check against.

## The setup

Everything ran on my Linux server: a 2019 laptop-class Intel i7-8665U (4 cores, 8 threads) with 31 GB of RAM and
no GPU. The model was Qwen3-Coder 30B in 4-bit form in both engines.

Every attempt got the same brief: the topic, seven points the reader should understand, and my blog's writing
rules (voice, structure, front matter, British spelling, references). Two extra rules for this test:

- You have no internet access. **Mark anything you are not sure of with `[CHECK]`.**
- Mark every reference `[FROM MEMORY]`.

I tried three ways of asking:

1. **An agent:** Claude Code 2.1.72 on the server, pointed at Colibri instead of Anthropic's servers through
   Colibri's [Anthropic-compatible API](https://github.com/JustVugg/colibri/blob/main/docs/api.md), with file
   tools and no web access.
2. **A plain request to Colibri:** one chat message with the rules and the brief, no tools.
3. **The same plain request to Ollama.**

## Attempt 1: the agent never got started

A coding agent does not send just your question. Before my brief, Claude Code sends its own instructions and the
description of every tool it can use. Colibri's health page showed the size of that first request:
**19,545 tokens**, about 37 times my benchmark prompt.

Colibri's documentation warns about exactly this: on the CPU path, an agent's preamble can mean
"[an hour of silent thinking](https://github.com/JustVugg/colibri/blob/main/docs/api.md) before the first output
token". On my server it was worse. After **84 minutes** Colibri was still reading the prompt and had not produced a
single token, so I stopped it.

Two lessons from the attempt that failed:

- **A local agent needs a GPU or a much smaller preamble.** On a CPU, the agent's own instructions cost more than
  the work.
- **Colibri did not notice that I had gone.** When I stopped Claude Code, Colibri kept reading the abandoned
  19,545-token prompt, and the next request would have queued behind it. I had to restart the server.

## Attempts 2 and 3: plain requests

Without an agent the prompt was 2,598 tokens, and both engines finished:

| | Colibri | Ollama |
|---|---|---|
| Time to the first word | 229 s | 271 s |
| Writing speed | 4.3 tokens/s | 3.2 tokens/s |
| Total time | 9.9 minutes | 13.5 minutes |
| Length | 975 words | 1,153 words |
| `[CHECK]` marks | **0** | **1** |

Both drafts read well. They followed the outline, used headings and code blocks, and sounded like a blog post. Then
I checked them line by line against the primary sources from my own post and against the model files on disk.

## What they got wrong

| Error | Colibri | Ollama |
|---|---|---|
| Cites a page that does not exist | Wikipedia "Weight (machine learning)", also linked from the image caption | `llama.cpp/docs/LLM.md` (404) |
| Cites a real paper for the wrong thing | arXiv 1906.02107 as a quantisation paper; it is about binarised networks | |
| Explains the 15 to 19 GB gap as "metadata and overhead" (the real cause: 3.1 GB of 16-bit weights and 1.8 GB of scales; the metadata is 28 KB) | yes | yes |
| Gets the size arithmetic wrong | divides by 1024³ and calls the result GB | |
| Calls Colibri a model; it is an engine | yes | |
| Says each expert lives in its own file; experts are tensors inside 49 shard files | yes | |
| Says weights files store training settings | yes | |
| Says a 30B model has "billions of neurons" (it has billions of parameters) | yes | |
| Says quantised models "often need retraining" (most methods [do not even need a calibration set](https://huggingface.co/docs/transformers/main/en/quantization/overview)) | | yes |
| Calls experts "expert neurons"; they are whole sub-networks | | yes |
| Says open source without open weights is possible; the [OSI definition](https://opensource.org/ai/open-source-ai-definition) requires the weights | yes | yes |
| Misdescribes my own earlier post | yes | |
| Puts the post in one of my series, as a part that does not exist | "AI in practice" part 6 | "Learning OSV" part 4, which already exists |
| Wrong date, and a timezone that hints at a location | yes | yes |
| Uses a shortcode my theme does not have; **the site build fails** | | yes |
| Leaves a placeholder in the image caption | | yes |
| Ignores formatting rules (wraps the file in a code fence, plain links, US spelling) | yes | yes |
| References not marked `[FROM MEMORY]` as asked | | yes |

Twelve substantive errors in one draft and ten in the other, from the same model. The single `[CHECK]` Ollama
placed was on the one number it had been given in the brief.

They were not wrong about everything. Both explained a neuron's weighted sum correctly, said that safetensors avoids
the security problem of pickle files, and described a router picking experts for each token. Ollama's draft got
the 15 GB arithmetic right and described correctly why Colibri can keep experts on disk.

## Why "mark what you're unsure of" did not work

The instruction assumes the model knows where its knowledge ends. It does not. The invented Wikipedia link and
the invented llama.cpp page were written with the same confidence as the correct facts, and the model gave no
sign which was which. A `[CHECK]` mark can only flag doubts the model has, and these errors came with no doubt
attached.

The same model also produced two different drafts from one prompt at temperature 0. The two engines store the
weights differently (Colibri's `int4` and Ollama's `Q4_K_M`), so the numbers inside the model are not identical,
and small differences grow over a thousand words.

## What I will use a local model for

| Job | Local 30B model? |
|---|---|
| A first outline, headings, a structure to react to | Yes |
| Rewording a paragraph I have already checked | Yes |
| Facts, numbers, versions, references | **No**, not without sources to read and a check afterwards |
| An agent loop on a CPU-only machine | No, the preamble alone took over an hour |
| Anything that goes straight to the blog | No: one draft would have broken the build, and both would have published a fake reference |

The version of the weights post I published was researched with web access, checked against the real files on
disk, and every number in it has a source. That took longer than ten minutes, and it is the only version I would
put my name on.

## Takeaways

- A local 30B model writes fluent, well-structured posts in about ten minutes on a CPU, with about one error
  in every hundred words.
- Asking it to flag uncertainty did not work: 22 errors between two drafts, one `[CHECK]` mark.
- Both drafts cited a page that does not exist. Check that every reference opens and says what the text claims.
- Coding agents send a large preamble. On a CPU-only machine with Colibri, that alone took more than 84 minutes.
- Use a local model for structure and wording; take facts only from sources you have read.

## References

- [Colibri API documentation](https://github.com/JustVugg/colibri/blob/main/docs/api.md): GitHub, the Anthropic-compatible endpoint, Claude Code set-up and the warning about agent preambles
- [JustVugg/colibri](https://github.com/JustVugg/colibri): GitHub, the engine used for attempts 1 and 2
- [Ollama](https://github.com/ollama/ollama): GitHub, the engine used for attempt 3
- [Qwen3-Coder-30B-A3B-Instruct](https://huggingface.co/Qwen/Qwen3-Coder-30B-A3B-Instruct): Hugging Face, the model
- [Quantization overview](https://huggingface.co/docs/transformers/main/en/quantization/overview): Hugging Face Transformers, quantisation methods and calibration
- [The Open Source AI Definition 1.0](https://opensource.org/ai/open-source-ai-definition): Open Source Initiative, what open source AI requires
- [arXiv 1906.02107](https://arxiv.org/abs/1906.02107): "Latent Weights Do Not Exist: Rethinking Binarized Neural Network Optimization", the paper one draft cited for something else
- The timings, the error checks and the build test are my own, from the runs described above.
