"""
Agent Orchestrator
Coordinates multi-agent pipelines where multiple specialized agents
collaborate to produce a final result (e.g. review → citation → recommendation).
"""
from agents.threat_agent.agent import threat_agent
from agents.review_agent.agent import review_agent
from agents.recommendation_agent.agent import recommendation_agent
from agents.citation_agent.agent import citation_agent
from agents.compliance_agent.agent import compliance_agent
from dataclasses import dataclass, field
from typing import List
import logging

logger = logging.getLogger(__name__)


@dataclass
class MultiAgentResult:
    threat_analysis: str = ""
    review: str = ""
    recommendations: List[str] = field(default_factory=list)
    citations: List[str] = field(default_factory=list)
    compliance_notes: str = ""


class AgentOrchestrator:
    """
    Runs agents in a defined pipeline sequence.
    Pattern: Threat → Review → Recommend → Cite → Compliance
    """

    async def run_full_pipeline(self, input_text: str, session_id: str = None) -> MultiAgentResult:
        result = MultiAgentResult()
        logger.info("Starting multi-agent pipeline")

        # Step 1: Threat Agent — initial threat analysis
        result.threat_analysis = await threat_agent.run(input_text, session_id)

        # Step 2: Review Agent — validate and deepen the analysis
        result.review = await review_agent.run(result.threat_analysis, session_id)

        # Step 3: Recommendation Agent — generate remediation steps
        rec_input = f"Threat: {input_text}\nAnalysis: {result.review}"
        raw_recs = await recommendation_agent.run(rec_input, session_id)
        result.recommendations = [line.strip() for line in raw_recs.split("\n") if line.strip()][:5]

        # Step 4: Citation Agent — add intelligence sources
        cite_input = f"Analysis: {result.review}"
        raw_cites = await citation_agent.run(cite_input, session_id)
        result.citations = [line.strip() for line in raw_cites.split("\n") if line.strip()][:3]

        # Step 5: Compliance Agent — map to regulatory frameworks
        result.compliance_notes = await compliance_agent.run(result.review, session_id)

        logger.info("Multi-agent pipeline completed")
        return result

    async def run_threat_review(self, threat_description: str, session_id: str = None) -> dict:
        """Lightweight 2-agent flow: Threat → Review only."""
        analysis = await threat_agent.run(threat_description, session_id)
        review = await review_agent.run(analysis, session_id)
        return {"analysis": analysis, "review": review}
