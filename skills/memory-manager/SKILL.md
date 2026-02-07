---
name: memory-manager
description: "Three-tier memory management: Episodic, Semantic, and Procedural memories. Organize knowledge like a human brain."
metadata:
  openclaw:
    emoji: "📚"
    version: "1.0.0"
    author: "OpenClaw Community"
    requires:
      os: ["darwin", "linux"]
    tags: ["memory", "knowledge", "organization", "three-tier"]
---

# memory-manager 📚

**Three-tier memory management system.**

Organize knowledge into three layers: Episodic (what happened), Semantic (what we know), and Procedural (how to do).

## Overview

memory-manager provides **human-like memory organization**:

| Tier | Type | Contents | Example |
|------|------|---------|---------|
| **Episodic** | Events | Daily logs, conversations | "We worked on the API today" |
| **Semantic** | Knowledge | Facts, concepts, topics | "REST APIs use HTTP methods" |
| **Procedural** | Skills | Workflows, processes, how-tos | "How to deploy to production" |

## Installation

### Option 1: Clone Repository

```bash
# Clone the skill
git clone https://github.com/infinitelab/openclaw-memory-architecture.git
cd openclaw-memory-architecture/skills/memory-manager

# Copy to OpenClaw skills directory
cp -r memory-manager ~/.openclaw/workspace/skills/
```

### Option 2: Copy Files Manually

```bash
# Create skill directory
mkdir -p ~/.openclaw/workspace/skills/memory-manager

# Copy SKILL.md
cp SKILL.md ~/.openclaw/workspace/skills/memory-manager/

# Create memory directories
mkdir -p ~/.openclaw/workspace/memory/{episodic,semantic,procedural}

# Initialize directory structure
cat > ~/.openclaw/workspace/memory-manager/init.sh << 'EOF'
#!/bin/bash
# Initialize memory-manager directories

# Create episodic directory
mkdir -p memory/episodic

# Create semantic subdirectories
mkdir -p memory/semantic/{topics,concepts,entities}

# Create procedural subdirectories
mkdir -p memory/procedural/{workflows,checklists,automation}

# Create state file
cat > memory/.memory-manager-state.json << 'JSON'
{
  "version": "1.0.0",
  "initialized_at": "$(date -Iseconds)",
  "last_backup": null
}
JSON

echo "✅ Memory directories initialized"
EOF

chmod +x ~/.openclaw/workspace/memory-manager/init.sh
```

### Enable in OpenClaw

Edit `~/.openclaw/openclaw.json`:

```json
{
  "skills": {
    "entries": {
      "memory-manager": {
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

### Initialize Memory Directories

```bash
# Run initialization script
~/.openclaw/workspace/memory-manager/init.sh
```

---

## Why Three-Tier?

### 1. Episodic Memory (What Happened)

- **When**: Time-stamped events
- **What**: Specific occurrences
- **Where**: Context and location

**Use for**: Daily logs, conversation history, task tracking

### 2. Semantic Memory (What We Know)

- **Facts**: "Paris is the capital of France"
- **Concepts**: "RESTful API principles"
- **Topics**: "Machine learning techniques"
- **Relationships**: How things connect

**Use for**: Knowledge base, FAQs, documentation

### 3. Procedural Memory (How To Do)

- **Workflows**: "How to set up development environment"
- **Processes**: "Code review checklist"
- **Recipes**: "Steps to deploy"
- **Muscle memory**: Automated routines

**Use for**: Standard operating procedures, automation

## Directory Structure

```
memory/
├── episodic/                    # What happened
│   └── YYYY-MM-DD.md           # Daily logs (raw)
│
├── semantic/                    # What we know
│   ├── topics/                 # Topic-based knowledge
│   │   ├── programming/
│   │   ├── devops/
│   │   └── ai-ml/
│   │
│   ├── concepts/               # Concept explanations
│   │   ├── oop.md
│   │   └── rest-api.md
│   │
│   └── entities/               # Entity definitions
│       ├── users.md
│       └── projects.md
│
└── procedural/                  # How to do
    ├── workflows/              # Step-by-step guides
    │   ├── setup-dev-env.md
    │   ├── deploy-app.md
    │   └── debug-issues.md
    │
    ├── checklists/            # Checklist items
    │   ├── code-review.md
    │   └── security-review.md
    │
    └── automation/             # Automated routines
        ├── daily-backup.sh
        └── sync-config.sh
```

## Quick Start

### Initialize memory-manager

```bash
# Initialize directory structure
~/.openclaw/workspace/skills/memory-manager/init.sh

# This creates:
# - memory/ (if not exists)
# - episodic/, semantic/, procedural/ subdirectories
# - Templates for each type
```

### Create a Daily Note (Episodic)

```markdown
# 2024-01-26

