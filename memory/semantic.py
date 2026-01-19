class SemanticMemory:
    def __init__(self):
        self.facts = []

    def add(self, abstraction: str):
        self.facts.append(abstraction)

    def all(self):
        return self.facts.copy()
