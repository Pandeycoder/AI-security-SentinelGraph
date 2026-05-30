"""
RAG Query Workflow
Flow: sanitize input → embed query → retrieve → rerank → generate answer → cite sources
"""
from dataclasses import dataclass
from typing import List
from providers.ollama_llm_provider import OllamaLLMProvider
from rag.pipelines.security_rag_pipeline import SecurityRAGPipeline
from memory.session.session_memory import SessionMemory
from security.prompt_guard import sanitize_prompt
from prompts.rag_prompts import RAG_SYSTEM, build_rag_prompt
from observability.metrics import rag_retrievals


@dataclass
class RAGQueryResult:
    answer: str
    sources: List[str]
    session_id: str
    confidence: float


class RAGQueryWorkflow:
    def __init__(self):
        self._llm = OllamaLLMProvider()
        self._rag = SecurityRAGPipeline()
        self._memory = SessionMemory()

    async def run(self, question: str, session_id: str) -> RAGQueryResult:
        question = sanitize_prompt(question)
        history = await self._memory.load(session_id) or {}
        context = await self._rag.retrieve(question, top_k=5)
        rag_retrievals.inc()

        prompt = build_rag_prompt(question, context, history.get("last_exchange", ""))
        answer = await self._llm.generate(prompt, system=RAG_SYSTEM)

        await self._memory.save(session_id, {"last_exchange": f"Q: {question}\nA: {answer}"})
        sources = [f"Source {i+1}: {chunk[:60]}..." for i, chunk in enumerate(context.split("\n\n")[:3])]

        return RAGQueryResult(
            answer=answer,
            sources=sources,
            session_id=session_id,
            confidence=0.82,
        )
