---
title: "Ollama or Colibri? A beginner's comparison on two of my machines"
date: 2026-11-04T21:21:17-05:00
description: "Two ways to run AI models on your own machine, tested with the same 30B model on a Linux server and a Windows desktop: what each is for, how to start, what I measured and which to try first."
categories: ["technical"]
tags: ["ai", "llm", "ollama", "colibri","experiment"]
featureimage: "feature.png"
draft: false
---

{{< lead >}}
A Fuji and a Granny Smith are both apples, and you would still not bake with the one you snack on. Ollama and
Colibri both run AI models on your own machine, but they were bred for different jobs.
{{< /lead >}}

![An anime orchard keeper holds up a glossy red apple in one hand and a crisp green apple in the other, looking unsure which to choose](overview.svg "Both apples. Not the same apple.")

I have used [Ollama]({{< relref "/posts/ollama-revolutionizing-language-models" >}}) for a while, and even
[built a small demo on it]({{< relref "/posts/building-a-minimal-langchain-ollama-demo" >}}). Colibri is new to me:
I installed it this week. So this is a comparison by someone who knows one tool well and is a beginner at the
other, which is probably where you are too.

## First, four words you will keep meeting

- **Inference engine:** the program that loads a model's weights and produces text from them. Both tools are one.
- **Quantisation:** storing weights at lower precision so they take less space. `int4` and `Q4` both mean about four
  bits per weight, against sixteen in the original release.
- **Tokens per second (tok/s):** how fast the answer appears. A token is roughly a word fragment; I covered them in
  [my post on tokens]({{< relref "/posts/ai-in-practice-3-tokens-and-tokenomics" >}}). Around 10 tok/s is fine for
  chat; below 1 tok/s, you go and make tea.
- **Mixture of experts (MoE):** a model built from many small sub-networks, called experts, where each token uses
  only a few. This one idea is why Colibri exists.

## Two varieties

