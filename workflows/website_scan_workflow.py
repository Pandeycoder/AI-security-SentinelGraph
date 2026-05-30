"""
Website Scan Workflow
Flow: extract domain → RAG lookup → LLM analysis → classify → score → recommend
"""
from dataclasses import dataclass, field
from typing import List
from providers.ollama_llm_provider import OllamaLLMProvider
from rag.pipelines.security_rag_pipeline import SecurityRAGPipeline
from prompts.website_scan_prompts import WEBSITE_SCAN_SYSTEM, build_scan_prompt
from observability.metrics import active_workflows


@dataclass
class WebsiteScanResult:
    url: str
    domain: str
    is_malicious: bool
    risk_score: float
    threat_categories: List[str]
    findings: List[str]
    recommendation: str
    raw_analysis: str = ""


class WebsiteScanWorkflow:
    def __init__(self):
        self._llm = OllamaLLMProvider()
        self._rag = SecurityRAGPipeline()

    async def run(self, url: str) -> WebsiteScanResult:
        domain = url.split("/")[2] if "//" in url else url.split("/")[0]
        active_workflows.inc()
        try:
            context = await self._rag.retrieve(f"malicious website phishing domain {domain}")
            prompt = build_scan_prompt(url, domain, context)
            analysis = await self._llm.generate(prompt, system=WEBSITE_SCAN_SYSTEM)

            is_malicious = any(kw in analysis.lower() for kw in ["malicious", "phishing", "dangerous", "block"])
            risk_score = 85.0 if is_malicious else 15.0
            categories = []
            for cat in ["phishing", "malware", "spam", "botnet", "cryptojacking"]:
                if cat in analysis.lower():
                    categories.append(cat)

            return WebsiteScanResult(
                url=url,
                domain=domain,
                is_malicious=is_malicious,
                risk_score=risk_score,
                threat_categories=categories,
                findings=[line.strip() for line in analysis.split("\n") if line.strip()][:5],
                recommendation="BLOCK: Domain flagged as malicious." if is_malicious else "SAFE: No threats detected.",
                raw_analysis=analysis,
            )
        finally:
            active_workflows.dec()
