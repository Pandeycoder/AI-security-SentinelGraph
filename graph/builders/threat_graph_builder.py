from langgraph.graph import StateGraph, END
from graph.state.threat_state import ThreatAnalysisState
from graph.nodes.retrieve_node import retrieve_node
from graph.nodes.review_node import review_node
from graph.nodes.risk_analysis_node import risk_analysis_node
from graph.nodes.recommendation_node import recommendation_node
from graph.nodes.citation_node import citation_node

def build_threat_analysis_graph():
    graph = StateGraph(ThreatAnalysisState)

    graph.add_node("retrieve", retrieve_node)
    graph.add_node("review", review_node)
    graph.add_node("risk_analysis", risk_analysis_node)
    graph.add_node("recommendation", recommendation_node)
    graph.add_node("citation", citation_node)

    graph.set_entry_point("retrieve")
    graph.add_edge("retrieve", "review")
    graph.add_edge("review", "risk_analysis")
    graph.add_edge("risk_analysis", "recommendation")
    graph.add_edge("recommendation", "citation")
    graph.add_edge("citation", END)

    return graph.compile()

threat_analysis_graph = build_threat_analysis_graph()
