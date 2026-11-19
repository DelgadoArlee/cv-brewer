from core.services.llm.log_models import LLMTimeoutError


class LLMAdapterError(Exception):
    pass


class LLMAdapterConnectionError(LLMAdapterError):
    pass


class LLMAdapterTimeoutError(LLMAdapterError, LLMTimeoutError):
    pass


class LLMAdapterResponseError(LLMAdapterError):
    pass


class LLMAdapterModelNotFoundError(LLMAdapterError):
    pass
