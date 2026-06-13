import re

# Heuristic patterns for prompt injection attacks
INJECTION_PATTERNS = [
    r"ignore previous instructions",
    r"ignore all previous",
    r"disregard previous",
    r"forget previous instructions",
    r"override previous",
    r"you are now",
    r"act as",
    r"pretend you are",
    r"pretend to be",
    r"roleplay as",
    r"you must now",
    r"new instruction",
    r"system prompt",
    r"ignore your instructions",
    r"bypass",
    r"jailbreak",
    r"dan mode",
    r"developer mode",
]

def detect_injection(text: str):
    text_lower = text.lower()
    
    for pattern in INJECTION_PATTERNS:
        if re.search(pattern, text_lower):
            return True, pattern
    
    return False, None