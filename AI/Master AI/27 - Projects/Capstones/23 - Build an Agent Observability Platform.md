---
tags: [project, observability, tracing, llmops, agents, capstone]
iteration: 13
created: 2026-08-08
last_updated: 2026-08-08
aliases: [Agent Observability, LangSmith Clone, Build LLM Observability]
---

# 23 — Build an Agent Observability Platform

> [!info] TL;DR
> Build a LangSmith-style observability platform for LLM agents: trace every LLM call, tool call, and decision; collect metrics (latency, cost, token usage); detect anomalies (hallucination, prompt injection, infinite loops); and provide a UI for debugging. This capstone integrates chapters 15 (AI Agents), 16 (Multi-Agent Systems), 20 (AI Infrastructure), and 21 (LLMOps) into a production-grade observability system. By 2026, every production agent system needs observability — this capstone builds the canonical implementation.

## Project Goals

By the end of this project, you will have built:
1. A tracing layer that captures every LLM call, tool call, and agent decision.
2. A storage layer for traces (Postgres + JSON columns).
3. A metrics layer (latency, cost, token usage, success rate).
4. An anomaly detection layer (hallucination sampling, prompt injection detection, loop detection).
5. A query layer (filter traces by session, agent, error, latency).
6. A simple web UI for browsing traces.

## Architecture

```mermaid
graph TD
    Agent[Agent Application] -->|trace events| SDK[Observability SDK]
    SDK -->|HTTP| Collector[Trace Collector API]
    Collector -->|async| Queue[Kafka/Redis Queue]
    Queue -->|consume| Storage[Storage Postgres]
    Storage --> Query[Query API]
    Query --> UI[Web UI]
    Storage --> Metrics[Metrics Computation]
    Metrics --> Alerts[Alerting Prometheus]
    Alerts --> UI
    Storage --> Anomaly[Anomaly Detection]
    Anomaly --> UI
```

## Prerequisites

```bash
pip install fastapi uvicorn sqlalchemy asyncpg pydantic
pip install openai anthropic  # for LLM calls
pip install prometheus-client  # for metrics
# Infrastructure: Postgres, Redis (for queue), Prometheus (for metrics)
```

## Step 1: Tracing SDK

The SDK is what the agent application imports. It wraps LLM calls and tool calls to capture traces.

```python
import time
import uuid
import json
from contextvars import ContextVar
from functools import wraps
from typing import Optional

# Context variables for trace propagation
current_trace_id: ContextVar[str] = ContextVar("trace_id", default="")
current_parent_span_id: ContextVar[str] = ContextVar("parent_span_id", default="")

class ObservabilityClient:
    """Lightweight client that buffers trace events and sends them async."""

    def __init__(self, collector_url: str = "http://localhost:8000"):
        self.collector_url = collector_url
        self._buffer = []

    def emit(self, event: dict):
        """Buffer an event; flush periodically."""
        self._buffer.append(event)
        if len(self._buffer) >= 50:
            self.flush()

    def flush(self):
        """Send buffered events to collector."""
        if not self._buffer:
            return
        import requests
        try:
            requests.post(f"{self.collector_url}/events", json=self._buffer, timeout=2.0)
            self._buffer = []
        except Exception as e:
            # Don't let observability break the app
            print(f"[observability] flush failed: {e}")

# Global client
_client = ObservabilityClient()


def trace_span(name: str, span_type: str = "function"):
    """Decorator: trace a function call as a span."""
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            span_id = str(uuid.uuid4())
            parent_id = current_parent_span_id.get()
            trace_id = current_trace_id.get() or str(uuid.uuid4())

            # Set context for nested spans
            token_trace = current_trace_id.set(trace_id)
            token_parent = current_parent_span_id.set(span_id)

            start = time.time()
            try:
                result = fn(*args, **kwargs)
                error = None
                return result
            except Exception as e:
                error = str(e)
                raise
            finally:
                end = time.time()
                event = {
                    "trace_id": trace_id,
                    "span_id": span_id,
                    "parent_id": parent_id,
                    "name": name,
                    "type": span_type,
                    "start_time": start,
                    "end_time": end,
                    "duration_ms": (end - start) * 1000,
                    "error": error,
                    "input": str(args)[:1000],  # truncate
                    "output": str(result)[:1000] if not error else None,
                }
                _client.emit(event)
                current_trace_id.reset(token_trace)
                current_parent_span_id.reset(token_parent)
        return wrapper
    return decorator


def trace_llm_call(model: str, prompt: str, response: str, **metadata):
    """Emit a trace event for an LLM call."""
    span_id = str(uuid.uuid4())
    parent_id = current_parent_span_id.get()
    trace_id = current_trace_id.get() or str(uuid.uuid4())
    event = {
        "trace_id": trace_id,
        "span_id": span_id,
        "parent_id": parent_id,
        "name": f"llm.{model}",
        "type": "llm",
        "start_time": time.time(),
        "end_time": time.time(),
        "duration_ms": 0,
        "model": model,
        "prompt": prompt[:5000],
        "response": response[:5000],
        "input_tokens": metadata.get("input_tokens"),
        "output_tokens": metadata.get("output_tokens"),
        "cost_usd": metadata.get("cost_usd"),
    }
    _client.emit(event)


def trace_tool_call(tool_name: str, tool_input: dict, tool_output: dict, duration_ms: float):
    """Emit a trace event for a tool call."""
    span_id = str(uuid.uuid4())
    parent_id = current_parent_span_id.get()
    trace_id = current_trace_id.get() or str(uuid.uuid4())
    event = {
        "trace_id": trace_id,
        "span_id": span_id,
        "parent_id": parent_id,
        "name": f"tool.{tool_name}",
        "type": "tool",
        "start_time": time.time() - duration_ms / 1000,
        "end_time": time.time(),
        "duration_ms": duration_ms,
        "tool_name": tool_name,
        "tool_input": json.dumps(tool_input)[:5000],
        "tool_output": json.dumps(tool_output)[:5000],
    }
    _client.emit(event)
```

