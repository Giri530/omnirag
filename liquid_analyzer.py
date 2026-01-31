class LiquidAnalyzer:
    def __init__(self, llm_client):
        self.llm = llm_client
    def analyze(self, query):
        prompt = f"""Analyze this question and determine the user's expertise level.
Question: "{query}"
Consider:
- Vocabulary used (simple vs technical)
- Question depth (basic vs advanced)
- Background knowledge assumed
- Phrasing style
Respond with ONLY ONE WORD: beginner, intermediate, or expert
Level:"""
        try:
            response = self.llm.generate(prompt, max_tokens=10, temperature=0.3)
            level = response.strip().lower()
            if level not in ['beginner', 'intermediate', 'expert']:
                level = self._fallback_analysis(query)
        except Exception as e:
            level = self._fallback_analysis(query)
        return {
            'complexity': level,
            'query': query
        }
    def _fallback_analysis(self, query):
        query_lower = query.lower()
        beginner_words = ['what is', 'how do', 'explain', 'simple', 'basic', 'help me', 'start']
        beginner_score = sum(1 for word in beginner_words if word in query_lower)
        expert_words = ['optimize', 'architecture', 'algorithm', 'implement', 'technical', 'advanced']
        expert_score = sum(1 for word in expert_words if word in query_lower)
        if beginner_score > expert_score:
            return "beginner"
        elif expert_score > beginner_score:
            return "expert"
        else:
            return "intermediate"
