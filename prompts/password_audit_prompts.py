PASSWORD_AUDIT_SYSTEM = """You are a password security expert. Provide clear, practical password improvement recommendations.
Never store, repeat, or echo back the actual password. Work only with the characteristics provided.
Be concise, friendly, and security-focused."""


def build_password_audit_prompt(
    length: int,
    has_upper: bool,
    has_lower: bool,
    has_digit: bool,
    has_special: bool,
    issues: list,
    score: int,
) -> str:
    characteristics = f"""Password Characteristics (password text NOT provided for security):
- Length        : {length} characters
- Has Uppercase : {has_upper}
- Has Lowercase : {has_lower}
- Has Digits    : {has_digit}
- Has Special   : {has_special}
- Current Score : {score}/100
- Detected Issues: {", ".join(issues) if issues else "None"}"""

    return f"""{characteristics}

Based on these characteristics and issues, provide:
1. 3-5 specific, actionable recommendations to improve this password
2. Best practices reminder
3. One sentence on why each issue matters

Do NOT suggest the user reuse this password. Encourage a password manager."""
