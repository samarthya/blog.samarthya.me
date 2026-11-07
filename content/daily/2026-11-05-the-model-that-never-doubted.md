---
title: "The model that never doubted"
date: 2026-11-05T21:44:00-05:00
slug: "the-model-that-never-doubted"
description: "I asked a local 30B model to write a blog post and to flag what it was unsure of. It flagged one thing and got 22 wrong."
categories: ["daily"]
tags: ["ai", "llm", "ollama", "colibri"]
draft: false
---

Evening experiment: could the local Qwen3-Coder 30B on my server write a post for this blog?

- **Fell:** Claude Code pointed at Colibri sent a 19,545-token opening request and was still reading it after
  84 minutes. Stopped it. Colibri kept reading anyway.
- **Got up:** sent the same brief as one plain request to Colibri and to Ollama. Both answered in 10 to 14 minutes
  with fluent, well-structured drafts.
- **Learned:** I had told them to mark anything they were unsure of. Between them: one mark, 22 errors, two
  references to pages that do not exist, and one draft that would have broken the site build.

Wrote it up: [Can a local 30B model write my blog?]({{< relref "/posts/can-a-local-model-write-my-blog" >}}),
with the version I trust: [What model weights are]({{< relref "/posts/what-model-weights-are" >}}).
