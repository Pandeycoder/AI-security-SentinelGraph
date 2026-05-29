from typing import TypedDict, Optional, List

class ThreatAnalysisState(TypedDict):
    threat_id: str
    description: str
    source_ip: str
    threat_type: str
    retrieved_context: Optional[str]
    ai_analysis: Optional[str]
    risk_score: Optional[float]
    recommendations: Optional[List[str]]
    citations: Optional[List[str]]
    validated: bool
    error: Optional[str]