**Ollama is the eating apple**: pleasant straight away, with nothing to prepare. You name a model, it downloads and
you chat. Its [README](https://github.com/ollama/ollama) lists llama.cpp as its supported backend, and it hides nearly
every decision behind sensible defaults.

**Colibri is the specialist.** The [project](https://github.com/JustVugg/colibri) describes itself as "tiny engine,
immense model". A mixture-of-experts model of hundreds of billions of parameters uses only a small part of itself for
each token, so Colibri keeps that part in RAM and reads the remaining experts from disk when the model asks for them.
It behaves like a library that keeps the popular books on the front desk and fetches the rest from the basement.

The author's own figures show the trade: GLM-5.2, with 744 billion parameters and a 429 GB download, needs only
16 to 24 GB of RAM, but it [manages 0.05 to 0.1 tok/s cold on a 25 GB laptop](https://github.com/JustVugg/colibri).
That is a model you could never otherwise load on such a machine, at a speed you would not want for a conversation.

| | Ollama | Colibri |
|---|---|---|
| Built for | Easy everyday local models | Very large MoE models on ordinary hardware |
| Version I used | 0.40.14 | 2.1.0 |
| Licence | [MIT](https://github.com/ollama/ollama) | [Apache 2.0](https://github.com/JustVugg/colibri) |
| Get a model | `ollama pull <name>` | `coli setup --model <id>`, or import a GGUF file |
| Default API port | [11434](https://docs.ollama.com/quickstart) | [8000](https://github.com/JustVugg/colibri) |
| OpenAI-style API | Yes, [a subset](https://docs.ollama.com/quickstart) | Yes |
| My integrated GPU | Skipped unless enabled | Supported through [Vulkan](https://github.com/JustVugg/colibri) |

## Getting started

**Ollama on Windows**, using the [official installer script](https://github.com/ollama/ollama). On macOS or Linux, use
`curl -fsSL https://ollama.com/install.sh | sh` instead.

```powershell
irm https://ollama.com/install.ps1 | iex
ollama run qwen3.5:0.8b
```

I would start with something this small: a 1 GB model tells you the setup works without an evening of downloading.
Type `/bye` to leave.

**Colibri on Windows**, per its [README](https://github.com/JustVugg/colibri): download the ZIP, unzip it and
double-click `START-HERE.bat`. On Linux or macOS:

```bash
git clone https://github.com/JustVugg/colibri
cd colibri
./start-here.sh --list    # compare the models against this machine
./start-here.sh
```

The setup checks your hardware, recommends a model, fetches the engine, downloads the model with resume support and
starts a server with a dashboard. On my machine it fetched the prebuilt 2.1.0 Windows engine and was downloading the
model in under a minute. I did not need a compiler.

Then came the wait. The smallest language model in Colibri's setup list is
[about 19 GB](https://github.com/JustVugg/colibri). At home that took most of a night: the setup estimated an hour and
three quarters, then the download sat still for several hours before finishing in the morning. I never found out why.
On my Linux server the same 19 GB came straight from Hugging Face in five minutes. Ollama's smallest models let you
be chatting in minutes either way. That difference is the first thing a beginner feels, and it is by design, since
Colibri exists for large models.

On Linux there is one extra step, building the engine, and it was painless: `make qwen36` finished in 25 seconds.

## What I measured

Both tools can run the same model, [Qwen3-Coder 30B](https://ollama.com/library/qwen3-coder), at 19 GB each, in
4-bit form (`Q4_K_M` in Ollama, `int4` in Colibri). It has 30 billion parameters and uses about 3.3 billion per token.
That makes it the closest thing to an apples-to-apples test I can run.

**How I measured.** One small Python client talked to each tool through the same OpenAI-style API, with the same
prompts, temperature 0 and a 200-token answer:

- **Decode speed:** a short coding prompt, run three times while warm; I report the median.
- **First word:** how long until the first token arrives, warm, for that short prompt and for a 518-token prompt.
- **Cold start:** the very first request after the server starts, which includes loading the model.
- Every prompt began with a run number, so neither tool could answer from a cache.

I used two machines:

| | Linux server | Windows desktop |
|---|---|---|
| CPU | Intel Core i7-8665U, 4 cores, 8 threads (2019, laptop-class) | AMD Ryzen 9 7940HS, 8 cores, 16 threads |
| RAM | 31 GB | 28 GB |
| GPU | none used | integrated Radeon 780M |
| Versions | Ollama 0.17.7, Colibri 2.1.0 | Ollama 0.40.14, Colibri 2.1.0 |

### Same model, same machine: the Linux server

| Qwen3-Coder 30B | Ollama | Colibri, default | Colibri, `--cap 128` |
|---|---|---|---|
| Decode speed, warm | **10.7 tok/s** | 10.1 tok/s | 7.6 tok/s |
| First word, warm | 2.4 s | **1.9 s** | 2.2 s |
| First word, 518-token prompt | 26.1 s | **20.7 s** | 27.9 s |
| Cold start, first word | **12.1 s** | 11.4 s, plus 5 s for the server | 16.6 s, plus 6 s for the server |
| Peak memory | 19.0 GB | **14.5 GB** | 16.0 GB |

On the same hardware the two are close: Ollama decodes about 6% faster, Colibri reads a long prompt about a fifth
faster and uses about 4.5 GB less memory. The answers were nearly identical too. Asked for a script that totals a CSV
of orders by customer, both wrote almost the same 25 lines, and both scripts ran correctly against my test file: they
skipped the bad row with a warning and exited with status 1 when the file was missing.

The surprise was the last column. Colibri's own
[model card](https://huggingface.co/Justvugg/Qwen3-Coder-30B-A3B-colibri-int4) says that without `--cap` the engine
"starts at the routing floor of 8 per layer and runs about three times slower", so I expected `--cap 128`, which keeps
all 128 experts of each layer in RAM, to win. On this server it was a quarter slower than the default. I ran each
configuration once, in that order, on a laptop-class CPU that may have been warmer by then, so I would not read much
into it, except that the default was already fine here.

### The same Colibri on my desktop

On my desktop the story was different. These numbers came from a busy machine, with Chrome and VS Code open, which
is exactly how many beginners will first try it:

| Colibri, Qwen3-Coder 30B, Windows | Decode speed, warm | First word, warm | First word, 518-token prompt | Peak memory |
|---|---|---|---|---|
| As the setup started it (Vulkan, automatic plan) | 3.1 tok/s | 11.4 s | 15.8 s | 11.5 GB |
| CPU only, `--cap 128` | **14.0 tok/s** | **0.9 s** | **8.4 s** | 16.0 GB |
| Vulkan on the iGPU, `--cap 128` | 10.7 tok/s | 2.6 s | not finished | not recorded |

Three things stood out:

1. **The default plan seems to follow free memory.** With my apps open, `coli plan` reported a RAM budget of only 3.4 GB
   and "0% projected expert residency", meaning nearly every expert would come from disk. The setup's server decoded
   at 3.1 tok/s. Telling it to keep every expert in RAM made it **4.5 times faster**, and the fastest result in this
   whole post. The model card's warning was right on this machine.
2. **The integrated GPU did not help.** Colibri's README reports the
   [Radeon 780M](https://github.com/JustVugg/colibri) lifting a sibling model from 6.0 to 9.9 tok/s. With this model,
   the CPU alone was faster. The iGPU shares system RAM, and my Vulkan run that tried to keep every expert in RAM ran
   the machine out of memory before it finished.
3. **Memory is the real limit.** Each tool wants 15 to 19 GB for this model, so on a 28 to 32 GB machine you run one
   at a time and close the browser. When I tried otherwise, things stalled and Windows started paging.

I could not finish the Ollama side on the desktop: its 19 GB download stalled, and restarting it began again from 2%.
For a sense of Ollama's speed there, here are the models I already had, timed with Ollama's own counters while the
Colibri download was running:

| Ollama model, Windows | Size on disk | Load, cold | Decode speed, warm | Memory in use |
|---|---|---|---|---|
| `qwen3.5:0.8b` | 1.0 GB | 2.7 s | 48.6 tok/s | 1.5 GB |
| `llama3.1:8b` | 4.9 GB | 7.8 s | 11.4 tok/s | 9.5 GB |
| `codellama:7b` | 3.8 GB | 7.2 s | 14.1 tok/s | 12.7 GB |
| `gpt-oss:20b` | 13.8 GB | 19.0 s | 13.9 tok/s | 14.1 GB |

`gpt-oss:20b` has more than twice the parameters of `llama3.1:8b` and runs faster, a useful warning that parameter
count alone does not predict speed.

**Ollama and the integrated GPU.** Ollama skipped my GPU without being asked. Its log says so plainly:

```text
dropping integrated GPU; to enable, set OLLAMA_IGPU_ENABLE=1
```

If `ollama ps` shows [`100% CPU`](https://docs.ollama.com/faq), this may be why. The
[GPU documentation](https://docs.ollama.com/gpu) does not confirm integrated Radeon support on Windows, so treat the
variable as an experiment. I tried it on a separate port: `llama3.1:8b` went from 11.4 to **15.0 tok/s**, with the
whole 5.3 GB in GPU memory. One model and one run is not a verdict, but on this machine it was worth trying:

```powershell
$env:OLLAMA_IGPU_ENABLE = "1"
ollama serve
```

## One thing they share: the API

You do not have to commit. Both speak the OpenAI-style chat API, so an application can switch between them by changing
the address and the model name. I ran this against Ollama:

```bash
curl http://localhost:11434/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "qwen3.5:0.8b",
    "messages": [{"role": "user", "content": "Name one apple variety."}]
  }'
```

For Colibri, the [same request](https://github.com/JustVugg/colibri) goes to `http://127.0.0.1:8000/v1/chat/completions`.
Its [Qwen3-Coder documentation](https://github.com/JustVugg/colibri/blob/main/docs/qwen36.md) gives the model id as
`qwen3-coder-30b-a3b-colibri`.

## Beginner traps

| Trap | Which tool | What to do |
|---|---|---|
| An empty answer, because a thinking model spends its tokens on reasoning first. `qwen3.5:0.8b` used 1,170 tokens to name one apple, and with `max_tokens` at 40 the reply had no content at all | Ollama | Leave room in `max_tokens`, and read the `reasoning` field when debugging |
| Long documents get cut off, because the [default context is 4,096 tokens](https://docs.ollama.com/faq) on my setup | Ollama | Raise `num_ctx`, or set `OLLAMA_CONTEXT_LENGTH` |
| The first answer after a break is slow, because [models unload after 5 minutes](https://docs.ollama.com/faq) | Ollama | Set `keep_alive` to hold it in memory |
| About three times slower than expected, because the [engine starts with only 8 experts per layer](https://huggingface.co/Justvugg/Qwen3-Coder-30B-A3B-colibri-int4) | Colibri | Pass `--cap`: `--cap 128` holds every expert in RAM, `--cap 32` suits 16 GB |
| Large models crawl, because [the disk sets the speed](https://github.com/JustVugg/colibri) | Colibri | Keep models on a fast NVMe drive, and check free space first |
| `coli stop` is "not recognised" after the one-click Windows setup, because `coli` is not on your PATH | Colibri | Run it from the checkout: `c\coli.cmd stop`, or press Ctrl+C in the `START-HERE.bat` window |
| The dashboard is not at port 8000 | Colibri | My setup chose 8001. `coli status` prints the real address |
| Two models at once, or one model plus a busy browser | Both | On 32 GB, run one 19 GB model at a time and close what you can |
| Trusting anyone's benchmark, including mine | Both | Run your own prompt on your own machine |

## Which should you try first?

| If you... | Start with |
|---|---|
| have never run a model locally | **Ollama** |
| have under 25 GB of disk to spare | **Ollama** |
| want quick answers from a small model | **Ollama** |
| want to try a model far larger than your RAM, and can wait for it | **Colibri** |
| are simply curious how MoE models work | **Colibri**: `coli plan` shows where the model lives |

My suggestion is to start with Ollama, because it answers "does this work on my machine?" in minutes. Move to Colibri
when you hit a real wall, not before.

## Takeaways

- Both run models privately on your own machine, but Ollama optimises for ease and Colibri for model size.
- With the same 30B model on the same machine they were close: Ollama decoded about 6% faster, Colibri read long prompts faster and used about 4.5 GB less memory.
- Colibri's automatic plan appears to size itself to the memory that is free. On my busy desktop, `--cap 128` made it 4.5 times faster; on my quiet server, the default was already best.
- Check where your model actually runs: Ollama skipped my integrated GPU by default, and `ollama ps` shows the split.
- The shared API makes this a low-stakes choice, since switching later is mostly a new address and model name.

## References

- [ollama/ollama](https://github.com/ollama/ollama): GitHub, install commands, llama.cpp backend, MIT licence
- [Ollama quickstart](https://docs.ollama.com/quickstart): Ollama docs, commands, port 11434, API styles and their limits
- [Ollama FAQ](https://docs.ollama.com/faq): Ollama docs, context length, keep-alive, `ollama ps`, local privacy
- [Ollama hardware support](https://docs.ollama.com/gpu): Ollama docs, AMD and Vulkan support on Windows
- [qwen3-coder](https://ollama.com/library/qwen3-coder): Ollama library, the 30b tag, size and active parameters
- [JustVugg/colibri](https://github.com/JustVugg/colibri): GitHub, how Colibri works, setup, commands, API, requirements, the author's benchmarks, licence
- [Colibri Qwen3.6 family documentation](https://github.com/JustVugg/colibri/blob/main/docs/qwen36.md): GitHub, Qwen3-Coder architecture, `--cap` and the API model id
- [Qwen3-Coder-30B-A3B for Colibri](https://huggingface.co/Justvugg/Qwen3-Coder-30B-A3B-colibri-int4): Hugging Face, model card with size, memory and speed figures
- Title image: hand-drawn SVG made for this post.
