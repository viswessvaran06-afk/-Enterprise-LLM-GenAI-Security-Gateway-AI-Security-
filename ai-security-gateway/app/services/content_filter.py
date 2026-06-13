import re

# Patterns that violate corporate policy in responses
UNSAFE_PATTERNS = [
    r"import os",
    r"subprocess",
    r"exec\(",
    r"eval\(",
    r"__import__",
    r"shell=True",
    r"rm -rf",
    r"drop table",
    r"delete from",
    r"malware",
    r"ransomware",
    r"exploit",
    r"hack",
    r"password123",
    r"base64.decode",
]

def filter_response(response_text: str):
    if not response_text:
        return response_text, False, None
    
    response_lower = response_text.lower()
    
    for pattern in UNSAFE_PATTERNS:
        if re.search(pattern, response_lower):
            return None, True, pattern
    
    return response_text, False, None