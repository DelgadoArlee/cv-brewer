from core.services.logger import LogEntry, LoggerService, LogError, LogPerformance, LogStatus
from core.services.llm.log_models import (
    LLMGenerationParameters,
    LLMRequestLog,
    LLMResponseLog,
    LLMTimeoutError,
    LLMUsageLog,
    build_llm_log_record,
)
from core.services.llm.models import (
    ChatMessage,
    GenerationResult,
    StructuredGenerationRequest,
)


def _join_messages(messages: list[ChatMessage], role: str) -> str | None:
    contents = [message.content for message in messages if message.role == role]
    return "\n".join(contents) if contents else None


def _user_prompt(messages: list[ChatMessage]) -> str:
    return "\n".join(
        message.content for message in messages if message.role != "system"
    )


def _request_log(request: StructuredGenerationRequest) -> LLMRequestLog:
    system_prompt = _join_messages(request.messages, "system")
    if system_prompt is None:
        system_prompt = _join_messages(request.messages, "assistant")
    return LLMRequestLog(
        system_prompt=system_prompt,
        prompt=_user_prompt(request.messages),
        parameters=LLMGenerationParameters(),
    )


def _response_log(result: GenerationResult | None) -> LLMResponseLog:
    if result is None:
        return LLMResponseLog()
    return LLMResponseLog(
        content=result.response_content,
        finish_reason=result.finish_reason,
    )


def _usage_log(result: GenerationResult | None) -> LLMUsageLog:
    if result is None:
        return LLMUsageLog()
    return LLMUsageLog(
        input_tokens=result.usage.input_tokens,
        output_tokens=result.usage.output_tokens,
        total_tokens=result.usage.total_tokens,
    )


def _status(error: Exception | None) -> str:
    if error is None:
        return LogStatus.SUCCESS
    if isinstance(error, (LLMTimeoutError, TimeoutError)):
        return LogStatus.TIMEOUT
    return LogStatus.FAILED


def _error_details(error: Exception | None) -> LogError:
    if error is None:
        return LogError()
    return LogError(type=type(error).__name__, message=str(error))


class LLMLogger:
    def __init__(self, provider: str, logger: LoggerService) -> None:
        self._provider = provider
        self._logger = logger

    def record_generation(
        self,
        request: StructuredGenerationRequest,
        performance: LogPerformance,
        result: GenerationResult | None = None,
        error: Exception | None = None,
    ) -> LogEntry:
        record = build_llm_log_record(
            provider=self._provider,
            model=request.model,
            request=_request_log(request),
            response=_response_log(result),
            usage=_usage_log(result),
            performance=performance,
            status=_status(error),
            error=_error_details(error),
        )
        self._logger.emit(record)
        return record
