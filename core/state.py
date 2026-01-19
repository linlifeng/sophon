class WorkingState:
    def __init__(self, max_turns=8):
        self.max_turns = max_turns
        self.buffer = []

    def add(self, role, content):
        self.buffer.append({"role": role, "content": content})
        if len(self.buffer) > self.max_turns:
            self.buffer.pop(0)

    def context(self):
        return self.buffer.copy()
