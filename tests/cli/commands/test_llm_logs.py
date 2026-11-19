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
        status="success",
        performance=LogPerformance(
            started_at=datetime(2026, 11, 19, 10, 0),
            duration_ms=12.5,
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


def _dependencies(records, failure=None) -> LoggerCLIDependencies:
    paths = StartupPaths(
        database=Path("/tmp/cvbrewer.db"),
        resumes=Path("/tmp/resumes"),
        generated=Path("/tmp/generated"),
    )

    def list_all():
        if failure is not None:
            raise failure
        return records

    return LoggerCLIDependencies(paths, SimpleNamespace(list_all=list_all))


def _build_dependencies(
    calls: list[LoggerEnvironment],
    environment: LoggerEnvironment,
    records: list[LLMLogRecord],
    failure: Exception | None,
    query_failure: Exception | None,
) -> LoggerCLIDependencies:
    calls.append(environment)
    if failure is not None:
        raise failure
    return _dependencies(records, query_failure)


def _sources(
    calls: list[LoggerEnvironment],
    environments: tuple[LoggerEnvironment, ...],
    records: list[LLMLogRecord] | None = None,
    *,
    failure: Exception | None = None,
    query_failure: Exception | None = None,
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
        )
        for environment in environments
    }


def test_logger_menu_has_only_llm_item() -> None:
    assert _OPTIONS == ["llm"]


def test_logger_cli_lists_all_logs() -> None:
    runner = CliRunner()
    app = create_logger_app(_sources([], ("dev",), [_record()]))

    result = runner.invoke(app, [], input="\n")

    assert result.exit_code == 0
    assert "llm" in result.output
    assert "LLM Activity Logs" in result.output
    assert "log-1" in result.output
    assert "llama3.1" in result.output


def test_logger_cli_displays_done_reason() -> None:
    record = replace(
        _record(),
        response=LLMResponseLog(finish_reason="stop"),
    )
    app = create_logger_app(_sources([], ("dev",), [record]))

    result = CliRunner().invoke(app, [], input="\n", env={"COLUMNS": "200"})

    assert result.exit_code == 0
    assert "Done Reason" in result.output
    assert "stop" in result.output


def test_logger_cli_displays_duration_in_seconds() -> None:
    record = replace(
        _record(),
        performance=LogPerformance(
            started_at=datetime(2026, 11, 19, 10, 0),
            duration_ms=2500,
        ),
    )
    app = create_logger_app(_sources([], ("dev",), [record]))

    result = CliRunner().invoke(app, [], input="\n", env={"COLUMNS": "200"})

    assert result.exit_code == 0
    assert "Duration" in result.output
    assert "(s)" in result.output
    assert "(ms)" not in result.output
    assert "2.500" in result.output


def test_logger_cli_displays_token_counts_in_separate_columns() -> None:
    record = replace(
        _record(),
        usage=LLMUsageLog(input_tokens=128, output_tokens=42, total_tokens=170),
    )
    app = create_logger_app(_sources([], ("dev",), [record]))

    result = CliRunner().invoke(app, [], input="\n", env={"COLUMNS": "200"})

    assert result.exit_code == 0
    assert "Input Tokens" in result.output
    assert "Output Tokens" in result.output
    assert "Total Tokens" in result.output
    assert "128" in result.output
    assert "42" in result.output
    assert "170" in result.output


def test_logger_cli_reports_empty_results() -> None:
    runner = CliRunner()
    app = create_logger_app(_sources([], ("dev",)))

    result = runner.invoke(app, [], input="\n")

    assert result.exit_code == 0
    assert "No LLM activity logs found." in result.output


def test_logger_cli_reports_query_failure() -> None:
    runner = CliRunner()
    app = create_logger_app(
        _sources([], ("dev",), query_failure=RuntimeError("query failed"))
    )

    result = runner.invoke(app, [], input="\n")

    assert result.exit_code == 0
    assert "query failed" in result.output


def test_logger_cli_offers_available_sources_in_order() -> None:
    calls: list[LoggerEnvironment] = []
    runner = CliRunner()
    app = create_logger_app(_sources(calls, ("dev", "e2e", "test"), [_record()]))

    result = runner.invoke(app, [], input="\n\n")

    assert result.exit_code == 0
    assert "  1. dev" in result.output
    assert "  2. e2e" in result.output
    assert "  3. test" in result.output
    assert calls == ["dev"]


def test_logger_cli_queries_the_selected_source() -> None:
    calls: list[LoggerEnvironment] = []
    runner = CliRunner()
    app = create_logger_app(_sources(calls, ("dev", "e2e", "test"), [_record()]))

    result = runner.invoke(app, [], input="3\n\n")

    assert result.exit_code == 0
    assert calls == ["test"]
    assert "LLM Activity Logs" in result.output


def test_logger_cli_skips_selection_for_a_single_source() -> None:
    calls: list[LoggerEnvironment] = []
    runner = CliRunner()
    app = create_logger_app(_sources(calls, ("e2e",), [_record()]))

    result = runner.invoke(app, [], input="\n")

    assert result.exit_code == 0
    assert calls == ["e2e"]
    assert "Log Database" not in result.output
    assert "LLM Activity Logs" in result.output


def test_logger_cli_reports_startup_failure_for_the_selected_source() -> None:
    calls: list[LoggerEnvironment] = []
    runner = CliRunner()
    app = create_logger_app(
        _sources(calls, ("dev",), failure=StartupError("startup failed"))
    )

    result = runner.invoke(app, [])

    assert result.exit_code == 0
    assert calls == ["dev"]
    assert "startup failed" in result.output
    assert "LLM Activity Logs" not in result.output


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
