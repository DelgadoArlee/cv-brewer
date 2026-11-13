class LLMAdapterError(Exception):
    pass


class LLMAdapterConnectionError(LLMAdapterError):
    pass


class LLMAdapterTimeoutError(LLMAdapterError):
    pass


class LLMAdapterResponseError(LLMAdapterError):
    pass


class LLMAdapterModelNotFoundError(LLMAdapterError):
    pass
