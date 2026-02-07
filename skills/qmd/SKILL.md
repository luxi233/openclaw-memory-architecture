---
name: qmd
description: "Vector database for semantic search and similarity matching. Powered by QMD (Query-Model-Database)."
metadata:
  openclaw:
    emoji: "🔍"
    version: "1.0.0"
    author: "OpenClaw Community"
    requires:
      os: ["darwin", "linux"]
    tags: ["search", "vector", "semantic", "similarity"]
---

# qmd 🔍

**Vector database for semantic search and similarity matching.**

Find related content by meaning, not just keywords.

## Overview

QMD (Query-Model-Database) provides **semantic search** capabilities:

| Feature | Description |
|---------|-------------|
| **Semantic Search** | Find by meaning, not just keywords |
| **Similarity Matching** | Find documents similar to a given one |
| **Auto Indexing** | Automatically index new content |
| **Fast Retrieval** | Sub-second search results |

## Why Semantic Search?

### Keyword Search vs Semantic Search

| Aspect | Keyword | Semantic |
|--------|---------|----------|
| **Query** | Exact words | Meaning |
| **"猫"** | Finds "猫" | Finds "cat", "kitten", "feline" |
| **"编程"** | Finds "编程" | Finds "coding", "programming", "development" |
| **Flexibility** | Exact match | Conceptual match |

### Use Cases

- ✅ Find related documentation
- ✅ Search past conversations
- ✅ Discover similar workflows
- ✅ Locate relevant knowledge

## Quick Start

### Installation

```bash
# Install QMD
pip install qmd-skill

# Or from source
git clone https://github.com/openclaw/skills/tree/main/skills/qmd.git
cd qmd
pip install -e .
```

### Configuration

```yaml
# ~/.config/qmd/config.yaml

storage: ~/.cache/qmd/
embedding_model: all-MiniLM-L6-v2
chunk_size: 512
chunk_overlap: 50

index:
  type: hnsw  # or "flat", "ivf"
  metric: cosine

search:
  default_top_k: 5
  similarity_threshold: 0.7
```

### Index Content

```bash
# Index a directory
qmd index ./memory/

# Index a single file
qmd index ./docs/api.md

# Index with tags
qmd index ./memory/semantic/ --tags "documentation,api"
```

## Usage Examples

### Semantic Search

```python
from qmd import QMD

# Initialize
qmd = QMD()

# Search by meaning
results = qmd.search(
    query="How to handle user authentication",
    top_k=5,
    threshold=0.7
)

for result in results:
    print(f"Score: {result.similarity:.2f}")
    print(f"File: {result.path}")
    print(f"Content: {result.content[:200]}...")
    print()
```

### Find Similar Documents

```python
# Find documents similar to a given one
similar = qmd.find_similar(
    document="memory/workflows/auth-setup.md",
    top_k=3
)

# Or by content
similar = qmd.find_similar(
    content="I need to implement JWT tokens for API authentication",
    top_k=5
)
```

### Auto-Indexing

```python
# Watch directory for changes
qmd.watch(
    directory="./memory/",
    on_change="reindex"
)

# Or manually trigger
qmd.reindex(path="./memory/")
```

## Architecture

### Components

```
┌─────────────────────────────────────┐
│            QMD System               │
├─────────────────────────────────────┤
│                                      │
│  ┌──────────┐    ┌──────────────┐  │
│  │ Embedding│    │ Vector Index │  │
│  │  Model   │    │   (HNSW)     │  │
│  └──────────┘    └──────────────┘  │
│        │                │           │
│        ▼                ▼           │
│  ┌─────────────────────────────────┤
│  │      Vector Database            │
│  │  • Store embeddings              │
│  │  • Retrieve by similarity        │
│  └─────────────────────────────────┘
│                   │
│                   ▼
│  ┌─────────────────────────────────┐
│  │      Search Interface           │
│  │  • Semantic query               │
│  │  • Similarity match              │
│  │  • Filters & tags               │
│  └─────────────────────────────────┘
│                                      │
└─────────────────────────────────────┘
```

### Data Flow

```
1. User Query
       │
       ▼
2. Embed Query (transform to vector)
       │
       ▼
3. Search Vector Index
       │
       ▼
4. Retrieve Top-K Similar
       │
       ▼
5. Return Results
```

## Configuration Options

### Embedding Models

```yaml
# Lightweight (fast)
embedding_model: all-MiniLM-L6-v2

# High quality (slower)
embedding_model: all-mpnet-base-v2

# Multilingual
embedding_model: paraphrase-multilingual-MiniLM-L12-v2
```

### Index Types

```yaml
# HNSW (Hierarchical Navigable Small World)
# - Fastest for large datasets
# - Memory efficient
index:
  type: hnsw
  ef_construction: 200
  M: 16

# Flat (brute force)
# - Exact results
# - Slow for large datasets
index:
  type: flat
  metric: cosine

# IVF (Inverted File Index)
# - Good balance
index:
  type: ivf
  nlist: 100
```

### Search Options

```yaml
search:
  default_top_k: 5          # Return top 5 results
  similarity_threshold: 0.7  # Filter below 70% similarity
  rerank: true              # Re-rank results
  highlight: true           # Highlight matches
```

## CLI Commands

### Indexing

```bash
# Index directory
qmd index ./memory/

# Index with options
qmd index ./memory/ \
  --chunk-size 1024 \
  --overlap 100 \
  --tags "docs,knowledge"

# Rebuild index
qmd index ./memory/ --rebuild

# Index specific file
qmd index ./docs/api.md
```

### Searching

```bash
# Simple search
qmd search "authentication"

# With options
qmd search "authentication" \
  --top-k 10 \
  --threshold 0.5 \
  --format json

# Search in specific directory
qmd search "REST API" --in ./memory/semantic/
```

### Maintenance

```bash
# Check index status
qmd status

# Index statistics
qmd stats

# Re-index everything
qmd rebuild

# Remove from index
qmd remove ./memory/old-doc.md
```

## Integration with Other Components

### With memory-manager

```python
# After updating semantic memory
memory_manager.update_topic("REST API Best Practices")

# Auto-index new content
qmd.index("./memory/semantic/rest-api.md")

# Now searchable
results = qmd.search("How to design APIs")
```

### With agent-memory

```python
# Remember a fact
mem.remember("User prefers concise responses")

# Index for search
qmd.index_text(
    text="User prefers concise responses",
    metadata={"source": "agent-memory", "tags": ["preference"]}
)

# Later: Search for it
results = qmd.search("What does user prefer")
```

### Full Workflow

```
User Input
    │
    ├──► WAL Protocol → SESSION-STATE.md
    │
    ├──► QMD Search → Find related content
    │
    ├──► agent-memory → Recall similar situations
    │
    └──► memory-manager → Update daily notes
```

## Performance

### Benchmarks

| Operation | 1K docs | 10K docs | 100K docs |
|-----------|---------|----------|-----------|
| **Index** | ~1s | ~10s | ~2min |
| **Search** | ~5ms | ~10ms | ~50ms |
| **Index Size** | ~50MB | ~500MB | ~5GB |

### Optimization Tips

1. **Chunk Size**: 512-1024 tokens works well
2. **Overlap**: 10-20% chunk overlap
3. **Model**: Smaller models for speed, larger for quality
4. **Index Type**: HNSW for >10K documents

## Files

- `~/.cache/qmd/` - Vector database storage
- `~/.config/qmd/config.yaml` - Configuration
- `~/.cache/qmd/index/` - Vector index

---

*Built with ❤️ by the OpenClaw community*
