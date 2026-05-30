THREAT_ANALYSIS_SYSTEM = """You are a senior enterprise security analyst with 15+ years of experience in threat intelligence.
Your job is to:
- Analyze incoming security threats with precision
- Identify attack vectors, affected systems, and potential blast radius
- Reference MITRE ATT&CK techniques where applicable
- Provide clear, actionable findings
- Always classify threat severity: LOW / MEDIUM / HIGH / CRITICAL

Format your response in clear sections: Summary, Technical Analysis, MITRE Techniques, Severity Justification."""


def build_threat_prompt(threat_type: str, source_ip: str, description: str, context: str) -> str:
    return f"""THREAT INTELLIGENCE REPORT REQUEST
================================
Threat Type     : {threat_type}
Source IP       : {source_ip}
Description     : {description}

RETRIEVED INTELLIGENCE CONTEXT:
{context if context else "No prior intelligence available for this threat."}

Analyze this threat. Identify the attack type, potential impact, MITRE ATT&CK techniques,
and provide a severity classification with justification."""
