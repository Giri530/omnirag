from omnirag import OmniRAG

# ============================================
# EXAMPLE 1: Basic Usage
# ============================================
# Initialize with Qwen model (recommended!)
rag = OmniRAG(
    model_name="Qwen/Qwen2.5-1.5B-Instruct",  # Fast & efficient
    verbose=True
)

# Add some documents
documents = [
    "Python is a high-level programming language known for its simplicity.",
    "Python is widely used in machine learning with libraries like TensorFlow and PyTorch.",
    "Qwen is a large language model developed by Alibaba Cloud.",
    "RAG combines retrieval and generation for better question answering."
]

rag.add_documents(documents)

# Query
result = rag.query("What is Python?")

print("\n💬 Question: What is Python?")
print(f"✅ Answer: {result['answer']}")

# ============================================
# EXAMPLE 2: PDF File Loading
# ============================================

# Uncomment and update path to your PDF file
# rag.load_from_file("dataset.pdf")
# result = rag.query("Summarize the main points")
# print(f"Answer: {result['answer']}")

print("💡 Tip: Upload a PDF and use rag.load_from_file('path/to/file.pdf')")

# ============================================
# EXAMPLE 3: Different User Levels
# ============================================


# Auto-detect user level (from query keywords)
result_beginner = rag.query("What is machine learning?")
print("\n💬 Beginner Query: What is machine learning?")
print(f"📊 Detected Level: {result_beginner.get('metadata', {}).get('user_level', 'N/A')}")
print(f"✅ Answer: {result_beginner['answer'][:100]}...")

# Force expert level
result_expert = rag.query(
    "Explain gradient descent optimization",
    user_level="expert"
)
print("\n💬 Expert Query: Explain gradient descent optimization")
print(f"✅ Answer: {result_expert['answer'][:100]}...")

# ============================================
# EXAMPLE 4: Complex Query (Chain RAG)
# ============================================


# Add more context
rag.add_documents([
    "Java is a statically-typed language used in enterprise applications.",
    "Java offers better performance than Python but has steeper learning curve.",
    "For beginners, Python is easier to learn due to simpler syntax."
])

# Complex query - will be automatically decomposed
complex_query = "Compare Python vs Java for beginners. Which should I learn first?"

result = rag.query(complex_query, return_metadata=True)

print(f"\n💬 Complex Query: {complex_query}")
print(f"\n📊 Metadata:")
print(f"   - User Level: {result['metadata']['user_level']}")
print(f"   - Sub-queries: {result['metadata']['sub_queries_count']}")
if result['metadata']['sub_queries_count'] > 1:
    for i, sq in enumerate(result['metadata']['sub_queries'], 1):
        print(f"      {i}. {sq}")

print(f"\n✅ Final Answer:\n{result['answer']}")

# ============================================
# EXAMPLE 5: Web Search (Optional)
# ============================================


# Initialize with web search enabled
rag_web = OmniRAG(
    model_name="Qwen/Qwen2.5-1.5B-Instruct",
    enable_web_search=True,  # Enable DuckDuckGo search
    verbose=False
)

# Add local documents
rag_web.add_documents([
    "OmniRAG is a universal RAG system combining three techniques."
])

# Query about recent events (will use web search)
# result = rag_web.query("What are the latest AI developments in 2025?")
# print(f"Answer: {result['answer']}")

print("💡 Tip: Enable web_search for queries about 'latest', 'recent', 'current' info")

# ============================================
# EXAMPLE 6: Multiple File Types
# ============================================


# Create a new RAG instance
rag_files = OmniRAG(model_name="google/flan-t5-base")  # Faster model

# Load from different sources
print("\n📝 Loading from different sources:")

# Text file
# rag_files.load_from_file("notes.txt")
print("   ✅ Text files: .txt, .md")

# JSON file
# rag_files.load_from_file("data.json")
print("   ✅ JSON files: .json")

# PDF file
# rag_files.load_from_file("document.pdf")
print("   ✅ PDF files: .pdf")

# CSV file
# rag_files.load_from_file("data.csv")
print("   ✅ CSV files: .csv")

# Entire folder
# rag_files.load_from_folder("./documents")
print("   ✅ Folders: load all at once")

# With chunking for large files
# rag_files.load_from_file("large_file.pdf", chunk_size=500)
print("   ✅ Chunking: split large files")

# ============================================
# EXAMPLE 7: Get Statistics
# ============================================


stats = rag.get_stats()

print("\n📈 Current System Stats:")
print(f"   - Documents: {stats['documents_count']}")
print(f"   - Cache Size: {stats['cache_size']}")
print(f"   - Web Search: {'Enabled' if stats['web_search_enabled'] else 'Disabled'}")

# ============================================
# TIPS & BEST PRACTICES
# ============================================

tips = """
1. Model Selection:
   - Qwen-0.5B: Fastest, 1GB RAM
   - Qwen-1.5B: Balanced (RECOMMENDED!)
   - Qwen-3B: Best quality, 4GB RAM
   
2. File Loading:
   - Use chunk_size for files > 1MB
   - Load folder for multiple files
   - Supported: PDF, TXT, JSON, CSV, MD
   
3. Query Optimization:
   - Specific questions get better answers
   - Complex queries auto-decompose
   - Use return_metadata=True for debugging
   
4. Performance:
   - GPU: 5-10x faster than CPU
   - Cache: 3x speedup on repeated queries
   - Smaller models: Faster but less accurate
   
5. Web Search:
   - Enable for "latest" or "recent" queries
   - Uses DuckDuckGo (free!)
   - Auto-detects when needed
"""

print(tips)

# ============================================
# SUMMARY
# ============================================

print("""
You've learned:
✅ Basic initialization
✅ Loading documents (PDF, TXT, etc.)
✅ Simple queries
✅ Complex queries
✅ User level detection
✅ Web search integration
✅ System statistics

Next Steps:
📖 Read full documentation: README.md
🌐 Check GitHub: https://github.com/Giri530/omnirag
💬 Ask questions: Open an issue on GitHub

Happy RAG-ing! 🚀
""")
