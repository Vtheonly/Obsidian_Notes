---
tags: [framework, semantic-kernel, agents, microsoft, multi-language, planning]
iteration: 10
created: 2026-08-08
aliases: [Semantic Kernel, SK, Microsoft Semantic Kernel]
---

# 15 — Semantic Kernel

> [!info] TL;DR
> Semantic Kernel (SK) is Microsoft's open-source agent orchestration SDK. Its distinctive feature is **first-class multi-language parity** — the same kernel, plugins, and planners run on Python, .NET, and Java — which makes it the natural choice for enterprises whose production stack mixes C# services, Java backends, and Python ML code. SK's other signature idea is **planners**: you register a set of "plugins" (functions exposed as semantic prompts or native code) and a planner LLM assembles them into a multi-step execution plan at runtime. This is a more declarative cousin of ReAct. Best for **enterprise integrations** where multi-language support, plugin reuse across teams, and integration with Microsoft 365 / Azure OpenAI matter more than cutting-edge research patterns.

## Overview

- **Developer**: Microsoft (originally 2023, stable 1.x releases from 2024).
- **Languages**: Python, .NET (C#), Java — feature parity across all three.
- **License**: MIT.
- **Status**: actively developed, GA in production at Microsoft (Copilot Stack, Microsoft 365 Copilot, Dynamics 365). Stable API since 1.0.

## Why Semantic Kernel Exists

Most agent frameworks are Python-first, treating other languages as second-class. Enterprise customers — banks, healthcare, government — often have C# / Java backends they cannot easily migrate. Before SK, teams in those environments either (a) ran a Python microservice alongside their C# stack, or (b) reimplemented agent logic in C# by hand. Both are painful.

SK addresses this by treating the kernel + plugins + planner as a language-agnostic core, with idiomatic bindings for each host language. The same plugin (e.g., "search the web", "summarize an email") can be authored once in C# and consumed by a Python agent, or vice versa. The kernel's design is also heavily influenced by Microsoft's internal needs: Copilot products require durable planning, enterprise auth, telemetry hooks, and integration with Microsoft Graph, Azure OpenAI, and 365 workloads — all of which are first-class in SK.

## Core Concepts

### Kernel

The kernel is the central orchestrator that holds services and plugins:

```python
from semantic_kernel import Kernel
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion

kernel = Kernel()
kernel.add_service(AzureChatCompletion(
    deployment_name="gpt-4o",
    endpoint="https://my-aoai.openai.azure.com",
    api_key="...",
))
```

The kernel is intentionally lightweight — it's a service locator + plugin registry, not a heavy runtime. You can construct one per request, share one across requests, or persist one per user session.

### Plugins

A plugin is a collection of functions. Functions come in two flavors:

1. **Semantic functions** — prompts written in SK's `prompt.yaml` / `skprompt.txt` format. The prompt template can contain `{{$input}}`, `{{$style}}` style variables that SK fills in.
2. **Native functions** — regular Python / C# / Java methods decorated with `@kernel_function`, with type hints converted to a JSON schema the LLM sees.

```python
from semantic_kernel.functions import kernel_function

class WebSearchPlugin:
    @kernel_function(description="Search the web and return top results", name="search")
    def search(self, query: str, max_results: int = 5) -> list[dict]:
        return web_search_api(query, limit=max_results)

kernel.add_plugin(WebSearchPlugin(), plugin_name="web")

class SummaryPlugin:
    @kernel_function(description="Summarize a long document into 3 bullet points")
    def summarize(self, document: str) -> str:
        return kernel.invoke_function_with_prompt(
            f"Summarize this into 3 bullets:\n{document}"
        )

kernel.add_plugin(SummaryPlugin(), plugin_name="summary")
```

The function's docstring / description is what the planner LLM sees when deciding which function to call. Type hints become the JSON schema for arguments.

### Planners

The planner is SK's distinctive feature. Given a user ask, the planner LLM inspects the available plugin functions and produces an execution plan — a sequence (or DAG) of function calls. Three planners ship with SK:

- **FunctionCallingStepwisePlanner** — uses the model's native tool-calling API (OpenAI function calling). Modern default. Best when the model supports function calling natively.
- **HandlebarsPlanner** — generates a Handlebars template that orchestrates the functions. Good for deterministic flows where you want to inspect the plan before executing.
- **SequentialPlanner** (legacy) — generates XML step lists. Original 2023 planner; still works but deprecated in favor of the above.

```python
from semantic_kernel.planners import FunctionCallingStepwisePlanner

planner = FunctionCallingStepwisePlanner(service_id="azure_openai")
result = await planner.invoke(kernel, "Find recent papers on Mamba-2 and summarize the top one.")
print(result.final_answer)
```

Under the hood, the planner issues a tool-calling loop: the LLM picks a function, SK executes it, the result goes back to the LLM, repeat until the LLM produces a final answer or hits a step budget.

### Memory and Filters

SK has a `memory` abstraction (semantic memory — store facts as embeddings, recall by similarity) and a `filters` system (hook into the function-invocation pipeline for logging, redaction, retry). These are the production-grade hooks that distinguish SK from research frameworks.

## Multi-Language Parity — The Real Differentiator

The same plugin written in C# can be invoked from Python by registering it as an HTTP endpoint, and vice versa. In practice, teams split work along language lines: ML engineers build the semantic functions and embedding pipelines in Python; application engineers compose them into business workflows in C#. The kernel protocol is identical on both sides.

This is what makes SK uniquely valuable in Microsoft-stack enterprises. LangChain, LangGraph, AutoGen, CrewAI, PydanticAI are all Python-only (or Python-first with limited bindings). SK is the only framework where a C# team can adopt agentic patterns without leaving their language.

## Worked Example: A Research Assistant

```python
import asyncio
from semantic_kernel import Kernel
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion
from semantic_kernel.functions import kernel_function
from semantic_kernel.planners import FunctionCallingStepwisePlanner

class ResearchPlugin:
    @kernel_function(description="Search arXiv for papers matching the query.")
    def search_arxiv(self, query: str, max_results: int = 5) -> list[dict]:
        # Calls arxiv API; returns [{title, abstract, url}, ...]
        return arxiv_api(query, limit=max_results)

    @kernel_function(description="Download and extract the full text of an arXiv paper by URL.")
    def fetch_paper_text(self, url: str) -> str:
        return download_and_extract(url)

    @kernel_function(description="Summarize paper text into 5 key findings.")
    def summarize_findings(self, text: str) -> str:
        # Calls the LLM through the kernel to summarize.
        return asyncio.run(kernel.invoke_function_with_prompt(
            f"List the 5 key findings from this paper:\n{text[:8000]}"
        )).value

async def main():
    kernel = Kernel()
    kernel.add_service(AzureChatCompletion("gpt-4o", endpoint=..., api_key=...))
    kernel.add_plugin(ResearchPlugin(), plugin_name="research")

    planner = FunctionCallingStepwisePlanner(service_id="azure_openai")
    result = await planner.invoke(
        kernel,
        "Find recent papers on Mamba-2 and summarize the top result's key findings."
    )
    print(result.final_answer)

asyncio.run(main())
```

The planner decides: call `search_arxiv("Mamba-2")` → call `fetch_paper_text(top_url)` → call `summarize_findings(text)` → produce final answer. No hand-written orchestration.

## Comparison with Other Frameworks

| Aspect                  | Semantic Kernel           | LangGraph              | AutoGen               | PydanticAI            |
|-------------------------|---------------------------|------------------------|-----------------------|-----------------------|
| Languages               | Python / C# / Java        | Python only            | Python / .NET (early) | Python only           |
| Core abstraction        | Kernel + plugins + planner | Graph + state         | Conversational agents | Agent + tools + types |
| Orchestration style     | LLM-as-planner (declarative) | Explicit graph (deterministic) | Multi-agent conversation | Single-agent loop |
| Type safety             | Native-function type hints | Python types           | Weak (stringly-typed) | Strong (Pydantic)     |
| Microsoft integration   | First-class (Azure OpenAI, MS Graph, 365) | None                 | None                  | None                  |
| Best for                | Enterprise C#/.NET stack  | Production Python agents | Research multi-agent  | Type-safe Python agents |
| Learning curve          | Moderate                  | Steep                  | Moderate              | Low                   |
| Production maturity     | GA at Microsoft scale     | GA (LangChain Inc.)    | Active research       | Newer, growing        |

## When to Choose Semantic Kernel

- **Enterprise C# / Java stack**: SK is the only viable option if your production code is C# or Java and you cannot easily run a Python service alongside.
- **Microsoft ecosystem**: heavy use of Azure OpenAI, Microsoft Graph, Microsoft 365 Copilot extensions, or Dynamics 365 — SK is the integration story Microsoft supports.
- **Cross-language plugin reuse**: a single plugin library used by both Python ML services and C# application services.
- **Compliance-heavy environments**: SK's telemetry, auth, and filter hooks are designed for enterprises that need audit trails and policy enforcement.

## When NOT to Choose Semantic Kernel

- **Pure Python shop**: LangGraph or PydanticAI will be more idiomatic and have a larger Python community.
- **Cutting-edge research patterns**: SK lags behind LangGraph and AutoGen for novel multi-agent patterns (e.g., swarm, debate, society of mind).
- **Small prototypes**: SK's planner overhead is overkill for single-tool prompts; just use OpenAI SDK directly.
- **Non-Microsoft LLMs**: SK supports OpenAI, Azure OpenAI, HuggingFace, Ollama, and Google Gemini, but the polish and feature lag are visibly Microsoft-prioritized.

## Production Patterns

### Plugin design

Write plugins that do **one thing** and have clear docstrings. The planner LLM relies entirely on the description to decide when to invoke a function. Vague descriptions ("process data") cause the planner to misuse the function; precise descriptions ("search arXiv for papers matching the query and return title, abstract, url") enable correct planning.

### Step budgets

Always set `max_iterations` on the planner. Without a budget, a confused LLM can loop indefinitely, burning tokens. Typical: 10–20 steps for research tasks, 3–5 for simple lookups.

### Telemetry hooks

Use SK's filter system to log every function invocation (name, args, result, latency) to OpenTelemetry. This is essential for debugging planner behavior and for cost attribution in multi-tenant deployments.

### Human-in-the-loop

For high-stakes actions (sending email, modifying data), wrap the function in a confirmation filter that pauses execution and asks the user to approve. SK's filter pipeline makes this a few lines of code.

## Common Pitfalls

- **Trusting the planner too much** — the LLM will sometimes hallucinate function arguments or call functions in the wrong order. Always validate inputs in native functions and set step budgets.
- **Vague plugin descriptions** — the planner can only use functions it understands. Spend time on docstrings; they're the API for the LLM.
- **Mixing Python and C# plugins naively** — the languages interop via HTTP/gRPC, not magically. Design the network boundary deliberately.
- **Forgetting to register plugins** — a common SK bug: define a plugin class but forget `kernel.add_plugin(...)`. The planner can't see unregistered functions.
- **Using legacy planners** — `SequentialPlanner` and `ActionPlanner` are deprecated. Use `FunctionCallingStepwisePlanner` or `HandlebarsPlanner`.

## Further Reading

- Microsoft, *Semantic Kernel Documentation* — https://learn.microsoft.com/semantic-kernel/
- Microsoft, *Semantic Kernel GitHub* — https://github.com/microsoft/semantic-kernel
- Microsoft, *Plan in Semantic Kernel* — planner design and tradeoffs.
- Wang et al. (2023), *Microsoft 365 Copilot architecture* — how SK is used at scale.

## Connection to Other Concepts

- [[25 - Frameworks and Tools/Agent Frameworks/01 - Framework Selection Guide|Framework Selection Guide]] — when SK is the right choice.
- [[25 - Frameworks and Tools/Agent Frameworks/03 - LangGraph|LangGraph]] — explicit-graph alternative.
- [[25 - Frameworks and Tools/Agent Frameworks/09 - AutoGen|AutoGen]] — multi-agent alternative (also Microsoft Research, different goals).
- [[25 - Frameworks and Tools/Agent Frameworks/11 - PydanticAI|PydanticAI]] — type-safe Python alternative.
- [[15 - AI Agents/Planning/07 - Planner-Executor Pattern|Planner-Executor Pattern]] — SK's planner is an instance of this pattern.
- [[15 - AI Agents/Tool Calling/04 - Function Calling|Function Calling]] — SK's `FunctionCallingStepwisePlanner` wraps native function calling.
- [[15 - AI Agents/Autonomy/09 - Human-in-the-Loop Patterns|Human-in-the-Loop Patterns]] — SK filters enable HiTL.
- [[19 - MCP/Architecture/01 - MCP Overview|MCP Overview]] — SK can act as an MCP client consuming MCP servers as plugins.

## Interview Questions

1. **Q: What is Semantic Kernel's distinctive feature compared to LangGraph or AutoGen?**
   A: First-class multi-language parity. The same kernel, plugins, and planners run on Python, .NET (C#), and Java with feature parity. This makes SK the natural choice for enterprises whose production stack mixes C# services, Java backends, and Python ML code — those teams previously had to either run a Python sidecar or hand-roll agent logic in C#. SK is also the integration story Microsoft supports for Copilot extensions, Microsoft Graph, and Azure OpenAI.

2. **Q: Explain the planner concept in Semantic Kernel. How does it differ from a hand-written ReAct loop?**
   A: SK's planner is an LLM that inspects the registered plugin functions (via their docstrings / descriptions) and produces a multi-step execution plan to satisfy a user ask. The planner then executes that plan by calling functions in sequence, feeding each result back to the LLM. The difference from ReAct: ReAct interleaves reasoning and action at every step ("think → act → observe → think"), while SK's planner produces an upfront plan (especially `HandlebarsPlanner`) and then executes it. `FunctionCallingStepwisePlanner` is closer to ReAct — it uses the model's native tool-calling API to interleave reasoning and calls. The advantage of the planner pattern is that the plan can be inspected, validated, or modified before execution — useful for compliance.

3. **Q: When would you NOT use Semantic Kernel?**
   A: Four cases. (1) Pure Python shop — LangGraph or PydanticAI are more idiomatic. (2) Cutting-edge multi-agent research patterns — SK lags LangGraph and AutoGen for novel patterns like swarm, debate, society of mind. (3) Small prototypes with single-tool prompts — the planner overhead is overkill; just use OpenAI SDK directly. (4) Non-Microsoft LLMs — SK supports OpenAI, Azure OpenAI, HuggingFace, Ollama, Google Gemini, but the polish is visibly Microsoft-prioritized.

4. **Q: What is the difference between a semantic function and a native function in SK?**
   A: A semantic function is a prompt written in SK's prompt format (YAML config + text template with `{{$variables}}`). When invoked, SK fills in the variables and calls the LLM with the resulting prompt. A native function is a regular Python/C#/Java method decorated with `@kernel_function`; its type hints become the JSON schema the LLM sees, and its docstring becomes the description. Semantic functions wrap LLM calls; native functions wrap arbitrary code (API calls, database queries, computations). Both are first-class plugin citizens — the planner treats them identically.

5. **Q: How does SK handle multi-tenant production deployment?**
   A: The kernel is lightweight — you can construct one per request, share one across requests, or persist one per user session. For multi-tenancy, the typical pattern is: per-request kernel construction (cheap), per-tenant plugin configuration (e.g., different search indexes, different LLM deployments), per-tenant auth via the filter pipeline, and per-tenant telemetry/cost attribution via OpenTelemetry tags. SK's filter system is the key hook — it intercepts every function invocation, letting you enforce tenant-scoped permissions, log usage, and inject tenant context.

6. **Q: How does SK integrate with MCP?**
   A: SK can act as an MCP client, consuming MCP servers as plugins. Each MCP tool exposed by a server becomes an SK native function callable by the planner. This is the bridge between SK's enterprise planner model and the open MCP ecosystem — you can mix SK-authored plugins with MCP-sourced plugins (e.g., a Slack MCP server, a GitHub MCP server) in the same kernel, and the planner treats them uniformly.

## See Also

- [[25 - Frameworks and Tools/MOC|Frameworks and Tools MOC]]
- [[25 - Frameworks and Tools/Agent Frameworks/01 - Framework Selection Guide|Framework Selection Guide]]
- [[25 - Frameworks and Tools/Agent Frameworks/03 - LangGraph|LangGraph]]
- [[25 - Frameworks and Tools/Agent Frameworks/09 - AutoGen|AutoGen]]
- [[25 - Frameworks and Tools/Agent Frameworks/11 - PydanticAI|PydanticAI]]
- [[15 - AI Agents/Planning/07 - Planner-Executor Pattern|Planner-Executor Pattern]]
- [[15 - AI Agents/Tool Calling/04 - Function Calling|Function Calling]]
- [[19 - MCP/Architecture/01 - MCP Overview|MCP Overview]]
