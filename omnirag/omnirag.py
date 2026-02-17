from llm_client import LLMClient
from vectordb_tool import VectorDBTool
from web_search_tool import WebSearchTool
from liquid_analyzer import LiquidAnalyzer
from agentic_planner import AgenticPlanner
from chain_decomposer import ChainDecomposer
from cache import SimpleCache
from content_transformer import ContentTransformer
from smart_translator import SmartTranslator
from voice_processor import VoiceProcessor
class OmniRAG:
    def __init__(
        self,
        model_name="Qwen/Qwen2.5-0.5B-Instruct",
        embedding_model="all-MiniLM-L6-v2",
        enable_web_search=False,
        use_4bit=False,
        verbose=False,
        output_language="auto", 
        enable_voice=False,     
    ):
        self.verbose = verbose
        self.output_language = output_language
        print(f"   Model: {model_name}")
        print(f"   Loading {model_name}...")
        self.llm = LLMClient(model_name, use_4bit)
        print(f"   Loading embedding model: {embedding_model}...")
        self.vectordb = VectorDBTool(embedding_model)
        self.liquid_analyzer = LiquidAnalyzer(self.llm)
        self.chain_decomposer = ChainDecomposer(self.llm)
        self.agentic_planner = AgenticPlanner(self.llm)
        self.cache = SimpleCache()
        self.content_transformer = ContentTransformer(self.llm)
        if enable_web_search:
            self.web_search = WebSearchTool()
            self.web_search_enabled = True
            print(f" Web search enabled")
        else:
            self.web_search = None
            self.web_search_enabled = False
        if output_language != "auto":
            self.translator = SmartTranslator()
            print(f" Smart Translation enabled (output: {output_language})")
        else:
            self.translator = None
        if enable_voice:
            self.voice = VoiceProcessor()
            print(f"Voice Input/Output enabled")
        else:
            self.voice = None
    def add_documents(self, documents):
        processed_docs = []
        for doc in documents:
            if isinstance(doc, str) and (doc.endswith('.pdf') or doc.endswith('.txt')):
                content = self.content_transformer.load_file(doc)
            else:
                content = doc
            processed_docs.append(content)
        self.vectordb.add_documents(processed_docs)
        print(f"Added {len(processed_docs)} documents to knowledge base")
    def query(self, user_query=None, output_language=None, speak_answer=False):
        target_lang = output_language or self.output_language
        if user_query is None:
            if self.voice:
                user_query = self.voice.listen()
                if not user_query:
                    return {
                        'answer': 'No speech detected. Please try again.',
                        'error': True
                    }
            else:
                return {
                    'answer': 'No query provided. Enable voice or provide text query.',
                    'error': True
                }
        if self.verbose:
            print(f" Query: {user_query}")
        cached_result = self.cache.get(user_query)
        if cached_result:
            if self.verbose:
                print(f"Cache hit!")
            answer = cached_result
            if self.translator and target_lang != "auto":
                answer = self.translator.translate_answer(
                    answer_text=answer,
                    source_chunks=[],
                    target_language=target_lang
                )
            if speak_answer and self.voice:
                self.voice.speak(answer, language=target_lang)
            return {
                'answer': answer,
                'cached': True,
                'output_language': target_lang
            }
        user_level = self.liquid_analyzer.analyze(user_query)
        if self.verbose:
            print(f" User level: {user_level}")
        sub_queries = self.chain_decomposer.decompose(user_query)
        if self.verbose:
            print(f" Sub-queries: {len(sub_queries)}")
            for i, sq in enumerate(sub_queries, 1):
                print(f"   {i}. {sq}")
        tools = self.agentic_planner.plan(user_query)
        if self.verbose:
            print(f"  Tools selected: {tools}")
        all_chunks = []
        chunks = self.vectordb.search(user_query, top_k=3)
        all_chunks.extend(chunks)
        for sq in sub_queries[:2]: 
            sq_chunks = self.vectordb.search(sq, top_k=2)
            all_chunks.extend(sq_chunks)
        if self.verbose:
            print(f" Retrieved {len(all_chunks)} chunks (original language)")
        if self.web_search_enabled and 'web_search' in tools:
            if self.verbose:
                print(f" Searching web...")
            web_results = self.web_search.search(user_query, max_results=3)
            all_chunks.extend(web_results)
            if self.verbose:
                print(f"   Found {len(web_results)} web results")
        answer = self._generate_answer(user_query, all_chunks, user_level)
        if self.verbose:
            print(f" Generated answer")
        self.cache.set(user_query, answer)
        if self.translator and target_lang != "auto":
            if self.verbose:
                print(f" Translating to {target_lang}...")
            answer = self.translator.translate_answer(
                answer_text=answer,
                source_chunks=all_chunks,
                target_language=target_lang
            )
        if speak_answer and self.voice:
            if self.verbose:
                print(f" Speaking answer...")
            self.voice.speak(answer, language=target_lang)
        result = {
            'answer': answer,
            'sources': all_chunks[:5],  # Top 5 sources
            'user_level': user_level,
            'tools_used': tools,
            'sub_queries': sub_queries,
            'output_language': target_lang,
            'voice_output': speak_answer,
            'cached': False
        }
        if self.verbose:
            print(f"{'='*60}\n")
        return result
    def voice_query(self, output_language=None):
        if not self.voice:
            print(" Voice not enabled! Initialize with enable_voice=True")
            return {'error': 'Voice not enabled'}
        return self.query(
            user_query=None,  
            output_language=output_language,
            speak_answer=True
        )
    def _generate_answer(self, query, chunks, user_level):
        if not chunks:
            return "I don't have enough information to answer this question. Please add more documents or enable web search."
        context = "\n\n".join([f"Source {i+1}: {chunk}" for i, chunk in enumerate(chunks[:5])])
        if user_level == "beginner":
            instruction = "Explain in simple terms with examples"
        elif user_level == "expert":
            instruction = "Provide detailed technical explanation"
        else:
            instruction = "Provide clear and accurate explanation"
        prompt = f"""{instruction}.
Context:
{context}
Question: {query}
Answer:"""
        answer = self.llm.generate(
            prompt,
            max_tokens=200,
            temperature=0.75
        )
        return answer.strip()
    def clear_cache(self):
        self.cache.clear()
        print("Cache cleared")
    def get_stats(self):
        return {
            'documents': self.vectordb.get_count(),
            'cache_size': self.cache.size(),
            'web_search_enabled': self.web_search_enabled,
            'translation_enabled': self.translator is not None,
            'voice_enabled': self.voice is not None,
            'output_language': self.output_language
        }