## Step 2: Trace Collector (FastAPI)

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import asyncpg
import json

app = FastAPI(title="Observability Collector")

# Postgres connection pool
_pool: Optional[asyncpg.Pool] = None

async def get_pool():
    global _pool
    if _pool is None:
        _pool = await asyncpg.create_pool(
            "postgresql://user:pass@localhost/observability",
            min_size=5, max_size=20,
        )
    return _pool


class TraceEvent(BaseModel):
    trace_id: str
    span_id: str
    parent_id: Optional[str]
    name: str
    type: str
    start_time: float
    end_time: float
    duration_ms: float
    error: Optional[str] = None
    input: Optional[str] = None
    output: Optional[str] = None
    model: Optional[str] = None
    prompt: Optional[str] = None
    response: Optional[str] = None
    input_tokens: Optional[int] = None
    output_tokens: Optional[int] = None
    cost_usd: Optional[float] = None
    tool_name: Optional[str] = None
    tool_input: Optional[str] = None
    tool_output: Optional[str] = None


@app.on_event("startup")
async def init_db():
    pool = await get_pool()
    async with pool.acquire() as conn:
        await conn.execute("""
            CREATE TABLE IF NOT EXISTS trace_events (
                trace_id TEXT,
                span_id TEXT PRIMARY KEY,
                parent_id TEXT,
                name TEXT,
                type TEXT,
                start_time TIMESTAMP,
                end_time TIMESTAMP,
                duration_ms FLOAT,
                error TEXT,
                input TEXT,
                output TEXT,
                model TEXT,
                prompt TEXT,
                response TEXT,
                input_tokens INT,
                output_tokens INT,
                cost_usd FLOAT,
                tool_name TEXT,
                tool_input TEXT,
                tool_output TEXT,
                created_at TIMESTAMP DEFAULT NOW()
            )
        """)
        await conn.execute("CREATE INDEX IF NOT EXISTS idx_trace_id ON trace_events(trace_id)")
        await conn.execute("CREATE INDEX IF NOT EXISTS idx_created_at ON trace_events(created_at)")


