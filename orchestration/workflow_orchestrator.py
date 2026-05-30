"""
Workflow Orchestrator
The central brain that routes incoming requests to the correct workflow,
manages lifecycle, handles failures, and publishes events.
"""
from enum import Enum
from workflows.threat_analysis_workflow import ThreatAnalysisWorkflow
from workflows.website_scan_workflow import WebsiteScanWorkflow
from workflows.password_audit_workflow import PasswordAuditWorkflow
from workflows.malware_analysis_workflow import MalwareAnalysisWorkflow
from workflows.rag_query_workflow import RAGQueryWorkflow
from events.threat_event_publisher import ThreatEventPublisher
from observability.metrics import active_workflows
import logging

logger = logging.getLogger(__name__)


class WorkflowType(str, Enum):
    THREAT_ANALYSIS = "threat_analysis"
    WEBSITE_SCAN = "website_scan"
    PASSWORD_AUDIT = "password_audit"
    MALWARE_ANALYSIS = "malware_analysis"
    RAG_QUERY = "rag_query"


class WorkflowOrchestrator:
    def __init__(self):
        self._workflows = {
            WorkflowType.THREAT_ANALYSIS: ThreatAnalysisWorkflow(),
            WorkflowType.WEBSITE_SCAN:    WebsiteScanWorkflow(),
            WorkflowType.PASSWORD_AUDIT:  PasswordAuditWorkflow(),
            WorkflowType.RAG_QUERY:       RAGQueryWorkflow(),
        }

    async def execute(self, workflow_type: WorkflowType, **kwargs) -> dict:
        workflow = self._workflows.get(workflow_type)
        if not workflow:
            raise ValueError(f"Unknown workflow: {workflow_type}")

        logger.info(f"Executing workflow: {workflow_type}")
        try:
            result = await workflow.run(**kwargs)
            logger.info(f"Workflow {workflow_type} completed successfully")
            return {"status": "success", "workflow": workflow_type, "result": result}
        except Exception as e:
            logger.error(f"Workflow {workflow_type} failed: {e}", exc_info=True)
            return {"status": "error", "workflow": workflow_type, "error": str(e)}

    async def analyze_threat(self, threat_id: str, source_ip: str, threat_type: str, description: str) -> dict:
        return await self.execute(
            WorkflowType.THREAT_ANALYSIS,
            threat_id=threat_id, source_ip=source_ip,
            threat_type=threat_type, description=description,
        )

    async def scan_website(self, url: str) -> dict:
        return await self.execute(WorkflowType.WEBSITE_SCAN, url=url)

    async def audit_password(self, password: str) -> dict:
        return await self.execute(WorkflowType.PASSWORD_AUDIT, password=password)

    async def query_knowledge(self, question: str, session_id: str) -> dict:
        return await self.execute(WorkflowType.RAG_QUERY, question=question, session_id=session_id)
