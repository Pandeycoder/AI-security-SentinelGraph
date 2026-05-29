from graph.state.threat_state import ThreatAnalysisState
from infrastructure.ollama.ollama_provider import OllamaProvider

llm = OllamaProvider()

async def recommendation_node(state: ThreatAnalysisState) -> ThreatAnalysisState:
    prompt = (
        f"Based on this threat analysis:\n{state.get('ai_analysis', '')}\n"
        f"Risk score: {state.get('risk_score', 0)}\n"
        "List 3 specific remediation recommendations."
    )
    response = await llm.generate(prompt)
    recs = [line.strip() for line in response.split("\n") if line.strip()]
    return {**state, "recommendations": recs[:3]}
