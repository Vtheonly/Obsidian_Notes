---
tags: [agents, human-in-the-loop, hitl, oversight, approval]
iteration: 12
created: 2026-08-08
last_updated: 2026-08-08
aliases: [Human-in-the-Loop, HiTL, Human Oversight, Approval Patterns]
---

# 09 — Human-in-the-Loop Patterns

> [!info] TL;DR
> Human-in-the-loop (HiTL) patterns add human oversight to autonomous agents at critical points: before destructive actions, when confidence is low, when novel situations arise, or when value judgments are required. The four main patterns are **approval gates** (pause for human yes/no before an action), **interactive refinement** (human edits the agent's output before it's used), **escalation** (agent autonomously decides to ask for help), and **supervision** (human monitors and intervenes at will). HiTL is essential for production agents that touch production systems, send communications, or make irreversible changes. LangGraph's `interrupt_before` is the canonical implementation; most agent frameworks support some form of HiTL.

## Why Human-in-the-Loop

Autonomous agents are powerful but unreliable. LLMs hallucinate, misunderstand intent, and make wrong decisions. For low-stakes actions (search the web, read a file), this is fine — the cost of an error is small. For high-stakes actions (send an email, deploy code, delete data, transfer money), an error can be catastrophic.

HiTL inserts human judgment at the points where errors are most costly. The human doesn't review every action — that would defeat the purpose of automation. Instead, the human reviews:

- **Irreversible actions**: anything that can't be undone.
- **High-impact actions**: anything with significant consequences.
- **Novel situations**: anything the agent hasn't seen before.
- **Low-confidence actions**: anything the agent is unsure about.
- **Value judgments**: anything requiring human values (e.g., is this content appropriate?).

The result: most actions are automated (fast, cheap); critical actions are reviewed (safe). This is the production sweet spot for agent systems.

## The Four HiTL Patterns

### Pattern 1: Approval Gates

The agent pauses before a critical action and asks a human for approval. The human can approve, reject, or modify the action.

```python
def execute_with_approval(action, require_approval_for=None):
    """Execute an action, asking for approval if it's in the critical list."""
    if require_approval_for and action.type in require_approval_for:
        approval = request_human_approval(action)
        if approval.status == "rejected":
            return ActionResult(success=False, reason="Human rejected")
        if approval.status == "modified":
            action = approval.modified_action
    
    return action.execute()
```

The human interface is typically:

- A chat message: "I'm about to send this email to alice@example.com. Approve?"
- A web UI: a card showing the proposed action with Approve / Reject / Modify buttons.
- An IDE integration: a popup in the editor.

Approval gates are the most common HiTL pattern. They're simple to implement and catch the majority of dangerous actions.

### Pattern 2: Interactive Refinement

The agent produces a draft output; the human edits it before it's used. This is appropriate when the output is a deliverable (email, document, code) where the agent's draft is a starting point but human polish is needed.

```python
def draft_and_refine(task):
    draft = agent.draft(task)
    edited = human_edit(draft)
    final = agent.finalize(edited)  # apply any post-processing
    return final
```

The human interface is a rich text editor with the draft pre-loaded. The human edits directly; the agent doesn't see the edits until finalize.

Interactive refinement is used in:

- **Email drafting**: agent writes the draft; human edits before sending.
- **Code generation**: agent writes code; human reviews and edits in IDE.
- **Content creation**: agent writes article; human edits and publishes.

### Pattern 3: Escalation

The agent autonomously decides to ask for help. This is appropriate when the agent encounters:

- **Ambiguity**: the request has multiple interpretations.
- **Missing information**: the agent needs data it doesn't have.
- **Low confidence**: the agent's confidence in its answer is below a threshold.
- **Out-of-scope**: the request is outside the agent's domain.

```python
def answer_with_escalation(question):
    response = agent.answer(question)
    if response.confidence < CONFIDENCE_THRESHOLD:
        return escalate_to_human(question, response, reason="low confidence")
    if response.out_of_scope:
        return escalate_to_human(question, response, reason="out of scope")
    return response
```

Escalation is more sophisticated than approval gates — the agent itself decides when to ask for help. This requires the agent to have reliable confidence estimates, which is an active research area.

### Pattern 4: Supervision

A human monitors the agent's activity in real-time and can intervene at will. Unlike approval gates (which pause at predefined points), supervision allows intervention at any point.

Implementation:

- **Activity feed**: a stream of the agent's actions, visible to the human.
- **Pause button**: the human can pause the agent at any time.
- **Override**: the human can override the agent's decisions.
- **Direct chat**: the human can message the agent with corrections.

Supervision is appropriate for:

- **High-stakes deployments**: where any error is unacceptable.
- **New agents**: during initial deployment, before trust is established.
- **Complex tasks**: where the agent may need guidance.

## Implementation in LangGraph

LangGraph (see [[03 - LangGraph]]) has first-class HiTL support via `interrupt_before`:

