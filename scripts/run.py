import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.agent import LivingAgent
from memory.consolidation import consolidate

agent = LivingAgent(model="llama3.2")

# Load previous state if it exists
if agent.load_state():
    print("Loaded previous memories and experiences.")
else:
    print("Starting fresh with new agent.")

print("Agent awake. Type 'sleep' to consolidate.\n")

try:
    while True:
        user = input("> ")
        if user.lower() == "sleep":
            print("Agent entering sleep phase...")
            
            # Consolidate episodic memories into semantic knowledge
            events = agent.episodic.sample_for_sleep(threshold=0.15)
            if events:
                abstracted = consolidate(events)
                
                # Identify which categories are being updated
                updated_categories = set()
                for new_fact in abstracted:
                    if "remember:" in new_fact or "asked to remember" in new_fact:
                        updated_categories.add("memory")
                    elif "preference:" in new_fact:
                        updated_categories.add("preference")
                    elif "behavior/habit:" in new_fact:
                        updated_categories.add("behavior")
                    elif "identity:" in new_fact or "stated:" in new_fact:
                        updated_categories.add("identity")
                    elif "fact:" in new_fact:
                        updated_categories.add("general")
                
                # Remove old facts in these categories to avoid conflicts
                if updated_categories:
                    new_semantic = []
                    category_keywords = {
                        "memory": ["remember", "passphrase", "phrase"],
                        "preference": ["preference:", "favorite", "like", "dislike"],
                        "behavior": ["behavior/habit:", "always", "never", "usually"],
                        "identity": ["stated:", "name", "i am"],
                        "general": ["fact:"]
                    }
                    
                    for fact in agent.semantic.facts:
                        # Check if this fact should be removed (belongs to an updated category)
                        should_remove = False
                        for category in updated_categories:
                            keywords = category_keywords.get(category, [])
                            if any(kw.lower() in fact.lower() for kw in keywords):
                                should_remove = True
                                break
                        
                        if not should_remove:
                            new_semantic.append(fact)
                    
                    agent.semantic.facts = new_semantic
                
                # Add new consolidated facts
                for abstraction in abstracted:
                    agent.semantic.add(abstraction)
                
                print(f"Consolidated {len(events)} important events into {len(abstracted)} facts.")
                for fact in abstracted:
                    print(f"  • {fact}")
            else:
                print("No important events to consolidate.")
            
            agent.save_state()
            break
        if user.strip():
            agent.observe(user)
            print(agent.respond())
finally:
    # Always save state on exit
    agent.save_state()
    print("\nMemories saved. Agent sleeping.")
