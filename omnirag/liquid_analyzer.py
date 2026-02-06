class LiquidAnalyzer:
    def __init__(self, llm_client):
        self.llm = llm_client  
    def analyze(self, query):
        prompt = self._create_classification_prompt(query)
        try:
            response = self.llm.generate(
                prompt, 
                max_tokens=50,
                temperature=0.1
            )
            result = self._parse_llm_response(response, query)
            if result['complexity'] not in ['beginner', 'intermediate', 'expert']:
                print(f" Invalid LLM response: {response}")
                result = self._fallback_analysis(query)
                result['method'] = 'fallback'
            else:
                result['method'] = 'llm'
            return result
        except Exception as e:
            print(f" LLM analysis failed: {e}")
            result = self._fallback_analysis(query)
            result['method'] = 'fallback'
            return result
    def _create_classification_prompt(self, query):
        prompt = (
            "You are an expert at analyzing user questions to determine their expertise level.\n\n"
            "TASK: Classify the user's expertise level based on their question.\n\n"
            f"QUESTION: \"{query}\"\n\n"
            "CLASSIFICATION CRITERIA:\n\n"
            "**BEGINNER** - User is new to the topic:\n"
            "- Uses simple, everyday language\n"
            "- Asks 'what is', 'how do I', 'explain' questions\n"
            "- Seeks basic definitions or introductions\n"
            "- Shows no assumed prior knowledge\n"
            "- Examples:\n"
            "  * What is machine learning?\n"
            "  * How do I start learning Python?\n\n"
            "**INTERMEDIATE** - User has some knowledge:\n"
            "- Uses some technical terms correctly\n"
            "- Asks about comparisons, differences, or best practices\n"
            "- Understands basics but seeks deeper understanding\n"
            "- Examples:\n"
            "  * What's the difference between supervised and unsupervised learning?\n"
            "  * When should I use a list vs a dictionary in Python?\n\n"
            "**EXPERT** - User has advanced knowledge:\n"
            "- Uses precise technical terminology\n"
            "- Asks about optimization, architecture, or implementation details\n"
            "- Discusses performance, scalability, or edge cases\n"
            "- Examples:\n"
            "  * How can I optimize my BERT model's inference latency?\n"
            "  * What's the best architecture for distributed training?\n\n"
            "ANALYSIS STEPS:\n"
            "1. Identify technical terms used\n"
            "2. Assess assumed background knowledge\n"
            "3. Evaluate question complexity\n"
            "4. Determine appropriate level\n\n"
            "OUTPUT FORMAT (respond with ONLY this format):\n"
            "LEVEL: [beginner/intermediate/expert]\n"
            "CONFIDENCE: [high/medium/low]\n"
            "REASON: [one sentence explaining why]\n\n"
            "Now analyze the question above:"
        )
        return prompt
    def _parse_llm_response(self, response, query):
        response_lower = response.lower().strip()
        level = 'intermediate'
        if 'level:' in response_lower:
            level_line = [line for line in response_lower.split('\n') if 'level:' in line]
            if level_line:
                level_text = level_line[0].split('level:')[1].strip()
                if 'beginner' in level_text:
                    level = 'beginner'
                elif 'expert' in level_text:
                    level = 'expert'
                elif 'intermediate' in level_text:
                    level = 'intermediate'
        else:
            if 'beginner' in response_lower:
                level = 'beginner'
            elif 'expert' in response_lower:
                level = 'expert'
            elif 'intermediate' in response_lower:
                level = 'intermediate'
        confidence = 0.8 
        if 'confidence:' in response_lower:
            if 'high' in response_lower:
                confidence = 0.95
            elif 'medium' in response_lower:
                confidence = 0.75
            elif 'low' in response_lower:
                confidence = 0.55
        reasoning = "LLM classification"
        if 'reason:' in response_lower:
            reason_line = [line for line in response.split('\n') if 'reason:' in line.lower()]
            if reason_line:
                reasoning = reason_line[0].split(':', 1)[1].strip()
        print(f"[LIQUID-LLM] Level: {level} | Confidence: {confidence:.2f}")
        print(f"[LIQUID-LLM] Reasoning: {reasoning}")
        return {
            'complexity': level,
            'confidence': confidence,
            'reasoning': reasoning,
            'query': query,
            'raw_response': response
        }
    def _fallback_analysis(self, query):
        query_lower = query.lower()
        beginner_score = 0
        intermediate_score = 0
        expert_score = 0
        beginner_keywords = {
            'what is': 4,
            'how do i': 4,
            'how to': 3,
            'explain': 3,
            'simple': 2,
            'basic': 2,
            'help me': 2,
            'understand': 2,
            'learn': 2,
            'tutorial': 3,
            'introduction': 3,
            'for beginners': 5,
            'getting started': 4,
            'first time': 3,
            "i'm new": 5,
            "i don't know": 4,
        }
        intermediate_keywords = {
            'difference between': 3,
            'compare': 2,
            'when to use': 3,
            'which is better': 2,
            'best practice': 3,
            'use case': 2,
            'vs': 1,
            'pros and cons': 2,
        }
        expert_keywords = {
            'optimize': 4,
            'optimization': 4,
            'algorithm': 3,
            'architecture': 4,
            'implement': 3,
            'implementation': 3,
            'performance': 3,
            'scalability': 4,
            'production': 3,
            'distributed': 4,
            'latency': 3,
            'throughput': 3,
            'memory management': 5,
            'complexity': 2,
            'edge case': 3,
            'bottleneck': 3,
        }
        for keyword, weight in beginner_keywords.items():
            if keyword in query_lower:
                beginner_score += weight
        for keyword, weight in intermediate_keywords.items():
            if keyword in query_lower:
                intermediate_score += weight
        for keyword, weight in expert_keywords.items():
            if keyword in query_lower:
                expert_score += weight
        words = query.split()
        word_count = len(words)
        if word_count < 7:
            beginner_score += 2
        elif word_count > 20:
            expert_score += 2
        elif word_count > 12:
            intermediate_score += 1
        technical_terms = [
            'api', 'json', 'sql', 'framework', 'library', 'function',
            'class', 'method', 'parameter', 'variable', 'gpu', 'cpu',
            'tensor', 'vector', 'matrix', 'neural', 'model', 'training',
            'inference', 'batch', 'epoch', 'gradient', 'hyperparameter'
        ]
        tech_count = sum(1 for term in technical_terms if term in query_lower)
        if tech_count == 0:
            beginner_score += 2
        elif tech_count >= 3:
            expert_score += 3
        elif tech_count >= 1:
            intermediate_score += 1
        question_starters = {
            'what is': 'beginner',
            'how do': 'beginner',
            'why': 'intermediate',
            'when': 'intermediate',
            'which': 'intermediate',
            'how can i optimize': 'expert',
            'how to implement': 'expert',
        }
        for starter, level_type in question_starters.items():
            if query_lower.startswith(starter):
                if level_type == 'beginner':
                    beginner_score += 2
                elif level_type == 'intermediate':
                    intermediate_score += 2
                elif level_type == 'expert':
                    expert_score += 2
                break
        total_score = beginner_score + intermediate_score + expert_score
        if total_score == 0:
            level = 'intermediate'
            confidence = 0.5
        else:
            scores = {
                'beginner': beginner_score,
                'intermediate': intermediate_score,
                'expert': expert_score
            }
            level = max(scores, key=scores.get)
            confidence = scores[level] / total_score
        reasoning = f"Keyword analysis: B={beginner_score}, I={intermediate_score}, E={expert_score}"
        print(f"[LIQUID-FALLBACK] Level: {level} | Confidence: {confidence:.2f}")
        print(f"[LIQUID-FALLBACK] {reasoning}")
        return {
            'complexity': level,
            'confidence': confidence,
            'reasoning': reasoning,
            'query': query,
            'scores': scores
        }