```python
from langgraph.graph import StateGraph, END

graph = StateGraph(AgentState)
graph.add_node("plan", plan_node)
graph.add_node("execute", execute_node)
graph.add_node("send_email", send_email_node)  # critical action

graph.set_entry_point("plan")
graph.add_edge("plan", "execute")
graph.add_edge("execute", "send_email")
graph.add_edge("send_email", END)

# Compile with interrupt before the critical node
app = graph.compile(
    interrupt_before=["send_email"],
    checkpointer=postgres_checkpointer,
)

# Run until the interrupt
result = app.invoke(input, config={"configurable": {"thread_id": "1"}})
# Agent has planned and executed, but paused before send_email

# Show the proposed email to the human
proposed_email = result["messages"][-1].content
approval = ask_human(proposed_email)

if approval:
    # Resume execution
    result = app.invoke(None, config={"configurable": {"thread_id": "1"}})
else:
    # Reject; agent doesn't send
    print("Email not sent")
```

The `checkpointer` persists state across the pause, so the agent can resume exactly where it left off. The `thread_id` identifies the conversation, so multiple users can have independent HiTL sessions.

## HiTL Decision Framework

When designing an agent, decide for each action:

| Action Type                    | HiTL Pattern             |
|--------------------------------|--------------------------|
| Read-only (search, get)        | None                     |
| Reversible write (edit file)   | None (or supervision)    |
| Irreversible local (delete file)| Approval gate           |
| External communication (email) | Approval gate            |
| Production deployment          | Approval gate + supervision |
| High-value transaction          | Approval gate + second approver |
| Creative content               | Interactive refinement   |
| Ambiguous requests             | Escalation               |

The framework balances automation (speed, cost) with safety (oversight). Most actions are automated; the few that matter get human review.

## Production Patterns

### Make Pauses Fast

When the agent pauses for approval, the human should be able to approve/reject in seconds. Long pauses (waiting for an email response) are frustrating and slow.

- **Push notifications**: notify the human via Slack, mobile push, etc.
- **Inline UI**: show the proposed action in the user's current context (chat, IDE).
- **Quick actions**: Approve / Reject buttons accessible in one click.

### Provide Context

The human needs to understand what they're approving. Show:

- **What the agent will do**: the action and its parameters.
- **Why**: the agent's reasoning (chain-of-thought).
- **What happens if rejected**: what the agent will do instead.
- **Source data**: the data the action is based on.

Without context, the human is just clicking "Approve" without understanding — which provides no safety benefit.

### Allow Modification

Binary approve/reject is limiting. Often the human wants to modify the action ("yes, but change the recipient to bob@"). Support modification:

- **Edit parameters**: change the action's inputs.
- **Edit output**: change the agent's draft (interactive refinement).
- **Redirect**: tell the agent to do something different.

### Set Timeouts on Pauses

A pause that waits forever is a stuck agent. Set timeouts:

- **Short timeout (5 minutes)**: reject automatically; tell the user.
- **Long timeout (24 hours)**: terminate the agent; reschedule.

The right timeout depends on the use case. Real-time chat needs short timeouts; batch processing can wait longer.

### Audit All HiTL Decisions

Log every approval, rejection, and modification:

- **Who** approved/rejected.
- **What** they approved/rejected.
- **When** they decided.
- **Why** (if they provided a reason).

This is essential for compliance (especially in regulated industries) and for improving the agent (patterns of rejection reveal what the agent does wrong).

### Calibrate Approval Thresholds

