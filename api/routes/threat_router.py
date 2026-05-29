from fastapi import APIRouter, Depends, HTTPException
from api.requests.threat_request import ThreatCreateRequest
from api.responses.threat_response import ThreatResponse
from api.dependencies.use_cases import get_analyze_threat_uc
from application.use_cases.analyze_threat import AnalyzeThreatUseCase
from domain.entities.threat import Threat
from domain.enums.threat_level import ThreatLevel
from domain.enums.threat_status import ThreatStatus
import uuid

router = APIRouter()

@router.post("/analyze", response_model=ThreatResponse)
async def analyze_threat(
    request: ThreatCreateRequest,
    use_case: AnalyzeThreatUseCase = Depends(get_analyze_threat_uc),
):
    threat = Threat(
        id=str(uuid.uuid4()),
        source_ip=request.source_ip,
        threat_type=request.threat_type,
        level=ThreatLevel[request.level.upper()],
        status=ThreatStatus.DETECTED,
        description=request.description,
    )
    result = await use_case.execute(threat)
    return ThreatResponse.from_entity(result)

@router.get("/{threat_id}", response_model=ThreatResponse)
async def get_threat(threat_id: str):
    # Injected via Depends in production
    raise HTTPException(status_code=501, detail="Not implemented")
