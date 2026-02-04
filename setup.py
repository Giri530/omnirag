from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="omnirag",
    version="1.0.2",
    author="Girinath V",
    author_email="girinathv48@gmail.com",
    description="OmniRAG: Universal RAG System combining Liquid + Agentic + Chain RAG",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Giri530/omnirag",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    install_requires=[
        "transformers>=4.30.0",
        "torch>=2.0.0",
        "sentence-transformers>=2.2.0",
        "faiss-cpu>=1.7.4",
        "numpy>=1.24.0",
        "accelerate>=0.20.0",
        "PyPDF2>=3.0.0",
        "duckduckgo-search>=3.9.0",
        "requests>=2.31.0",
    ],
    keywords="rag llm ai faiss huggingface qwen machine-learning nlp pdf",
)
