import time

class EpisodicMemory:
    def __init__(self):
        self.events = []

    def store(self, content, salience=0.1):
        self.events.append({
            "time": time.time(),
            "content": content,
            "salience": salience
        })

    def sample_for_sleep(self, threshold=0.5):
        return [e for e in self.events if e["salience"] >= threshold]
