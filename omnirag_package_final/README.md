# 🚀 OmniRAG - The Universal RAG System

**Intelligent RAG combining Liquid + Agentic + Chain architectures**

100% FREE using HuggingFace models (Qwen, Flan-T5, etc.)!

## What is OmniRAG?

OmniRAG combines three powerful RAG techniques:

1. **🌊 Liquid RAG** - Automatically adapts answers to user expertise (beginner/expert)
2. **🤖 Agentic RAG** - Smartly chooses between local docs and web search
3. **⛓️ Chain RAG** - Handles complex multi-part questions

## Installation

```bash
pip install omnirag
```

## Quick Start

```python
from omnirag import OmniRAG

# Initialize (supports Qwen, Flan-T5, Mistral, etc.)
rag = OmniRAG(
    model_name="Qwen/Qwen2.5-1.5B-Instruct",  # or "google/flan-t5-large"
    verbose=True
)

# Load documents
rag.load_from_file("dataset.pdf")  # Supports PDF, TXT, JSON, CSV

# Query
result = rag.query("Your question here")
print(result['answer'])
```

## Features

✅ **Smart User Detection** - Automatically detects expertise level
✅ **PDF Support** - Load PDF files directly
✅ **Multiple Models** - Qwen, Flan-T5, Mistral, Phi-2
✅ **FAISS Vector DB** - Fast similarity search
✅ **Web Search** - DuckDuckGo integration (optional)
✅ **Query Decomposition** - Handles complex questions
✅ **Fast Caching** - 3x speedup on repeated queries
✅ **100% FREE** - No API costs!

## Supported Models

```python
# Qwen models (Recommended!)
rag = OmniRAG(model_name="Qwen/Qwen2.5-0.5B-Instruct")  # Fast
rag = OmniRAG(model_name="Qwen/Qwen2.5-1.5B-Instruct")  # Balanced
rag = OmniRAG(model_name="Qwen/Qwen2.5-3B-Instruct")    # Best

# Flan-T5 models
rag = OmniRAG(model_name="google/flan-t5-base")   # 250M params
rag = OmniRAG(model_name="google/flan-t5-large")  # 780M params

# Other models
rag = OmniRAG(model_name="microsoft/phi-2")  # 2.7B params
```

## Examples

### Load Different File Types

```python
# PDF
rag.load_from_file("research_paper.pdf")

# Text
rag.load_from_file("notes.txt")

# JSON
rag.load_from_file("data.json")

# Folder
rag.load_from_folder("./documents")

# With chunking (for large files)
rag.load_from_file("big_file.pdf", chunk_size=500)
```

### Different User Levels

```python
# Auto-detect user level
result = rag.query("What is machine learning?")

# Force specific level
result = rag.query("Explain ML", user_level="expert")

# Get metadata
result = rag.query("Question", return_metadata=True)
print(result['metadata']['user_level'])
```

### Complex Queries

```python
# Automatically breaks down and answers each part
result = rag.query("""
Compare Python vs Java for ML.
Which is better for beginners?
What are the performance differences?
""")
```

### Enable Web Search

```python
rag = OmniRAG(
    model_name="Qwen/Qwen2.5-1.5B-Instruct",
    enable_web_search=True  # Uses DuckDuckGo
)

# Now queries about "latest" or "recent" use web search
result = rag.query("Latest AI developments in 2025")
```

## How It Works

```
User Query
    ↓
Liquid RAG: Detect user level (beginner/expert)
    ↓
Chain RAG: Break into sub-queries (if complex)
    ↓
Agentic RAG: Choose tool (vectordb/web) for each
    ↓
Retrieve & Transform content to user level
    ↓
Chain RAG: Synthesize final answer
    ↓
Liquid RAG: Final polish
    ↓
Perfect Answer!
```

## Requirements

- Python 3.8+
- 2-4GB RAM (depends on model)
- Works on CPU or GPU

## License

MIT License - Free for commercial and personal use!

## Links

- GitHub: https://github.com/Giri530/omnirag
- Issues: https://github.com/Giri530/omnirag/issues

## Citation

```bibtex
@software{omnirag2025,
  title={OmniRAG: The Universal RAG System},
  author={Your Name},
  year={2025},
  url={https://github.com/Giri530/omnirag}
}
```
