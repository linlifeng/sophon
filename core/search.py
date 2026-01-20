import requests
import json
from typing import List, Dict, Optional

class InternetSearch:
    """
    Search the internet for information using DuckDuckGo API (no API key required).
    Falls back to other methods if needed.
    """
    
    def __init__(self):
        self.duckduckgo_url = "https://api.duckduckgo.com"
    
    def search_duckduckgo(self, query: str, max_results: int = 3) -> List[Dict]:
        """
        Search using DuckDuckGo's free API.
        Returns list of search results with title, snippet, and URL.
        """
        try:
            params = {
                "q": query,
                "format": "json",
                "no_html": 1,
                "skip_disambig": 1
            }
            
            response = requests.get(self.duckduckgo_url, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                results = []
                
                # Parse abstract if available
                if data.get("AbstractText"):
                    results.append({
                        "title": data.get("Heading", "Summary"),
                        "snippet": data.get("AbstractText"),
                        "url": data.get("AbstractURL", ""),
                        "source": "DuckDuckGo"
                    })
                
                # Parse related topics
                for topic in data.get("RelatedTopics", [])[:max_results]:
                    if isinstance(topic, dict) and "Text" in topic:
                        results.append({
                            "title": topic.get("FirstURL", "").split("/")[-1] or "Result",
                            "snippet": topic.get("Text", ""),
                            "url": topic.get("FirstURL", ""),
                            "source": "DuckDuckGo"
                        })
                
                return results[:max_results]
            else:
                return []
        
        except requests.exceptions.Timeout:
            return []
        except Exception as e:
            print(f"Warning: DuckDuckGo search failed: {e}")
            return []
    
    def search(self, query: str, max_results: int = 3) -> str:
        """
        Search the internet and format results as a readable string.
        Returns formatted search results or empty string if no results.
        """
        results = self.search_duckduckgo(query, max_results)
        
        if not results:
            return ""
        
        formatted = f"\n=== SEARCH RESULTS FOR: {query} ===\n"
        for i, result in enumerate(results, 1):
            formatted += f"\n{i}. {result['title']}\n"
            formatted += f"   {result['snippet']}\n"
            if result['url']:
                formatted += f"   URL: {result['url']}\n"
        formatted += "=== END SEARCH RESULTS ===\n"
        
        return formatted
    
    def should_search(self, query: str) -> bool:
        """
        Determine if the query would benefit from an internet search.
        Returns True if query seems to ask for factual, current information.
        """
        search_triggers = [
            "what is", "who is", "when", "where", "how", "latest", "current",
            "news", "today", "2024", "2025", "2026", "weather", "stock",
            "how do", "why", "what's new", "tell me about", "search for"
        ]
        
        query_lower = query.lower()
        return any(trigger in query_lower for trigger in search_triggers)
