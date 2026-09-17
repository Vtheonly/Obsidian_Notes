---
tags: [agents, reasoning, react, tools, agent-loop]
iteration: 7
created: 2026-08-07
last_updated: 2026-08-08
aliases: [ReAct Pattern, ReAct, Reasoning and Acting, Agent Loop]
---

# ReAct Pattern

> [!info] TL;DR
> ReAct (Yao et al., 2022) interleaves **Reasoning** (Thought) and **Acting** (Action) so the model can use tools while reasoning. The model thinks, chooses an action, observes the result, then thinks again. The foundation of most modern agent frameworks. This note covers the idea, the four components, implementation (both classic text-parsing and modern function calling), why it works, variants, production patterns, common pitfalls, and comparison to alternatives.

## The Idea

Pure [[02 - Chain-of-Thought|CoT]] has a limitation: the model can only reason with what it already knows. If it needs fresh information (a calculation, a web search, a database query), it's stuck. The model can hallucinate an answer, but it can't verify.

ReAct interleaves reasoning with tool use:

```
Thought: I need to find the population of France.
Action: search("population of France 2024")
Observation: 68 million (2024 estimate)
Thought: Now I need to compare with Germany.
Action: search("population of Germany 2024")
Observation: 84 million
Thought: Germany has more people. Final answer.
Action: finish("Germany has more people than France (84M vs 68M).")
```

The pattern: **Thought → Action → Observation → Thought → Action → Observation → ... → Finish**.

This cycle continues until the model decides it has enough information to produce a final answer, or until a maximum iteration count is reached.

## The Four Components

### 1. Thought
The model's reasoning about what to do next. This is where [[02 - Chain-of-Thought|CoT]] happens — the model explains its plan, considers options, and decides.

The thought serves two purposes:
- **Externalizes reasoning**: makes the model's logic visible (for debugging and for the model to "think out loud").
- **Improves quality**: studies show that models that reason step-by-step make fewer errors than models that act directly.

### 2. Action
A structured tool call. The model picks a tool from its available tools and provides arguments. The framework parses this and executes the tool.

Actions are structured (not free text) so the framework can parse them reliably. In the original ReAct, actions were text (`Action: search("query")`); in modern implementations, they're structured function calls (JSON with name + arguments).

### 3. Observation
The tool's output, fed back to the model as the next message. This is what the model "sees" of the world.

Observations should be:
- **Concise**: long outputs waste context. Summarize or extract relevant parts.
- **Structured**: parse raw outputs into a clean format.
- **Error-aware**: if the tool failed, the observation should describe the error clearly.

### 4. Finish
The model decides it has enough information and produces the final answer. Terminates the loop.

The finish action is a special tool that signals "I'm done; here's the answer." Without it, the model would loop forever looking for more information.

## Implementation Sketch

### Classic Text-Based ReAct

The original ReAct paper used text-based parsing:

```python
SYSTEM_PROMPT = """Answer the question using the ReAct pattern.

Available tools:
- search(query): Search the web.
- calculator(expression): Evaluate a math expression.
- finish(answer): Return the final answer.

Format:
Thought: <your reasoning>
Action: <tool_name>(<arguments>)

You will receive:
Observation: <tool output>

Continue until you can use finish() with the final answer.
"""

tools = {
    "search": web_search,
    "calculator": calculator,
    "finish": lambda x: None,  # signals loop exit
}

def react_agent(question, max_iters=10):
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": question},
    ]
    
    for _ in range(max_iters):
        # LLM produces Thought + Action
        response = llm.chat(messages=messages)
        messages.append({"role": "assistant", "content": response.content})
        
        # Parse the Action from text
        action, args = parse_action(response.content)
        
        if action == "finish":
            return args  # final answer
        
        # Execute the tool
        try:
            result = tools[action](**args)
        except Exception as e:
            result = f"Error: {e}"
        
        # Feed back as Observation
        messages.append({"role": "user", "content": f"Observation: {result}"})
    
    return "Max iterations reached."
```

### Modern Form: Native Function Calling

Modern LLMs have **native function calling** — the model returns a structured `tool_calls` field that's already parsed. This is more reliable than text parsing:

