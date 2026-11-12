from pathlib import Path
from typing import Any

from rich.console import Console
from rich.table import Table
from rich.text import Text

from core.models import ResumeProcessingOutcome, ResumeProcessingStatus


_STATUS_LABELS = {
    ResumeProcessingStatus.STORED: ("Imported", "green"),
    ResumeProcessingStatus.DUPLICATE: ("Duplicate", "yellow"),
    ResumeProcessingStatus.INVALID_FILE_TYPE: ("Rejected", "red"),
    ResumeProcessingStatus.INVALID_PDF: ("Rejected", "red"),
    ResumeProcessingStatus.UNREADABLE: ("Rejected", "red"),
    ResumeProcessingStatus.SCHEMA_INVALID: ("Rejected", "red"),
    ResumeProcessingStatus.LLM_FAILURE: ("Failed", "red"),
    ResumeProcessingStatus.STORAGE_FAILURE: ("Failed", "red"),
    ResumeProcessingStatus.PROCESSING_FAILURE: ("Failed", "red"),
}

_STATUS_DETAILS = {
    ResumeProcessingStatus.STORED: "Stored successfully.",
    ResumeProcessingStatus.DUPLICATE: "Resume content already exists.",
    ResumeProcessingStatus.INVALID_FILE_TYPE: "File is not a valid PDF.",
    ResumeProcessingStatus.INVALID_PDF: "PDF is invalid or password-protected.",
    ResumeProcessingStatus.UNREADABLE: "PDF does not contain readable text.",
    ResumeProcessingStatus.SCHEMA_INVALID: "Parsed data did not match the resume schema.",
    ResumeProcessingStatus.LLM_FAILURE: "Language model processing failed.",
    ResumeProcessingStatus.STORAGE_FAILURE: "Resume could not be saved.",
    ResumeProcessingStatus.PROCESSING_FAILURE: "Processing failed.",
}


def render_empty_folder(console: Console, folder: Path | str) -> None:
    console.print(f"[yellow]No resume files found in {folder}.[/yellow]")


def render_upload_results(
    console: Console,
    folder: Path | str,
    outcomes: list[ResumeProcessingOutcome],
) -> None:
    if not outcomes:
        console.print(f"[green]Import complete: no files to process in {folder}.[/green]")
        return

    table = Table(title="Resume Import Results")
    table.add_column("File", style="cyan", no_wrap=True)
    table.add_column("Result", style="bold")
    table.add_column("Details")

    stored = 0
    duplicates = 0
    failed = 0

    for outcome in outcomes:
        label, color = _STATUS_LABELS.get(
            outcome.status, ("Unknown", "white")
        )
        details = outcome.message or _STATUS_DETAILS.get(
            outcome.status, "No details available."
        )
        if outcome.resume_id:
            details = f"{details} Resume ID: {outcome.resume_id}."
        if outcome.duplicate_resume_id:
            details = f"{details} Existing ID: {outcome.duplicate_resume_id}."

        table.add_row(
            outcome.file_name,
            Text(label, style=color),
            details,
        )

        if outcome.status is ResumeProcessingStatus.STORED:
            stored += 1
        elif outcome.status is ResumeProcessingStatus.DUPLICATE:
            duplicates += 1
        else:
            failed += 1

    console.print(table)
    console.print(
        f"[green]Import complete:[/green] {stored} imported, "
        f"{duplicates} duplicates, {failed} failed."
    )
    if failed == 0:
        console.print("[green]All resume files were processed successfully.[/green]")


_STAGE_LABELS = {
    "file_type_validation": "Checking file type",
    "metadata_extraction": "Reading metadata",
    "deduplication": "Checking for duplicates",
    "pdf_validation": "Validating PDF",
    "content_extraction": "Extracting text",
    "parsing": "Parsing resume",
    "schema_validation": "Validating schema",
    "storage": "Storing resume",
}


def format_stage_description(
    file_name: str,
    stage: str,
    current: int | None = None,
    total: int | None = None,
) -> str:
    label = _STAGE_LABELS.get(stage, stage)
    description = f"Importing {file_name} — {label}"
    if current is not None and total is not None:
        description = f"{description} ({current}/{total})"
    return description
