---
title: "How an LLM is built, part 2: pre-training, months of guessing the next word"
date: 2026-11-10T09:43:00-05:00
description: "What actually happens in LLM pre-training: the next-token objective, a training loop you can run, the compute bill, the optimiser trick (MuonClip) that kept Kimi K2's 15.5-trillion-token run stable, how a 1-trillion-parameter model is split across GPUs, and how the context grows to 128K."
featureimage: "feature.png"
categories: ["technical"]
tags: ["ai", "llm", "ml", "gpu", "python"]
series: ["How an LLM is built"]
series_order: 2
draft: false
---

{{< lead >}}
Pre-training is a guessing game played trillions of times. Cover the next word, guess it, check, adjust a little.
Nothing in it is clever on its own; what makes it hard is doing it 15.5 trillion times without the whole thing
falling over.
{{< /lead >}}

![Pre-training Kimi K2: a loop of four steps (read a batch of 67M tokens, guess every next token, measure the loss, update the weights with MuonClip) repeated over 15.5 trillion tokens; a learning-rate curve that warms up, holds at 2e-4 for 10T tokens and decays to 2e-5; a GPU grid split three ways (16-way pipeline, 16-way expert, data parallel); and a context bar growing from 4K to 32K to 128K tokens.](overview.svg "One loop, repeated 15.5 trillion tokens")

