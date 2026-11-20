from dataclasses import replace
from datetime import datetime
from pathlib import Path

from sqlalchemy import create_engine, inspect

from core.services.processing_log import (
    ProcessingError,
    ProcessingLogStatus,
    ProcessingPerformance,
    ProcessingStepInput,
    ProcessingStepOutput,
    ProcessingSummary,
)
from database import create_processing_log_service, initialize_database


def _finalized_run(run, *, resume_id: str | None = None):
    return replace(
        run,
        status=ProcessingLogStatus.SUCCESS,
        result="stored",
        resume_id=resume_id,
        completed_at=datetime(2026, 11, 20, 10, 0, 5),
        duration_ms=5000.0,
        summary=ProcessingSummary(
            total_steps=1,
            completed_steps=1,
            failed_steps=0,
            skipped_steps=0,
        ),
        performance=ProcessingPerformance(
            duration_ms=5000.0,
            start_memory_mb=100.0,
            peak_memory_mb=150.0,
            end_memory_mb=120.0,
            memory_delta_mb=20.0,
            cpu_avg_percent=5.0,
            cpu_peak_percent=10.0,
            sample_count=3,
        ),
    )


def _finalized_step(step):
    return replace(
        step,
        status=ProcessingLogStatus.SUCCESS,
        completed_at=datetime(2026, 11, 20, 10, 0, 1),
        duration_ms=1000.0,
        output=ProcessingStepOutput(type="parsing", metadata={"fields": 10}),
        performance=ProcessingPerformance(
            duration_ms=1000.0,
            start_memory_mb=100.0,
            peak_memory_mb=110.0,
            end_memory_mb=105.0,
            memory_delta_mb=5.0,
            sample_count=0,
        ),
    )


def test_processing_logs_round_trip(tmp_path: Path) -> None:
    database_path = tmp_path / "processing-logs.db"
    initialize_database(database_path)
    service = create_processing_log_service(database_path)

    run = service.start_run(
        process_name="resume_processing",
        process_version="1.0",
    )
    step = service.start_step(
        run_id=run.run_id,
        step_name="parsing",
        step_order=6,
        input_data=ProcessingStepInput(type="extracted_text", size_bytes=128),
    )
    service.finalize_step(_finalized_step(step))
    service.finalize_run(_finalized_run(run, resume_id="resume-1"))

    stored_run = service.get_run(run.run_id)
    stored_steps = service.list_steps(run.run_id)

    assert stored_run is not None
    assert stored_run.status == ProcessingLogStatus.SUCCESS
    assert stored_run.result == "stored"
    assert stored_run.resume_id == "resume-1"
    assert stored_run.summary.total_steps == 1
    assert stored_run.performance.cpu_avg_percent == 5.0
    assert stored_run.performance.sample_count == 3
    assert [stored_step.step_name for stored_step in stored_steps] == ["parsing"]
    assert stored_steps[0].output.metadata == {"fields": 10}
    assert stored_steps[0].performance.sample_count == 0


def test_processing_logs_list_runs_by_resume_identifier(tmp_path: Path) -> None:
    database_path = tmp_path / "lookup.db"
    initialize_database(database_path)
    service = create_processing_log_service(database_path)

    stored = service.start_run(process_name="resume_processing", process_version="1.0")
    service.finalize_run(_finalized_run(stored, resume_id="resume-1"))
    duplicate = service.start_run(
        process_name="resume_processing",
        process_version="1.0",
    )
    service.finalize_run(
        replace(
            duplicate,
            status=ProcessingLogStatus.SUCCESS,
            result="duplicate",
            matched_resume_id="resume-1",
            completed_at=datetime(2026, 11, 20, 10, 1, 0),
            duration_ms=1000.0,
            summary=ProcessingSummary(),
            performance=ProcessingPerformance(duration_ms=1000.0),
        )
    )

    runs = service.list_runs_by_resume_id("resume-1")

    assert {run.result for run in runs} == {"stored", "duplicate"}
    assert all(
        run.resume_id == "resume-1" or run.matched_resume_id == "resume-1"
        for run in runs
    )


