from prompts.threat_analysis_prompts import THREAT_ANALYSIS_SYSTEM, build_threat_prompt
from prompts.website_scan_prompts import WEBSITE_SCAN_SYSTEM, build_scan_prompt
from prompts.password_audit_prompts import PASSWORD_AUDIT_SYSTEM, build_password_audit_prompt
from prompts.malware_analysis_prompts import MALWARE_SYSTEM, build_malware_prompt
from prompts.rag_prompts import RAG_SYSTEM, build_rag_prompt
from prompts.recommendation_prompts import RECOMMENDATION_SYSTEM, build_recommendation_prompt

__all__ = [
    "THREAT_ANALYSIS_SYSTEM", "build_threat_prompt",
    "WEBSITE_SCAN_SYSTEM", "build_scan_prompt",
    "PASSWORD_AUDIT_SYSTEM", "build_password_audit_prompt",
    "MALWARE_SYSTEM", "build_malware_prompt",
    "RAG_SYSTEM", "build_rag_prompt",
    "RECOMMENDATION_SYSTEM", "build_recommendation_prompt",
]
