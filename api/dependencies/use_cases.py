from fastapi import Depends
from application.use_cases.analyze_threat import AnalyzeThreatUseCase
from application.use_cases.scan_website import ScanWebsiteUseCase
from application.use_cases.ask_security_question import AskSecurityQuestionUseCase
from infrastructure.ollama.ollama_provider import OllamaProvider
from infrastructure.postgres.threat_repository import PostgresThreatRepository
from domain.services.threat_scorer import ThreatScorerService
from events.threat_event_publisher import ThreatEventPublisher
from rag.pipelines.security_rag_pipeline import SecurityRAGPipeline

def get_analyze_threat_uc() -> AnalyzeThreatUseCase:
    return AnalyzeThreatUseCase(
        threat_repo=PostgresThreatRepository(),
        llm=OllamaProvider(),
        scorer=ThreatScorerService(),
        publisher=ThreatEventPublisher(),
    )

def get_scan_website_uc() -> ScanWebsiteUseCase:
    return ScanWebsiteUseCase(llm=OllamaProvider(), rag_pipeline=SecurityRAGPipeline())

def get_ask_security_uc() -> AskSecurityQuestionUseCase:
    return AskSecurityQuestionUseCase(llm=OllamaProvider(), rag_pipeline=SecurityRAGPipeline())
