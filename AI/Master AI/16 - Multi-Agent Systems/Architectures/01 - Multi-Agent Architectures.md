---
tags: [multi-agent, architectures, langgraph, autogen, crewai]
iteration: 8
created: 2026-08-07
last_updated: 2026-08-08
aliases: [Multi-Agent Architectures]
---

# 01 - Multi-Agent Architectures

> [!info] TL;DR
> Multi-agent systems coordinate multiple LLM-based agents to solve tasks. Common patterns: hierarchical (planner + workers), swarm (peer agents), blackboard (shared state), marketplace (bidding). Frameworks: LangGraph, AutoGen, CrewAI, PydanticAI. Higher capability, higher cost, harder to debug.

## Why Multi-Agent?

Single-agent systems hit limits on complex tasks:
- One agent can't be expert at everything.
- Context windows fill up; the agent "forgets" earlier parts.
- Sequential single-agent is slow.

Multi-agent addresses these:
- **Specialization**: each agent handles a sub-task it's good at.
- **Parallelism**: independent sub-tasks run in parallel.
- **Modularity**: easier to debug and improve individual agents.
- **Discussion / verification**: agents can critique each other.

Tradeoff: multi-agent is more complex to build, harder to debug, and costs more (multiple LLM calls per step).

## Common Patterns

### 1. Hierarchical (Planner-Executor)
```
[Planner Agent] → [Plan: step1, step2, step3]
                      ↓
[Executor Agent] → [Step 1 result]
                      ↓
[Executor Agent] → [Step 2 result]
                      ↓
[Executor Agent] → [Step 3 result]
```

The planner decomposes; the executor carries out each step. Optionally, a third "synthesizer" combines results.

Used by: ReWOO, Plan-and-Execute, LangGraph's planner-executor pattern.

### 2. Manager-Worker
```
[Manager Agent] ← task
   ↓ assigns to:
[Worker 1] [Worker 2] [Worker 3]
   ↓ results flow back:
[Manager Agent] → final answer
```

The manager delegates and synthesizes. Workers are specialists.

### 3. Peer Swarm
```
[Agent A] ↔ [Agent B] ↔ [Agent C]
              ↓
        [Discussion / consensus]
```

All agents are peers. They share information, debate, and converge. Used by: AutoGen's group chat, CAMEL.

### 4. Blackboard
```
[Shared Memory / Blackboard]
       ↑ ↓ ↑ ↓ ↑ ↓
[Agent A] [Agent B] [Agent C]
```

A shared state ("blackboard") that agents read from and write to. No direct agent-to-agent communication — all via the shared state. Classic AI pattern (1980s); reviving for LLMs.

### 5. Marketplace / Bidding
```
[Task posted]
   ↓
[Agent 1: bid 0.8] [Agent 2: bid 0.6] [Agent 3: bid 0.9]
   ↓ highest bid wins:
[Agent 3] does the task
```

Agents bid on tasks based on self-assessed capability. The highest bidder executes. Useful for load balancing and specialization.

## Multi-Agent Frameworks

### LangGraph (LangChain)
- Stateful, cyclic graphs of agents.
- Durable execution (resumes after crashes).
- Strong production story.
- Most popular for serious multi-agent deployments.

```python
from langgraph.graph import StateGraph

graph = StateGraph(State)
graph.add_node("planner", planner_agent)
graph.add_node("executor", executor_agent)
graph.add_node("synthesizer", synth_agent)
graph.add_edge("planner", "executor")
graph.add_edge("executor", "synthesizer")
app = graph.compile()
```

### AutoGen (Microsoft)
- Conversational multi-agent pattern.
- Agents talk to each other in group chats.
- AutoGen 0.4+ (2025): major rewrite with better architecture.

### CrewAI
- Role-based agents ("researcher", "writer", "reviewer").
- Simpler API than LangGraph; less flexible.
- Good for straightforward workflows.

### PydanticAI
- Type-safe agents with Pydantic schemas.
- Strong Python type hints throughout.
- Good for structured output and tool use.

### OpenAI Agents SDK (2024+)
- OpenAI's first-party agent framework.
- Tight integration with OpenAI models and APIs.
- Useful if you're committed to OpenAI stack.

## Worked Example (LangGraph Planner-Executor)

```python
from langgraph.graph import StateGraph, END
from typing import TypedDict, List

class State(TypedDict):
    task: str
    plan: List[str]
    results: List[str]
    final: str

def planner(state):
    plan = llm.generate(f"Break down: {state['task']}").split('\n')
    return {"plan": plan}

def executor(state):
    results = []
    for step in state['plan']:
        result = llm.generate(f"Execute: {step}")
        results.append(result)
    return {"results": results}

def synthesizer(state):
    final = llm.generate(f"Synthesize: {state['results']}")
    return {"final": final}

graph = StateGraph(State)
graph.add_node("planner", planner)
graph.add_node("executor", executor)
graph.add_node("synthesizer", synthesizer)
graph.set_entry_point("planner")
graph.add_edge("planner", "executor")
graph.add_edge("executor", "synthesizer")
graph.add_edge("synthesizer", END)
app = graph.compile()
```