```python
tools_schema = [
    {
        "type": "function",
        "function": {
            "name": "search",
            "description": "Search the web for current information.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "The search query"}
                },
                "required": ["query"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "calculator",
            "description": "Evaluate a mathematical expression.",
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {"type": "string"}
                },
                "required": ["expression"]
            }
        }
    }
]

def react_agent_modern(question, max_iters=10):
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": question},
    ]
    
    for _ in range(max_iters):
        response = llm.chat(
            messages=messages,
            tools=tools_schema,
            tool_choice="auto",  # let the model decide
        )
        messages.append(response.message)
        
        if not response.tool_calls:
            # No tool call = final answer
            return response.content
        
        # Execute each tool call
        for call in response.tool_calls:
            try:
                result = execute_tool(call.name, call.arguments)
            except Exception as e:
                result = f"Error: {e}"
            
            messages.append({
                "role": "tool",
                "tool_call_id": call.id,
                "content": str(result),
            })
    
    return "Max iterations reached."
```

Native function calling is more reliable than text parsing and is the standard in 2024+. See [[04 - Function Calling]].

### LangGraph Implementation

LangGraph provides a clean ReAct implementation:

```python
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode
from typing import TypedDict, Annotated
from langgraph.graph.message import add_messages

class AgentState(TypedDict):
    messages: Annotated[list, add_messages]

def call_model(state):
    response = model.invoke(state["messages"])
    return {"messages": [response]}

def should_continue(state):
    last_message = state["messages"][-1]
    if last_message.tool_calls:
        return "tools"
    return END

graph = StateGraph(AgentState)
graph.add_node("agent", call_model)
graph.add_node("tools", ToolNode(tools))
graph.set_entry_point("agent")
graph.add_conditional_edges("agent", should_continue)
graph.add_edge("tools", "agent")

app = graph.compile()
result = app.invoke({"messages": [HumanMessage(content="What's the weather in Tokyo?")]})
```

## Why ReAct Works

### 1. External knowledge
Tools give the model access to information beyond its training cutoff — current web data, fresh database queries, real-time computations. The model isn't limited to what it memorized during pretraining.

### 2. Verified computations
Instead of guessing arithmetic (which LLMs do poorly), the model calls a calculator and gets the exact answer. This eliminates a whole class of errors.

### 3. Decomposition with verification
Each step's output is observed, so errors don't compound silently. The model can catch a bad search result and try a different query. This is much better than generating a long answer in one shot, where errors in early reasoning propagate.

### 4. Grounded answers
The final answer can cite the observations — "Based on [search result X], the answer is Y." This is the basis of agentic RAG. Users can verify the reasoning by checking the cited sources.

### 5. Explicit reasoning improves quality
Studies show that models that reason explicitly (via Thought) make fewer errors than models that act directly. The Thought step forces the model to plan before acting.

### 6. Iterative refinement
If the first action doesn't yield useful information, the model can try a different approach. This is more robust than one-shot generation, where a bad approach fails completely.

## Variants and Extensions

### ReWOO (Reasoning WithOut Observation)
Decomposes ReAct into a separate planner and executor. The planner produces all reasoning upfront; the executor just runs tools. Reduces LLM calls (one for planning, one for synthesis, vs. one per step in ReAct).

