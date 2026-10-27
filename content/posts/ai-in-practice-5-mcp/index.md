---
title: "AI in practice, part 5: MCP, the Model Context Protocol"
date: 2026-10-26T18:40:00-04:00
description: "What the Model Context Protocol is, how hosts, clients and servers fit together, the tools-resources-prompts building blocks, a minimal Python server, and the security rules that matter."
categories: ["technical"]
tags: ["ai", "llm", "mcp", "agents", "tools", "python"]
series: ["AI in practice"]
series_order: 5
draft: false
---

{{< lead >}}
Before USB, every device needed its own port. Before MCP, every AI application needed its own connector for
every data source. The Model Context Protocol is the common plug.
{{< /lead >}}

## The problem it solves

[Part 4](/posts/ai-in-practice-4-tools-and-agents/) showed how a model uses tools. The catch: each AI
application (a chat app, an IDE assistant, an agent framework) described tools its own way. Connecting M
applications to N data sources meant up to **M × N** custom integrations.

The **Model Context Protocol (MCP)**, published by Anthropic as an open standard in November 2024, defines one
way for AI applications to discover and use external tools and data. Write an MCP server for your system once,
and any MCP-capable application can use it: **M + N** instead of M × N. Other major AI vendors and developer
tools added support during 2025, which is what made it a standard rather than a feature.

## Hosts, clients and servers

| Role | What it is | Example |
|---|---|---|
| **Host** | The AI application the user works in | a desktop chat app, an IDE, an agent |
| **Client** | A connector inside the host, one per server | created by the host for each configured server |
| **Server** | A program that exposes capabilities over MCP | a server for your files, database, tickets or calendar |

Messages are **JSON-RPC 2.0**. A session starts with an `initialize` handshake in which both sides declare what
they support, so older and newer versions can still talk.

**Transports:**

- **stdio:** the host starts the server as a local process and talks over standard input/output. Simple, and
  nothing is exposed on the network.
- **Streamable HTTP:** for remote servers, with OAuth-based authorization so users can grant access without
  handing over passwords.

## The building blocks

Servers offer three kinds of things, distinguished by **who is in control**:

| Primitive | Controlled by | What it is | Example |
|---|---|---|---|
| **Tools** | the model | Functions the model can call | `create_ticket`, `run_query` |
| **Resources** | the application | Data the host can read into context | a file, a database schema, a log |
| **Prompts** | the user | Reusable templates the user picks | "summarise this incident" |

Clients can offer capabilities back to servers too: **sampling** (a server asks the host's model for a
completion), **roots** (which folders or locations the server may work in) and **elicitation** (a server asks
the user for missing information).

## A minimal server in Python

With the official Python SDK, a server is a few decorated functions:

```python
# notes_server.py  (pip install "mcp[cli]")
from pathlib import Path

from mcp.server.fastmcp import FastMCP

NOTES = Path.home() / "notes"
mcp = FastMCP("notes")


@mcp.tool()
def search_notes(term: str) -> list[str]:
    """Return the names of notes that mention the term."""
    return [p.name for p in NOTES.glob("*.md") if term.lower() in p.read_text().lower()]


@mcp.resource("notes://{name}")
def read_note(name: str) -> str:
    """The full text of one note."""
    return (NOTES / name).read_text()


if __name__ == "__main__":
    mcp.run()  # stdio by default
```

The function signature and docstring become the tool's schema and description, which is what the model reads
when deciding to use it. A host is then told how to start the server, typically with a small configuration entry:

```json
{
  "mcpServers": {
    "notes": {"command": "python", "args": ["/path/to/notes_server.py"]}
  }
}
```

From then on, the model in that host can find and read your notes, and the same server works in any other MCP host.

## Security: the rules that matter

MCP makes connecting things easy, which includes connecting the wrong things. The risks are the agent risks
from part 4, now one install away:

- **Treat servers as code you run.** A local server runs with your user's permissions. Install them from sources
  you trust, pin versions, and read what they do.
- **Least privilege.** Expose only what's needed: read-only tools where possible, narrow roots, scoped tokens.
- **Untrusted content is untrusted instructions.** Text returned by a tool or resource (a web page, an email,
  an issue comment) can contain prompt injection. Tool descriptions themselves can be malicious ("tool poisoning").
- **Keep a human in the loop** for anything destructive or outward-facing; good hosts ask before running tools.
- **Don't pass tokens through.** A remote server should use its own properly scoped credentials, not forward
  the user's.

## How MCP connects the series

| Part | Piece of the puzzle |
|---|---|
| [1. Frameworks](/posts/ai-in-practice-1-choosing-a-framework/) | where MCP sits in the stack: next to orchestration |
| [2. Vertex AI pipelines](/posts/ai-in-practice-2-vertex-ai-pipelines/) | the models and the platform behind an application |
| [3. Tokens](/posts/ai-in-practice-3-tokens-and-tokenomics/) | every tool definition and result is paid for in tokens |
| [4. Tools and agents](/posts/ai-in-practice-4-tools-and-agents/) | what MCP standardises |
| 5. MCP | the common plug between AI applications and everything else |

## Takeaways

- MCP is an open protocol that lets any AI application use tools and data from any MCP server.
- Hosts contain clients; clients talk JSON-RPC to servers over stdio or Streamable HTTP.
- Tools are model-controlled, resources application-controlled, prompts user-controlled.
- A server is easy to write and easy to install, so apply least privilege, trust carefully, and keep a human
  in front of irreversible actions.

## Further reading

- [modelcontextprotocol.io](https://modelcontextprotocol.io): the specification and guides
- [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk)

Previous: [part 4, tools and agents](/posts/ai-in-practice-4-tools-and-agents/). All the AI posts in order:
[the reading map](/posts/ai-reading-map/).
