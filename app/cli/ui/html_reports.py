from dataclasses import dataclass
from datetime import datetime, timezone
from html import escape
from pathlib import Path
import re

from rich.console import Console

from cli.modules.logger_context import LoggerCLIDependencies


@dataclass(frozen=True, slots=True)
class ReportTable:
    title: str
    columns: tuple[str, ...]
    rows: tuple[tuple[str, ...], ...]


def _slug(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")


def _timestamp(created_at: datetime | None) -> str:
    moment = created_at or datetime.now(timezone.utc)
    return moment.strftime("%Y-%m-%dT%H%M%S%fZ")


def report_path(
    logs_dir: Path,
    source: str,
    log_type: str,
    created_at: datetime | None = None,
) -> Path:
    filename = f"{_timestamp(created_at)}-{_slug(log_type)}.html"
    return logs_dir / source / filename


def _render_table(table: ReportTable) -> str:
    headers = "".join(f"<th>{escape(column)}</th>" for column in table.columns)
    if table.rows:
        body_rows = []
        for row in table.rows:
            cells = "".join(f"<td>{escape(value)}</td>" for value in row)
            body_rows.append(f"<tr>{cells}</tr>")
        body = "".join(body_rows)
    else:
        body = (
            f'<tr><td colspan="{len(table.columns)}">No records found.</td></tr>'
        )
    return (
        "<table><thead><tr>"
        f"{headers}"
        "</tr></thead><tbody>"
        f"{body}"
        "</tbody></table>"
    )


def build_html_document(table: ReportTable) -> str:
    title = escape(table.title)
    return (
        "<!doctype html>\n"
        '<html lang="en">\n'
        "<head>\n"
        '<meta charset="utf-8">\n'
        f"<title>{title}</title>\n"
        "<style>\n"
        "body { font-family: Arial, sans-serif; margin: 24px; }\n"
        "table { border-collapse: collapse; width: 100%; font-size: 12px; }\n"
        "th, td { border: 1px solid #cccccc; padding: 6px; "
        "text-align: left; vertical-align: top; }\n"
        "th { background: #f2f2f2; }\n"
        "</style>\n"
        "</head>\n"
        "<body>\n"
        f"<h1>{title}</h1>\n"
        f"{_render_table(table)}\n"
        "</body>\n"
        "</html>\n"
    )


def generate_html_report(
    dependencies: LoggerCLIDependencies,
    table: ReportTable,
    *,
    log_type: str,
    console: Console,
    created_at: datetime | None = None,
) -> Path:
    path = report_path(
        dependencies.logs_dir,
        dependencies.source,
        log_type,
        created_at,
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(build_html_document(table), encoding="utf-8")
    console.print(f"HTML report written to: {path.resolve()}", soft_wrap=True)

    try:
        opened = dependencies.open_browser(path.resolve().as_uri())
    except Exception as exc:
        console.print(f"[yellow]Warning:[/yellow] Could not open browser: {exc}")
    else:
        if not opened:
            console.print(
                "[yellow]Warning:[/yellow] Could not open the default browser."
            )
    return path
