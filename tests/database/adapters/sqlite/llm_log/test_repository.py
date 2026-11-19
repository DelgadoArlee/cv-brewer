from datetime import datetime
from pathlib import Path

from core.services.logger import LogError, LogPerformance
from core.services.llm import (
    LLMGenerationParameters,
    LLMLogRecord,
    LLMRequestLog,
    LLMResponseLog,
    LLMUsageLog,
)
from database import create_llm_log_service, initialize_database


def _record(record_id: str, created_at: datetime) -> LLMLogRecord:
    return LLMLogRecord(
        id=record_id,
        operation="generate_structured",
        status="success",
        performance=LogPerformance(
            started_at=created_at,
            completed_at=created_at,
            duration_ms=12.5,
            memory_before_bytes=100,
            memory_after_bytes=120,
            memory_peak_bytes=150,
            memory_delta_bytes=20,
        ),
        error=LogError(),
        created_at=created_at,
        provider="ollama",
        model="llama3.1",
        request=LLMRequestLog(
            system_prompt="Extract data.",
            prompt="Resume text.",
            parameters=LLMGenerationParameters(),
        ),
        response=LLMResponseLog(
            content='{"name": "Ada"}',
            finish_reason="stop",
        ),
        usage=LLMUsageLog(
            input_tokens=10,
            output_tokens=5,
            total_tokens=15,
        ),
    )


def test_repository_saves_and_lists_llm_logs(tmp_path: Path) -> None:
    database_path = tmp_path / "llm-logs.db"
    initialize_database(database_path)
    repository = create_llm_log_service(database_path)
    first = _record("first", datetime(2026, 11, 19, 10, 0))
    second = _record("second", datetime(2026, 11, 19, 10, 1))

    repository.save(first)
    repository.save(second)

    records = repository.list_all()
    assert [record.id for record in records] == ["first", "second"]
    assert records[0].provider == "ollama"
    assert records[0].request.system_prompt == "Extract data."
    assert records[0].request.parameters.temperature is None
    assert records[0].response.finish_reason == "stop"
    assert records[0].usage.total_tokens == 15
    assert records[0].performance.duration_ms == 12.5


def test_repository_lists_empty_database(tmp_path: Path) -> None:
    database_path = tmp_path / "empty.db"
    initialize_database(database_path)

    assert create_llm_log_service(database_path).list_all() == []
