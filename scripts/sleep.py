import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from memory.consolidation import consolidate
from storage.db import save
from core.agent import LivingAgent

# Create agent and load its current state
agent = LivingAgent()
agent.load_state()

# Get high-salience events for consolidation (lower threshold to capture more)
events = agent.episodic.sample_for_sleep(threshold=0.15)

if events:
    # Consolidate events into semantic abstractions
    abstracted = consolidate(events)
    
    # Add abstractions to semantic memory
    for abstraction in abstracted:
        agent.semantic.add(abstraction)
    
    # Save updated agent state
    agent.save_state()
    
    print(f"Sleep complete. Consolidated {len(events)} important events into {len(abstracted)} facts.")
    print("\nLearned facts:")
    for fact in abstracted:
        print(f"  - {fact}")
else:
    print("Sleep complete. No important events to consolidate.")
