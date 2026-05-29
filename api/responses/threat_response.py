from pydantic import BaseModel
from datetime import datetime
from domain.entities.threat import Threat

class ThreatResponse(BaseModel):
    id: str
    source_ip: str
    threat_type: str
    level: str
    status: str
    risk_score: float
    detected_at: datetime

    @classmethod
    def from_entity(cls, threat: Threat) -> "ThreatResponse":
        return cls(
            id=threat.id,
            source_ip=threat.source_ip,
            threat_type=threat.threat_type,
            level=threat.level.name,
            status=threat.status.value,
            risk_score=threat.risk_score,
            detected_at=threat.detected_at,
        )
