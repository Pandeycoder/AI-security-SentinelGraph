from dataclasses import dataclass, field
from datetime import datetime
from domain.enums.threat_level import ThreatLevel
from domain.enums.threat_status import ThreatStatus

@dataclass
class Threat:
    id: str
    source_ip: str
    threat_type: str
    level: ThreatLevel
    status: ThreatStatus
    description: str
    risk_score: float = 0.0
    detected_at: datetime = field(default_factory=datetime.utcnow)
    metadata: dict = field(default_factory=dict)

    def is_critical(self) -> bool:
        return self.level == ThreatLevel.CRITICAL

    def escalate(self) -> None:
        if self.level != ThreatLevel.CRITICAL:
            self.level = ThreatLevel(min(self.level.value + 1, ThreatLevel.CRITICAL.value))
