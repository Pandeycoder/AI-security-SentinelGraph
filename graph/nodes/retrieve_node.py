from graph.state.threat_state import ThreatAnalysisState
from rag.pipelines.security_rag_pipeline import SecurityRAGPipeline

rag = SecurityRAGPipeline()

async def retrieve_node(state: ThreatAnalysisState) -> ThreatAnalysisState:
    query = f"{state['threat_type']} {state['description']}"
    context = await rag.retrieve(query)
    return {**state, "retrieved_context": context}
