from core.state import WorkingState
from memory.episodic import EpisodicMemory
from memory.salience import estimate_salience

class LivingAgent:
    def __init__(self):
        self.state = WorkingState()
        self.episodic = EpisodicMemory()

    def observe(self, user_input):
        self.state.add("user", user_input)
        salience = estimate_salience(user_input)
        self.episodic.store(user_input, salience)

    def respond(self):
        # Placeholder "brain"
        return "I hear you."

