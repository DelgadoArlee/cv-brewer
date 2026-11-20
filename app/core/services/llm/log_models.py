from dataclasses import dataclass, field
from uuid import uuid4

from core.services.logger.models import LogEntry, LogError, LogPerformance, utc_now


class LLMTimeoutError(Exception):
    pass


@dataclass(frozen=True, slots=True)
class LLMGenerationParameters:
    temperature: float | None = None
    top_p: float | None = None
    top_k: int | None = None
    num_ctx: int | None = None
    max_tokens: int | None = None


@dataclass(frozen=True, slots=True)
class LLMRequestLog:
    system_prompt: str | None
    prompt: str
    parameters: LLMGenerationParameters = field(default_factory=LLMGenerationParameters)


@dataclass(frozen=True, slots=True)
class LLMResponseLog:
    content: str | None = None
    finish_reason: str | None = None


@dataclass(frozen=True, slots=True)
class LLMUsageLog:
    input_tokens: int | None = None
    output_tokens: int | None = None
    total_tokens: int | None = None


@dataclass(frozen=True, slots=True)
class LLMLogRecord(LogEntry):
    provider: str = ""
    model: str = ""
    request: LLMRequestLog = field(
        default_factory=lambda: LLMRequestLog(system_prompt=None, prompt="")
    )
    response: LLMResponseLog = field(default_factory=LLMResponseLog)
    usage: LLMUsageLog = field(default_factory=LLMUsageLog)


def new_log_id() -> str:
    return str(uuid4())


def build_llm_log_record(
    provider: str,
    model: str,
    request: LLMRequestLog,
    response: LLMResponseLog,
    usage: LLMUsageLog,
    performance: LogPerformance,
    status: str,
    error: LogError | None = None,
    processing_step_id: str | None = None,
) -> LLMLogRecord:
    return LLMLogRecord(
        id=new_log_id(),
        provider=provider,
        model=model,
        operation="generate_structured",
        status=status,
        request=request,
        response=response,
        usage=usage,
        performance=performance,
        error=error or LogError(),
        created_at=utc_now(),
        processing_step_id=processing_step_id,
    )


__all__ = [
    "LLMGenerationParameters",
    "LLMLogRecord",
    "LLMRequestLog",
    "LLMResponseLog",
    "LLMTimeoutError",
    "LLMUsageLog",
    "build_llm_log_record",
    "new_log_id",
]
