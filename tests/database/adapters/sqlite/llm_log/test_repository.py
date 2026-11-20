from datetime import datetime
from pathlib import Path

from sqlalchemy import create_engine, inspect

from core.services.logger import LogError, LogPerformance
from core.services.llm import (
    LLMGenerationParameters,
    LLMLogRecord,
    LLMRequestLog,
    LLMResponseLog,
    LLMUsageLog,
)
from database import (
    create_llm_log_service,
    create_processing_log_service,
    initialize_database,
)


def _record(
    record_id: str,
    created_at: datetime,
    *,
    processing_step_id: str | None = None,
    status: str = "SUCCESS",
    error: LogError | None = None,
) -> LLMLogRecord:
    return LLMLogRecord(
        id=record_id,
        operation="generate_structured",
        status=status,
        performance=LogPerformance(
            started_at=created_at,
            completed_at=created_at,
            duration_ms=12.5,
            start_memory_mb=100.0,
            peak_memory_mb=150.0,
            end_memory_mb=120.0,
            memory_delta_mb=20.0,
            cpu_avg_percent=10.0,
            cpu_peak_percent=15.0,
            sample_count=2,
        ),
        error=error or LogError(),
        created_at=created_at,
        processing_step_id=processing_step_id,
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
    processing_logs = create_processing_log_service(database_path)
    run = processing_logs.start_run(
        process_name="resume_processing",
        process_version="1.0",
    )
    step = processing_logs.start_step(
        run_id=run.run_id,
        step_name="parsing",
        step_order=6,
    )
    first = _record(
        "first",
        datetime(2026, 11, 19, 10, 0),
        processing_step_id=step.step_id,
    )
    second = _record("second", datetime(2026, 11, 19, 10, 1))

    repository.save(first)
    repository.save(second)

    records = repository.list_all()
    assert [record.id for record in records] == ["first", "second"]
    assert records[0].provider == "ollama"
    assert records[0].status == "SUCCESS"
    assert records[0].processing_step_id == step.step_id
    assert records[1].processing_step_id is None
    assert records[0].request.system_prompt == "Extract data."
    assert records[0].request.parameters.temperature is None
    assert records[0].response.finish_reason == "stop"
    assert records[0].usage.total_tokens == 15
    assert records[0].performance.duration_ms == 12.5
    assert records[0].performance.start_memory_mb == 100.0
    assert records[0].performance.cpu_avg_percent == 10.0
    assert records[0].performance.sample_count == 2


def test_repository_lists_empty_database(tmp_path: Path) -> None:
    database_path = tmp_path / "empty.db"
    initialize_database(database_path)

    assert create_llm_log_service(database_path).list_all() == []


def test_repository_lists_recent_and_error_logs(tmp_path: Path) -> None:
    database_path = tmp_path / "query.db"
    initialize_database(database_path)
    repository = create_llm_log_service(database_path)
    records = [
        _record("old", datetime(2026, 11, 19, 10, 0)),
        _record(
            "error-text",
            datetime(2026, 11, 19, 10, 1),
            error=LogError(type="ValueError", message="bad output"),
        ),
        _record("failed", datetime(2026, 11, 19, 10, 2), status="FAILED"),
        _record("timeout", datetime(2026, 11, 19, 10, 3), status="TIMEOUT"),
        _record("newest", datetime(2026, 11, 19, 10, 4)),
    ]
    for record in records:
        repository.save(record)

    recent = repository.list_recent(3)
    errors = repository.list_errors(3)

    assert [record.id for record in recent] == ["newest", "timeout", "failed"]
    assert [record.id for record in errors] == ["timeout", "failed", "error-text"]


def test_migration_creates_llm_log_processing_link(tmp_path: Path) -> None:
    database_path = tmp_path / "schema.db"
    initialize_database(database_path)
    engine = create_engine(f"sqlite:///{database_path}")

    inspector = inspect(engine)
    columns = {column["name"] for column in inspector.get_columns("llm_logs")}
    foreign_keys = inspector.get_foreign_keys("llm_logs")
    check_constraints = inspector.get_check_constraints("llm_logs")

    assert {
        "processing_step_id",
        "start_memory_mb",
        "peak_memory_mb",
        "end_memory_mb",
        "memory_delta_mb",
        "cpu_avg_percent",
        "cpu_peak_percent",
        "sample_count",
    }.issubset(columns)
    assert "memory_before_bytes" not in columns
    assert any(
        foreign_key["referred_table"] == "resume_processing_steps"
        and foreign_key["options"].get("ondelete") == "SET NULL"
        for foreign_key in foreign_keys
    )
    assert any(
        "SUCCESS" in constraint["sqltext"]
        for constraint in check_constraints
    )
