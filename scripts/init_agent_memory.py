#!/usr/bin/env python3
"""
Initialize Agent Memory Database

Creates the SQLite database and tables for agent-memory skill.
"""

import sqlite3
from pathlib import Path
from datetime import datetime


def init_agent_memory(db_path: str = "~/.agent-memory/memory.db"):
    """Initialize the agent-memory SQLite database."""
    
    # Expand path
    db_file = Path(db_path).expand()
    
    # Create directory if needed
    db_file.parent.mkdir(parents=True, exist_ok=True)
    
    # Connect to database
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    
    # Create tables
    cursor.executescript("""
        -- Facts table
        CREATE TABLE IF NOT EXISTS facts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            content TEXT NOT NULL,
            entities TEXT,  -- JSON
            tags TEXT,      -- JSON array
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        -- Lessons table
        CREATE TABLE IF NOT EXISTS lessons (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            action TEXT NOT NULL,
            context TEXT NOT NULL,
            outcome TEXT NOT NULL CHECK(outcome IN ('positive', 'negative')),
            insight TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        -- Entities table
        CREATE TABLE IF NOT EXISTS entities (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            attributes TEXT,  -- JSON
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        -- Indexes for faster queries
        CREATE INDEX IF NOT EXISTS idx_facts_tags ON facts(tags);
        CREATE INDEX IF NOT EXISTS idx_lessons_outcome ON lessons(outcome);
        CREATE INDEX IF NOT EXISTS idx_lessons_context ON lessons(context);
        CREATE INDEX IF NOT EXISTS idx_entities_name ON entities(name);
    """)
    
    conn.commit()
    
    # Print status
    print(f"✅ Agent Memory initialized at: {db_file}")
    print(f"   Tables: facts, lessons, entities")
    
    return db_file


def check_status(db_path: str = "~/.agent-memory/memory.db"):
    """Check the status of agent-memory database."""
    
    db_file = Path(db_path).expand()
    
    if not db_file.exists():
        print("❌ Database not found. Run init first.")
        return False
    
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    
    # Count records
    cursor.execute("SELECT COUNT(*) FROM facts")
    facts_count = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM lessons")
    lessons_count = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM entities")
    entities_count = cursor.fetchone()[0]
    
    print(f"📊 Agent Memory Status:")
    print(f"   Facts: {facts_count}")
    print(f"   Lessons: {lessons_count}")
    print(f"   Entities: {entities_count}")
    
    conn.close()
    return True


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "--status":
        check_status()
    else:
        init_agent_memory()
