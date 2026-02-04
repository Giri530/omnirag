import os
import json
from omnirag.liquid_analyzer import LiquidAnalyzer
from omnirag.chain_decomposer import ChainDecomposer
from omnirag.agentic_planner import AgenticPlanner
from omnirag.content_transformer import ContentTransformer
from omnirag.vectordb_tool import VectorDBTool
from omnirag.web_search_tool import WebSearchTool
from omnirag.llm_client import LLMClient
from omnirag.cache import SimpleCache
class OmniRAG:
    def __init__(self,
                 model_name="Qwen/Qwen2.5-0.5B-Instruct",
                 embedding_model="all-MiniLM-L6-v2",
                 enable_web_search=False,
                 use_4bit=False,
                 verbose=False):
        self.verbose = verbose
        if verbose:
            print("\n[1/7] Loading LLM...")
        self.llm = LLMClient(model_name=model_name, use_4bit=use_4bit)
        if verbose:
            print("\n[2/7] Initializing Liquid RAG (User Detection)...")
        self.liquid_analyzer = LiquidAnalyzer(self.llm)
        self.content_transformer = ContentTransformer(self.llm)
        if verbose:
            print("[3/7] Initializing Chain RAG (Query Decomposition)...")
        self.chain_decomposer = ChainDecomposer(self.llm)
        if verbose:
            print("[4/7] Initializing Agentic RAG (Tool Selection)...")
        self.agentic_planner = AgenticPlanner(self.llm)
        if verbose:
            print(f"\n[5/7] Initializing VectorDB ({embedding_model})...")
        self.vectordb = VectorDBTool(embedding_model=embedding_model)
        if verbose:
            print(f"[6/7] Initializing Web Search: {enable_web_search}...")
        self.web_search = WebSearchTool() if enable_web_search else None
        if verbose:
            print("[7/7] Initializing Cache...")
        self.cache = SimpleCache()
    def add_documents(self, documents):
        if self.verbose:
            print(f"Adding {len(documents)} documents...")
        self.vectordb.add_documents(documents)
    def load_from_file(self, file_path, chunk_size=500):
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
        file_ext = os.path.splitext(file_path)[1].lower()
        documents = []
        if file_ext in ['.txt', '.md']:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                documents = self._chunk_text(content, chunk_size)
        elif file_ext == '.json':
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                if isinstance(data, list):
                    documents = [str(item) for item in data]
                else:
                    documents = [str(data)]
        elif file_ext == '.pdf':
            try:
                from PyPDF2 import PdfReader
                reader = PdfReader(file_path)
                text = ""
                for page in reader.pages:
                    text += page.extract_text() + "\n"
                documents = self._chunk_text(text, chunk_size)
            except ImportError:
                print("❌ PyPDF2 not installed! Install with: pip install PyPDF2")
                return
        else:
            raise ValueError(f"Unsupported file type: {file_ext}")
        self.add_documents(documents)
    def _chunk_text(self, text, chunk_size=500):
        words = text.split()
        chunks = []
        for i in range(0, len(words), chunk_size):
            chunk = ' '.join(words[i:i + chunk_size])
            if chunk.strip():
                chunks.append(chunk)
        return chunks
    def query(self, user_query, force_complexity=None, max_sub_queries=4):
        cached = self.cache.get(user_query)
        if cached:
            if self.verbose:
                print("Returning cached result")
            return cached
        if force_complexity:
            container = {"complexity": force_complexity, "query": user_query}
        else:
            container = self.liquid_analyzer.analyze(user_query)
        if self.verbose:
            print(f"\n [LIQUID] User Level Detected: {container['complexity'].upper()}")
        is_complex = self.chain_decomposer.is_complex(user_query)
        if is_complex:
            sub_queries = self.chain_decomposer.decompose(user_query)
            sub_queries = sub_queries[:max_sub_queries]
            if self.verbose:
                print(f"\n [CHAIN] Complex Query! Decomposed into {len(sub_queries)} parts:")
                for i, sq in enumerate(sub_queries, 1):
                    print(f"   {i}. {sq}")
        else:
            sub_queries = [user_query]
            if self.verbose:
                print(f"\n [CHAIN] Simple Query - No decomposition needed")
        all_sub_results = []
        for idx, sub_query in enumerate(sub_queries, 1):
            if self.verbose:
                print(f"\n Processing Sub-Query {idx}/{len(sub_queries)}: {sub_query}")
            plan = self.agentic_planner.plan(
                sub_query,
                web_available=(self.web_search is not None)
            )
            if self.verbose:
                print(f" [AGENTIC] Tool: {plan['tool']}")
                print(f" Reasoning: {plan['reasoning']}")
            if plan['tool'] == 'web_search' and self.web_search:
                chunks = self.web_search.search(sub_query, max_results=3)
            else:
                chunks = self.vectordb.search(sub_query, top_k=3)
            if self.verbose:
                print(f" Retrieved {len(chunks)} chunks")
            transformed_chunks = []
            for chunk in chunks:
                transformed = self.content_transformer.transform(
                    chunk,
                    container['complexity']
                )
                transformed_chunks.append(transformed)
            if self.verbose:
                print(f"[LIQUID] Transformed to '{container['complexity']}' level")
            context = "\n\n".join(transformed_chunks)
            prompt = f"""Based on the context, answer the question clearly and concisely.
Context:
{context}
Question: {sub_query}
Answer (for {container['complexity']} level user):"""
            sub_answer = self.llm.generate(
                prompt,
                max_tokens=300,
                temperature=0.75
            )
            all_sub_results.append({
                'sub_query': sub_query,
                'answer': sub_answer,
                'tool': plan['tool']
            })
        if len(all_sub_results) > 1:
            if self.verbose:
                print(f"\n [CHAIN] Synthesizing {len(all_sub_results)} sub-answers...")
            combined = "\n\n".join([
                f"Q: {r['sub_query']}\nA: {r['answer']}"
                for r in all_sub_results
            ])
            synthesis_prompt = f"""Combine these sub-answers into one coherent, complete answer.
Original Question: {user_query}
Sub-Answers:
{combined}
Create a unified answer for a {container['complexity']} level user:"""
            synthesized_answer = self.llm.generate(
                synthesis_prompt,
                max_tokens=500,
                temperature=0.75
            )
        else:
            synthesized_answer = all_sub_results[0]['answer']
        if self.verbose:
            print(f"\n [LIQUID] Final polish for {container['complexity']} level...")
        final_answer = self.content_transformer.polish(
            synthesized_answer,
            container['complexity']
        )
        result = {
            'answer': final_answer,
            'metadata': {
                'user_level': container['complexity'],
                'sub_queries_count': len(sub_queries),
                'tools_used': [r['tool'] for r in all_sub_results],
                'was_complex': is_complex
            }
        }
        self.cache.set(user_query, result)
        return result
    def get_stats(self):
        return {
            'documents_count': self.vectordb.count(),
            'cache_size': self.cache.size(),
            'model': self.llm.model_name,
            'device': self.llm.device
        }
    def clear_cache(self):
        self.cache.clear()
        if self.verbose:
            print(" Cache cleared")
    def clear_database(self):
        self.vectordb.clear()
        if self.verbose:
            print(" Database cleared")
