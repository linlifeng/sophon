def estimate_salience(text: str) -> float:
    # Placeholder: heuristic
    keywords = ["remember", "important", "prefer", "always", "never"]
    score = 0.1
    for k in keywords:
        if k in text.lower():
            score += 0.2
    return min(score, 1.0)
