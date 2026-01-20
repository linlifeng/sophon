import requests
import json
from pathlib import Path
from datetime import datetime
from core.state import WorkingState
from core.search import InternetSearch
from memory.episodic import EpisodicMemory
from memory.semantic import SemanticMemory
from memory.salience import estimate_salience
from storage.db import save, load

AGENT_STATE_FILE = Path("storage/agent_state.json")

class LivingAgent:
    def __init__(self, model="llama2", ollama_url="http://localhost:11434"):
        self.state = WorkingState()
        self.episodic = EpisodicMemory()
        self.semantic = SemanticMemory(ollama_url=ollama_url)
        self.search = InternetSearch()
        self.model = model
        self.ollama_url = ollama_url

    def observe(self, user_input):
        self.state.add("user", user_input)
        salience = estimate_salience(user_input)
        self.episodic.store(user_input, salience)

    def respond(self):
        """Generate response using local Ollama model with semantic memory and internet search."""
        context = self.state.context()
        
        # Build conversation history for context
        conversation = "\n".join([
            f"{msg['role'].upper()}: {msg['content']}"
            for msg in context
        ])
        
        # Get the last user message
        last_user_msg = next(
            (msg['content'] for msg in reversed(context) if msg['role'] == 'user'),
            ""
        )
        
        # Get current date
        current_date = datetime.now().strftime("%B %d, %Y")
        
        # Retrieve relevant semantic memories
        relevant_memories = self.semantic.retrieve_relevant(last_user_msg)
        
        # Build memory section
        memory_section = ""
        if relevant_memories:
            memory_section = "\n=== PERSISTENT KNOWLEDGE FROM ALL PAST CONVERSATIONS ===\n" + "\n".join(
                f"• {fact}" for fact in relevant_memories
            ) + "\n=== END OF PERSISTENT KNOWLEDGE ===\n"
        
        # Check if we should search the internet for this query
        search_section = ""
        search_performed = False
        if self.search.should_search(last_user_msg):
            search_results = self.search.search(last_user_msg, max_results=3)
            if search_results:
                search_section = "\n" + search_results
                search_performed = True
        
        # Create the final prompt with all context
        # Be VERY explicit if search was performed
        search_instruction = ""
        if search_performed:
            search_instruction = "\nIMPORTANT: I have searched the internet for current information above. You MUST use the search results provided. Do not talk about your training data or knowledge cutoff - use the search results instead.\n"
        
        prompt = f"""You are a helpful assistant with persistent long-term memory and access to current internet information.

CURRENT DATE: {current_date}

{memory_section}{search_section}{search_instruction}CURRENT CONVERSATION:
{conversation}

INSTRUCTIONS:
1. The current date is {current_date}
2. If search results are provided above, ALWAYS base your answer on those results
3. Use persistent knowledge for personal facts about the user
4. When answering, cite sources: "According to the search results...", "I found that..."
5. Do NOT mention your training data or knowledge cutoff
6. Do NOT say you don't have access to real-time information if search results are provided
7. Answer naturally and conversationally
8. Be factual and accurate

Respond to the user's last message."""
        
        try:
            response = requests.post(
                f"{self.ollama_url}/api/generate",
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "stream": False
                },
                timeout=60
            )
            
            if response.status_code == 200:
                result = response.json()
                assistant_response = result.get("response", "").strip()
                
                # Store the response in working memory
                self.state.add("assistant", assistant_response)
                
                return assistant_response if assistant_response else "I'm thinking..."
            else:
                return f"Error: Ollama returned status {response.status_code}"
        
        except requests.exceptions.ConnectionError:
            return "Error: Cannot connect to Ollama. Is it running on http://localhost:11434?"
        except Exception as e:
            return f"Error: {str(e)}"
    
    def save_state(self):
        """Save agent state (memories) to disk for persistence across sessions."""
        state_data = {
            "semantic_memory": self.semantic.all(),
            "episodic_memory": self.episodic.events,
            "working_memory": self.state.context()
        }
        AGENT_STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
        AGENT_STATE_FILE.write_text(json.dumps(state_data, indent=2))
    
    def load_state(self):
        """Load agent state (memories) from disk if it exists."""
        if AGENT_STATE_FILE.exists():
            state_data = json.loads(AGENT_STATE_FILE.read_text())
            
            # Load semantic memory
            for fact in state_data.get("semantic_memory", []):
                self.semantic.add(fact)
            
            # Load episodic memory
            for event in state_data.get("episodic_memory", []):
                self.episodic.events.append(event)
            
            # Don't load working memory (keep it fresh for new session)
            return True
        return False

