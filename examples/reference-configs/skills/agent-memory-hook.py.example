#!/usr/bin/env python3
"""
AgentMemory Session Hooks
Automated memory loading/saving for OpenClaw sessions.

Usage:
    agent-memory-hook start   # Session start - load memories
    agent-memory-hook end    # Session end - prompt for summary
"""

import sys
import os

# Add agent-memory to path
AGENT_MEMORY_PATH = "/Users/infinitelab/.openclaw/workspace/skills/agent-memory/src"
sys.path.insert(0, AGENT_MEMORY_PATH)

from agent_memory import AgentMemory

def session_start():
    """Load relevant memories at session start."""
    mem = AgentMemory()
    
    print("=== AgentMemory Session Start ===\n")
    
    # Load recent lessons
    lessons = mem.get_lessons(limit=10)
    if lessons:
        print("📚 Recent Lessons:")
        for i, lesson in enumerate(lessons, 1):
            print(f"  {i}. [{lesson.outcome}] {lesson.context}: {lesson.insight[:50]}...")
    
    # Load entities
    print("\n👤 Tracked Entities:")
    stats = mem.stats()
    print(f"   Facts: {stats['active_facts']}, Entities: {stats['entities']}")
    
    print("\n✓ Memory loaded. Use mem.remember() and mem.learn() during session.")

def session_end():
    """Prompt for session summary at end."""
    mem = AgentMemory()
    
    print("\n=== AgentMemory Session End ===")
    print("Consider storing:")
    print("  1. Key decisions made")
    print("  2. Lessons learned")
    print("  3. User preferences expressed")
    print("  4. Important facts mentioned")
    
    print("\nExample:")
    print('  mem.remember("User mentioned preference for concise updates", tags=["preference"])')
    print('  mem.learn(action="Did X", context="situation", outcome="positive", insight="Learned Y")')
    
    print("\n✓ End of session hook ready.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: agent-memory-hook [start|end]")
        sys.exit(1)
    
    if sys.argv[1] == "start":
        session_start()
    elif sys.argv[1] == "end":
        session_end()
    else:
        print(f"Unknown command: {sys.argv[1]}")
        sys.exit(1)
