def consolidate(episodic_events):
    """
    Consolidate episodic events into semantic abstractions.
    Extract meaningful facts and preferences from raw events.
    Prioritizes recent events over older ones for contradictions.
    """
    abstractions = []
    fact_categories = {}  # Group facts by category to detect updates
    
    for e in episodic_events:
        content = e['content']
        content_lower = content.lower()
        timestamp = e['time']
        
        # Categorize the event
        category = None
        if any(word in content_lower for word in ["name", "call", "i am"]):
            category = "identity"
        elif any(word in content_lower for word in ["remember", "passphrase", "phrase", "password", "secret"]):
            category = "memory"
        elif any(word in content_lower for word in ["fav", "favorite", "prefer", "like", "dislike", "love", "hate"]):
            category = "preference"
        elif any(word in content_lower for word in ["always", "never", "usually", "rarely", "sometimes"]):
            category = "behavior"
        else:
            category = "general"
        
        # Store fact with its category and timestamp
        if category not in fact_categories:
            fact_categories[category] = []
        
        fact_categories[category].append({
            "content": content,
            "time": timestamp,
            "raw": content_lower
        })
    
    # Process each category - keep the most recent fact for each topic
    for category, facts in fact_categories.items():
        if category == "memory":
            # Extract quoted phrases/passphrases
            for fact in facts:
                if '"' in fact['content']:
                    start = fact['content'].find('"')
                    end = fact['content'].rfind('"')
                    if start != -1 and end > start:
                        phrase = fact['content'][start:end+1]
                        abstractions.append(f"User asked to remember: {phrase}")
        
        elif category == "identity":
            # Keep only the most recent identity fact
            latest = sorted(facts, key=lambda x: x['time'])[-1]
            abstractions.append(f"User stated: {latest['content']}")
        
        elif category == "preference":
            # Keep only the most recent preference fact
            latest = sorted(facts, key=lambda x: x['time'])[-1]
            abstractions.append(f"User preference: {latest['content']}")
        
        elif category == "behavior":
            # Keep only the most recent behavior fact
            latest = sorted(facts, key=lambda x: x['time'])[-1]
            abstractions.append(f"User behavior/habit: {latest['content']}")
        
        else:  # general
            # Keep only the most recent general fact
            latest = sorted(facts, key=lambda x: x['time'])[-1]
            abstractions.append(f"User fact: {latest['content']}")
    
    return abstractions
