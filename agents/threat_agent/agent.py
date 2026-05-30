from agents.threat_agent.prompt import SYSTEM_PROMPT
from agents.threat_agent.tools import get_tools
from agents.threat_agent.memory import AgentMemory
from agents.threat_agent.validator import validate_input, validate_output


class _Agent:
    def __init__(self, llm=None, memory: AgentMemory = None):
        from providers.ollama_llm_provider import OllamaLLMProvider
        self._llm = llm or OllamaLLMProvider()
        self._tools = get_tools()
        self._memory = memory or AgentMemory()
        self._system = SYSTEM_PROMPT

    async def run(self, input_text: str, session_id: str = None) -> str:
        if not validate_input({"text": input_text}):
            return "Invalid input provided."
        context = await self._memory.recall(session_id) if session_id else ""
        prompt = f"{context}\nUser: {input_text}" if context else input_text
        result = await self._llm.generate(prompt, system=self._system)
        if not validate_output(result):
            return "Agent produced no valid output."
        if session_id:
            await self._memory.store(session_id, input_text, result)
        return result


# Module-level singleton
threat_agent = _Agent()
