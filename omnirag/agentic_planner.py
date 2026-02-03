class AgenticPlanner:
    def __init__(self, llm_client):
        self.llm = llm_client
        self.web_keywords = [
            'latest', 'recent', 'current', 'now', 'today',
            '2024', '2025', '2026', 'news', 'trending',
            'this year', 'this month', 'update'
        ]
    def plan(self, query, web_available=False):
        query_lower = query.lower()
        needs_current_info = any(keyword in query_lower for keyword in self.web_keywords)
        if needs_current_info and web_available:
            return {
                'tool': 'web_search',
                'reasoning': 'Query requires current/recent information from web'
            }
        return {
            'tool': 'vectordb',
            'reasoning': 'Using local knowledge base for general information'
        }
