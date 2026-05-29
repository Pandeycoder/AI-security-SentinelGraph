class AskSecurityQuestionUseCase:
    def __init__(self, llm, rag_pipeline):
        self._llm = llm
        self._rag = rag_pipeline

    async def execute(self, question: str, session_id: str) -> str:
        context = await self._rag.retrieve(question)
        prompt = f"Context:\n{context}\n\nQuestion: {question}"
        return await self._llm.generate(prompt, system="You are an enterprise security expert.")
