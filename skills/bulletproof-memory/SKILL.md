---
name: bulletproof-memory
description: "Never lose context again. The Write-Ahead Log (WAL) protocol with SESSION-STATE.md gives your agent bulletproof memory that survives compaction, restarts, and distractions. Part of the Hal Stack 🦞"
metadata:
  openclaw:
    emoji: "🛡️"
    version: "1.0.0"
    author: "Hal The Lobster"
    requires:
      os: ["darwin", "linux"]
    tags: ["memory", "context", "wal", "persistence"]
---

# bulletproof-memory 🛡️

**Bulletproof context protection using Write-Ahead Log (WAL) protocol.**

Never lose your agent's context again!

## Overview

The Write-Ahead Log (WAL) protocol ensures that every piece of context is persisted **before** it's needed, not after. This means your agent can survive:

- ✅ Context compression
- ✅ Session restarts
- ✅ Unexpected interruptions
- ✅ Distractions and topic changes

## How It Works

### The WAL Protocol

```
User Input → Write to SESSION-STATE.md → Respond to User
```

**Key Rule**: Always write to `SESSION-STATE.md` BEFORE responding to the user.

### When to Write

Write to `SESSION-STATE.md` when the user provides:

- ✅ Names (people, places, projects)
- ✅ Decisions (what was decided and why)
- ✅ Corrections (clarifications and corrections)
- ✅ Preferences (likes, dislikes, requirements)
- ✅ Open threads (unfinished tasks, pending items)

### SESSION-STATE.md Template

Create `~/.openclaw/workspace/SESSION-STATE.md`:

```markdown
# Current Task
Brief description of what we're working on

# Immediate Context
Key information that must not be lost

# Recent Decisions
- Decision 1: Reason
- Decision 2: Reason

# Open Threads
- Thread 1: What's pending
- Thread 2: What's pending

# Key Files
- /path/to/file1
- /path/to/file2

# User Preferences
- Prefers concise responses
- Likes technical details
```

## Session Start Protocol

When a session begins:

1. **FIRST**: Read `SESSION-STATE.md` (highest priority)
2. **SECOND**: Read `SOUL.md`, `USER.md`
3. **THIRD**: Read today's daily notes
4. **FOURTH**: Load `MEMORY.md`

## Integration with OpenClaw

### Enable in openclaw.json

```json
{
  "skills": {
    "entries": {
      "bulletproof-memory": {
        "enabled": true
      }
    }
  }
}
```

## Usage Examples

### Basic Usage

```bash
# Read current state
cat ~/.openclaw/workspace/SESSION-STATE.md

# Update state manually
echo -e "\n- New decision: Use bulletproof-memory" >> ~/.openclaw/workspace/SESSION-STATE.md
```

### Programmatic Usage

```python
import json
from pathlib import Path

SESSION_STATE_FILE = Path("~/.openclaw/workspace/SESSION-STATE.md")

def update_session_state(task: str, context: str, decisions: list):
    """Update the session state file."""
    state = {
        "task": task,
        "context": context,
        "decisions": decisions,
        "updated_at": datetime.now().isoformat()
    }
    
    # Write to file
    SESSION_STATE_FILE.write_text(f"""# Current Task
{task}

# Immediate Context
{context}

# Recent Decisions
{chr(10).join(f'- {d}' for d in decisions)}
""")

def read_session_state():
    """Read and parse the session state."""
    if SESSION_STATE_FILE.exists():
        return SESSION_STATE_FILE.read_text()
    return None
```

## Session Recovery Protocol

When context is lost (compaction, restart):

1. **Read SESSION-STATE.md** - This has the active task state
2. **Read today's + yesterday's daily notes** - For additional context
3. **Use memory_search** - Semantic search for missing context
4. **Present**: "Recovered from SESSION-STATE.md. Last task was X. Continue?"

## Memory Flush Protocol

Monitor context usage. Flush important context before compaction:

| Context % | Action |
|-----------|--------|
| < 50% | Normal operation |
| 50-70% | Write key points after substantial exchanges |
| 70-85% | Active flushing — write everything important NOW |
| > 85% | Emergency flush — full summary before next response |

## Files

- `SESSION-STATE.md` - Active task working memory (create this)
- `SKILL.md` - This documentation

## Related

- Part of the **Hal Stack** 🦞
- Works with [agent-memory](...) for cross-session persistence
- Complements [memory-manager](...) for long-term memory

---

*Built with ❤️ by the OpenClaw community*
