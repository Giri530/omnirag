class ContentTransformer:
    def __init__(self, llm_client):
        self.llm = llm_client
    def transform(self, content, user_level):
        if user_level == "intermediate":
            return content
        if user_level == "beginner":
            return self._simplify(content)
        if user_level == "expert":
            return self._add_technical_depth(content)
        return content
    def _simplify(self, content):
        """Make content simple for beginners"""
        prompt = f"""Rewrite this text for complete beginners:
Original Text:
{content}
Instructions:
- Use VERY simple language
- Remove all jargon and technical terms
- Add everyday analogies
- Keep it short and clear
- Explain like teaching a child
Simplified Version:"""
        return self.llm.generate(prompt, max_tokens=300)
    def _add_technical_depth(self, content):
        """Add technical details for experts"""
        prompt = f"""Enhance this text with technical depth for experts:
Original Text:
{content}
Instructions:
- Add precise technical terminology
- Include implementation details
- Add relevant algorithms or methods
- Be concise but thorough
- Assume expert knowledge
Technical Version:"""
        return self.llm.generate(prompt, max_tokens=300)
    def polish(self, answer, user_level):
        prompt = f"""Polish this answer for a {user_level} level user:
Draft Answer:
{answer}
Instructions:
- Ensure consistent tone for {user_level} level
- Remove any inappropriate complexity
- Make structure clear
- Keep concise and focused
Polished Answer:"""
        return self.llm.generate(prompt, max_tokens=500)
