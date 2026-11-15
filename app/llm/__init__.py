from core.services.llm import LLMService

from llm.adapters.ollama import OllamaAdapter, OllamaConfig, create_ollama_client


def create_llm_service(config: OllamaConfig | None = None) -> LLMService:
    client = create_ollama_client(config or OllamaConfig())
    return LLMService(OllamaAdapter(client))


__all__ = ["create_llm_service"]
