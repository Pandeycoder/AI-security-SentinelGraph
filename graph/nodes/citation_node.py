from graph.state.threat_state import ThreatAnalysisState

async def citation_node(state: ThreatAnalysisState) -> ThreatAnalysisState:
    context = state.get("retrieved_context", "")
    citations = [f"Source: {line[:80]}" for line in context.split("\n") if line.strip()][:3]
    return {**state, "citations": citations}