def test_repository_lists_recent_and_error_runs(tmp_path: Path) -> None:
    database_path = tmp_path / "query-runs.db"
    initialize_database(database_path)
    service = create_processing_log_service(database_path)
    statuses = [
        ("success", datetime(2026, 11, 20, 10, 0), ProcessingLogStatus.SUCCESS, None),
        ("failed", datetime(2026, 11, 20, 10, 1), ProcessingLogStatus.FAILED, None),
        (
            "validation",
            datetime(2026, 11, 20, 10, 2),
            ProcessingLogStatus.VALIDATION_FAILED,
            None,
        ),
        (
            "partial",
            datetime(2026, 11, 20, 10, 3),
            ProcessingLogStatus.PARTIAL_SUCCESS,
            None,
        ),
        ("newest", datetime(2026, 11, 20, 10, 4), ProcessingLogStatus.SUCCESS, None),
        (
            "with-error",
            datetime(2026, 11, 20, 10, 5),
            ProcessingLogStatus.SUCCESS,
            ProcessingError(code="ERROR", type="Failure", message="bad"),
        ),
    ]
    for run_id, started_at, status, error in statuses:
        run = service.start_run(
            process_name="resume_processing",
            process_version="1.0",
            run_id=run_id,
            started_at=started_at,
        )
        service.finalize_run(
            replace(
                run,
                status=status,
                result="stored",
                completed_at=started_at,
                duration_ms=1000.0,
                summary=ProcessingSummary(),
                performance=ProcessingPerformance(duration_ms=1000.0),
                error=error,
            )
        )

    recent = service.list_recent_runs(2)
    errors = service.list_error_runs(3)

    assert [run.run_id for run in recent] == ["with-error", "newest"]
    assert [run.run_id for run in errors] == ["with-error", "partial", "validation"]


def test_repository_lists_steps_with_limit(tmp_path: Path) -> None:
    database_path = tmp_path / "query-steps.db"
    initialize_database(database_path)
    service = create_processing_log_service(database_path)
    run = service.start_run(
        process_name="resume_processing",
        process_version="1.0",
        started_at=datetime(2026, 11, 20, 10, 0),
    )
    for index in range(3):
        step = service.start_step(
            run_id=run.run_id,
            step_name=f"step-{index}",
            step_order=index + 1,
            started_at=datetime(2026, 11, 20, 10, index + 1),
        )
        service.finalize_step(
            replace(
                step,
                status=ProcessingLogStatus.SUCCESS,
                completed_at=datetime(2026, 11, 20, 10, index + 2),
                duration_ms=1000.0,
            )
        )

    steps = service.list_steps(run.run_id)
    limited = service.list_steps(run.run_id, limit=2)

    assert [step.step_order for step in steps] == [1, 2, 3]
    assert [step.step_name for step in limited] == ["step-2", "step-1"]


def test_migration_creates_processing_log_schema(tmp_path: Path) -> None:
    database_path = tmp_path / "schema.db"
    initialize_database(database_path)
    engine = create_engine(f"sqlite:///{database_path}")

    inspector = inspect(engine)
    table_names = set(inspector.get_table_names())
    run_columns = {
        column["name"] for column in inspector.get_columns("resume_processing_runs")
    }
    step_columns = {
        column["name"] for column in inspector.get_columns("resume_processing_steps")
    }
    step_foreign_keys = inspector.get_foreign_keys("resume_processing_steps")

    assert "resume_processing_runs" in table_names
    assert "resume_processing_steps" in table_names
    assert "resume_processing_history" not in table_names
    assert "summary" in run_columns
    assert "performance" in run_columns
    assert "input" in step_columns
    assert "output" in step_columns
    assert "metadata" in step_columns
    assert any(
        foreign_key["referred_table"] == "resume_processing_runs"
        and foreign_key["options"].get("ondelete") == "CASCADE"
        for foreign_key in step_foreign_keys
    )
