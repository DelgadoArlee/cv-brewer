from datetime import datetime, timedelta
from functools import partial
from pathlib import Path
from types import SimpleNamespace

from typer.testing import CliRunner

from cli.commands.all_logs import _query_records as query_all_records
from cli.logger_app import create_logger_app
from cli.modules.logger_context import LoggerCLIDependencies
from cli.modules.paths import StartupPaths
from core.services.logger import LogError, LogPerformance
from core.services.llm import (
    LLMGenerationParameters,
    LLMLogRecord,
    LLMRequestLog,
    LLMResponseLog,
    LLMUsageLog,
)
from core.services.processing_log import (
    ProcessingError,
    ProcessingLogStatus,
    ProcessingPerformance,
    ProcessingRunRecord,
    ProcessingStepInput,
    ProcessingStepOutput,
    ProcessingStepRecord,
    ProcessingSummary,
)


def _llm_record(
    record_id: str,
    created_at: datetime,
    *,
    status: str = "SUCCESS",
    error: LogError | None = None,
) -> LLMLogRecord:
    return LLMLogRecord(
        id=record_id,
        operation="generate_structured",
        status=status,
        performance=LogPerformance(
            started_at=created_at,
            duration_ms=10.0,
            start_memory_mb=10.5,
            peak_memory_mb=20.5,
            end_memory_mb=12.5,
            memory_delta_mb=2.0,
            cpu_avg_percent=4.5,
            cpu_peak_percent=9.0,
            sample_count=3,
        ),
        error=error or LogError(),
        created_at=created_at,
        provider="ollama",
        model="llama3.1",
        request=LLMRequestLog(
            system_prompt=None,
            prompt="Resume text.",
            parameters=LLMGenerationParameters(),
        ),
        response=LLMResponseLog(),
        usage=LLMUsageLog(),
    )


def _run_record(
    run_id: str,
    started_at: datetime,
    *,
    status: str = ProcessingLogStatus.SUCCESS,
    result: str = "stored",
    error: ProcessingError | None = None,
) -> ProcessingRunRecord:
    return ProcessingRunRecord(
        run_id=run_id,
        process_name="resume_processing",
        process_version="1.0",
        status=status,
        result=result,
        resume_id="resume-1",
        matched_resume_id=None,
        started_at=started_at,
        completed_at=started_at + timedelta(seconds=1),
        duration_ms=1000.0,
        summary=ProcessingSummary(
            total_steps=8,
            completed_steps=8,
            failed_steps=0,
            skipped_steps=0,
        ),
        performance=ProcessingPerformance(
            duration_ms=1000.0,
            start_memory_mb=100.5,
            peak_memory_mb=200.5,
            end_memory_mb=120.5,
            memory_delta_mb=20.0,
            cpu_avg_percent=12.5,
            cpu_peak_percent=25.5,
            sample_count=5,
        ),
        error=error,
    )


def _step_record(step_id: str, started_at: datetime) -> ProcessingStepRecord:
    return ProcessingStepRecord(
        step_id=step_id,
        run_id="run-1",
        step_name="parsing",
        step_order=6,
        attempt_number=1,
        status=ProcessingLogStatus.SUCCESS,
        started_at=started_at,
        completed_at=started_at + timedelta(seconds=1),
        duration_ms=1000.0,
        input=ProcessingStepInput(type="extracted_text"),
        output=ProcessingStepOutput(type="resume_data"),
        performance=ProcessingPerformance(
            duration_ms=1000.0,
            start_memory_mb=1.5,
            peak_memory_mb=2.5,
            end_memory_mb=1.8,
            memory_delta_mb=0.3,
            cpu_avg_percent=1.2,
            cpu_peak_percent=2.4,
            sample_count=2,
        ),
        metadata={"file_name": "resume.pdf"},
    )


def _report_text(logs_dir: Path) -> str:
    reports = sorted((logs_dir / "dev").glob("*.html"))
    assert reports
    return reports[-1].read_text(encoding="utf-8")


def _dependencies(
    logs_dir: Path,
    llm_records: list[LLMLogRecord] | None = None,
    runs: list[ProcessingRunRecord] | None = None,
    steps_by_run: dict[str, list[ProcessingStepRecord]] | None = None,
    *,
    failure: Exception | None = None,
    calls: list[tuple[str, int | None]] | None = None,
    opened_urls: list[str] | None = None,
) -> LoggerCLIDependencies:
    selected_llm_records = llm_records or []
    selected_runs = runs or []
    selected_steps = steps_by_run or {}
    observed_calls = calls if calls is not None else []

    def list_recent(limit: int) -> list[LLMLogRecord]:
        observed_calls.append(("llm_recent", limit))
        if failure is not None:
            raise failure
        return selected_llm_records[:limit]

    def list_errors(limit: int) -> list[LLMLogRecord]:
        observed_calls.append(("llm_errors", limit))
        if failure is not None:
            raise failure
        return selected_llm_records[:limit]

    def list_recent_runs(limit: int) -> list[ProcessingRunRecord]:
        observed_calls.append(("runs_recent", limit))
        if failure is not None:
            raise failure
        return selected_runs[:limit]

    def list_error_runs(limit: int) -> list[ProcessingRunRecord]:
        observed_calls.append(("runs_errors", limit))
        if failure is not None:
            raise failure
        return selected_runs[:limit]

    def list_steps(run_id: str, *, limit: int | None = None):
        observed_calls.append(("steps", limit))
        if failure is not None:
            raise failure
        return selected_steps.get(run_id, [])[:limit]

    def open_browser(url: str) -> bool:
        if opened_urls is not None:
            opened_urls.append(url)
        return True

    paths = StartupPaths(
        database=Path("/tmp/cvbrewer.db"),
        resumes=Path("/tmp/resumes"),
        generated=Path("/tmp/generated"),
    )
    return LoggerCLIDependencies(
        paths,
        SimpleNamespace(list_recent=list_recent, list_errors=list_errors),
        SimpleNamespace(
            list_recent_runs=list_recent_runs,
            list_error_runs=list_error_runs,
            list_steps=list_steps,
        ),
        "dev",
        logs_dir,
        open_browser,
    )


