---
name: agent-memory
description: "Persistent cross-session memory for AI agents using SQLite. Remember facts, learn from lessons, track entities across all conversations."
metadata:
  openclaw:
    emoji: "🗄️"
    version: "1.0.0"
    author: "OpenClaw Community"
    requires:
      os: ["darwin", "linux"]
    tags: ["memory", "sqlite", "persistence", "facts", "lessons"]
---

# agent-memory 🗄️

**Persistent cross-session memory using SQLite.**

Remember important facts, learn from successes and failures, and track entities across all conversations.

## Overview

agent-memory provides **cross-session persistence** that survives:
- ✅ Session restarts
- ✅ System reboots
- ✅ Context compression
- ✅ Memory limits

## Installation

### Install from Source

```bash
# Clone the repository
git clone https://github.com/openclaw/skills/tree/main/skills/agent-memory.git
cd agent-memory

# Install dependencies
pip install -r requirements.txt

# Install the package
pip install -e .
```

### Configure OpenClaw

```json
{
  "skills": {
    "entries": {
      "agent-memory": {
        "enabled": true
      }
    }
  }
}
```

## Quick Start

### Basic Usage

```python
from agent_memory import AgentMemory

# Initialize
mem = AgentMemory()

# Session Start: Load relevant memories
lessons = mem.get_lessons(limit=10)
entities = mem.get_entity("user_name")

# During Session: Store important info
mem.remember("User prefers concise updates", tags=["preference"])

mem.learn(
    action="What was done",
    context="situation",
    outcome="positive",  # or "negative"
    insight="What was learned"
)

# Session End: Summarize and persist
mem.remember("Today's key points", tags=["summary"])
```

## Core Functions

### Remember Facts

```python
# Remember a single fact
mem.remember(
    "User prefers concise responses",
    tags=["preference", "communication"]
)

# Remember with entities
mem.remember(
    "User John works at Company X",
    entities={"name": "John", "company": "Company X"},
    tags=["person", "work"]
)
```

### Learn from Experience

```python
# Record a positive outcome
mem.learn(
    action="Used short paragraphs",
    context="User asked for summary",
    outcome="positive",
    insight="User appreciated the concise format"
)

# Record a negative outcome
mem.learn(
    action="Sent long detailed email",
    context="Following up with client",
    outcome="negative",
    insight="User didn't read the full email, should use bullet points"
)
```

### Recall and Search

```python
# Search memories
facts = mem.recall("user preferences communication")

# Get recent lessons
lessons = mem.get_lessons(
    limit=5,
    context="email",
    outcome="negative"
)

# Get entity information
info = mem.get_entity("John")
```

### Track Entities

```python
# Update entity
mem.track_entity(
    name="John",
    attributes={
        "role": "developer",
        "company": "TechCorp",
        "timezone": "PST"
    }
)

# Get all attributes
entity = mem.get_entity("John")
print(entity.attributes)
```

## Database Schema

### Facts Table

```sql
CREATE TABLE facts (
    id INTEGER PRIMARY KEY,
    content TEXT NOT NULL,
    entities TEXT,  -- JSON
    tags TEXT,      -- JSON array
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP
);
```

### Lessons Table

```sql
CREATE TABLE lessons (
    id INTEGER PRIMARY KEY,
    action TEXT NOT NULL,
    context TEXT NOT NULL,
    outcome TEXT NOT NULL,  -- 'positive' or 'negative'
    insight TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Entities Table

```sql
CREATE TABLE entities (
    id INTEGER PRIMARY KEY,
    name TEXT UNIQUE NOT NULL,
    attributes TEXT,  -- JSON
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP
);
```

## Configuration

### Environment Variables

```bash
# Database location
export AGENT_MEMORY_DB=~/.agent-memory/memory.db

# Auto-save interval (seconds)
export AGENT_MEMORY_SAVE_INTERVAL=60

# Enable auto-learning
export AGENT_MEMORY_AUTO_LEARN=true
```

### Python Configuration

```python
from agent_memory import AgentMemory

mem = AgentMemory(
    db_path="~/.agent-memory/memory.db",
    auto_save=True,
    save_interval=60,
    auto_learn=True
)
```

## Use Cases

### Remember User Preferences

```python
# User says they prefer bullet points
mem.remember(
    "User prefers bullet points over paragraphs",
    tags=["preference", "formatting"]
)

# Later: Recall this preference
preferences = mem.recall("user prefers bullet")
# Returns: ["User prefers bullet points over paragraphs"]
```

### Learn from Failures

```python
# Something didn't work
mem.learn(
    action="Used technical jargon",
    context="Explaining to non-technical user",
    outcome="negative",
    insight="Should use simple language, avoid acronyms"
)

# Get all failures related to communication
failures = mem.get_lessons(
    context="communication",
    outcome="negative"
)
```

### Track Project Context

```python
# Track a project
mem.track_entity(
    name="Project Alpha",
    attributes={
        "status": "in progress",
        "deadline": "2026-02-15",
        "team_size": 3,
        "technologies": ["Python", "FastAPI"]
    }
)
```

## Automation Hooks

### Session Start

```python
# hooks/session_start.py
from agent_memory import AgentMemory

def on_session_start():
    mem = AgentMemory()
    
    # Load recent lessons
    lessons = mem.get_lessons(limit=10)
    
    # Load entities
    user = mem.get_entity("user")
    project = mem.get_entity("current_project")
    
    return {
        "lessons": lessons,
        "user": user,
        "project": project
    }
```

### Session End

```python
# hooks/session_end.py
from agent_memory import AgentMemory

def on_session_end(session_summary: str):
    mem = AgentMemory()
    
    # Remember key points
    mem.remember(session_summary, tags=["session_summary"])
    
    # Log any new learnings
    # (Implement based on your workflow)
```

## Integration with Other Components

### With bulletproof-memory

```
Session Start:
  1. Read SESSION-STATE.md (bulletproof-memory)
  2. Load from agent-memory (facts, lessons, entities)
```

### With memory-manager

```
Session End:
  1. Organize knowledge → memory-manager
  2. Persist facts → agent-memory
```

## Files

- `src/memory.py` - Core memory implementation
- `hooks/` - Session automation hooks
- `tests/` - Unit tests
- `requirements.txt` - Dependencies

---

*Built with ❤️ by the OpenClaw community*
