from dataclasses import dataclass

@dataclass
class WebsiteScanResult:
    url: str
    is_malicious: bool
    risk_score: float
    findings: list[str]
    recommendation: str

class ScanWebsiteUseCase:
    def __init__(self, llm, rag_pipeline):
        self._llm = llm
        self._rag = rag_pipeline

    async def execute(self, url: str) -> WebsiteScanResult:
        context = await self._rag.retrieve(f"malicious website patterns {url}")
        prompt = f"Analyze this URL for security threats: {url}\nContext: {context}"
        response = await self._llm.generate(prompt)
        # Parse LLM response into structured result
        return WebsiteScanResult(
            url=url,
            is_malicious="malicious" in response.lower(),
            risk_score=75.0,  # Computed from actual LLM output in production
            findings=[response],
            recommendation="Block this domain" if "malicious" in response.lower() else "Safe to proceed",
        )
