from graph.state.threat_state import ThreatAnalysisState
from infrastructure.ollama.ollama_provider import OllamaProvider

llm = OllamaProvider()

async def review_node(state: ThreatAnalysisState) -> ThreatAnalysisState:
    prompt = (
        f"Threat: {state['description']}\n"
        f"Context: {state.get('retrieved_context', '')}\n"
        "Provide a detailed security analysis."
    )
    analysis = await llm.generate(prompt, system="You are a senior security analyst.")
    return {**state, "ai_analysis": analysis}
