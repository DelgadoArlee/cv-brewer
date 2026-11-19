from core.services.llm import LLMPort, LLMService
from core.services.llm.logger import LLMLogger

from llm.adapters.logging import LoggingLLMPort
from llm.adapters.ollama import OllamaAdapter, OllamaConfig, create_ollama_client


def create_llm_service(
    config: OllamaConfig | None = None,
    logger: LLMLogger | None = None,
) -> LLMService:
    client = create_ollama_client(config or OllamaConfig())
    port: LLMPort = OllamaAdapter(client)
    if logger is not None:
        port = LoggingLLMPort(port, logger)
    return LLMService(port)


__all__ = ["create_llm_service"]
