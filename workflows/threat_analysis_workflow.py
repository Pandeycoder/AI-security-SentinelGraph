"""
Threat Analysis Workflow
Flow: ingest → retrieve context → AI review → risk score → recommend → cite → emit event
"""
from graph.builders.threat_graph_builder import threat_analysis_graph
from graph.state.threat_state import ThreatAnalysisState
from events.threat_event_publisher import ThreatEventPublisher
from observability.metrics import active_workflows, ai_latency
import time


class ThreatAnalysisWorkflow:
    def __init__(self, publisher: ThreatEventPublisher = None):
        self._graph = threat_analysis_graph
        self._publisher = publisher or ThreatEventPublisher()

    async def run(self, threat_id: str, source_ip: str, threat_type: str, description: str) -> dict:
        initial_state: ThreatAnalysisState = {
            "threat_id": threat_id,
            "source_ip": source_ip,
            "threat_type": threat_type,
            "description": description,
            "retrieved_context": None,
            "ai_analysis": None,
            "risk_score": None,
            "recommendations": None,
            "citations": None,
            "validated": False,
            "error": None,
        }

        active_workflows.inc()
        start = time.perf_counter()
        try:
            result = await self._graph.ainvoke(initial_state)
            return result
        except Exception as e:
            return {**initial_state, "error": str(e)}
        finally:
            ai_latency.observe(time.perf_counter() - start)
            active_workflows.dec()
