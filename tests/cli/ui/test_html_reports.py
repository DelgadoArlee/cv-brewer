from datetime import datetime
from io import StringIO
from pathlib import Path
from types import SimpleNamespace

from rich.console import Console

from cli.modules.logger_context import LoggerCLIDependencies
from cli.modules.paths import StartupPaths
from cli.ui.html_reports import (
    ReportTable,
    build_html_document,
    generate_html_report,
    report_path,
)


def _dependencies(
    logs_dir: Path,
    *,
    opened_urls: list[str] | None = None,
    open_result: bool = True,
    open_error: Exception | None = None,
) -> LoggerCLIDependencies:
    def open_browser(url: str) -> bool:
        if opened_urls is not None:
            opened_urls.append(url)
        if open_error is not None:
            raise open_error
        return open_result

    paths = StartupPaths(
        database=Path("/tmp/cvbrewer.db"),
        resumes=Path("/tmp/resumes"),
        generated=Path("/tmp/generated"),
    )
    querier = SimpleNamespace(
        list_recent=lambda limit: [],
        list_errors=lambda limit: [],
        list_recent_runs=lambda limit: [],
        list_error_runs=lambda limit: [],
        list_steps=lambda run_id, *, limit=None: [],
    )
    return LoggerCLIDependencies(paths, querier, querier, "dev", logs_dir, open_browser)


def test_report_path_uses_utc_timestamp_and_sanitized_log_type(tmp_path: Path) -> None:
    path = report_path(
        tmp_path / "logs",
        "dev",
        "processing-steps-run/1",
        datetime(2026, 11, 20, 1, 2, 3, 456789),
    )

    assert path == (
        tmp_path
        / "logs"
        / "dev"
        / "2026-11-20T010203456789Z-processing-steps-run-1.html"
    )


def test_build_html_document_escapes_title_and_cells() -> None:
    table = ReportTable(
        "<title>&",
        ("Cell",),
        (("<b>&</b>",),),
    )

    document = build_html_document(table)

    assert "&lt;title&gt;&amp;" in document
    assert "&lt;b&gt;&amp;&lt;/b&gt;" in document
    assert "<b>&</b>" not in document


def test_build_html_document_reports_empty_results() -> None:
    document = build_html_document(ReportTable("Empty", ("ID",), ()))

    assert '<td colspan="1">No records found.</td>' in document


def test_generate_html_report_writes_prints_and_opens_report(tmp_path: Path) -> None:
    logs_dir = tmp_path / "logs"
    opened_urls: list[str] = []
    output = StringIO()
    console = Console(file=output, width=200)
    table = ReportTable("Report", ("ID",), (("log-1",),))

    path = generate_html_report(
        _dependencies(logs_dir, opened_urls=opened_urls),
        table,
        log_type="llm",
        console=console,
        created_at=datetime(2026, 11, 20, 1, 2, 3, 456789),
    )

    assert path.name == "2026-11-20T010203456789Z-llm.html"
    assert "Report" in path.read_text(encoding="utf-8")
    assert "HTML report written to:" in output.getvalue()
    assert opened_urls == [path.resolve().as_uri()]


def test_generate_html_report_warns_when_browser_open_fails(tmp_path: Path) -> None:
    output = StringIO()
    console = Console(file=output, width=200)

    generate_html_report(
        _dependencies(tmp_path / "logs", open_result=False),
        ReportTable("Report", ("ID",), (("log-1",),)),
        log_type="llm",
        console=console,
    )

    assert "HTML report written to:" in output.getvalue()
    assert "Could not open the default browser." in output.getvalue()


def test_generate_html_report_warns_when_browser_raises(tmp_path: Path) -> None:
    output = StringIO()
    console = Console(file=output, width=200)

    generate_html_report(
        _dependencies(tmp_path / "logs", open_error=RuntimeError("no browser")),
        ReportTable("Report", ("ID",), (("log-1",),)),
        log_type="llm",
        console=console,
    )

    assert "HTML report written to:" in output.getvalue()
    assert "Could not open browser: no browser" in output.getvalue()