Trade-off: less adaptive than ReAct (can't change plan based on observations), but cheaper and faster.

See [[07 - Planner-Executor Pattern]] for details.

### Plan-and-Execute
Similar to ReWOO: a planner agent produces a multi-step plan, then an executor agent carries out each step. Better for long horizons (10+ steps) where ReAct drifts.

### LATS (Language Agent Tree Search)
Combines ReAct with Monte Carlo Tree Search — explores multiple action branches and picks the best. Expensive but powerful. Useful for tasks where the right action isn't obvious.

### Reflexion
Adds a reflection step after errors — the model verbalizes what went wrong and incorporates the lesson into subsequent attempts. See [[05 - Reflection]] and [[32 - Reflexion 2023]].

### Self-Consistency with ReAct
Run ReAct multiple times, take the majority answer. Reduces variance but multiplies cost.

### Tool-Enhanced CoT
A simpler variant: the model does CoT, but can call tools at specific points. Less structured than ReAct but easier to implement.

## Comparison to Alternatives

| Pattern          | LLM Calls | Adaptive | Best For                          |
|------------------|-----------|----------|-----------------------------------|
| Direct generation| 1         | N/A      | Simple questions                  |
| CoT              | 1         | N/A      | Multi-step reasoning              |
| ReAct            | N (per step) | Yes   | Tool use, fresh info              |
| ReWOO            | 2-3       | No       | Predictable multi-step tasks      |
| Plan-and-Execute | 2-5       | Limited  | Long-horizon tasks                |
| LATS             | Many      | Yes      | Hard reasoning with branching     |
| Reflexion        | N × M     | Yes      | Tasks with verifiable success     |

ReAct is the default for most agent use cases. Move to alternatives when ReAct's limitations (drift, cost) become problematic.

## Worked Example: A Multi-Tool ReAct Agent

```python
import openai
import json

client = openai.OpenAI()

# Define tools
def search_web(query: str) -> str:
    """Search the web."""
    # ... implementation ...
    return f"Search results for: {query}"

def calculator(expression: str) -> str:
    """Evaluate a math expression."""
    try:
        result = eval(expression)  # use a safe evaluator in production
        return str(result)
    except Exception as e:
        return f"Error: {e}"

def get_weather(city: str) -> str:
    """Get weather for a city."""
    # ... implementation ...
    return f"Weather in {city}: 20°C, sunny"

def write_file(path: str, content: str) -> str:
    """Write content to a file."""
    try:
        with open(path, 'w') as f:
            f.write(content)
        return f"Wrote {len(content)} chars to {path}"
    except Exception as e:
        return f"Error: {e}"

tools = {
    "search_web": search_web,
    "calculator": calculator,
    "get_weather": get_weather,
    "write_file": write_file,
}

tools_schema = [
    {"type": "function", "function": {
        "name": "search_web",
        "description": "Search the web for current information.",
        "parameters": {
            "type": "object",
            "properties": {"query": {"type": "string"}},
            "required": ["query"]
        }
    }},
    {"type": "function", "function": {
        "name": "calculator",
        "description": "Evaluate a mathematical expression. Use for exact arithmetic.",
        "parameters": {
            "type": "object",
            "properties": {"expression": {"type": "string"}},
            "required": ["expression"]
        }
    }},
    {"type": "function", "function": {
        "name": "get_weather",
        "description": "Get the current weather for a city.",
        "parameters": {
            "type": "object",
            "properties": {"city": {"type": "string"}},
            "required": ["city"]
        }
    }},
    {"type": "function", "function": {
        "name": "write_file",
        "description": "Write content to a file.",
        "parameters": {
            "type": "object",
            "properties": {
                "path": {"type": "string"},
                "content": {"type": "string"}
            },
            "required": ["path", "content"]
        }
    }},
]

SYSTEM_PROMPT = """You are a helpful assistant with access to tools.

Use the ReAct pattern:
1. Think about what to do (internally).
2. Choose a tool and provide arguments.
3. Observe the result.
4. Repeat until you can answer.

Always use the calculator for math. Always search for current information.
Be concise in your final answer.
"""

def react_agent(question, max_iters=10):
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": question},
    ]
    
    for iteration in range(max_iters):
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=messages,
            tools=tools_schema,
            tool_choice="auto",
        )
        msg = response.choices[0].message
        messages.append(msg)
        
        if not msg.tool_calls:
            return msg.content  # final answer
        
        # Execute each tool call
        for call in msg.tool_calls:
            args = json.loads(call.function.arguments)
            try:
                result = tools[call.function.name](**args)
            except Exception as e:
                result = f"Error executing {call.function.name}: {e}"
            
            messages.append({
                "role": "tool",
                "tool_call_id": call.id,
                "content": str(result),
            })
    
    return "Max iterations reached without a final answer."

# Example usage
answer = react_agent("What's the weather in Tokyo? If it's above 15°C, write 'warm day' to /tmp/weather.txt.")
print(answer)
```

## Why This Matters for AI

- ReAct is the **canonical agent pattern**. Every agent framework (LangChain, LangGraph, OpenAI Agents SDK, PydanticAI) implements some variant of it.
- The shift from "prompt → response" to "prompt → tool calls → observations → response" is the architectural shift that defines modern agentic AI.
- ReAct works with any tool: web search, code execution, database queries, file operations, API calls, MCP servers. The pattern is tool-agnostic.
- For most production agents, ReAct (or a refinement) is the right starting point. Don't reinvent it.
- ReAct is the basis for agentic RAG, code agents, autonomous agents, and multi-agent systems.

## Production Implications

- **Always set max iterations**. Without a cap, agents can loop forever on errors. 10-20 iterations is typical.
- **Tool call validation**. LLMs will pass invalid arguments. Validate before executing; return clear error messages on failure.
- **Observation size**. Long tool outputs (e.g., full web pages) blow up context. Compress or summarize observations before feeding back. Truncate to a reasonable length (e.g., 1000 chars).
- **Tracing is essential**. Log every thought, action, and observation. Without traces, ReAct agents are impossible to debug. Use LangSmith, OpenTelemetry, or custom logging.
- **Tool selection**. Too many tools → model picks wrong ones; too few → limited capability. 5–20 tools is a typical sweet spot.
- **Error recovery**. Plan for tool failures. The model should be able to retry with different arguments, fall back to a different tool, or report failure to the user.
- **Cost monitoring**. ReAct makes multiple LLM calls per query. Track token usage per query; set budgets.
- **Latency**. Each ReAct iteration adds latency (LLM call + tool execution). Stream tokens to mask latency.
- **Human-in-the-loop**. For high-stakes tools (write_file, send_email), add approval gates. See [[09 - Human-in-the-Loop Patterns]].
- **Streaming**. Stream the model's "Thought" to the UI so users see progress. Don't wait for the full answer.

## Common Pitfalls

- **No max iterations** — agent loops forever on errors. Always set a cap.
- **Tools without descriptions** — model can't choose correctly. Every tool needs a clear, specific description.
- **Returning raw HTML/JSON as observation** — wastes context. Parse and summarize.
- **Forgetting the system prompt** — without clear instructions, the model doesn't know when to use tools vs. answer directly.
- **Tool argument hallucination** — model invents arguments that don't fit the schema. Use strict JSON schema validation.
- **No retry on transient errors** — API calls fail; the agent should retry with backoff, not give up.
- **Trusting the model's self-reported reasoning** — like CoT, the "Thought" may not reflect actual model computation. Verify with traces.
- **Tool name collisions** — if two tools have similar names, the model gets confused. Use distinct, descriptive names.
- **Forgetting to handle parallel tool calls** — modern LLMs can call multiple tools in one response. Execute them in parallel.
- **Context window overflow** — long ReAct loops accumulate messages. Summarize or truncate old messages.
- **Forgetting to handle the "no tool call" case** — if the model doesn't call a tool, it's giving the final answer. Handle this case explicitly.

## Debugging ReAct Agents

When a ReAct agent fails, the trace tells you where:

1. **Bad tool selection** — the model picked the wrong tool. Improve tool descriptions.
2. **Bad arguments** — the model passed wrong arguments. Improve the tool's parameter descriptions. Add few-shot examples.
3. **Bad observation parsing** — the tool returned something the model couldn't interpret. Format observations more clearly.
4. **Loop** — the model repeats the same action. Add a repetition detector; force the model to try a different approach.
5. **Premature finish** — the model gives up too early. Adjust the system prompt to encourage persistence.
6. **Max iterations** — the model never converges. Either the task is too hard, or the tools are insufficient.

Without traces, you're guessing. With traces, the failure mode is usually obvious.

## Interview Questions

- **Q: What is the ReAct pattern?**  
  A: Interleaving Reasoning (Thought) and Acting (Action) so the model can use tools while reasoning. The cycle: Thought → Action → Observation → ... → Finish.

- **Q: Why is ReAct better than pure CoT?**  
  A: CoT can only reason with what the model already knows. ReAct lets the model use tools to get fresh information, verify computations, and ground answers in observations.

- **Q: How does modern function calling relate to ReAct?**  
  A: Modern function calling is the structured form of ReAct's "Action" component. Instead of parsing `Action: search("query")` from text, the model returns a structured `tool_calls` field. More reliable than text parsing.

- **Q: What are the limitations of ReAct?**  
  A: (1) Cost: multiple LLM calls per query. (2) Drift: long ReAct loops lose focus. (3) Latency: each iteration adds delay. (4) Loops: without max iterations, can run forever.

- **Q: When would you use Plan-and-Execute instead of ReAct?**  
  A: For long-horizon tasks (10+ steps) where ReAct drifts. Plan-and-Execute produces a global plan upfront, then executes each step. Less adaptive but more coherent.

## Further Reading

- Yao et al. (2022), *ReAct: Synergizing Reasoning and Acting in Language Models*.
- Xu et al. (2023), *ReWOO: Decoupling Reasoning from Observations*.
- Shinn et al. (2023), *Reflexion: Language Agents with Verbal Reinforcement Learning*. See [[32 - Reflexion 2023]].
- OpenAI Function Calling docs.
- LangGraph ReAct documentation.

## See Also

- [[02 - Chain-of-Thought]] — the reasoning component
- [[04 - Function Calling]] — the modern action mechanism
- [[05 - Reflection]] — adding self-critique
- [[06 - Tree of Thoughts and Self Consistency]] — alternative reasoning patterns
- [[07 - Planner-Executor Pattern]] — alternative for long horizons
- [[08 - Autonomous Agent Lifecycles]] — production ReAct
- [[01 - Agent vs Workflow vs LLM Application]] — what makes something an agent
- [[15 - AI Agents/MOC|AI Agents MOC]]
- [[17 - RAG/MOC|RAG MOC]] — agentic RAG uses ReAct
- [[03 - Build a Mini Agent]] — implementing ReAct from scratch
