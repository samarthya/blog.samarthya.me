---
title: "AI in practice, part 4: From RAG to tools and agents"
date: 2026-10-26T18:30:00-04:00
description: "How language models went from answering questions to taking actions: function calling, the agent loop, and the guardrails that keep agents useful and safe."
categories: ["technical"]
tags: ["ai", "llm", "agents", "rag", "tools"]
series: ["AI in practice"]
series_order: 4
draft: false
---

{{< lead >}}
RAG lets a model read what it didn't know. Tools let it do things. An agent is what you get when the model
decides, step by step, which tools to use until the job is done.
{{< /lead >}}

## Three levels of "the model knows something"

1. **Only its training.** The model answers from patterns learned before its cutoff. It can't see your files
   and doesn't know today's date unless you tell it.
2. **Retrieval (RAG).** Your application searches your documents and pastes the relevant passages into the
   prompt. The model reads, then answers. I built one of these
   [here](/posts/building-a-practical-retrieval-augmented-personal-assistant-rag/). The *application* decides what to retrieve.
3. **Tools.** The model itself asks for something to be done: "search the docs for X", "run this query",
   "create the ticket". The *model* decides when and how; your application carries it out.

## Function calling, step by step

With tool use (often called *function calling*), you describe each tool to the model: a name, a description
and a JSON schema for its arguments.

```json
{
  "name": "get_weather",
  "description": "Current weather for a city",
  "input_schema": {
    "type": "object",
    "properties": {"city": {"type": "string"}},
    "required": ["city"]
  }
}
```

Then the conversation goes like this:

| Turn | Who | What |
|---|---|---|
| 1 | User | "Should I take an umbrella in London today?" |
| 2 | Model | Doesn't answer. Returns a tool call: `get_weather({"city": "London"})` |
| 3 | Your code | Runs the real function, sends back the result: `{"rain_chance": 0.8}` |
| 4 | Model | "Yes, there's an 80% chance of rain." |

The model never runs anything itself. It produces a structured request; your code decides whether to run it.
That boundary is where all the safety lives.

## The agent loop

An **agent** is that exchange in a loop: the model plans, calls a tool, reads the result, and decides the next
step until the goal is met or a limit is reached.

```text
goal ──► model ──► tool call? ──yes──► run tool ──► result ──┐
            ▲            │                                     │
            │            no: final answer                      │
            └──────────────────────────────────────────────────┘
```

Each lap is a full model call carrying the growing context, which is why agents can be slow and expensive
([part 3](/posts/ai-in-practice-3-tokens-and-tokenomics/) has the arithmetic).

Frameworks such as LangGraph package this loop with state, memory and retries, but the core is the same few
lines: call the model, run any tools it asks for, append the results, repeat.

## What makes agents work well

- **Few, sharp tools.** Clear names and descriptions matter more than clever prompts; the model chooses tools
  by reading their descriptions.
- **Useful results.** Return what the model needs to decide the next step, including clear error messages it
  can recover from.
- **Hard limits.** Cap the number of steps, the time and the tokens. An agent without a stop condition will
  eventually find a way to spend all three.
- **Logs.** Record every tool call and result. When an agent does something odd, the trace is the only way to see why.

## What makes agents dangerous

An agent acts with whatever permissions its tools have. Two things follow:

- **Least privilege.** A tool that only needs to read shouldn't be able to write. A tool that writes should
  touch as little as possible.
- **Untrusted input steers the model.** Text that comes back from a web page, an email or a document can
  contain instructions ("ignore previous instructions and…"). This is **prompt injection**, and the model can't
  reliably tell your instructions from an attacker's. Keep a human approval step in front of anything
  irreversible: payments, deletions, messages sent on your behalf.

My blog's break-in ([part 1 of that story](/posts/rebuilding-1-the-day-the-blog-fell/)) was about a stolen
password, not AI, but the lesson carries over: whatever can act with your credentials will eventually be
pointed at something you didn't intend. [The Ghost Board](/posts/the-ghost-board/) is my fictional take on
what happens when many agents act without the oversight they assume exists.

## Where this is heading

Every application used to describe its tools in its own way, so every pairing of an AI app and a data source
needed custom glue. [Part 5](/posts/ai-in-practice-5-mcp/) covers the open standard that fixes that: the
Model Context Protocol.

## Takeaways

- RAG: the application fetches context. Tools: the model asks for actions. Agents: the model loops over tools.
- The model only *requests* actions; your code decides what actually runs.
- Few clear tools, hard limits, full logs, least privilege, and a human in front of anything irreversible.

Previous: [part 3, tokens and tokenomics](/posts/ai-in-practice-3-tokens-and-tokenomics/). Next:
[part 5](/posts/ai-in-practice-5-mcp/), MCP.
