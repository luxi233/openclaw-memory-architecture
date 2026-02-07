# SESSION-STATE.md — Active Working Memory

This file is the agent's "RAM" — the hot transaction log for the current active task.
Chat history is a BUFFER. This file is STORAGE.

---

## Current Task
[What we're actively working on right now]

## Immediate Context
[Key details, decisions, corrections from this session]

## Key Files
[Paths to relevant files for this task]

## Last Updated
[Timestamp]

---

## WAL Protocol (Write-Ahead Log)

**Rule:** If user provides a concrete detail, UPDATE THIS FILE BEFORE responding.

Examples:
- Names, locations, corrections
- Decisions made
- User preferences
- Important context

**Format:** Add to "Immediate Context" with timestamp.
