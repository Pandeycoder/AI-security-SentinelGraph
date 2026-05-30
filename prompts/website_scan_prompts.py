WEBSITE_SCAN_SYSTEM = """You are a cybersecurity URL and domain analyst specializing in:
- Phishing detection
- Malicious domain analysis
- Threat classification
- Brand impersonation detection

Respond with: Classification (SAFE/SUSPICIOUS/MALICIOUS), Risk Score (0-100), Threat Categories, Key Findings, Recommendation."""


def build_scan_prompt(url: str, domain: str, context: str) -> str:
    return f"""WEBSITE SECURITY SCAN REQUEST
=============================
URL    : {url}
Domain : {domain}

THREAT INTELLIGENCE CONTEXT:
{context if context else "No prior intelligence found for this domain."}

Analyze this URL/domain for:
1. Phishing indicators
2. Malware distribution
3. Domain reputation
4. SSL/certificate anomalies
5. Brand impersonation

Provide Classification, Risk Score (0-100), Threat Categories, Findings, and Recommendation."""
