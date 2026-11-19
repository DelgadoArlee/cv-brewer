from rich.console import Console
from rich.table import Table

from core.services.llm.log_models import LLMLogRecord


_LABELS = {
    "success": ("Success", "green"),
    "failed": ("Failed", "red"),
    "timeout": ("Timeout", "yellow"),
}


def _token_count(value: int | None) -> str:
    return "-" if value is None else str(value)


def _optional_text(value: str | None) -> str:
    return "-" if value is None else value


def _duration(duration_ms: float | None) -> str:
    return "-" if duration_ms is None else f"{duration_ms / 1000:.3f}"


def _error(record: LLMLogRecord) -> str:
    if record.error.type is None and record.error.message is None:
        return "-"
    error_type = record.error.type or "Error"
    message = record.error.message or ""
    return f"{error_type}: {message}" if message else error_type


def render_llm_logs(
    console: Console,
    records: list[LLMLogRecord],
) -> None:
    if not records:
        console.print("[yellow]No LLM activity logs found.[/yellow]")
        return

    table = Table(title="LLM Activity Logs", width=max(console.width, 160))
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("Created", style="bold")
    table.add_column("Status")
    table.add_column("Provider")
    table.add_column("Model")
    table.add_column("Done Reason")
    table.add_column("Input Tokens")
    table.add_column("Output Tokens")
    table.add_column("Total Tokens")
    table.add_column("Duration (s)")
    table.add_column("Error")

    for record in records:
        label, color = _LABELS.get(record.status, ("Unknown", "white"))
        table.add_row(
            record.id,
            record.created_at.isoformat(sep=" "),
            label,
            record.provider,
            record.model,
            _optional_text(record.response.finish_reason),
            _token_count(record.usage.input_tokens),
            _token_count(record.usage.output_tokens),
            _token_count(record.usage.total_tokens),
            _duration(record.performance.duration_ms),
            _error(record),
        )

    console.print(table, crop=False)
