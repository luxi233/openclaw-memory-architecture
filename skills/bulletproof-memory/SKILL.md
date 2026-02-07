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

## Table of Contents

- [Installation](#installation)
- [Configuration](#configuration)
- [Usage Examples](#usage-examples)
- [API Reference](#api-reference)
- [Protocols](#protocols)
- [Files](#files)

---

## Installation

### Option 1: Clone Repository

```bash
# Clone the skill
git clone https://github.com/infinitelab/openclaw-memory-architecture.git
cd openclaw-memory-architecture/skills/bulletproof-memory

# Copy to OpenClaw skills directory
cp -r bulletproof-memory ~/.openclaw/workspace/skills/
```

### Option 2: Copy Files Manually

```bash
# Create skill directory
mkdir -p ~/.openclaw/workspace/skills/bulletproof-memory

# Copy SKILL.md
cp SKILL.md ~/.openclaw/workspace/skills/bulletproof-memory/

# Create SESSION-STATE.md template
cat > ~/.openclaw/workspace/SESSION-STATE.md << 'EOF'
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
EOF
```

### Enable in OpenClaw

Edit `~/.openclaw/openclaw.json`:

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

Then restart OpenClaw:

```bash
openclaw gateway restart
```

---

## Configuration

### openclaw.json Configuration

```json
{
  "skills": {
    "entries": {
      "bulletproof-memory": {
        "enabled": true,
        "options": {
          "auto_write": true,
          "recovery_enabled": true,
          "backup_interval": 30
        }
      }
    }
  }
}
```

### Configuration Options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `enabled` | boolean | `true` | Enable/disable the skill |
| `auto_write` | boolean | `true` | Auto-write on user input |
| `recovery_enabled` | boolean | `true` | Enable context recovery |
| `backup_interval` | integer | `30` | Backup interval in minutes |

### Environment Variables

```bash
# Session state file path
export BULLETPROOF_STATE_FILE=~/.openclaw/workspace/SESSION-STATE.md

# Enable auto-write
export BULLETPROOF_AUTO_WRITE=true
```

---

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
from datetime import datetime

# Expand user path correctly
SESSION_STATE_FILE = Path("~/.openclaw/workspace/SESSION-STATE.md").expand()

def update_session_state(task: str, context: str, decisions: list):
    """Update the session state file."""
    state = {
        "task": task,
        "context": context,
        "decisions": decisions,
        "updated_at": datetime.now().isoformat()
    }
    
    # Write to file
    content = f"""# Current Task
{task}

# Immediate Context
{context}

# Recent Decisions
"""
    for d in decisions:
        content += f"- {d}\n"
    
    content += f"""
# Updated At
{datetime.now().isoformat()}
"""
    
    SESSION_STATE_FILE.write_text(content)
    print(f"✅ Session state updated: {SESSION_STATE_FILE}")

def read_session_state():
    """Read and parse the session state."""
    if SESSION_STATE_FILE.exists():
        content = SESSION_STATE_FILE.read_text()
        print(f"✅ Read {len(content)} bytes from session state")
        return content
    return None
```

### Auto-Write Example

```python
def wal_write_on_input(user_input: str, current_state: dict):
    """
    Write-Ahead Log Protocol:
    Always write BEFORE responding to user.
    """
    # 1. Extract important info from user input
    important_info = extract_important_info(user_input)
    
    # 2. Update session state
    current_state.update(important_info)
    
    # 3. Write to SESSION-STATE.md (BEFORE responding)
    write_session_state(current_state)
    
    # 4. Now respond to user
    return generate_response(user_input)
```

---

## API Reference

### Functions

#### `update_session_state(task, context, decisions)`

Update the session state file.

**Parameters:**
- `task` (str): Current task description
- `context` (str): Immediate context
- `decisions` (list): List of recent decisions

**Example:**
```python
update_session_state(
    task="Set up memory architecture",
    context="Installing bulletproof-memory skill",
    decisions=[
        "Decision: Use WAL protocol for context protection",
        "Decision: Enable auto-recovery"
    ]
)
```

#### `read_session_state()`

Read and parse the session state.

**Returns:**
- `dict` or `None`: Session state dictionary, or None if file doesn't exist

**Example:**
```python
state = read_session_state()
if state:
    print(f"Current task: {state.get('task')}")
```

#### `backup_session_state()`

Create a timestamped backup of the session state.

**Example:**
```python
backup_path = backup_session_state()
print(f"Backup created: {backup_path}")
```

#### `restore_session_state(backup_path)`

Restore session state from a backup file.

**Parameters:**
- `backup_path` (str): Path to backup file

**Example:**
```python
restore_session_state("/path/to/backup/SESSION-STATE.md.backup")
```

---

## Protocols

### Session Start Protocol

When a session begins:

1. **FIRST**: Read `SESSION-STATE.md` (highest priority)
2. **SECOND**: Read `SOUL.md`, `USER.md`
3. **THIRD**: Read today's daily notes
4. **FOURTH**: Load `MEMORY.md`

### Session Recovery Protocol

When context is lost (compaction, restart):

1. **Read SESSION-STATE.md** - This has the active task state
2. **Read today's + yesterday's daily notes** - For additional context
3. **Use memory_search** - Semantic search for missing context
4. **Present**: "Recovered from SESSION-STATE.md. Last task was X. Continue?"

### Memory Flush Protocol

Monitor context usage. Flush important context before compaction:

| Context % | Action |
|-----------|--------|
| < 50% | Normal operation |
| 50-70% | Write key points after substantial exchanges |
| 70-85% | Active flushing — write everything important NOW |
| > 85% | Emergency flush — full summary before next response |

---

## Files

- `SESSION-STATE.md` - Active task working memory (create this)
- `SKILL.md` - This documentation

---

## Related

- Part of the **Hal Stack** 🦞
- Works with [agent-memory](...) for cross-session persistence
- Complements [memory-manager](...) for long-term memory

---

*Built with ❤️ by the OpenClaw community*
