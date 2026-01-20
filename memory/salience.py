def estimate_salience(text: str) -> float:
    """
    Estimate how important/salient a piece of text is.
    Higher scores indicate more important information.
    """
    score = 0.1  # Base score
    text_lower = text.lower()
    
    # Explicit importance markers (with higher boost for explicit "remember" requests)
    importance_markers = [
        ("remember", 0.4),
        ("remmeber", 0.4),  # Common typo
        ("membe", 0.4),  # Partial match for typos
        ("important", 0.35),
        ("prefer", 0.25),
        ("always", 0.2),
        ("never", 0.2),
        ("my name is", 0.35),
        ("i am", 0.2),
        ("i like", 0.15),
        ("i dislike", 0.15),
        ("i hate", 0.2),
        ("i love", 0.2),
        ("passphrase", 0.4),
        ("password", 0.4),
        ("secret", 0.3),
    ]
    
    for marker, boost in importance_markers:
        if marker in text_lower:
            score += boost
    
    # Length-based scoring (longer messages often have more info)
    text_length = len(text.split())
    if text_length > 10:
        score += 0.1
    if text_length > 30:
        score += 0.1
    
    # Punctuation (questions and exclamations are often important)
    if "?" in text:
        score += 0.15
    if "!" in text:
        score += 0.1
    
    return min(score, 1.0)
