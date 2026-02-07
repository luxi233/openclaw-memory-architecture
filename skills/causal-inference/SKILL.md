---
name: causal-inference
description: "Add causal reasoning to agent actions. Predict outcomes, not just pattern-match correlations. Part of the Hal Stack 🦞"
metadata:
  openclaw:
    emoji: "🎯"
    version: "1.0.0"
    author: "OpenClaw Community"
    requires:
      os: ["darwin", "linux"]
    tags: ["reasoning", "causal", "prediction", "decision"]
---

# causal-inference 🎯

**Causal reasoning and outcome prediction for AI agents.**

Predict what will happen when you take action, not just pattern-match correlations.

## Overview

Traditional AI relies on **correlations** (patterns that happen together). causal-inference adds **causality** (what causes what), allowing your agent to:

- ✅ Predict outcomes before acting
- ✅ Debug failures by tracing causal chains
- ✅ Learn from history to improve decisions
- ✅ Avoid repeating mistakes

## Core Invariant

**Every action must be representable as an explicit intervention on a causal model, with:**

1. **Predicted effects** - What will happen?
2. **Uncertainty bounds** - How confident are we?
3. **Falsifiable audit trail** - Can we verify this prediction?

## When to Trigger

Trigger on **ANY high-level action**, including:

### Communication

| Action | Example |
|--------|---------|
| Send email | `send_email(recipient="client", subject="follow-up")` |
| Send message | `send_message(platform="slack", channel="team")` |
| Reply | `reply(thread_id="123", tone="formal")` |
| Follow-up | `follow_up(days=3, previous_touches=2)` |

### Calendar

| Action | Example |
|--------|---------|
| Create meeting | `create_meeting(title="sync", duration=30)` |
| Move meeting | `move_meeting(from="9am", to="2pm")` |
| Cancel meeting | `cancel_meeting(reason="conflict")` |
| Set reminder | `set_reminder(when="tomorrow", task="review")` |

### Tasks

| Action | Example |
|--------|---------|
| Create task | `create_task(title="write doc", priority="high")` |
| Complete task | `complete_task(task_id="123")` |
| Defer task | `defer_task(task_id="123", to="next_week")` |
| Assign task | `assign_task(to="john", task="bug_fix")` |

### Files & System

| Action | Example |
|--------|---------|
| Create file | `create_file(path="notes.md")` |
| Edit file | `edit_file(path="config.json", content="...")` |
| Deploy | `deploy(environment="prod")` |
| Config change | `update_config(key="timeout", value=30)` |

## Workflow

### Before Every Action

```
1. Log pre_state (what's the situation now?)
2. Query causal model: What's the predicted outcome?
3. If uncertainty > threshold → Confirm with user
4. If expected harm > threshold → Escalate or refuse
```

### After Every Action

```
1. Log action + context + timestamp
2. Set reminder to check outcome (if not immediate)
```

### When Outcome is Observed

```
1. Log post_state + outcome
2. Update action log
3. Re-estimate treatment effects (if enough new data)
```

## Architecture

### A. Action Log

Store in `memory/causal/action_log.jsonl`:

```json
{
  "action": "send_followup_email",
  "domain": "email",
  "context": {
    "recipient_type": "warm_lead",
    "prior_touches": 2,
    "days_since_contact": 7
  },
  "pre_state": {
    "days_since_last_contact": 7,
    "previous_response": "positive"
  },
  "post_state": {
    "reply_received": true,
    "reply_delay_hours": 4
  },
  "outcome": "positive_reply",
  "outcome_observed_at": "2025-01-26T14:00:00Z",
  "predicted_outcome": {
    "probability": 0.35,
    "uncertainty": 0.15
  },
  "backfilled": false
}
```

### B. Causal Graphs

Store in `memory/causal/graphs/`:

```yaml
# email.yaml
email:
  nodes:
    send_time:
      type: categorical
      values: [morning, afternoon, evening]
    subject_style:
      type: categorical
      values: [short, long, question, direct]
    recipient_type:
      type: categorical
      values: [new, warm, cold, vip]
  
  edges:
    - source: send_time
      target: reply_probability
      effect: "Morning sends have 35% higher reply rate"
    
    - source: subject_style
      target: open_rate
      effect: "Questions in subject increase open rate by 20%"
    
    - source: recipient_type
      target: reply_probability
      effect: "Warm leads reply 2x more than cold"

# calendar.yaml
calendar:
  nodes:
    meeting_time:
      type: time
    attendee_count:
      type: integer
      range: [1, 20]
    buffer_time:
      type: integer
      range: [0, 60]
  
  edges:
    - source: meeting_time
      target: attendance_rate
      effect: "Morning meetings have 15% higher attendance"
    
    - source: attendee_count
      target: slip_risk
      effect: "Each additional attendee adds 5% slip risk"
```

### C. Treatment Effects

Store in `memory/causal/estimates/`:

