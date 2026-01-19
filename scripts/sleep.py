from memory.consolidation import consolidate
from storage.db import save
from core.agent import LivingAgent

agent = LivingAgent()
events = agent.episodic.sample_for_sleep()

abstracted = consolidate(events)

save({
    "semantic_memory": abstracted
})

print("Sleep complete. Knowledge consolidated.")
