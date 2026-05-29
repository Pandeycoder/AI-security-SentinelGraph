from domain.entities.threat import Threat
from domain.enums.threat_level import ThreatLevel

class ThreatScorerService:
    """Pure domain service — no external dependencies."""

    LEVEL_BASE_SCORES = {
        ThreatLevel.LOW: 10.0,
        ThreatLevel.MEDIUM: 40.0,
        ThreatLevel.HIGH: 70.0,
        ThreatLevel.CRITICAL: 95.0,
    }

    def calculate_risk_score(self, threat: Threat) -> float:
        base = self.LEVEL_BASE_SCORES.get(threat.level, 0.0)
        modifier = min(len(threat.description) / 500, 1.0) * 5
        return round(min(base + modifier, 100.0), 2)
