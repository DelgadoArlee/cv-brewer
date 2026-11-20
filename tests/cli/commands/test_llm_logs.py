from dataclasses import replace
from datetime import datetime
from functools import partial
from pathlib import Path
from types import SimpleNamespace

import pytest
from typer.testing import CliRunner

import logger_main
from cli.commands.application_startup import StartupError
from cli.commands.llm_menu import _OPTIONS
from cli.logger_app import create_logger_app
from cli.modules.logger_context import (
    LoggerCLIDependencies,
    LoggerEnvironment,
    LoggerSources,
)
from cli.modules.paths import StartupPaths
from core.services.logger import LogError, LogPerformance
from core.services.llm import (
    LLMGenerationParameters,
    LLMLogRecord,
    LLMRequestLog,
    LLMResponseLog,
    LLMUsageLog,
)


def _record() -> LLMLogRecord:
    return LLMLogRecord(
        id="log-1",
        operation="generate_structured",
        status="SUCCESS",
        performance=LogPerformance(
            started_at=datetime(2026, 11, 19, 10, 0),
            duration_ms=12.5,
            start_memory_mb=10.5,
            peak_memory_mb=20.5,
            end_memory_mb=12.5,
            memory_delta_mb=2.0,
            cpu_avg_percent=4.5,
            cpu_peak_percent=9.0,
            sample_count=3,
        ),
        error=LogError(),
        created_at=datetime(2026, 11, 19, 10, 0, 1),
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


def _latest_report(logs_dir: Path, source: str = "dev") -> Path:
    reports = sorted((logs_dir / source).glob("*.html"))
    assert reports
    return reports[-1]


def _report_text(logs_dir: Path, source: str = "dev") -> str:
    return _latest_report(logs_dir, source).read_text(encoding="utf-8")


def _dependencies(
    records,
    failure=None,
    *,
    logs_dir: Path,
    source: LoggerEnvironment = "dev",
    opened_urls: list[str] | None = None,
) -> LoggerCLIDependencies:
    paths = StartupPaths(
        database=Path("/tmp/cvbrewer.db"),
        resumes=Path("/tmp/resumes"),
        generated=Path("/tmp/generated"),
    )

    def list_all():
        if failure is not None:
            raise failure
        return records

    def list_recent(limit):
        if failure is not None:
            raise failure
        return records[:limit]

    def list_errors(limit):
        if failure is not None:
            raise failure
        return records[:limit]

    def open_browser(url: str) -> bool:
        if opened_urls is not None:
            opened_urls.append(url)
        return True

    llm_querier = SimpleNamespace(
        list_all=list_all,
        list_recent=list_recent,
        list_errors=list_errors,
    )
    processing_querier = SimpleNamespace(
        list_recent_runs=lambda limit: [],
        list_error_runs=lambda limit: [],
        list_steps=lambda run_id, *, limit=None: [],
    )
    return LoggerCLIDependencies(
        paths,
        llm_querier,
        processing_querier,
        source,
        logs_dir,
        open_browser,
    )


def _build_dependencies(
    calls: list[LoggerEnvironment],
    environment: LoggerEnvironment,
    records: list[LLMLogRecord],
    failure: Exception | None,
    query_failure: Exception | None,
    logs_dir: Path,
    opened_urls: list[str] | None,
) -> LoggerCLIDependencies:
    calls.append(environment)
    if failure is not None:
        raise failure
    return _dependencies(
        records,
        query_failure,
        logs_dir=logs_dir,
        source=environment,
        opened_urls=opened_urls,
    )


def _sources(
    calls: list[LoggerEnvironment],
    environments: tuple[LoggerEnvironment, ...],
    logs_dir: Path,
    records: list[LLMLogRecord] | None = None,
    *,
    failure: Exception | None = None,
    query_failure: Exception | None = None,
    opened_urls: list[str] | None = None,
) -> LoggerSources:
    selected_records = records if records is not None else []
    return {
        environment: partial(
            _build_dependencies,
            calls,
            environment,
            selected_records,
            failure,
            query_failure,
            logs_dir,
            opened_urls,
        )
        for environment in environments
    }


def test_logger_menu_has_expected_items() -> None:
    assert _OPTIONS == ["llm", "resume-upload", "error", "all"]


def test_logger_cli_generates_report_for_all_logs(tmp_path: Path) -> None:
    logs_dir = tmp_path / "logs"
    opened_urls: list[str] = []
    app = create_logger_app(
        _sources([], ("dev",), logs_dir, [_record()], opened_urls=opened_urls)
    )

    result = CliRunner().invoke(app, [], input="\n")

    assert result.exit_code == 0
    assert "HTML report written to:" in result.output
    report = _report_text(logs_dir)
    assert "LLM Activity Logs" in report
    assert "log-1" in report
    assert "llama3.1" in report
    assert len(opened_urls) == 1
    assert opened_urls[0].startswith("file://")


def test_logger_cli_report_includes_done_reason(tmp_path: Path) -> None:
    logs_dir = tmp_path / "logs"
    record = replace(
        _record(),
        response=LLMResponseLog(finish_reason="stop"),
    )
    app = create_logger_app(_sources([], ("dev",), logs_dir, [record]))

    result = CliRunner().invoke(app, [], input="\n")

    assert result.exit_code == 0
    report = _report_text(logs_dir)
    assert "Done Reason" in report
    assert "stop" in report


def test_logger_cli_report_duration_in_seconds(tmp_path: Path) -> None:
    logs_dir = tmp_path / "logs"
    record = replace(
        _record(),
        performance=LogPerformance(
            started_at=datetime(2026, 11, 19, 10, 0),
            duration_ms=2500,
        ),
    )
    app = create_logger_app(_sources([], ("dev",), logs_dir, [record]))

    result = CliRunner().invoke(app, [], input="\n")

    assert result.exit_code == 0
    report = _report_text(logs_dir)
    assert "Duration (s)" in report
    assert "(ms)" not in report
    assert "2.500" in report


def test_logger_cli_report_includes_cpu_and_memory_performance(tmp_path: Path) -> None:
    logs_dir = tmp_path / "logs"
    app = create_logger_app(_sources([], ("dev",), logs_dir, [_record()]))

    result = CliRunner().invoke(app, [], input="\n")

    assert result.exit_code == 0
    report = _report_text(logs_dir)
    assert "Start Mem (MB)" in report
    assert "Peak Mem (MB)" in report
    assert "End Mem (MB)" in report
    assert "Mem Delta (MB)" in report
    assert "CPU Avg (%)" in report
    assert "CPU Peak (%)" in report
    assert "Samples" in report
    assert "10.5" in report
    assert "20.5" in report
    assert "2.0" in report
    assert "4.5" in report
    assert "9.0" in report


def test_logger_cli_report_includes_token_counts_in_separate_columns(
    tmp_path: Path,
) -> None:
    logs_dir = tmp_path / "logs"
    record = replace(
        _record(),
        usage=LLMUsageLog(input_tokens=128, output_tokens=42, total_tokens=170),
    )
    app = create_logger_app(_sources([], ("dev",), logs_dir, [record]))

    result = CliRunner().invoke(app, [], input="\n")

    assert result.exit_code == 0
    report = _report_text(logs_dir)
    assert "Input Tokens" in report
    assert "Output Tokens" in report
    assert "Total Tokens" in report
    assert "128" in report
    assert "42" in report
    assert "170" in report


def test_logger_cli_generates_empty_report(tmp_path: Path) -> None:
    logs_dir = tmp_path / "logs"
    app = create_logger_app(_sources([], ("dev",), logs_dir))

    result = CliRunner().invoke(app, [], input="\n")

    assert result.exit_code == 0
    assert "HTML report written to:" in result.output
    assert "No records found." in _report_text(logs_dir)


def test_logger_cli_reports_query_failure(tmp_path: Path) -> None:
    logs_dir = tmp_path / "logs"
    app = create_logger_app(
        _sources([], ("dev",), logs_dir, query_failure=RuntimeError("query failed"))
    )

    result = CliRunner().invoke(app, [], input="\n")

    assert result.exit_code == 0
    assert "query failed" in result.output
    assert "HTML report written to:" not in result.output
    assert not (logs_dir / "dev").exists()


def test_logger_cli_offers_available_sources_in_order(tmp_path: Path) -> None:
    calls: list[LoggerEnvironment] = []
    app = create_logger_app(_sources(calls, ("dev", "e2e", "test"), tmp_path / "logs"))

    result = CliRunner().invoke(app, [], input="\n\n")

    assert result.exit_code == 0
    assert "  1. dev" in result.output
    assert "  2. e2e" in result.output
    assert "  3. test" in result.output
    assert calls == ["dev"]


def test_logger_cli_queries_the_selected_source(tmp_path: Path) -> None:
    calls: list[LoggerEnvironment] = []
    logs_dir = tmp_path / "logs"
    app = create_logger_app(
        _sources(calls, ("dev", "e2e", "test"), logs_dir, [_record()])
    )

    result = CliRunner().invoke(app, [], input="3\n\n")

    assert result.exit_code == 0
    assert calls == ["test"]
    assert "LLM Activity Logs" in _report_text(logs_dir, "test")
    assert not (logs_dir / "dev").exists()
    assert not (logs_dir / "e2e").exists()


def test_logger_cli_skips_selection_for_a_single_source(tmp_path: Path) -> None:
    calls: list[LoggerEnvironment] = []
    logs_dir = tmp_path / "logs"
    app = create_logger_app(_sources(calls, ("e2e",), logs_dir, [_record()]))

    result = CliRunner().invoke(app, [], input="\n")

    assert result.exit_code == 0
    assert calls == ["e2e"]
    assert "Log Database" not in result.output
    assert "LLM Activity Logs" in _report_text(logs_dir, "e2e")


def test_logger_cli_reports_startup_failure_for_the_selected_source(
    tmp_path: Path,
) -> None:
    calls: list[LoggerEnvironment] = []
    logs_dir = tmp_path / "logs"
    app = create_logger_app(
        _sources(calls, ("dev",), logs_dir, failure=StartupError("startup failed"))
    )

    result = CliRunner().invoke(app, [])

    assert result.exit_code == 0
    assert calls == ["dev"]
    assert "startup failed" in result.output
    assert "HTML report written to:" not in result.output
    assert not (logs_dir / "dev").exists()


def test_logger_reports_when_no_database_exists(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    monkeypatch.setattr(logger_main, "available_log_sources", lambda: {})

    with pytest.raises(SystemExit) as exc:
        logger_main.main()

    assert exc.value.code == 1
    assert "No log databases found." in capsys.readouterr().out


def test_available_log_sources_only_includes_existing_databases(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    data_dirs: dict[LoggerEnvironment, Path] = {
        "dev": tmp_path / "dev",
        "e2e": tmp_path / "e2e",
        "test": tmp_path / "test",
    }
    for directory in data_dirs.values():
        directory.mkdir()
    (data_dirs["dev"] / "cvbrewer.db").touch()
    (data_dirs["test"] / "cvbrewer.db").touch()
    monkeypatch.setattr(logger_main, "_ENVIRONMENT_DATA_DIRS", data_dirs)

    sources = logger_main.available_log_sources()

    assert list(sources) == ["dev", "test"]