@app.post("/events")
async def ingest_events(events: List[TraceEvent]):
    """Bulk ingest trace events."""
    pool = await get_pool()
    async with pool.acquire() as conn:
        rows = [(e.trace_id, e.span_id, e.parent_id, e.name, e.type,
                 e.start_time, e.end_time, e.duration_ms, e.error,
                 e.input, e.output, e.model, e.prompt, e.response,
                 e.input_tokens, e.output_tokens, e.cost_usd,
                 e.tool_name, e.tool_input, e.tool_output) for e in events]
        await conn.executemany("""
            INSERT INTO trace_events
            (trace_id, span_id, parent_id, name, type, start_time, end_time,
             duration_ms, error, input, output, model, prompt, response,
             input_tokens, output_tokens, cost_usd, tool_name, tool_input, tool_output)
            VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, $14, $15, $16, $17, $18, $19, $20)
            ON CONFLICT (span_id) DO NOTHING
        """, rows)
    return {"ingested": len(events)}


@app.get("/traces/{trace_id}")
async def get_trace(trace_id: str):
    """Get all events for a trace, organized as a tree."""
    pool = await get_pool()
    async with pool.acquire() as conn:
        rows = await conn.fetch(
            "SELECT * FROM trace_events WHERE trace_id = $1 ORDER BY start_time",
            trace_id
        )
    if not rows:
        raise HTTPException(404, "Trace not found")
    # Build tree from flat list
    events = [dict(r) for r in rows]
    return {"trace_id": trace_id, "events": events}


@app.get("/traces")
async def list_traces(limit: int = 50, error_only: bool = False):
    """List recent traces, optionally filtered to only errors."""
    pool = await get_pool()
    async with pool.acquire() as conn:
        if error_only:
            rows = await conn.fetch("""
                SELECT trace_id, MIN(start_time) as start, MAX(end_time) as end,
                       COUNT(*) as span_count, SUM(cost_usd) as total_cost,
                       BOOL_OR(error IS NOT NULL) as has_error
                FROM trace_events GROUP BY trace_id
                HAVING BOOL_OR(error IS NOT NULL)
                ORDER BY start DESC LIMIT $1
            """, limit)
        else:
            rows = await conn.fetch("""
                SELECT trace_id, MIN(start_time) as start, MAX(end_time) as end,
                       COUNT(*) as span_count, SUM(cost_usd) as total_cost,
                       BOOL_OR(error IS NOT NULL) as has_error
                FROM trace_events GROUP BY trace_id
                ORDER BY start DESC LIMIT $1
            """, limit)
    return {"traces": [dict(r) for r in rows]}


@app.get("/metrics")
async def get_metrics(window_minutes: int = 60):
    """Aggregate metrics: total traces, avg latency, total cost, error rate."""
    pool = await get_pool()
    async with pool.acquire() as conn:
        rows = await conn.fetch("""
            SELECT
                COUNT(DISTINCT trace_id) as total_traces,
                AVG(duration_ms) as avg_latency_ms,
                SUM(cost_usd) as total_cost_usd,
                SUM(input_tokens) as total_input_tokens,
                SUM(output_tokens) as total_output_tokens,
                COUNT(CASE WHEN error IS NOT NULL THEN 1 END) as error_count,
                COUNT(*) as total_spans
            FROM trace_events
            WHERE created_at > NOW() - INTERVAL '%s minutes'
        """ % window_minutes)
    return dict(rows[0])
```

## Step 3: Anomaly Detection

```python
import re

PROMPT_INJECTION_PATTERNS = [
    r"ignore (previous|all) instructions",
    r"disregard (the|your) system prompt",
    r"you are now (in|a) (developer|root|admin) mode",
    r"reveal (your|the) (system|initial) prompt",
    r"print (your|the) instructions",
]

def detect_prompt_injection(text: str) -> list:
    """Detect common prompt injection patterns in input."""
    findings = []
    for pattern in PROMPT_INJECTION_PATTERNS:
        matches = re.findall(pattern, text, re.IGNORECASE)
        if matches:
            findings.append({"pattern": pattern, "matches": matches})
    return findings


def detect_infinite_loop(trace_events: list, max_iterations: int = 50) -> bool:
    """Detect if an agent is looping (same tool called > max_iterations times)."""
    tool_calls = [e for e in trace_events if e["type"] == "tool"]
    if len(tool_calls) > max_iterations:
        return True
    # Check for repeated identical tool calls
    tool_signatures = [(e["tool_name"], e["tool_input"]) for e in tool_calls]
    if len(set(tool_signatures)) < len(tool_signatures) * 0.5:
        # >50% duplicate calls
        return True
    return False


