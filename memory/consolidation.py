def consolidate(episodic_events):
    abstractions = []
    for e in episodic_events:
        abstractions.append(f"User preference or fact: {e['content']}")
    return abstractions