{{< alert "circle-info" >}}
New terms are explained in plain words in [Keywords](/posts/how-an-llm-is-built-2-pre-training/#keywords) at the
end.
{{< /alert >}}

[Part 1]({{< relref "/posts/how-an-llm-is-built-1-data-and-design" >}}) built the library (15.5 trillion tokens)
and designed the student (a 1.04-trillion-parameter Mixture-of-Experts). This part is the training run that
connects them, again following the [Kimi K2 technical report](https://arxiv.org/abs/2507.20534).

## The one job: predict the next token

Take a piece of training text, say "the cat sat on the mat". At every position the model sees only what came
before and must guess what comes next:

| The model sees | It should guess |
|---|---|
| the | cat |
| the cat | sat |
| the cat sat | on |
| the cat sat on | the |
| the cat sat on the | mat |

One sentence gives five guesses, and a batch of text gives millions, all scored at once. The score is the
**loss**: how surprised the model was by the real next token (technically the cross-entropy, the negative log of
the probability it gave the right answer). A model that gave "mat" 90% has a small loss; one that gave it 1% has a
large one.

Training then works out, for every weight, which direction would have made the loss smaller (the **gradient**,
computed by *backpropagation*) and moves each weight a tiny step that way. That is one **training step**:

1. **Read** a batch of text.
2. **Guess** every next token (the *forward pass*).
3. **Score** the guesses (the loss).
4. **Adjust** every weight a little (the *backward pass* and the *optimiser step*).

There is no step where anyone teaches the model grammar, facts or code. All of that emerges because it helps the
next guess.

## A pre-training run on your laptop

Here is the whole idea at toy scale: a one-layer transformer that learns my blog's motto from scratch. It has the
same four steps as K2, with about 10,000 parameters instead of a trillion.

```python
# pip install torch          (runs on a CPU in a few seconds)
import torch, torch.nn as nn, torch.nn.functional as F

torch.manual_seed(0)
text = "fall. get up. build again. " * 50              # the "library"
chars = sorted(set(text))                               # the "tokenizer": one token per character
data = torch.tensor([chars.index(c) for c in text])
V, CTX = len(chars), 8                                  # vocabulary size, context length

class TinyLM(nn.Module):
    def __init__(self, d=32):
        super().__init__()
        self.tok = nn.Embedding(V, d)                   # token -> vector
        self.pos = nn.Embedding(CTX, d)                 # position -> vector
        self.att = nn.MultiheadAttention(d, 2, batch_first=True)
        self.ff = nn.Sequential(nn.Linear(d, 64), nn.ReLU(), nn.Linear(64, d))
        self.out = nn.Linear(d, V)                      # vector -> a score for every token

    def forward(self, x):
        T = x.shape[1]
        h = self.tok(x) + self.pos(torch.arange(T))
        no_peeking = torch.triu(torch.ones(T, T, dtype=torch.bool), 1)
        h = h + self.att(h, h, h, attn_mask=no_peeking)[0]   # look back, never ahead
        h = h + self.ff(h)
        return self.out(h)

model = TinyLM()
opt = torch.optim.AdamW(model.parameters(), lr=3e-3)
for step in range(301):
    starts = torch.randint(0, len(data) - CTX - 1, (32,))                 # 1. read a batch
    x = torch.stack([data[s:s + CTX] for s in starts])
    y = torch.stack([data[s + 1:s + CTX + 1] for s in starts])            #    (the answers: shifted by one)
    loss = F.cross_entropy(model(x).reshape(-1, V), y.reshape(-1))        # 2. guess, 3. score
    opt.zero_grad(); loss.backward(); opt.step()                          # 4. adjust
    if step % 100 == 0:
        print(f"step {step:3}  loss {loss.item():.3f}")

x, out = data[:CTX].unsqueeze(0), ""                    # now let it write
for _ in range(40):
    nxt = model(x[:, -CTX:])[0, -1].softmax(-1).multinomial(1)
    x = torch.cat([x, nxt.unsqueeze(0)], dim=1)
    out += chars[nxt.item()]
print(out)
```

On my machine (PyTorch 2.15, CPU) it prints:

```text
step   0  loss 2.958
step 100  loss 0.122
step 200  loss 0.094
step 300  loss 0.125
t up. build again. fall. get up. build a
```

The loss falls from about 3 (pure guessing among 14 characters) to about 0.1, and the model writes the motto
back. It has memorised one sentence rather than learnt language, which is exactly why real runs need trillions of
*different* tokens (part 1).

## The bill: how much compute

A common estimate from [Kaplan et al.](https://arxiv.org/abs/2001.08361) is that training takes about
`C ≈ 6 × N × D` floating-point operations, for N parameters and D training tokens (roughly 2 for the forward pass
and 4 for the backward pass, per parameter per token).

For K2, N is the **active** parameters, because only those work on each token:

| | N (parameters) | D (tokens) | C ≈ 6ND |
|---|---|---|---|
| K2 as built (MoE) | 32.6 billion active | 15.5 trillion | **≈ 3 × 10²⁴** operations |
| If it were dense | 1.04 trillion | 15.5 trillion | ≈ 9.7 × 10²⁵ operations |

The MoE design makes the same knowledge about 32 times cheaper to train. Even so, 3 × 10²⁴ is enormous: at
an effective 400 trillion operations per second per GPU, it would take one GPU about 240 years, which is why the
run needs thousands of them working together.

## The optimiser, and the run that never spiked

The **optimiser** is the rule that turns gradients into weight updates. Almost every LLM uses **AdamW**, which
adapts the step size for each weight. Moonshot had shown in [an earlier paper](https://arxiv.org/abs/2502.16982)
that **Muon**, an optimiser that orthogonalises each update matrix (so no single direction dominates the step),
reaches the same loss with about half the compute.

Half the compute on a run this size is worth a great deal, but Muon brought a problem at K2's scale. In attention,
each token's *query* is compared with every earlier token's *key*, and the result (an **attention logit**) decides
how much attention that token gets. In a smaller test run (9B active, 53B total parameters), these logits grew
past **1,000**. Logits that large make attention brittle, and the run is heading for a **loss spike**: a sudden
jump in loss that can wreck days of training and force a rollback to an earlier checkpoint.

Moonshot's fix, **QK-Clip**, is a small safety valve:

1. After each optimiser step, look at each attention head's largest logit in the batch.
2. If it is above a threshold **τ = 100**, scale that head's query and key weights down by just enough to bring
   it back to 100.
3. Leave every other head alone.

Muon plus QK-Clip is **MuonClip**. The report shows the full 15.5-trillion-token run with **zero loss spikes**;
the clip was active early on and stopped being needed as training settled. Clipping weights *after* the update,
rather than changing the model, is why it could be bolted on without redesigning anything.

## The schedule

The **learning rate** sets how big each step is. Too big and training is unstable; too small and it crawls. K2's
schedule:

| Phase | Tokens | Learning rate |
|---|---|---|
| Warm-up | first 500 steps | rising from 0 to 2e-4 |
| Hold | first 10 trillion | constant 2e-4 |
| Decay | next 5.5 trillion | cosine decay to 2e-5 |
| Anneal | 400 billion (4K) + 60 billion (32K) | 2e-5 down to 7e-6 |

Each step reads a **batch of 67 million tokens**, so 15.5 trillion tokens is roughly 230,000 steps. Holding the
rate steady for most of the run, then decaying it, is called a *warmup-stable-decay* schedule; the long flat part
lets a team change plans (more data, a different mix) without restarting.

## The machines: splitting a trillion parameters

K2 trained on **NVIDIA H800 GPUs**, eight per machine (*node*), connected inside a node by NVLink and between
nodes by 8 × 400 Gbps networking. One GPU has tens of gigabytes of memory; the model's parameters and gradients
alone need about **6 TB**. So the model is split three ways at once:

| Split | What each GPU gets | Analogy | K2 |
|---|---|---|---|
| **Pipeline parallelism** | A slice of the layers | An assembly line: each station does a few layers and passes the work on | 16-way |
| **Expert parallelism** | A share of the 384 experts | Cooks spread across several kitchens; tokens are sent to whoever has their expert | 16-way |
| **Data parallelism** (ZeRO-1) | The same job on a different batch, with optimiser state shared out | Several identical teams, each on different text, comparing notes after each step | the rest |

Spread over 256 GPUs, the 6 TB of parameters and gradients leaves about **30 GB per GPU** for everything else,
mainly the *activations* (the intermediate results of the forward pass, kept for the backward pass). K2 squeezes
those three ways: it **recomputes** cheap ones instead of storing them, stores some in **FP8** (8-bit numbers),
and moves the rest to the node's 2 TB of CPU memory while they are not needed.

## Long context: from a page to a book

Attention cost grows with the square of the input length, so most of the run uses short **4,096-token** windows.
Only at the end does the model learn long inputs:

1. **Anneal** at 4K on 400 billion tokens, with the learning rate falling further, typically on the
   highest-quality data.
2. Continue at **32K** tokens for 60 billion tokens.
3. Stretch to **128K** with **YaRN**, which rescales the model's position encoding so it can handle positions it
   never saw. [YaRN's paper](https://arxiv.org/abs/2309.00071) reports it needs 10× fewer tokens and 2.5× fewer
   steps than earlier methods.

## What comes out: a base model

The result is **Kimi-K2-Base**, which Moonshot also [released](https://huggingface.co/moonshotai/Kimi-K2-Instruct).
It knows an enormous amount and continues any text fluently. But it is not an assistant: ask it "How do I restart
a pod?" and it may answer, or it may continue with three more questions, as if it were reading a forum thread.
Part 3 covers how it is taught to answer, use tools and behave.

## Takeaways

- **One objective:** predict the next token. Grammar, facts and code all emerge from it.
- **Compute is roughly 6 × parameters × tokens**, and MoE counts only the active parameters: about 3 × 10²⁴
  operations for K2 instead of nearly 10²⁶.
- **Stability is the real engineering.** QK-Clip, a per-head clip at τ = 100, kept a 15.5-trillion-token run free
  of loss spikes.
- **A trillion parameters do not fit anywhere,** so the model is split by layers, by experts and by data at once.
- **Long context comes last,** in short, cheap extensions from 4K to 128K.

## Keywords

| Term | What it means |
|---|---|
| **Pre-training** | The long first training stage on general text, producing a base model. |
| **Next-token prediction** | The training task: guess the next token from the ones before it. |
| **Loss (cross-entropy)** | How surprised the model was by the real next token; training makes it smaller. |
| **Gradient** | For each weight, the direction that would reduce the loss. |
| **Backpropagation** | The method that computes all gradients in one backward pass. |
| **Training step** | One round of read, guess, score, adjust. |
| **Batch** | The text processed in one step; 67 million tokens for K2. |
| **FLOP** | One floating-point operation; training compute is counted in them. |
| **Optimiser** | The rule that turns gradients into weight updates (AdamW, Muon). |
| **Muon** | An optimiser that orthogonalises each update matrix; about 2× more efficient than AdamW in Moonshot's tests. |
| **Attention logit** | The raw score of how much one token attends to another. |
| **QK-Clip / MuonClip** | Scaling a head's query and key weights down when its largest logit passes 100; Muon plus this clip. |
| **Loss spike** | A sudden jump in loss that can derail a run. |
| **Checkpoint** | A saved copy of the model's weights to resume or roll back to. |
| **Learning rate** | How big each update step is. |
| **Warmup-stable-decay** | A schedule that ramps up, holds steady, then decays. |
| **Node** | One machine, here with eight GPUs. |
| **Pipeline / expert / data parallelism** | Splitting the work by layers, by experts, or by batches. |
| **ZeRO-1** | A data-parallel method that shares the optimiser's memory across GPUs instead of copying it. |
| **Activations** | Intermediate results of the forward pass, kept for the backward pass. |
| **FP8** | An 8-bit number format: half the memory of 16-bit. |
| **Annealing** | Lowering the learning rate at the end, usually on the best data. |
| **YaRN** | A method to extend the context window by rescaling position encoding. |
| **Base model** | The pre-trained model: fluent at continuing text, not yet an assistant. |

## References

- [Kimi K2: Open Agentic Intelligence](https://arxiv.org/abs/2507.20534): Kimi Team, Moonshot AI (arXiv, v2); QK-Clip and MuonClip, the logit growth in the 9B/53B test run, τ = 100, the spike-free loss curve, the learning-rate schedule, batch size, context extension, H800 cluster, parallelism and memory figures
- [Muon is Scalable for LLM Training](https://arxiv.org/abs/2502.16982): Moonshot AI (arXiv); Muon and its roughly 2× compute efficiency over AdamW
- [Scaling Laws for Neural Language Models](https://arxiv.org/abs/2001.08361): Kaplan et al., OpenAI (arXiv); the `C ≈ 6NBS` training-compute estimate
- [YaRN: Efficient Context Window Extension of Large Language Models](https://arxiv.org/abs/2309.00071): Peng et al. (arXiv); context extension with 10× fewer tokens and 2.5× fewer steps
- [Kimi-K2-Instruct model card](https://huggingface.co/moonshotai/Kimi-K2-Instruct): Moonshot AI on Hugging Face; the released Base and Instruct checkpoints

Related: [from matrix multiplication to GPUs]({{< relref "/posts/matrix-multiplication-to-gpus" >}}).