## Why This Matters for AI

- Multi-agent is **the** frontier of agentic AI in 2026. Most ambitious agent products (Devin, Cursor, Claude Code) use multi-agent internally.
- Multi-agent enables tasks no single agent can do: complex software engineering, multi-source research, content production pipelines.
- For production, the frameworks (LangGraph, AutoGen, PydanticAI) are mature enough for serious use.
- The architectural patterns (hierarchical, swarm, blackboard) translate from classical AI to LLM agents.

## Production Implications

- **Start single-agent**. Move to multi-agent only when single-agent hits limits.
- **LangGraph is the production standard** for serious multi-agent — durable, observable, well-supported.
- **Cost management is critical**: multi-agent systems can burn 10-100x more tokens than single-agent. Budget per request.
- **Observability**: trace every agent's actions. Without traces, multi-agent is impossible to debug.
- **Failure modes compound**: if each agent has 95% success rate, a 5-agent pipeline has 77% success. Plan for retries and fallbacks.

## Common Pitfalls

- **Too many agents** — coordination overhead exceeds the benefit.
- **No clear roles** — agents step on each other; redundant work.
- **Unbounded conversation** — peer-swarm agents can talk forever. Always set turn limits.
- **No global state** — without shared memory, agents repeat each other's work.
- **Forgetting that LLMs are stochastic** — same input, different outputs. Multi-agent systems amplify this variance.

## Further Reading

- Wu et al. (2023), *AutoGen: Enabling Next-Gen LLM Applications via Multi-Agent Conversation*.
- Hong et al. (2023), *MetaGPT: Meta Programming for Multi-Agent Collaborative Framework*.
- LangGraph docs: https://langchain-ai.github.io/langgraph/

## When to Use Multi-Agent vs Single-Agent

The decision to use multi-agent should be deliberate, not default. Most LLM applications are better served by a single well-prompted LLM with good tools.

**Use multi-agent when:**
1. The task naturally decomposes into specialist roles (researcher + writer + reviewer).
2. A single LLM's context window can't hold all needed information.
3. Different sub-tasks benefit from different models (e.g., a reasoning model for planning, a fast model for execution).
4. You need verification — one agent produces, another critiques.
5. The task is long-running and benefits from parallelism.

**Use single-agent when:**
1. The task is short and well-defined.
2. One LLM with good tools can do it.
3. Latency and cost matter (multi-agent is 5-50× more expensive).
4. You need determinism (multi-agent systems are more variable).

**Rule of thumb**: start single-agent. Move to multi-agent only when you've hit a clear ceiling with single-agent and the multi-agent structure addresses that specific ceiling.

## Comparison of Multi-Agent Patterns

| Pattern                | Strengths                                  | Weaknesses                                  | Best For                                       |
|------------------------|--------------------------------------------|---------------------------------------------|------------------------------------------------|
| Hierarchical (Planner-Executor) | Clear division of labor, predictable flow | Rigid, planner errors cascade                 | Multi-step workflows with clear sub-tasks      |
| Manager-Worker         | Dynamic delegation, parallel execution     | Manager is a bottleneck; coordination overhead | Specialized sub-tasks (research, coding)        |
| Peer Swarm            | Robust via discussion, no single point of failure | Unbounded conversation, hard to converge     | Brainstorming, exploration, verification       |
| Blackboard             | Decoupled agents, shared state             | Coordination complexity, race conditions     | Long-running complex tasks with shared context |
| Marketplace / Bidding  | Self-organizing, load balancing            | Bidding strategies are hard to design         | Heterogeneous agent pools                       |

## Cost and Latency Analysis

Multi-agent systems multiply cost. A 4-agent pipeline where each agent makes 3 LLM calls costs 12× a single-agent call. Concretely (2026 pricing, Llama 3 70B self-hosted at $0.50/1M tokens):
- Single agent: 1 call, ~500 tokens output = ~$0.00025.
- 4-agent pipeline, 3 calls each, 500 tokens output each = $0.003 — 12× cost.
- 4-agent pipeline with reasoning model (o3-mini, 15K CoT per call): $0.18 — 720× cost.

Latency:
- Sequential multi-agent: sum of agent latencies (4 agents × 3s = 12s).
- Parallel multi-agent: max of agent latencies (~3s if all parallel).
- Pipeline with reasoning model: 4 × 30s = 120s — unacceptable for real-time.

