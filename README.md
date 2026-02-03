# 🚀 OmniRAG - The Universal RAG System

**Intelligent RAG combining Liquid + Agentic + Chain architectures**

100% FREE using HuggingFace model (Qwen) + FAISS!

---

## 🎯 What is OmniRAG?

OmniRAG is an advanced Retrieval-Augmented Generation system that combines three powerful RAG techniques:

### 🌊 Liquid RAG
Automatically adapts answers to user expertise level:
- **Beginner**: Simple explanations with examples
- **Intermediate**: Balanced technical content
- **Expert**: Deep technical details

### 🤖 Agentic RAG
Intelligently chooses the best information source:
- **VectorDB**: For local documents
- **Web Search**: For current information

### ⛓️ Chain RAG
Handles complex multi-part questions:
- Breaks down complex queries
- Answers each part separately
- Synthesizes coherent final answer

---

## ✨ Features

✅ **PDF Support** - Load PDF files directly  
✅ **Multiple LLM Models** - Qwen, Flan-T5, Mistral, Phi-2  
✅ **FAISS Vector DB** - Fast similarity search  
✅ **Web Search** - DuckDuckGo integration (free!)  
✅ **Smart User Detection** - Auto expertise level detection  
✅ **Query Decomposition** - Handles complex questions  
✅ **Fast Caching** - 3x speedup on repeated queries  
✅ **100% FREE** - No API costs!  
✅ **Works on CPU** - No GPU required (but faster with GPU)

---

## 📦 Installation

```bash
pip install omnirag
```

### From Source

```bash
git clone https://github.com/Giri530/omnirag.git
cd omnirag
pip install -e .
```

---

## 🚀 Quick Start

```python
from omnirag import OmniRAG

# Initialize with your preferred model
rag = OmniRAG(
    model_name="Qwen/Qwen2.5-1.5B-Instruct",  # or "google/flan-t5-large"
    verbose=True
)

# Load documents
rag.load_from_file("dataset.pdf")

# Query
result = rag.query("What is the main concept?")
print(result['answer'])
```

**That's it!** OmniRAG automatically:
- Detects user expertise level
- Retrieves relevant information
- Adapts content to user level
- Generates perfect answer

---

## 💡 Usage Examples

### Load Different File Types

```python
# PDF files
rag.load_from_file("research_paper.pdf")

# Text files
rag.load_from_file("notes.txt")

# JSON data
rag.load_from_file("data.json")

# Entire folder
rag.load_from_folder("./documents")

# With chunking for large files
rag.load_from_file("big_file.pdf", chunk_size=500)

# Direct text
rag.add_documents([
    "Python is great for ML.",
    "Qwen is a powerful language model."
])
```

### Different User Levels

```python
# Auto-detect user level
result = rag.query("What is machine learning?")

# Force specific level
result = rag.query("Explain ML", user_level="expert")

# Get detailed metadata
result = rag.query("Question", return_metadata=True)
print(result['metadata']['user_level'])
print(result['metadata']['sub_queries'])
```

### Complex Queries

```python
# OmniRAG automatically breaks down and answers
result = rag.query("""
Compare Python vs Java for machine learning.
Which is better for beginners?
What are the performance differences?
""")

print(result['answer'])
```

### Enable Web Search

```python
rag = OmniRAG(
    model_name="Qwen/Qwen2.5-1.5B-Instruct",
    enable_web_search=True  # Free DuckDuckGo search
)

# Queries about "latest" or "recent" automatically use web
result = rag.query("Latest AI developments in 2025")
```

---

## 🎨 Supported Models

### Qwen Models (Recommended!)

```python
# Fast & Efficient
rag = OmniRAG(model_name="Qwen/Qwen2.5-0.5B-Instruct")

# Balanced (Best Choice!)
rag = OmniRAG(model_name="Qwen/Qwen2.5-1.5B-Instruct")

# High Quality
rag = OmniRAG(model_name="Qwen/Qwen2.5-3B-Instruct")
```

### Flan-T5 Models

```python
# Small & Fast
rag = OmniRAG(model_name="google/flan-t5-base")   # 250M params

# Larger & Better
rag = OmniRAG(model_name="google/flan-t5-large")  # 780M params
```

### Other Models

```python
# Microsoft Phi
rag = OmniRAG(model_name="microsoft/phi-2")  # 2.7B params

# Mistral
rag = OmniRAG(model_name="mistralai/Mistral-7B-Instruct-v0.2")  # 7B params
```

---

## 🏗️ Architecture

```
User Query
    ↓
🌊 LIQUID RAG: Detect expertise level
    ↓
⛓️ CHAIN RAG: Break into sub-queries (if complex)
    ↓
FOR EACH SUB-QUERY:
    ↓
🤖 AGENTIC RAG: Choose tool (VectorDB or Web)
    ↓
    Retrieve relevant chunks
    ↓
🌊 LIQUID RAG: Transform to user level
    ↓
    Generate sub-answer
    ↓
⛓️ CHAIN RAG: Synthesize all sub-answers
    ↓
🌊 LIQUID RAG: Final polish
    ↓
✨ Perfect Answer!
```

