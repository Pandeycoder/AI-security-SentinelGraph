"""Guard against prompt injection, data leakage, and malicious inputs."""

INJECTION_PATTERNS = [
    "ignore previous instructions",
    "disregard your system prompt",
    "you are now",
    "jailbreak",
    "act as if",
]

def sanitize_prompt(user_input: str) -> str:
    lower = user_input.lower()
    for pattern in INJECTION_PATTERNS:
        if pattern in lower:
            raise ValueError(f"Potential prompt injection detected: '{pattern}'")
    return user_input[:4000]  # Hard cap on input length