Production guidance: budget per request, route to multi-agent only when the marginal capability justifies the marginal cost. Most production systems use multi-agent for batch or async tasks, not real-time chat.

## Worked Example: Hierarchical Code Review System

A complete LangGraph example showing a planner-coder-reviewer-fix cycle:

```python
from langgraph.graph import StateGraph, END
from typing import TypedDict, List, Optional

class CodeReviewState(TypedDict):
    task: str                              # the coding task
    plan: List[str]                         # steps from the planner
    code: str                               # the code from the coder
    review: Optional[str]                   # the reviewer's feedback
    final_code: Optional[str]              # the fixed code
    iterations: int                         # how many review cycles

def planner(state):
    """Decompose the task into coding steps."""
    prompt = f"""You are a software architect. Decompose this task into 3-5 steps:
    Task: {state['task']}
    Output one step per line, no numbering."""
    plan = llm.invoke(prompt).split('\n')
    return {"plan": [s.strip() for s in plan if s.strip()]}

def coder(state):
    """Implement the plan as code."""
    prompt = f"""You are a senior engineer. Implement this plan as Python code:
    Plan: {chr(10).join(state['plan'])}
    Output only the code, no explanation."""
    code = llm.invoke(prompt)
    return {"code": code, "iterations": state.get("iterations", 0) + 1}

def reviewer(state):
    """Review the code for bugs and issues."""
    prompt = f"""You are a code reviewer. Find bugs, edge cases, and improvements.
    Code: {state['code']}
    If the code is acceptable, respond 'APPROVED'. Otherwise, list issues."""
    review = llm.invoke(prompt)
    return {"review": review}

def fixer(state):
    """Fix the issues found by the reviewer."""
    if "APPROVED" in state["review"]:
        return {"final_code": state["code"]}
    prompt = f"""Fix the issues in this code:
    Code: {state['code']}
    Issues: {state['review']}
    Output the corrected code."""
    fixed = llm.invoke(prompt)
    return {"code": fixed, "review": None}

def should_fix_or_finish(state):
    if state.get("final_code"):
        return END
    if state.get("iterations", 0) >= 3:  # cap at 3 review cycles
        return END
    if state.get("review") and "APPROVED" in state["review"]:
        return "fixer"
    return "coder"  # re-code if not approved

graph = StateGraph(CodeReviewState)
graph.add_node("planner", planner)
graph.add_node("coder", coder)
graph.add_node("reviewer", reviewer)
graph.add_node("fixer", fixer)
graph.set_entry_point("planner")
graph.add_edge("planner", "coder")
graph.add_edge("coder", "reviewer")
graph.add_conditional_edges("reviewer", should_fix_or_finish, {
    "fixer": "fixer",
    "coder": "coder",
    END: END,
})
graph.add_edge("fixer", END)
app = graph.compile()

result = app.invoke({"task": "Write a function to compute the Fibonacci sequence with memoization."})
print(result["final_code"] or result["code"])
```

Notable design choices:
- **Cycle cap** (3 iterations): prevents infinite loops.
- **Conditional routing**: reviewer's output determines next step.
- **State threading**: code persists across iterations so the coder can incrementally fix.
- **Two terminal conditions**: APPROVED or iteration cap.

This pattern (plan → execute → review → fix → repeat) is the canonical multi-agent code-generation workflow, used by Devin, Cursor's agent mode, and SWE-Agent internally.

## Coordination Failure Modes

Multi-agent systems have unique failure modes beyond single-agent issues:

1. **Echo chamber**: peer agents agree too quickly, missing errors. Fix: assign one agent as "devil's advocate" by default.
2. **Deadlock**: two agents disagree indefinitely. Fix: timeout + arbitration (a third agent decides).
3. **Livelock**: agents keep revising without converging. Fix: iteration cap + "declare done after N rounds."
4. **Cascade errors**: planner error corrupts all downstream agents. Fix: planner verification (a separate agent checks the plan before execution).
5. **Context bloat**: shared state grows unboundedly. Fix: state summarization (compress old entries).
6. **Token budget exhaustion**: agents run out of context. Fix: per-agent token budget + handoff (a new agent takes over with a summary).

## Production Observability for Multi-Agent

Multi-agent systems need richer observability than single-agent:
- **Per-agent traces**: which agent did what, when.
- **Token accounting per agent**: cost attribution.
- **State transitions**: how the shared state evolved.
- **Failure attribution**: which agent caused the failure.
- **Cycle detection**: alert on agents stuck in loops.

Tools: LangSmith (best for LangGraph), Langfuse (open-source), Arize Phoenix, OpenTelemetry with LLM semconv.

