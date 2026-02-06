class WebSearchTool:
    def __init__(self):
        self.enabled = True
    def search(self, query, max_results=3):
            try:
                from ddgs import DDGS
            except ImportError:
                from duckduckgo_search import DDGS
            results = []
            with DDGS() as ddgs:
                for r in ddgs.text(query, max_results=max_results):
                    body = r.get('body', '')
                    if body:
                        results.append(body)
            print(f"DuckDuckGo: Found {len(results)} results")
            return results
        except ImportError:
            print("DuckDuckGo package not installed!")
            print("Install with: pip install ddgs")
            return []
        except Exception as e:
            print(f" DuckDuckGo search error: {e}")
            return []
