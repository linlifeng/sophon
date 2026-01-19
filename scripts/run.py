from core.agent import LivingAgent

agent = LivingAgent()

print("Agent awake. Type 'sleep' to consolidate.\n")

while True:
    user = input("> ")
    if user == "sleep":
        break
    agent.observe(user)
    print(agent.respond())