Over time, analyze which approvals are routinely approved vs. rejected. If an action is approved 99% of the time, remove the approval gate (it's just friction). If an action is rejected 50% of the time, the agent is making bad proposals — improve the agent.

This calibration is the key to scaling HiTL: start with many approval gates, then remove them as the agent earns trust.

### Support Multiple Approvers

For high-stakes actions (production deploys, large transactions), require approval from multiple humans:

- **Sequential**: first approver, then second approver.
- **Parallel**: any of N approvers can approve.
- **Quorum**: K of N approvers required.

Multi-approver patterns add friction but reduce single-point-of-failure risk.

## Common Pitfalls

### Approval Fatigue

If every action requires approval, humans start rubber-stamping. They click "Approve" without reading. This provides no safety benefit.

Solution: minimize approval gates. Only require approval for genuinely critical actions. Calibrate thresholds over time.

### Stale Approvals

The agent pauses for approval. The human approves 3 days later. In the meantime, the situation has changed — the approved action is now wrong.

Solution: invalidate approvals after a timeout. Re-evaluate the situation before executing.

### No Audit Trail

Without logging, you can't tell what was approved, by whom, or why. This is a compliance nightmare in regulated industries.

Solution: log everything. Audit logs are non-negotiable for production HiTL.

### HiTL as a Crutch

If the agent is so unreliable that every action needs approval, the agent isn't production-ready. HiTL should catch rare errors, not compensate for systematic unreliability.

Solution: improve the agent. HiTL is a safety net, not a substitute for capability.

### Friction in the Wrong Places

Requiring approval for read-only actions (search, get) adds friction without safety benefit. Reserve HiTL for actions that actually need it.

Solution: audit your approval gates. Remove any that don't catch real errors.

## When to Use Each Pattern

### Approval Gates
- **Use for**: irreversible actions, external communications, production changes.
- **Don't use for**: read-only actions, reversible writes, low-stakes decisions.

### Interactive Refinement
- **Use for**: creative content (emails, documents, code) where human polish adds value.
- **Don't use for**: structured data extraction, classification, routing.

### Escalation
- **Use for**: ambiguous requests, low-confidence situations, out-of-scope queries.
- **Don't use for**: clear, in-scope, high-confidence requests.

### Supervision
- **Use for**: new agent deployments, high-stakes environments, complex tasks.
- **Don't use for**: mature, well-tested agents doing routine work.

## See Also

- [[08 - Autonomous Agent Lifecycles]] — how HiTL fits into the agent lifecycle
- [[07 - Planner-Executor Pattern]] — planner-executor with HiTL gates
- [[03 - LangGraph]] — first-class HiTL support via `interrupt_before`
- [[09 - AutoGen]] — multi-agent with HiTL
- [[10 - CrewAI]] — HiTL via split runs
- [[05 - Reflection]] — agents that self-critique (reduces HiTL need)
- [[15 - AI Agents/MOC|15 AI Agents MOC]]


## Interview Questions

1. **Q: What are the four HiTL patterns and when do you use each?**
   A: (1) **Approval gates** — pause before critical actions (irreversible, external communication). (2) **Interactive refinement** — human edits the agent's draft (creative content, emails, code). (3) **Escalation** — agent autonomously asks for help (ambiguity, low confidence, out-of-scope). (4) **Supervision** — human monitors and intervenes at will (new deployments, high-stakes). Most production agents use approval gates for critical actions and supervision for new deployments.

2. **Q: What is approval fatigue and how do you prevent it?**
   A: If every action requires approval, humans start rubber-stamping — clicking "Approve" without reading. This provides no safety benefit. Prevent by: (1) minimizing approval gates — only for genuinely critical actions; (2) calibrating thresholds — if an action is approved 99% of the time, remove the gate; (3) providing context — show what, why, and consequences so the human can make an informed decision.

3. **Q: How does LangGraph implement HiTL?**
   A: Via `interrupt_before` — compile the graph with a list of nodes that should pause before execution. When the agent reaches an interrupt node, it pauses and persists state via the checkpointer. The human reviews the proposed action and resumes (approve) or stops (reject). The `thread_id` identifies the conversation, so multiple users can have independent HiTL sessions. The checkpointer ensures state survives across the pause.

4. **Q: How do you calibrate approval thresholds over time?**
   A: Track approval/rejection rates per action type. If an action is approved 99% of the time, remove the approval gate (it's just friction). If rejected 50% of the time, the agent is making bad proposals — improve the agent. This calibration is the key to scaling HiTL: start with many gates, remove them as the agent earns trust. The goal is to approve only the actions that genuinely need human judgment.

5. **Q: What is the difference between escalation and approval gates?**
   A: Approval gates: the agent always pauses at predefined points (before critical actions). The human knows when to expect a pause. Escalation: the agent autonomously decides to ask for help (when confidence is low, request is ambiguous, or situation is out-of-scope). The human doesn't know when the agent will escalate. Escalation is more sophisticated — it requires the agent to have reliable confidence estimates.

6. **Q: Why is audit logging essential for HiTL?**
   A: Log every approval, rejection, and modification: who, what, when, why. This is essential for: (1) compliance — regulated industries require audit trails; (2) improvement — patterns of rejection reveal what the agent does wrong; (3) accountability — if something goes wrong, you need to know who approved it. Without logging, HiTL is a black box — you can't tell if it's working or if humans are rubber-stamping.

## Connection to Other Concepts

- [[15 - AI Agents/Autonomy/08 - Autonomous Agent Lifecycles|Autonomous Agent Lifecycles]] — HiTL fits into the lifecycle.
- [[15 - AI Agents/Planning/07 - Planner-Executor Pattern|Planner-Executor]] — HiTL gates in planner-executor.
- [[25 - Frameworks and Tools/Agent Frameworks/03 - LangGraph|LangGraph]] — first-class HiTL via `interrupt_before`.
- [[25 - Frameworks and Tools/Agent Frameworks/09 - AutoGen|AutoGen]] — multi-agent with HiTL.
- [[25 - Frameworks and Tools/Agent Frameworks/10 - CrewAI|CrewAI]] — HiTL via split runs.
- [[15 - AI Agents/Patterns/05 - Reflection|Reflection]] — reduces HiTL need by self-correcting.
- [[22 - Production AI/Security/01 - LLM Security and Prompt Injection|LLM Security]] — HiTL as a security measure.
- [[22 - Production AI/Architecture/03 - Gateway and Router Patterns|Gateway Patterns]] — approval gates as middleware.