def detect_hallucination_sampling(trace_events: list, sample_rate: float = 0.01):
    """Mark a sample of LLM responses for hallucination review."""
    llm_events = [e for e in trace_events if e["type"] == "llm"]
    import random
    sampled = random.sample(llm_events, int(len(llm_events) * sample_rate))
    return [e["span_id"] for e in sampled]


def detect_cost_anomaly(trace_events: list, threshold_usd: float = 1.0) -> bool:
    """Flag traces that exceed cost threshold."""
    total_cost = sum(e.get("cost_usd") or 0 for e in trace_events)
    return total_cost > threshold_usd
```

## Step 4: Metrics Layer

```python
from prometheus_client import Counter, Histogram, Gauge

# Prometheus metrics
LLM_CALLS = Counter("llm_calls_total", "Total LLM calls", ["model"])
LLM_LATENCY = Histogram("llm_latency_seconds", "LLM call latency", ["model"])
LLM_TOKENS = Counter("llm_tokens_total", "Total tokens used", ["model", "direction"])
LLM_COST = Counter("llm_cost_usd_total", "Total LLM cost in USD", ["model"])
TOOL_CALLS = Counter("tool_calls_total", "Total tool calls", ["tool_name"])
TOOL_ERRORS = Counter("tool_errors_total", "Total tool errors", ["tool_name"])
TRACE_ERRORS = Counter("trace_errors_total", "Total traces with errors")
ACTIVE_TRACES = Gauge("active_traces", "Currently active traces")


def record_llm_metrics(model: str, latency_s: float, input_tokens: int, output_tokens: int, cost_usd: float):
    LLM_CALLS.labels(model=model).inc()
    LLM_LATENCY.labels(model=model).observe(latency_s)
    LLM_TOKENS.labels(model=model, direction="input").inc(input_tokens)
    LLM_TOKENS.labels(model=model, direction="output").inc(output_tokens)
    LLM_COST.labels(model=model).inc(cost_usd)


def record_tool_metrics(tool_name: str, error: bool = False):
    TOOL_CALLS.labels(tool_name=tool_name).inc()
    if error:
        TOOL_ERRORS.labels(tool_name=tool_name).inc()