## Tasks Completed
- [x] Set up development environment
- [x] Implement user authentication
- [x] Write unit tests

## Decisions Made
- Use PostgreSQL for primary database
- Implement JWT for authentication

## Open Threads
- Need to design the API endpoints
- Waiting for design review feedback

## Notes
- Discovered a useful library: pydantic
- Remember to update documentation
```

### Add Semantic Knowledge

```markdown
# Topic: REST API Best Practices

## Core Principles
- **Stateless**: Each request contains all necessary information
- **Resource-based**: Use nouns, not verbs (e.g., `/users` not `/getUsers`)
- **HTTP methods**: GET (read), POST (create), PUT/PATCH (update), DELETE (remove)

## Status Codes
- 200: OK
- 201: Created
- 400: Bad Request
- 401: Unauthorized
- 404: Not Found
- 500: Internal Server Error

## Best Practices
1. Use versioning (/v1/users)
2. Pagination for lists
3. Filtering and sorting
4. Consistent error format
```

### Document a Workflow (Procedural)

```markdown
# Workflow: Deploy Application to Production

## Prerequisites
- [ ] All tests passing
- [ ] Code review approved
- [ ] Security review completed
- [ ] Configuration updated for production

## Steps

### 1. Prepare Release
```bash
git checkout main
git pull origin main
git tag v1.2.3
```

### 2. Build Container
```bash
docker build -t myapp:v1.2.3 .
docker tag myapp:v1.2.3 registry/myapp:latest
docker push registry/myapp:v1.2.3
```

### 3. Deploy
```bash
kubectl set image deployment/myapp app=registry/myapp:v1.2.3
kubectl rollout status deployment/myapp
```

### 4. Verify
- [ ] Health check passes
- [ ] Logs show no errors
- [ ] Metrics are normal
```

## Usage Examples

### Daily Workflow

```python
from datetime import datetime
from pathlib import Path

def start_day():
    """Start a new day - create daily note."""
    today = datetime.now().strftime("%Y-%m-%d")
    path = Path(f"memory/episodic/{today}.md")
    
    if not path.exists():
        path.write_text(f"""# {today}

## Tasks Completed

## Decisions Made

## Open Threads

## Notes

""")

def add_entry(category: str, entry: str):
    """Add entry to today's note."""
    today = datetime.now().strftime("%Y-%m-%d")
    path = Path(f"memory/episodic/{today}.md")
    
    section = f"## {category}\n- {entry}\n"
    
    with open(path, "a") as f:
        f.write(section)
```

### Search Semantic Memory

```bash
# Search for a topic
~/.openclaw/workspace/skills/memory-manager/search.sh semantic "REST API"

# Search for a concept
~/.openclaw/workspace/skills/memory-manager/search.sh concept "authentication"

# Search all semantic memory
~/.openclaw/workspace/skills/memory-manager/search.sh semantic "deploy*"
```

### Run a Workflow

```bash
# Run a procedural workflow
~/.openclaw/workspace/skills/memory-manager/run.sh deploy-app

# This executes the steps in memory/procedural/workflows/deploy-app.md
```

## Integration

### With bulletproof-memory

```
Session End:
  1. Write key points → SESSION-STATE.md
  2. Update daily note → memory/episodic/YYYY-MM-DD.md
  3. Add to knowledge base → memory/semantic/
```

### With agent-memory

```
Daily Review:
  1. Extract key learnings → agent-memory
  2. Organize into semantic memory → memory-manager
  3. Index for search → QMD
```

## Commands

### Initialization

```bash
# Initialize memory directories
memory-manager init

# Create from template
memory-manager create --type episodic --name "2024-01-26"
memory-manager create --type semantic --name "topics/rest-api"
memory-manager create --type procedural --name "workflows/deploy"
```

### Search

```bash
# Search all memory
memory-manager search "authentication"

# Search specific tier
memory-manager search --episodic "yesterday"
memory-manager search --semantic "REST"
memory-manager search --procedural "deploy"

# Search with filters
memory-manager search --type md --tag "best-practice" "API"
```

### Maintenance

```bash
# Detect compression risk
memory-manager detect

# Archive old notes
memory-manager archive --older-than 30d

# Generate index
memory-manager index --rebuild

# Check storage usage
memory-manager stats
```

## Benefits

| Benefit | Description |
|---------|-------------|
| **Organization** | Clear structure for different memory types |
| **Searchability** | Easy to find information |
| **Discoverability** | New insights from connections |
| **Persistence** | Survives session restarts |
| **Growth** | Knowledge base grows over time |

## Best Practices

1. **Daily Notes**: Write every session
2. **Knowledge Base**: Add insights when learned
3. **Workflows**: Document reusable processes
4. **Review Weekly**: Consolidate and organize
5. **Tag Everything**: Use tags for cross-referencing

---

*Built with ❤️ by the OpenClaw community*