```yaml
# email-send_time-reply_probability.yaml
treatment: send_time
outcome: reply_probability

estimates:
  morning:
    mean: 0.35
    std: 0.08
    n_samples: 150
  
  afternoon:
    mean: 0.28
    std: 0.07
    n_samples: 120
  
  evening:
    mean: 0.22
    std: 0.09
    n_samples: 80
```

## Usage Examples

### Predict Before Acting

```python
from causal import CausalModel

# Initialize
causal = CausalModel()

# Before sending an email
prediction = causal.predict(
    action="send_email",
    context={
        "recipient_type": "warm_lead",
        "send_time": "morning",
        "subject_style": "question"
    }
)

print(f"Reply probability: {prediction.probability:.1%}")
print(f"Uncertainty: {prediction.uncertainty:.1%}")

# Decision: proceed if uncertainty < 30%
if prediction.uncertainty < 0.3:
    proceed_with_email()
else:
    ask_user_for_confirmation()
```

### Debug a Failure

```python
# Something went wrong - trace the cause
analysis = causal.debug(
    action="send_followup",
    expected_outcome="positive_reply",
    actual_outcome="no_response"
)

# Returns causal chain:
# 1. Follow-up sent at 8pm (evening)
# 2. Evening sends have 50% lower response rate
# 3. Root cause: timing
# 4. Recommendation: Send between 9am-11am
```

### Learn from History

```python
# After observing outcomes, update estimates
causal.update_estimates(
    action="send_email",
    context={"send_time": "morning"},
    outcome="positive_reply"
)

# Query learned patterns
pattern = causal.query_pattern(
    treatment="send_time",
    outcome="reply_probability"
)
```

## Configuration

### Config File

```yaml
# memory/causal/config.yaml
domains:
  - email
  - calendar
  - messaging
  - tasks
  - files

thresholds:
  max_uncertainty: 0.3        # Don't act if P(outcome) uncertain > 30%
  min_expected_utility: 0.1    # Don't act if expected gain < 10%

protected_actions:
  - delete_email              # Requires user approval
  - cancel_meeting            # Requires user approval
  - send_to_new_contact      # Requires user approval
  - financial_transaction    # Requires user approval
  - delete_file               # Requires user approval
  - git_force_push           # Requires user approval

graphs_dir: memory/causal/graphs/
estimates_dir: memory/causal/estimates/
action_log: memory/causal/action_log.jsonl
```

## Setup

### 1. Create Directory Structure

```bash
mkdir -p memory/causal/{graphs,estimates}
touch memory/causal/action_log.jsonl
```

### 2. Create Config

```bash
cp config/causal-config.yaml memory/causal/config.yaml
```

### 3. Configure OpenClaw

```json
{
  "skills": {
    "entries": {
      "causal-inference": {
        "enabled": true
      }
    }
  }
}
```

## Safety Constraints

### Protected Actions

These actions **require explicit user approval**:

```yaml
protected_actions:
  - delete_email: "Deleting emails permanently"
  - cancel_meeting: "Cancelling scheduled meetings"
  - send_to_new_contact: "First contact with new recipient"
  - financial_transaction: "Any monetary transaction"
  - delete_file: "Permanent file deletion"
  - git_force_push: "Rewriting git history"
```

### Uncertainty Thresholds

```yaml
thresholds:
  max_uncertainty: 0.3        # 30% uncertainty ceiling
  min_expected_utility: 0.1   # 10% minimum expected gain
```

When uncertainty > 30% or expected utility < 10%:
1. Log the situation
2. Ask user for confirmation
3. Proceed only with approval

## Example Causal Graphs

### Email Domain

```
send_time → reply_probability
    │
    └── Morning: 35% reply rate
    └── Afternoon: 28% reply rate
    └── Evening: 22% reply rate

subject_style → open_rate
    │
    └── Question: 45% open rate
    └── Direct: 38% open rate
    └── Long: 25% open rate

recipient_type → reply_probability
    │
    └── Warm: 40% reply rate
    └── New: 25% reply rate
    └── Cold: 15% reply rate
```

### Calendar Domain

```
meeting_time → attendance_rate
    │
    └── 9am: 95% attendance
    └── 2pm: 85% attendance
    └── 5pm: 70% attendance

attendee_count → slip_risk
    │
    └── 1-3 people: 10% slip risk
    └── 4-6 people: 25% slip risk
    └── 7+ people: 45% slip risk
```

### Task Domain

```
due_date_proximity → completion_probability
    │
    └── >1 week: 90% completion
    └── 1-7 days: 75% completion
    └── <1 day: 50% completion

context_switches → error_rate
    │
    └── 0-2 switches: 5% error rate
    └── 3-5 switches: 15% error rate
    └── 6+ switches: 35% error rate
```

## Files

- `memory/causal/action_log.jsonl` - All logged actions
- `memory/causal/graphs/` - Domain-specific causal graphs
- `memory/causal/estimates/` - Learned treatment effects
- `memory/causal/config.yaml` - Safety thresholds and config

## Related

- Part of the **Hal Stack** 🦞
- Works with [bulletproof-memory](...) for context protection
- Works with [agent-memory](...) for persistent learning

---

*Built with ❤️ by the OpenClaw community*