## Framework Selection Matrix (2026)

| Framework          | Best For                                | Strengths                              | Weaknesses                            |
|--------------------|-----------------------------------------|----------------------------------------|---------------------------------------|
| LangGraph          | Production multi-agent                  | Durable, observable, mature            | Steep learning curve, LangChain tie-in|
| OpenAI Agents SDK  | OpenAI-only stacks                      | First-party, simple API                | OpenAI lock-in, less flexible         |
| AutoGen            | Research, conversational agents         | Flexible, multi-pattern                | Less production-ready, v0.4 rewrite   |
| CrewAI             | Simple role-based workflows              | Easy API, readable                     | Less flexible, less observable        |
| PydanticAI         | Type-safe structured agents              | Excellent type hints, validation       | Newer ecosystem, less battle-tested   |
| Custom (no framework) | Maximum control, simple workflows    | No lock-in, full control               | You build everything                  |

Production recommendation: LangGraph for serious deployments. PydanticAI if type safety is critical. Custom if the workflow is simple enough to not need a framework.

## Connection to Other Concepts

- [[15 - AI Agents/Architecture/01 - Agent vs Workflow vs LLM Application|Agent vs Workflow]] — the foundational distinction.
- [[15 - AI Agents/Reasoning/03 - ReAct Pattern|ReAct Pattern]] — single-agent pattern that composes into multi-agent.
- [[15 - AI Agents/Planning/07 - Planner-Executor Pattern|Planner-Executor]] — the most common multi-agent pattern.
- [[16 - Multi-Agent Systems/Communication/02 - Communication Patterns|Communication Patterns]] — how agents talk.
- [[16 - Multi-Agent Systems/Coordination/03 - Coordination and Consensus|Coordination]] — consensus algorithms.
- [[16 - Multi-Agent Systems/Enterprise/04 - Enterprise Multi-Agent Architectures|Enterprise Architectures]] — production patterns.
- [[25 - Frameworks and Tools/Agent Frameworks/01 - Framework Selection Guide|Framework Selection Guide]] — choosing a framework.

## Interview Questions

1. **Q: When should you use a multi-agent system instead of a single agent?**
   A: Use multi-agent when (1) the task naturally decomposes into specialist roles, (2) a single LLM's context can't hold all needed information, (3) different sub-tasks need different models (reasoning for planning, fast for execution), (4) you need verification (one agent produces, another critiques), (5) the task is long-running and benefits from parallelism. Start single-agent; move to multi-agent only when you hit a clear ceiling.

2. **Q: Compare hierarchical, peer swarm, and blackboard architectures.**
   A: Hierarchical (planner-executor): clear division of labor, predictable, rigid — best for multi-step workflows. Peer swarm: agents discuss as equals, robust via diversity, but unbounded conversation — best for brainstorming and verification. Blackboard: shared state that all agents read/write, decoupled but coordination-heavy — best for long-running complex tasks with shared context.

3. **Q: How do you prevent multi-agent systems from looping forever?**
   A: Four safeguards: (1) iteration cap per agent and per workflow, (2) timeout per agent and per overall task, (3) convergence detection (state stops changing → terminate), (4) cycle detection in graph-based systems (LangGraph has built-in recursion limits). Combine all four; no single safeguard is sufficient.

4. **Q: How do you attribute cost in a multi-agent system?**
   A: Per-agent token accounting. Each agent's LLM calls are logged with prompt/completion token counts and cost. Aggregate by agent role (planner, executor, reviewer) to see which roles dominate cost. Use this to decide where to optimize (e.g., if the planner is 50% of cost, consider a smaller planner model).

5. **Q: What's the difference between a multi-agent system and a workflow with LLM calls?**
   A: A workflow has a fixed control flow — the LLM is called at specific points but doesn't decide the next step. A multi-agent system has LLMs deciding the next step — the control flow is dynamic. Workflows are predictable and debuggable; multi-agent systems are flexible and powerful. Most production systems are hybrids: a workflow with embedded agent decision points.

6. **Q: Why is LangGraph the production standard for multi-agent in 2026?**
   A: Four reasons: (1) durable execution — survives crashes via checkpointing; (2) observable — LangSmith integration gives full traces; (3) graph-based — explicit state and edges make the control flow debuggable; (4) mature — battle-tested in production at scale. Alternatives (AutoGen, CrewAI) are improving but lag on durability and observability.

## See Also

- [[15 - AI Agents/MOC|15 AI Agents]]
- [[25 - Frameworks and Tools/MOC|25 Frameworks]]
- [[22 - Production AI/MOC|22 Production AI]]
- [[16 - Multi-Agent Systems/MOC|Multi-Agent MOC]]