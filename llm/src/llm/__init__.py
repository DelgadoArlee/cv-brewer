from llm.adapters.ollama import OllamaAdapter, OllamaConfig, create_ollama_client
from llm.llm_service import LLMService


def create_llm_service(config: OllamaConfig | None = None) -> LLMService:
    client = create_ollama_client(config or OllamaConfig())
    return LLMService(OllamaAdapter(client))


__all__ = [
    "LLMService",
    "OllamaAdapter",
    "OllamaConfig",
    "create_llm_service",
    "create_ollama_client",
]
