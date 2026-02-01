class ChainDecomposer:
    def __init__(self, llm_client):
        self.llm = llm_client
        self.complex_indicators = [
            'compare', 'vs', 'versus', 'difference between',
            'and also', 'what are', 'list', 'explain each',
            'step by step', 'how and why'
        ]
    def is_complex(self, query):
        query_lower = query.lower()
        has_multiple_sentences = query.count('.') + query.count('?') + query.count('\n') > 1
        has_complex_words = any(ind in query_lower for ind in self.complex_indicators)
        is_long = len(query.split()) > 15
        return has_multiple_sentences or has_complex_words or is_long
    def decompose(self, query):
        prompt = f"""Break this complex question into 2-4 simpler questions.
Original Question: {query}

Instructions:
- Return ONLY the sub-questions
- One question per line
- NO numbering, bullets, or explanations
- Keep questions simple and clear
Sub-questions:"""
        response = self.llm.generate(prompt, max_tokens=200)
        lines = [line.strip() for line in response.split('\n') if line.strip()]
        sub_queries = []
        for line in lines:
            cleaned = line
            for prefix in ['1.', '2.', '3.', '4.', '-', '*', '•', 'Q:', 'Question:']:
                if cleaned.startswith(prefix):
                    cleaned = cleaned[len(prefix):].strip()
            if cleaned and len(cleaned) > 5 and '?' in cleaned or len(cleaned.split()) > 3:
                sub_queries.append(cleaned)
        return sub_queries[:4] if sub_queries else [query]
