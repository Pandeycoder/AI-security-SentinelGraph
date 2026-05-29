from domain.entities.threat import Threat
from domain.services.threat_scorer import ThreatScorerService

class GenerateRiskScoreUseCase:
    def __init__(self, scorer: ThreatScorerService):
        self._scorer = scorer

    async def execute(self, threat: Threat) -> float:
        return self._scorer.calculate_risk_score(threat)