```

## Step 5: Simple Web UI

A minimal HTML/JS UI for browsing traces:

```html
<!-- traces.html -->
<!DOCTYPE html>
<html>
<head>
    <title>Agent Observability</title>
    <style>
        body { font-family: sans-serif; margin: 20px; }
        .trace { border: 1px solid #ddd; padding: 10px; margin: 5px 0; }
        .error { border-left: 4px solid red; }
        .ok { border-left: 4px solid green; }
        .span { margin-left: 20px; padding: 5px; border-left: 2px solid #ccc; }
        .llm { background: #eef; }
        .tool { background: #efe; }
    </style>
</head>
<body>
    <h1>Recent Traces</h1>
    <div id="traces"></div>
    <script>
        async function loadTraces() {
            const r = await fetch('/traces?limit=50');
            const data = await r.json();
            const div = document.getElementById('traces');
            div.innerHTML = data.traces.map(t => `
                <div class="trace ${t.has_error ? 'error' : 'ok'}">
                    <strong>${t.trace_id}</strong>
                    spans: ${t.span_count}
                    cost: $${(t.total_cost || 0).toFixed(4)}
                    ${t.has_error ? '⚠ ERROR' : '✓'}
                </div>
            `).join('');
        }
        loadTraces();
        setInterval(loadTraces, 5000);  // auto-refresh
    </script>
</body>
</html>
```

## Production Hardening Checklist

1. **Async ingestion**: never block the agent on observability. Use a queue (Kafka/Redis) between SDK and collector; flush asynchronously.
2. **Sampling for high-volume**: at >1000 traces/sec, sample (e.g., 10%) to control storage cost. Always sample errors at 100%.
3. **PII redaction**: redact PII (emails, phone numbers, SSNs) before storing prompts/responses. Use Presidio or regex patterns.
4. **Retention policy**: 7–30 days hot storage; archive to S3 for cold storage. Otherwise Postgres costs explode.
5. **Cost attribution**: tag every trace with user/tenant/project. Cost-per-tenant dashboards are essential for SaaS.
6. **OpenTelemetry compatibility**: emit traces as OpenTelemetry spans so they integrate with existing observability stacks (Jaeger, Datadog, Honeycomb).
7. **Streaming support**: for streaming LLM responses, capture token-by-token deltas, not just the final response. Important for debugging streaming UX bugs.
8. **Tool input/output truncation**: tool inputs (e.g., a 1MB PDF) can blow up storage. Truncate to 5KB; store full content in S3 if needed.
9. **Multi-tenant isolation**: traces should be isolated by tenant. Row-level security in Postgres; or per-tenant databases.
10. **Latency overhead**: the SDK adds <1ms per LLM call. Profile and optimize; if it adds >5ms, agents will skip observability.
11. **Alerting**: alert on (1) error rate >5%, (2) p99 latency >10s, (3) cost anomaly (>3σ from baseline), (4) prompt injection detection.
12. **Comparison to LangSmith**: LangSmith (LangChain's commercial offering) does all of the above. Use this capstone to understand how it works; use LangSmith in production unless you need custom features.

## Modern Developments (2024–2026)

### OpenTelemetry for LLMs
The OpenTelemetry community added LLM-specific semantic conventions in 2024. By 2026, OTel is the standard for LLM observability — most production systems emit OTel traces rather than vendor-specific formats.

### LangSmith (2024)
LangChain's commercial observability platform. The reference implementation for LLM observability. Most production teams use LangSmith or a similar SaaS rather than building their own.

### Arize Phoenix (2024)
Open-source LLM observability. Apache 2.0 license. Self-hosted alternative to LangSmith. Good for teams that can't send data to a third party.

### Helicone (2024)
LLM observability SaaS focused on cost tracking and prompt logging. Simpler than LangSmith; good for cost-conscious teams.

### LLM-as-Judge Sampling (2025)
Modern observability platforms sample 1–5% of responses for LLM-as-judge evaluation. Catches quality issues that traditional metrics (latency, error rate) miss.

### Agent-Specific Observability (2025)
Beyond LLM observability: agent-specific traces that show planning, tool selection, reflection loops. Critical for debugging autonomous agents. LangGraph Studio (2025) is the reference implementation.

### Real-Time Prompt Injection Detection (2026)
Real-time classifiers that flag suspicious inputs as they're being traced. Integrates with the observability platform — flagged inputs are marked for human review.

## Common Failure Modes — Diagnostic Table

| Symptom                                  | Likely Cause                                        | Fix                                                              |
|------------------------------------------|------------------------------------------------------|------------------------------------------------------------------|
| Traces not appearing in UI                | SDK buffer not flushed; or collector down              | Add flush-on-shutdown; monitor collector health                  |
| High overhead on agent                    | Synchronous SDK emit                                 | Make emit fully async; use a queue                               |
| Storage growing fast                      | No retention policy; or no truncation                  | 7–30 day retention; truncate tool inputs                          |
| Missing tool inputs/outputs              | Tool I/O not traced                                   | Wrap all tool calls with trace_tool_call                          |
| Cost not tracked                          | LLM call doesn't include cost_usd                     | Add cost computation based on model + tokens                     |
| Can't find specific trace                | No trace_id propagation                               | Use ContextVar to propagate trace_id across async calls          |
| UI shows traces out of order              | start_time not indexed                                | Add index on start_time; sort in query                            |
| Multi-tenant data leaks                   | No row-level security                                 | Add tenant_id column; enforce RLS                                |
| PII in storage                            | No redaction                                          | Add redaction in collector before storage                         |
| Agent hangs but no trace                  | Agent crashed before flushing                         | Add flush-on-exit handler; or use atexit                          |
| Cost spikes undetected                    | No alerting                                           | Add Prometheus alert: total cost >3σ from baseline               |
| Hallucinations not caught                 | No LLM-as-judge sampling                              | Sample 1–5% of responses; LLM-as-judge                           |

## Interview Questions

1. **Q: Walk through what you'd trace in a ReAct agent.**
   A: For each ReAct iteration: (1) **Thought span**: the LLM call that produces the next thought; trace prompt, response, model, tokens, cost. (2) **Action span**: the tool call; trace tool name, input, output, duration. (3) **Observation span**: how the observation is processed (e.g., truncated, summarized). (4) **Iteration wrapper**: a parent span that captures the whole Thought→Action→Observation loop. (5) **Final answer span**: the final LLM call that produces the user-facing answer. All spans share a trace_id; nested spans have parent_id chain. From this, you can debug: which iteration was slow, which tool failed, which thought was illogical.

2. **Q: How do you detect prompt injection via observability?**
   A: Two layers. (1) **Pattern matching**: regex for common injection patterns ("ignore previous instructions", "reveal system prompt", "you are now in developer mode"). Run on every input; flag matches in the trace. (2) **LLM-based classifier**: train a small model (or use GPT-4o-mini) to classify each input as benign/suspicious/malicious. Sample 100% of inputs (cheap; gpt-4o-mini is $0.15/1M tokens). Flag suspicious inputs in the trace and alert on malicious ones. Critical: don't block on the classifier (latency); run async and flag retroactively.

3. **Q: How do you keep observability overhead low?**
   A: Three techniques. (1) **Async emit**: the SDK buffers events and sends them in batches via a background thread. Agent never blocks on observability. (2) **Sampling**: at high volume (>1000 traces/sec), sample 10% of successful traces. Always sample 100% of errors. (3) **Truncation**: cap prompt/response/tool I/O at 5KB before storing. Most traces don't need the full content; the truncated version is enough for debugging. Combined: <1ms overhead per LLM call, <1% of agent runtime.

4. **Q: How do you attribute cost to tenants?**
   A: Tag every trace with `tenant_id` (or `user_id`, `project_id`). The SDK accepts tenant_id as a constructor argument or context variable. The collector stores it as a column. Aggregate by tenant_id for cost-per-tenant dashboards. Critical for SaaS: charge customers based on their actual usage. Also enables cost anomalies per tenant (a single tenant suddenly using 10× normal could indicate abuse or a bug).

5. **Q: How do you debug a multi-agent system with observability?**
   A: Three things. (1) **Trace propagation**: all agents in a multi-agent system share a top-level trace_id. Each agent's spans are nested under an "agent" span. The full trace shows the multi-agent interaction as a tree. (2) **Inter-agent messages**: trace the messages passed between agents (which agent sent what to which). Critical for debugging communication failures. (3) **Coordination patterns**: for hierarchical (planner-executor) patterns, trace the planner's decisions and each executor's actions. For swarm patterns, trace the message bus. Without this, multi-agent systems are impossible to debug — you'd see "agent A failed" with no context.

6. **Q: How do you evaluate agent quality (not just latency/cost)?**
   A: Two approaches. (1) **LLM-as-judge sampling**: sample 1–5% of agent runs, ask GPT-4o to rate the agent's decisions on a 1–5 scale. Aggregate per agent, per task type. Catches quality issues that latency/error metrics miss. (2) **Task-specific metrics**: for tasks with ground truth (e.g., code generation), track pass@k. For tasks without ground truth, track user feedback (thumbs up/down). Combine both for a holistic view. Modern observability platforms (LangSmith, Arize Phoenix) integrate LLM-as-judge natively.

## Connection to Other Concepts

- [[15 - AI Agents/MOC]] — parent chapter for agents.
- [[16 - Multi-Agent Systems/MOC]] — multi-agent context.
- [[20 - AI Infrastructure/Observability/05 - Observability Stack]] — observability infrastructure.
- [[21 - LLMOps and MLOps/MOC]] — LLMOps context.
- [[21 - LLMOps and MLOps/Monitoring/05 - Production Monitoring]] — production monitoring.
- [[21 - LLMOps and MLOps/Cost/06 - Cost Optimization]] — cost tracking.
- [[22 - Production AI/Security/01 - LLM Security and Prompt Injection]] — prompt injection detection.
- [[22 - Production AI/Reliability/06 - Failure Modes and Graceful Degradation]] — failure modes.
- [[25 - Frameworks and Tools/Agent Frameworks/03 - LangGraph]] — LangGraph has built-in tracing via LangSmith.
- [[27 - Projects/MOC]] — projects index.

## See Also

- [[27 - Projects/MOC|27 Projects MOC]]
- [[20 - AI Infrastructure/Observability/05 - Observability Stack|Observability Stack]]
