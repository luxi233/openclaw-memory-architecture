#!/usr/bin/env python3
"""
Check the status of all memory architecture components.
"""

import sys
from pathlib import Path


def check_bulletproof_memory():
    """Check bulletproof-memory status."""
    state_file = Path("~/.openclaw/workspace/SESSION-STATE.md").expand()
    
    if state_file.exists():
        size = state_file.stat().st_size
        print(f"✅ bulletproof-memory: {state_file}")
        print(f"   Size: {size} bytes")
        return True
    else:
        print(f"⚠️ bulletproof-memory: SESSION-STATE.md not found")
        print(f"   Expected: {state_file}")
        return False


def check_agent_memory():
    """Check agent-memory status."""
    db_file = Path("~/.agent-memory/memory.db").expand()
    
    if db_file.exists():
        import sqlite3
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()
        
        try:
            cursor.execute("SELECT COUNT(*) FROM facts")
            facts = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM lessons")
            lessons = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM entities")
            entities = cursor.fetchone()[0]
            
            print(f"✅ agent-memory: {db_file}")
            print(f"   Facts: {facts}")
            print(f"   Lessons: {lessons}")
            print(f"   Entities: {entities}")
            
            conn.close()
            return True
        except Exception as e:
            print(f"❌ agent-memory error: {e}")
            conn.close()
            return False
    else:
        print(f"⚠️ agent-memory: Database not found")
        return False


def check_causal_inference():
    """Check causal-inference status."""
    memory_dir = Path("~/.openclaw/workspace/memory/causal").expand()
    
    if memory_dir.exists():
        print(f"✅ causal-inference: {memory_dir}")
        
        graphs = (memory_dir / "graphs").exists()
        estimates = (memory_dir / "estimates").exists()
        action_log = (memory_dir / "action_log.jsonl").exists()
        config = (memory_dir / "config.yaml").exists()
        
        print(f"   Graphs: {'✅' if graphs else '❌'}")
        print(f"   Estimates: {'✅' if estimates else '❌'}")
        print(f"   Action Log: {'✅' if action_log else '❌'}")
        print(f"   Config: {'✅' if config else '❌'}")
        
        return graphs and config
    else:
        print(f"⚠️ causal-inference: Directory not found")
        return False


def check_memory_manager():
    """Check memory-manager status."""
    memory_dir = Path("~/.openclaw/workspace/memory").expand()
    
    if memory_dir.exists():
        print(f"✅ memory-manager: {memory_dir}")
        
        episodic = (memory_dir / "episodic").exists()
        semantic = (memory_dir / "semantic").exists()
        procedural = (memory_dir / "procedural").exists()
        
        print(f"   Episodic: {'✅' if episodic else '❌'}")
        print(f"   Semantic: {'✅' if semantic else '❌'}")
        print(f"   Procedural: {'✅' if procedural else '❌'}")
        
        return episodic and semantic
    else:
        print(f"⚠️ memory-manager: Directory not found")
        return False


def check_qmd():
    """Check QMD status."""
    cache_dir = Path("~/.cache/qmd").expand()
    
    if cache_dir.exists():
        print(f"✅ QMD: {cache_dir}")
        
        # Check for index files
        index_files = list(cache_dir.glob("*.bin"))
        print(f"   Index files: {len(index_files)}")
        
        return True
    else:
        print(f"⚠️ QMD: Cache directory not found")
        return False


def main():
    """Check all memory components."""
    print("🧠 OpenClaw Memory Architecture Status")
    print("=" * 50)
    
    results = []
    
    results.append(("bulletproof-memory", check_bulletproof_memory()))
    print()
    
    results.append(("agent-memory", check_agent_memory()))
    print()
    
    results.append(("causal-inference", check_causal_inference()))
    print()
    
    results.append(("memory-manager", check_memory_manager()))
    print()
    
    results.append(("QMD", check_qmd()))
    print()
    
    # Summary
    print("=" * 50)
    print("📊 Summary:")
    all_passed = True
    for name, passed in results:
        status = "✅" if passed else "❌"
        print(f"   {status} {name}")
        if not passed:
            all_passed = False
    
    print()
    if all_passed:
        print("🎉 All components are healthy!")
    else:
        print("⚠️ Some components need attention")
    
    return 0 if all_passed else 1


if __name__ == "__main__":
    sys.exit(main())
