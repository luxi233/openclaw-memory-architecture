# 🧠 OpenClaw Memory Architecture

<div align="center">

![Memory Architecture](docs/images/architecture.png)

**Complete Memory System for OpenClaw AI Assistant**

[English](README_EN.md) | [中文](README.md)

</div>

---

## 📋 Table of Contents

- [🎯 Overview](#-overview)
- [🏗️ Architecture](#️-architecture)
- [📦 Components](#-components)
- [🚀 Quick Start](#-quick-start)
- [⚙️ Configuration](#️-configuration)
- [📝 Usage](#-usage)
- [🔧 Development](#-development)
- [🤝 Contributing](#-contributing)
- [📄 License](#-license)

---

## 🎯 Overview

### What is Memory Architecture?

OpenClaw Memory Architecture is a **complete memory management system** for AI assistants:

- ✅ **Persistent Memory** - Save important info across sessions
- ✅ **Context Management** - Never lose current task state
- ✅ **Causal Reasoning** - Predict outcomes, learn from experience
- ✅ **Semantic Search** - Find related content quickly
- ✅ **Three-Tier Memory** - Episodic/Semantic/Procedural

### Core Design Principles

1. **Never Lose** - Recover state even after context compression
2. **Complementary** - Each component focuses on specific functions
3. **Automated** - Minimal manual operation
4. **Extensible** - Easy to add new components

---

## 🏗️ Architecture

### Overall Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                    OpenClaw Memory System                              │
├─────────────────────────────────────────────────────────────────────┤
│                                                                       │
│  ┌────────────────────┐    ┌────────────────────┐                  │
│  │ bulletproof-memory │    │    agent-memory     │                  │
│  │     (WAL Protocol) │    │   (SQLite Store)   │                  │
│  │                    │    │                    │                  │
│  │ • SESSION-STATE   │    │ • Facts            │                  │
│  │ • Proactive Write │    │ • Lessons          │                  │
│  │ • Context Recovery│    │ • Entities         │                  │
│  └────────────────────┘    └────────────────────┘                  │
│                                                                       │
│  ┌────────────────────┐    ┌────────────────────┐                  │
│  │   memory-manager  │    │       QMD          │                  │
│  │  (Three-Tier)     │    │ (Vector Search)    │                  │
│  │                    │    │                    │                  │
│  │ • Episodic        │    │ • Semantic Search  │                  │
│  │ • Semantic        │    │ • Similarity Match │                  │
│  │ • Procedural      │    │ • Auto Indexing    │                  │
│  └────────────────────┘    └────────────────────┘                  │
│                                                                       │
│  ┌───────────────────────────────────────────────────────────────┐  │
│  │                    causal-inference                          │  │
│  │                 (Causal Reasoning & Prediction)               │  │
│  └───────────────────────────────────────────────────────────────┘  │
│                                                                       │
└─────────────────────────────────────────────────────────────────────┘
```

### Component Comparison

| Component | Type | Location | Function |
|-----------|------|---------|---------|
| **bulletproof-memory** | WAL Protocol | `SESSION-STATE.md` | Active context protection |
| **agent-memory** | SQLite | `~/.agent-memory/` | Facts/Lessons/Entities persistence |
| **causal-inference** | Reasoning | `memory/causal/` | Causal reasoning & prediction |
| **memory-manager** | Filesystem | `memory/` | Three-tier memory |
| **QMD** | Vector DB | `~/.cache/qmd/` | Semantic search |

---

## 📦 Components

### 1. bulletproof-memory 🛡️

**Function**: Uses Write-Ahead Log (WAL) protocol to ensure active tasks never get lost.

**Key Features**:
- Write immediately on user input
- Doesn't rely on agent memory
- Auto recovery after context compression

### 2. agent-memory 🗄️

**Function**: Cross-session persistence for facts, lessons, and entities.

**Key Features**:
- SQLite database storage
- Tag-based queries
- Auto learning from experience

### 3. causal-inference 🎯

**Function**: Add causal reasoning to actions, predict outcomes.

**Key Features**:
- Predict action outcomes
- Debug failures
- Learn from history
- Safety constraints

### 4. memory-manager 📚

**Function**: Three-tier memory management.

**Key Features**:
- Episodic (what happened)
- Semantic (what we know)
- Procedural (how to do)

### 5. QMD 🔍

**Function**: Vector database for semantic search and similarity matching.

**Key Features**:
- Semantic search
- Similarity matching
- Auto indexing
- Fast retrieval

---

## 🚀 Quick Start

### Requirements

- Python 3.8+
- OpenClaw latest version
- SQLite 3
- 100MB+ free space

### Installation

```bash
# Clone repository
git clone https://github.com/infinitelab/openclaw-memory-architecture.git
cd openclaw-memory-architecture

# Install dependencies
pip install -r requirements.txt

# Configure OpenClaw
# Edit ~/.openclaw/open# Initialize
claw.json

mkdir -p ~/.openclaw/workspace/memory/causal/{graphs,estimates}
mkdir -p ~/.agent-memory/

# Restart OpenClaw
openclaw gateway restart
```

---

## 📄 License

MIT License

See [LICENSE](LICENSE) for details.

---

<div align="center">

**⭐ Star this project if it helps you!**

Made with 🦭 by Luxi & infinitelab

</div>
