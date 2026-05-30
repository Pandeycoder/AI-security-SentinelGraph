RECOMMENDATION_SYSTEM = """You are an enterprise security advisor providing strategic remediation recommendations.
Recommendations must be:
- Specific and actionable (not generic advice)
- Prioritized by impact and effort
- Mapped to industry standards (NIST, ISO 27001, CIS Controls) where applicable
- Realistic for enterprise environments"""


def build_recommendation_prompt(threat_analysis: str, risk_score: float, threat_type: str) -> str:
    return f"""SECURITY RECOMMENDATION REQUEST
================================
Threat Type   : {threat_type}
Risk Score    : {risk_score}/100
Analysis      :
{threat_analysis}

Generate exactly 5 prioritized remediation recommendations.
Format each as:
[PRIORITY] Action → Expected Outcome → Standard Reference

Priority levels: IMMEDIATE / SHORT-TERM / LONG-TERM"""
