from dataclasses import asdict
from typing import Any

from sqlalchemy import select
from sqlalchemy.orm import Session, sessionmaker

from core.services.logger import LogEntry, LogError, LogPerformance, LogSink
from core.services.llm.log_models import (
    LLMGenerationParameters,
    LLMLogRecord,
    LLMRequestLog,
    LLMResponseLog,
    LLMUsageLog,
)
from core.services.llm.log_port import LLMLogRepository
from database.adapters.sqlite.engine import session_scope
from database.adapters.sqlite.llm_log.models import LLMLog


def _parameters_from_model(value: Any) -> LLMGenerationParameters:
    if not isinstance(value, dict):
        value = {}
    return LLMGenerationParameters(
        temperature=value.get("temperature"),
        top_p=value.get("top_p"),
        top_k=value.get("top_k"),
        num_ctx=value.get("num_ctx"),
        max_tokens=value.get("max_tokens"),
    )


def _to_model(record: LLMLogRecord) -> LLMLog:
    return LLMLog(
        id=record.id,
        provider=record.provider,
        model=record.model,
        operation=record.operation,
        status=record.status,
        system_prompt=record.request.system_prompt,
        prompt=record.request.prompt,
        parameters=asdict(record.request.parameters),
        response_content=record.response.content,
        finish_reason=record.response.finish_reason,
        input_tokens=record.usage.input_tokens,
        output_tokens=record.usage.output_tokens,
        total_tokens=record.usage.total_tokens,
        started_at=record.performance.started_at,
        completed_at=record.performance.completed_at,
        duration_ms=record.performance.duration_ms,
        memory_before_bytes=record.performance.memory_before_bytes,
        memory_after_bytes=record.performance.memory_after_bytes,
        memory_peak_bytes=record.performance.memory_peak_bytes,
        memory_delta_bytes=record.performance.memory_delta_bytes,
        error_type=record.error.type,
        error_message=record.error.message,
        created_at=record.created_at,
    )


def _to_record(model: LLMLog) -> LLMLogRecord:
    return LLMLogRecord(
        id=model.id,
        operation=model.operation,
        status=model.status,
        performance=LogPerformance(
            started_at=model.started_at,
            completed_at=model.completed_at,
            duration_ms=model.duration_ms,
            memory_before_bytes=model.memory_before_bytes,
            memory_after_bytes=model.memory_after_bytes,
            memory_peak_bytes=model.memory_peak_bytes,
            memory_delta_bytes=model.memory_delta_bytes,
        ),
        error=LogError(type=model.error_type, message=model.error_message),
        created_at=model.created_at,
        provider=model.provider,
        model=model.model,
        request=LLMRequestLog(
            system_prompt=model.system_prompt,
            prompt=model.prompt,
            parameters=_parameters_from_model(model.parameters),
        ),
        response=LLMResponseLog(
            content=model.response_content,
            finish_reason=model.finish_reason,
        ),
        usage=LLMUsageLog(
            input_tokens=model.input_tokens,
            output_tokens=model.output_tokens,
            total_tokens=model.total_tokens,
        ),
    )


class SqliteLLMLogRepository(LLMLogRepository, LogSink):
    def __init__(self, session_factory: sessionmaker[Session]) -> None:
        self._session_factory = session_factory

    def save(self, record: LLMLogRecord) -> None:
        with session_scope(self._session_factory) as session:
            session.add(_to_model(record))

    def write(self, entry: LogEntry) -> None:
        if not isinstance(entry, LLMLogRecord):
            raise TypeError("Only LLM log records can be written to this sink.")
        self.save(entry)

    def list_all(self) -> list[LLMLogRecord]:
        with session_scope(self._session_factory) as session:
            statement = select(LLMLog).order_by(LLMLog.created_at)
            models = session.scalars(statement).all()
            return [_to_record(model) for model in models]
