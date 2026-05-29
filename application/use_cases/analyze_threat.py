from domain.entities.threat import Threat
from domain.interfaces.threat_repository import IThreatRepository
from domain.interfaces.llm_provider import ILLMProvider
from domain.services.threat_scorer import ThreatScorerService
from events.threat_event_publisher import ThreatEventPublisher

class AnalyzeThreatUseCase:
    def __init__(
        self,
        threat_repo: IThreatRepository,
        llm: ILLMProvider,
        scorer: ThreatScorerService,
        publisher: ThreatEventPublisher,
    ):
        self._repo = threat_repo
        self._llm = llm
        self._scorer = scorer
        self._publisher = publisher

    async def execute(self, threat: Threat) -> Threat:
        threat.risk_score = self._scorer.calculate_risk_score(threat)
        prompt = f"Analyze this security threat: {threat.description}. Provide key findings."
        analysis = await self._llm.generate(prompt, system="You are a senior security analyst.")
        threat.metadata["ai_analysis"] = analysis
        saved = await self._repo.save(threat)
        await self._publisher.publish(saved)
        return saved
