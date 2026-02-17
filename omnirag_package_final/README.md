# OmniRAG

<div align="center">

[![PyPI version](https://badge.fury.io/py/omnirag.svg)](https://pypi.org/project/omnirag/)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Downloads](https://pepy.tech/badge/omnirag)](https://pepy.tech/project/omnirag)

**Intelligent Retrieval-Augmented Generation with Multi-Language Support and Voice Interface**

[Features](#features) •
[Installation](#installation) •
[Quick Start](#quick-start) •
[Documentation](#documentation) •
[Examples](#examples) •
[Contributing](#contributing)

</div>

---

## Overview

OmniRAG is a production-ready RAG (Retrieval-Augmented Generation) framework that combines adaptive learning, intelligent tool selection, and native multi-language capabilities. Unlike traditional RAG systems, OmniRAG translates outputs after retrieval, preserving semantic quality while supporting 27+ languages with built-in voice interface.

### Key Capabilities

- **Adaptive Intelligence**: Automatically adjusts response complexity based on user expertise level
- **Multi-Language Translation**: Native support for 27+ languages including Tamil, Hindi, Spanish, and more
- **Voice Interface**: Built-in speech-to-text and text-to-speech capabilities
- **Intelligent Tool Selection**: Automatically chooses between local knowledge base and web search
- **Production Ready**: Optimized for real-world applications with caching and error handling

---

## Features

### Core Features

- **🌊 Liquid RAG**: Adapts responses to user expertise (beginner, intermediate, expert)
- **🤖 Agentic RAG**: Intelligently selects optimal information sources
- **⛓️ Chain RAG**: Decomposes and handles complex multi-part queries
- **📄 Document Processing**: Native support for PDF, TXT, JSON, and more
- **🔍 Vector Search**: High-performance FAISS-based similarity search
- **💾 Smart Caching**: Automatic response caching for improved performance

### v2.0 New Features

- **🌍 Post-Retrieval Translation**
  - Preserves embedding quality by maintaining original language documents
  - Significantly more storage efficient than pre-translation approaches
  - Supports full language names ("Spanish" vs "es") for better usability
  
- **🎤 Native Voice Interface**
  - Built-in speech recognition and synthesis
  - No external API dependencies
  - Multi-language voice support
  - Works offline

- **🔧 Production Enhancements**
  - UTF-8 encoding support for non-Latin scripts
  - Improved error handling and logging
  - Comprehensive documentation and examples

---

## Installation

### Basic Installation

```bash
pip install omnirag
```

### With Voice Input Support

Voice output is enabled by default. For voice input (speech recognition), install additional dependencies:

**Windows**
```bash
pip install pipwin
pipwin install pyaudio
pip install omnirag[voice-input]
```

**macOS**
```bash
brew install portaudio
pip install omnirag[voice-input]
```

**Linux**
```bash
sudo apt-get install portaudio19-dev python3-pyaudio
pip install omnirag[voice-input]
```

### From Source

```bash
git clone https://github.com/Giri530/omnirag.git
cd omnirag
pip install -e .
```

---

## Quick Start

### Basic Usage

```python
from omnirag import OmniRAG

# Initialize with your preferred model
rag = OmniRAG(model_name="google/flan-t5-small")

# Add documents
rag.add_documents([
    "Python is a high-level programming language.",
    "It emphasizes code readability and simplicity."
])

# Query the system
result = rag.query("What is Python?")
print(result['answer'])
```

### Multi-Language Translation

```python
from omnirag import OmniRAG

# Initialize with target language
rag = OmniRAG(
    model_name="google/flan-t5-small",
    output_language="Spanish"
)

# Add English documents
rag.add_documents([
    "Artificial Intelligence enables machines to learn from experience.",
    "Machine Learning is a subset of AI."
])

# Query in any language, receive Spanish response
result = rag.query("What is AI?")
print(result['answer'])
# Output: "La Inteligencia Artificial permite a las máquinas aprender de la experiencia."
```

### Voice-Enabled RAG

```python
from omnirag import OmniRAG

# Initialize with voice support
rag = OmniRAG(
    enable_voice=True,
    output_language="Tamil"
)

rag.add_documents(["Quantum computing uses quantum mechanics principles."])

# Text query with spoken response
result = rag.query("Explain quantum computing", speak_answer=True)

# Full voice interaction (requires microphone)
result = rag.voice_query()
```

---

## Supported Languages

OmniRAG supports 27+ languages with both full names and ISO codes:

**Indian Languages**: Tamil, Hindi, Telugu, Marathi, Gujarati, Kannada, Malayalam, Punjabi, Bengali

**European Languages**: Spanish, French, German, Italian, Portuguese, Russian, Polish, Dutch, Turkish

**Asian Languages**: Chinese (Simplified), Japanese, Korean, Vietnamese, Thai, Indonesian, Malay

**Other**: Arabic, English

---

## Model Support

### Recommended Models

| Model | Parameters | RAM | Speed | Quality | Use Case |
|-------|------------|-----|-------|---------|----------|
| `google/flan-t5-small` | 80M | 0.5GB | ⚡⚡⚡ | ⭐⭐ | Development, Testing |
| `google/flan-t5-base` | 250M | 1GB | ⚡⚡⚡ | ⭐⭐⭐ | Production (Balanced) |
| `Qwen/Qwen2.5-0.5B-Instruct` | 500M | 1GB | ⚡⚡ | ⭐⭐⭐ | High Quality |
| `Qwen/Qwen2.5-1.5B-Instruct` | 1.5B | 2GB | ⚡⚡ | ⭐⭐⭐⭐ | Best Quality |
| `Qwen/Qwen2.5-3B-Instruct` | 3B | 4GB | ⚡ | ⭐⭐⭐⭐⭐ | Maximum Quality |

---

## Advanced Configuration

```python
rag = OmniRAG(
    model_name="google/flan-t5-base",      # LLM model
    embedding_model="all-MiniLM-L6-v2",    # Embedding model
    enable_web_search=True,                 # Enable web search
    output_language="Tamil",                # Target language
    enable_voice=True,                      # Voice interface
    use_4bit=False,                         # 4-bit quantization
    verbose=True                            # Debug logging
)
```

---

## Examples

### Document Q&A System

```python
# Load documents from various sources
rag.load_from_file("company_handbook.pdf")
rag.load_from_folder("./policy_documents")

# Query with automatic source attribution
result = rag.query("What is the remote work policy?")
print(f"Answer: {result['answer']}")
print(f"Sources: {result['sources']}")
```

### Multi-Language Customer Support

```python
# Initialize for Hindi-speaking users
support_rag = OmniRAG(
    output_language="Hindi",
    enable_voice=True
)

support_rag.load_from_file("product_manual.pdf")

# Customer query with voice response
result = support_rag.query(
    "How do I reset my password?",
    speak_answer=True
)
```

### Educational Assistant

```python
# Initialize for students
edu_rag = OmniRAG(model_name="google/flan-t5-base")

edu_rag.load_from_file("physics_textbook.pdf")

# Automatically adapts to user level
beginner_result = rag.query("Explain photosynthesis")  # Simple explanation
expert_result = rag.query("Explain quantum entanglement")  # Technical detail
```

### Complex Query Handling

```python
# Automatically decomposes complex queries
result = rag.query("""
Compare the advantages and disadvantages of solar and wind energy.
Which is more cost-effective for residential use?
What are the environmental impacts of each?
""")
```

---

## API Reference

### Core Methods

#### `__init__(**kwargs)`
Initialize OmniRAG with configuration parameters.

**Parameters:**
- `model_name` (str): HuggingFace model identifier
- `embedding_model` (str): Sentence transformer model
- `enable_web_search` (bool): Enable web search capability
- `output_language` (str): Target language for responses
- `enable_voice` (bool): Enable voice interface
- `use_4bit` (bool): Use 4-bit quantization for memory efficiency
- `verbose` (bool): Enable detailed logging

#### `query(user_query, output_language=None, speak_answer=False)`
Submit a query to the RAG system.

**Parameters:**
- `user_query` (str): The question or prompt
- `output_language` (str, optional): Override default output language
- `speak_answer` (bool): Enable voice response

**Returns:** Dictionary containing:
- `answer` (str): Generated response
- `sources` (list): Retrieved source documents
- `user_level` (str): Detected expertise level
- `output_language` (str): Language code of response

#### `add_documents(documents)`
Add documents to the knowledge base.

**Parameters:**
- `documents` (list): List of text strings or file paths

#### `load_from_file(file_path, chunk_size=None)`
Load and process a document file.

**Parameters:**
- `file_path` (str): Path to document file
- `chunk_size` (int, optional): Character limit per chunk

#### `voice_query(output_language=None)`
Process voice input and provide voice output.

**Parameters:**
- `output_language` (str, optional): Override default output language

**Returns:** Same structure as `query()`

---

## Architecture

```
┌─────────────┐
│ User Query  │
└──────┬──────┘
       │
       ▼
┌─────────────────────┐
│  Liquid Analyzer    │  ← Detect user expertise level
└──────┬──────────────┘
       │
       ▼
┌─────────────────────┐
│  Chain Decomposer   │  ← Break complex queries
└──────┬──────────────┘
       │
       ▼
┌─────────────────────┐
│  Agentic Planner    │  ← Select tools (Vector DB / Web)
└──────┬──────────────┘
       │
       ▼
┌─────────────────────┐
│  Information        │
│  Retrieval          │  ← Fetch relevant chunks
└──────┬──────────────┘
       │
       ▼
┌─────────────────────┐
│  Content            │
│  Transformation     │  ← Adapt to user level
└──────┬──────────────┘
       │
       ▼
┌─────────────────────┐
│  LLM Generation     │  ← Generate response
└──────┬──────────────┘
       │
       ▼
┌─────────────────────┐
│  Smart Translator   │  ← Translate (if needed)
└──────┬──────────────┘
       │
       ▼
┌─────────────────────┐
│  Voice Processor    │  ← Synthesize speech (if enabled)
└──────┬──────────────┘
       │
       ▼
┌─────────────┐
│   Response  │
└─────────────┘
```

---

## Use Cases

### Enterprise Applications
- **Customer Support**: Multi-language support with voice interface
- **Internal Knowledge Base**: Quick access to company documentation
- **Training Systems**: Adaptive content delivery based on employee expertise

### Education
- **Study Assistants**: Personalized explanations for students
- **Language Learning**: Cross-language practice and translation
- **Accessibility**: Voice interface for visually impaired students

### Research
- **Literature Review**: Query across multiple papers and documents
- **Data Analysis**: Natural language interface to research data
- **Collaborative Tools**: Multi-language research team support

---

## Performance Optimization

### Memory Management

```python
# Use 4-bit quantization for large models
rag = OmniRAG(
    model_name="Qwen/Qwen2.5-3B-Instruct",
    use_4bit=True  # Reduces memory usage by ~75%
)
```

### Caching

```python
# Automatic caching of frequent queries
result1 = rag.query("What is Python?")  # ~2s
result2 = rag.query("What is Python?")  # <10ms (from cache)

# Clear cache when needed
rag.clear_cache()
```

### Batch Processing

```python
questions = [
    "What is machine learning?",
    "What is deep learning?",
    "What is neural network?"
]

results = [rag.query(q) for q in questions]
```

---

## Comparison with Other Frameworks

| Feature | LangChain | LlamaIndex | OmniRAG |
|---------|-----------|------------|---------|
| Built-in Translation* | ❌ | ❌ | ✅ |
| Built-in Voice I/O* | ❌ | ❌ | ✅ |
| Adaptive Responses | ⚠️ Manual | ⚠️ Manual | ✅ Auto |
| Indian Languages | ⚠️ External | ⚠️ External | ✅ Native |
| Beginner Friendly | ⚠️ Complex | ⚠️ Complex | ✅ Simple |
| Open Source | ✅ | ✅ | ✅ |
| Free to Use | ✅ | ✅ | ✅ |

\* Built-in = Native implementation without external APIs or services

---

## Troubleshooting

### Common Issues

**Import Errors**
```python
# Ensure proper installation
pip install --upgrade omnirag

# Verify installation
python -c "from omnirag import OmniRAG; print('Success!')"
```

**Voice Input Issues**
```bash
# Windows
pipwin install pyaudio

# macOS
brew install portaudio && pip install pyaudio

# Linux
sudo apt-get install portaudio19-dev python3-pyaudio
```

**Out of Memory**
```python
# Use smaller model or enable quantization
rag = OmniRAG(
    model_name="google/flan-t5-small",  # Smaller model
    use_4bit=True  # Enable quantization
)
```

---

## Contributing

We welcome contributions! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Add tests for new functionality
5. Commit changes (`git commit -m 'Add amazing feature'`)
6. Push to branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

### Development Setup

```bash
git clone https://github.com/Giri530/omnirag.git
cd omnirag
pip install -e ".[dev]"
pytest tests/  # Run tests
```

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## Citation

If you use OmniRAG in your research or project, please cite:

```bibtex
@software{omnirag2025,
  title={OmniRAG: Intelligent Multi-Language RAG Framework},
  author={Girinath V},
  year={2025},
  version={2.0.0},
  url={https://github.com/Giri530/omnirag},
  license={MIT}
}
```

---

## Acknowledgments

Built with these excellent open-source projects:
- [Transformers](https://github.com/huggingface/transformers) by Hugging Face
- [FAISS](https://github.com/facebookresearch/faiss) by Meta Research
- [Sentence Transformers](https://www.sbert.net/) by UKP Lab
- [Deep Translator](https://github.com/nidhaloff/deep-translator)
- [pyttsx3](https://github.com/nateshmbhat/pyttsx3)

---

## Support

- **Documentation**: [Complete Guide (PDF)](https://github.com/Giri530/omnirag/blob/main/docs/OmniRAG_Complete_Guide.pdf)
- **Issues**: [GitHub Issues](https://github.com/Giri530/omnirag/issues)
- **Discussions**: [GitHub Discussions](https://github.com/Giri530/omnirag/discussions)
- **Email**: girinathv48@gmail.com

---

## Roadmap

### v2.0 (Current)
- ✅ Multi-language translation
- ✅ Voice interface
- ✅ UTF-8 support

### v2.1 (Planned)
- [ ] DOCX and XLSX support
- [ ] Custom translation models
- [ ] Voice language selection
- [ ] Web UI

### v3.0 (Future)
- [ ] Multi-modal support (images, audio)
- [ ] Real-time translation
- [ ] Cloud deployment templates
- [ ] REST API server

---

<div align="center">

**Made with ❤️ by [Girinath V](https://github.com/Giri530)**

[⭐ Star us on GitHub](https://github.com/Giri530/omnirag) •
[📦 Install from PyPI](https://pypi.org/project/omnirag/) •
[📖 Read the Docs](https://github.com/Giri530/omnirag#readme)

</div>
