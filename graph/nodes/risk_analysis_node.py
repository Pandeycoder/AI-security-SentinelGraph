from graph.state.threat_state import ThreatAnalysisState

async def risk_analysis_node(state: ThreatAnalysisState) -> ThreatAnalysisState:
    analysis = state.get("ai_analysis", "")
    score = 50.0
    if "critical" in analysis.lower(): score = 95.0
    elif "high" in analysis.lower(): score = 75.0
    elif "medium" in analysis.lower(): score = 45.0
    elif "low" in analysis.lower(): score = 15.0
    return {**state, "risk_score": score}
