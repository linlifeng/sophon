import requests
import json

class SemanticMemory:
    def __init__(self, ollama_url="http://localhost:11434", embedding_model="nomic-embed-text"):
        self.facts = []
        self.ollama_url = ollama_url
        self.embedding_model = embedding_model
        self.embeddings_cache = {}  # Cache embeddings to avoid recomputing
    
    def add(self, abstraction: str):
        self.facts.append(abstraction)
        # Clear cache when new facts are added
        self.embeddings_cache.clear()
    
    def all(self):
        return self.facts.copy()
    
    def _get_embedding(self, text: str) -> list:
        """Get embedding vector for text using Ollama's embedding model."""
        if text in self.embeddings_cache:
            return self.embeddings_cache[text]
        
        try:
            response = requests.post(
                f"{self.ollama_url}/api/embed",
                json={"model": self.embedding_model, "input": text},
                timeout=30
            )
            if response.status_code == 200:
                embedding = response.json()["embeddings"][0]
                self.embeddings_cache[text] = embedding
                return embedding
            else:
                # Fallback to None if embedding fails
                return None
        except Exception as e:
            print(f"Warning: Could not get embedding: {e}")
            return None
    
    def _cosine_similarity(self, vec1: list, vec2: list) -> float:
        """Compute cosine similarity between two vectors."""
        if vec1 is None or vec2 is None:
            return 0.0
        
        dot_product = sum(a * b for a, b in zip(vec1, vec2))
        magnitude1 = sum(a ** 2 for a in vec1) ** 0.5
        magnitude2 = sum(b ** 2 for b in vec2) ** 0.5
        
        if magnitude1 == 0 or magnitude2 == 0:
            return 0.0
        
        return dot_product / (magnitude1 * magnitude2)
    
    def retrieve_relevant(self, query: str, max_facts=None) -> list:
        """
        Retrieve semantically relevant facts using embedding similarity.
        Uses the local LLM's embedding model for semantic understanding.
        """
        if not self.facts:
            return []
        
        # Get embedding for the query
        query_embedding = self._get_embedding(query)
        if query_embedding is None:
            # Fallback to empty list if embedding fails
            return []
        
        # Score all facts by semantic similarity
        scored_facts = []
        for fact in self.facts:
            fact_embedding = self._get_embedding(fact)
            if fact_embedding is not None:
                similarity = self._cosine_similarity(query_embedding, fact_embedding)
                scored_facts.append((fact, similarity))
        
        # Sort by similarity score (descending)
        scored_facts.sort(key=lambda x: x[1], reverse=True)
        
        # Return top matches (or all if max_facts is None)
        max_facts = max_facts or len(scored_facts)
        
        # Only return facts with meaningful similarity (> 0.5)
        # But if all facts have low similarity, return the top ones anyway
        relevant = [fact for fact, score in scored_facts if score > 0.5]
        if not relevant:
            relevant = [fact for fact, score in scored_facts[:max_facts]]
        
        return relevant[:max_facts]