def _invoke(dependencies: LoggerCLIDependencies, input_text: str):
    sources = {"dev": partial(lambda dependencies: dependencies, dependencies)}
    return CliRunner().invoke(
        create_logger_app(sources), [], input=input_text, env={"COLUMNS": "300"}
    )


def test_resume_upload_view_runs_generates_processing_run_report(
    tmp_path: Path,
) -> None:
    logs_dir = tmp_path / "logs"
    run = _run_record("run-1", datetime(2026, 11, 20, 10, 0))
    result = _invoke(_dependencies(logs_dir, runs=[run]), "2\n1\n")

    assert result.exit_code == 0
    assert "Resume Upload Logs" in result.output
    assert "view runs" in result.output
    report = _report_text(logs_dir)
    assert "Processing Runs" in report
    assert "run-1" in report
    assert "resume-1" in report
    assert "CPU Avg (%)" in report
    assert "200.5" in report
    assert "12.5" in report


def test_resume_upload_view_steps_generates_step_report(tmp_path: Path) -> None:
    logs_dir = tmp_path / "logs"
    run = _run_record("run-1", datetime(2026, 11, 20, 10, 0))
    step = _step_record("step-1", datetime(2026, 11, 20, 10, 0, 2))
    result = _invoke(
        _dependencies(logs_dir, runs=[run], steps_by_run={"run-1": [step]}),
        "2\n2\n1\n",
    )

    assert result.exit_code == 0
    assert "view steps" in result.output
    assert "run-1 - 2026-11-20 10:00:00" in result.output
    report = _report_text(logs_dir)
    assert "Processing Steps - run-1" in report
    assert "step-1" in report
    assert "resume.pdf" in report
    assert "Peak Mem (MB)" in report
    assert "2.5" in report
    assert "CPU Peak (%)" in report
    assert "2.4" in report


def test_error_view_generates_llm_and_processing_run_report(tmp_path: Path) -> None:
    logs_dir = tmp_path / "logs"
    llm = _llm_record(
        "log-error",
        datetime(2026, 11, 20, 11, 0),
        status="FAILED",
        error=LogError(type="RuntimeError", message="failed"),
    )
    run = _run_record(
        "run-error",
        datetime(2026, 11, 20, 10, 0),
        status=ProcessingLogStatus.FAILED,
        error=ProcessingError(code="RESUME_FAILURE", type="Failure", message="bad"),
    )
    result = _invoke(_dependencies(logs_dir, [llm], [run]), "3\n")

    assert result.exit_code == 0
    report = _report_text(logs_dir)
    assert "Error Logs" in report
    assert "log-error" in report
    assert "run-error" in report
    assert "Start Mem (MB)" in report
    assert "10.5" in report
    assert "100.5" in report


def test_all_view_generates_llm_logs_and_processing_runs_report(
    tmp_path: Path,
) -> None:
    logs_dir = tmp_path / "logs"
    llm = _llm_record("log-1", datetime(2026, 11, 20, 11, 0))
    run = _run_record("run-1", datetime(2026, 11, 20, 10, 0))
    result = _invoke(_dependencies(logs_dir, [llm], [run]), "4\n")

    assert result.exit_code == 0
    report = _report_text(logs_dir)
    assert "All Logs" in report
    assert "log-1" in report
    assert "run-1" in report
    assert "CPU Avg (%)" in report
    assert "4.5" in report
    assert "12.5" in report


def test_all_view_reports_query_failure(tmp_path: Path) -> None:
    logs_dir = tmp_path / "logs"
    result = _invoke(
        _dependencies(logs_dir, failure=RuntimeError("query failed")), "4\n"
    )

    assert result.exit_code == 0
    assert "query failed" in result.output
    assert "HTML report written to:" not in result.output
    assert not (logs_dir / "dev").exists()


def test_combined_query_caps_at_one_hundred_newest_records(tmp_path: Path) -> None:
    calls: list[tuple[str, int | None]] = []
    start = datetime(2026, 11, 20, 12, 0)
    llm_records = [
        _llm_record(f"llm-{index}", start + timedelta(seconds=index))
        for index in range(60)
    ]
    llm_records[0] = _llm_record("EXCLUDED_OLDEST", datetime(2020, 1, 1))
    runs = [
        _run_record(f"run-{index}", start + timedelta(seconds=60 + index))
        for index in range(60)
    ]
    dependencies = _dependencies(tmp_path / "logs", llm_records, runs, calls=calls)

    records = query_all_records(dependencies)

    assert len(records) == 100
    assert all(record.record_id != "EXCLUDED_OLDEST" for record in records)
    assert calls == [("llm_recent", 100), ("runs_recent", 100)]
