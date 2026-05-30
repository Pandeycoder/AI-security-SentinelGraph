from fastapi import APIRouter
from orchestration.workflow_orchestrator import WorkflowOrchestrator
from orchestration.agent_orchestrator import AgentOrchestrator
from pydantic import BaseModel

router = APIRouter()
_workflow_orch = WorkflowOrchestrator()
_agent_orch = AgentOrchestrator()


class ThreatRequest(BaseModel):
    threat_id: str
    source_ip: str
    threat_type: str
    description: str

class URLRequest(BaseModel):
    url: str

class PasswordRequest(BaseModel):
    password: str

class QuestionRequest(BaseModel):
    question: str
    session_id: str = "default"

class AgentPipelineRequest(BaseModel):
    input_text: str
    session_id: str = None


@router.post("/threat")
async def orchestrate_threat(req: ThreatRequest):
    return await _workflow_orch.analyze_threat(
        threat_id=req.threat_id, source_ip=req.source_ip,
        threat_type=req.threat_type, description=req.description,
    )

@router.post("/scan")
async def orchestrate_scan(req: URLRequest):
    return await _workflow_orch.scan_website(url=req.url)

@router.post("/password")
async def orchestrate_password(req: PasswordRequest):
    return await _workflow_orch.audit_password(password=req.password)

@router.post("/query")
async def orchestrate_query(req: QuestionRequest):
    return await _workflow_orch.query_knowledge(question=req.question, session_id=req.session_id)

@router.post("/agents/full-pipeline")
async def run_agent_pipeline(req: AgentPipelineRequest):
    result = await _agent_orch.run_full_pipeline(req.input_text, req.session_id)
    return {
        "threat_analysis": result.threat_analysis,
        "review": result.review,
        "recommendations": result.recommendations,
        "citations": result.citations,
        "compliance_notes": result.compliance_notes,
    }