See [Architecture Diagram](docs/architecture.drawio) for detailed visualization.

---

## 📊 Performance

| Model | Size | RAM | Speed | Quality |
|-------|------|-----|-------|---------|
| Qwen-0.5B | 0.5B | 1GB | ⚡⚡⚡ | ⭐⭐ |
| **Qwen-1.5B** | 1.5B | 2GB | ⚡⚡ | ⭐⭐⭐ ⭐ |
| Qwen-3B | 3B | 4GB | ⚡ | ⭐⭐⭐⭐⭐ |
| Flan-T5-Base | 250M | 1GB | ⚡⚡⚡ | ⭐⭐⭐ |
| Flan-T5-Large | 780M | 2GB | ⚡⚡ | ⭐⭐⭐⭐ |

**Recommended:** Qwen-1.5B for best balance!

---

## 🔧 Configuration

```python
rag = OmniRAG(
    # LLM Model
    model_name="Qwen/Qwen2.5-1.5B-Instruct",
    
    # Embedding Model
    embedding_model="all-MiniLM-L6-v2",
    
    # Web Search
    enable_web_search=True,
    
    # Verbose Output
    verbose=True
)
```

---

## 📖 API Reference

### OmniRAG Class

#### `__init__(model_name, embedding_model, enable_web_search, verbose)`
Initialize OmniRAG system.

#### `load_from_file(file_path, chunk_size=None)`
Load documents from file (.pdf, .txt, .json, .csv, .md).

#### `load_from_folder(folder_path, file_extensions=None, chunk_size=None)`
Load all documents from folder.

#### `add_documents(documents)`
Add documents directly as list.

#### `query(user_query, user_level=None, max_sources=5, return_metadata=False)`
Query the system and get answer.

**Returns:**
```python
{
    'answer': str,  # Generated answer
    'metadata': {   # Optional
        'user_level': str,
        'sub_queries_count': int,
        'sub_queries': list,
        'tools_used': list
    }
}
```

#### `get_stats()`
Get system statistics.

#### `clear_cache()`
Clear query cache.

---

## 🌍 Use Cases

### Research Assistant
```python
rag.load_from_file("research_papers.pdf")
result = rag.query("What are the key findings?")
```

### Document Q&A
```python
rag.load_from_folder("./company_docs")
result = rag.query("What is our refund policy?")
```

### Educational Tool
```python
rag.load_from_file("textbook.pdf")
result = rag.query("Explain photosynthesis simply")
# Auto-detects beginner level!
```

### Code Documentation
```python
rag.load_from_folder("./docs", file_extensions=['.md', '.txt'])
result = rag.query("How do I deploy this?")
```

---

## 🛠️ Development

### Install for Development

```bash
git clone https://github.com/Giri530/omnirag.git
cd omnirag
pip install -e ".[dev]"
```

### Run Tests

```bash
pytest tests/
```

### Project Structure

```
omnirag/
├── omnirag/
│   ├── __init__.py
│   ├── omnirag.py              # Main class
│   ├── liquid_analyzer.py      # User level detection
│   ├── chain_decomposer.py     # Query decomposition
│   ├── agentic_planner.py      # Tool selection
│   ├── content_transformer.py  # Content adaptation
│   ├── vectordb_tool.py        # FAISS database
│   ├── web_search_tool.py      # Web search
│   ├── llm_client.py           # LLM wrapper
│   └── cache.py                # Caching
├── examples/
│   └── quickstart.py
├── setup.py
├── requirements.txt
└── README.md
```

---

## 🤝 Contributing

Contributions welcome! Please:

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing`)
5. Open Pull Request

---

## 📝 Requirements

- Python 3.8+
- 2-4GB RAM (depends on model)
- CPU or GPU (GPU recommended for speed)

**Dependencies:**
- transformers
- torch
- sentence-transformers
- faiss-cpu
- PyPDF2
- duckduckgo-search

---

## 📄 License

MIT License - Free for commercial and personal use!

See [LICENSE](LICENSE) for details.

---

## 🙏 Acknowledgments

- **HuggingFace** for transformers library
- **Qwen Team** for excellent models
- **FAISS** for fast vector search
- **Sentence Transformers** for embeddings

---

## 📧 Contact

- **GitHub Issues**: [Report bugs or request features](https://github.com/Giri530/omnirag/issues)
- **Email**: your@email.com

---

## 🌟 Star History

If you find OmniRAG useful, please ⭐ star the repo!

---

## 📚 Citation

```bibtex
@software{omnirag2025,
  title={OmniRAG: The Universal RAG System},
  author={Girinath V},
  year={2025},
  url={https://github.com/Giri530/omnirag}
}
```

---

## 🎯 Roadmap

- [ ] Support for more file formats (DOCX, XLSX)
- [ ] Advanced caching strategies
- [ ] Multi-language support
- [ ] Custom embedding models
- [ ] GUI interface
- [ ] Cloud deployment guides

---

**Made with ❤️ - 100% FREE Forever!**

**Happy RAG-ing! 🚀**
