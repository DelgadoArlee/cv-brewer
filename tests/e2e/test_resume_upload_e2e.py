from pathlib import Path
from types import SimpleNamespace
from typing import Any

import pytest
from typer.testing import CliRunner

from tests.fixtures.resumes.pdf_factory import build_pdf


def _run_upload(application: SimpleNamespace) -> Any:
    return CliRunner().invoke(application.app, [], input="1\n3\n")


def _write_resume(
    application: SimpleNamespace,
    file_name: str,
    text: str,
) -> Path:
    path = application.paths.resumes / file_name
    path.write_bytes(build_pdf(text))
    return path


def _records_by_file_name(application: SimpleNamespace) -> dict[str, Any]:
    return {
        record.metadata.file_name: record
        for record in application.resume_service.list_resumes()
    }


@pytest.mark.requires_empty_data
def test_upload_reports_empty_input_folder(e2e_cli: SimpleNamespace) -> None:
    before = len(e2e_cli.resume_service.list_resumes())

    result = _run_upload(e2e_cli)

    assert result.exit_code == 0
    assert "No resume files found" in result.output
    assert len(e2e_cli.resume_service.list_resumes()) == before


def test_upload_imports_single_resume(e2e_cli: SimpleNamespace) -> None:
    _write_resume(
        e2e_cli,
        "single.pdf",
        "Alice Single\nalice.single@example.com\nSkills: Python, SQL",
    )

    result = _run_upload(e2e_cli)

    assert result.exit_code == 0
    assert "1 imported" in result.output
    record = _records_by_file_name(e2e_cli)["single.pdf"]
    assert record.metadata.file_name == "single.pdf"
    assert record.parsed_data.personal_info.name == "Alice Single"
    assert record.parsed_data.personal_info.email == "alice.single@example.com"
    assert record.validation_status.schema_validation_passed is True


def test_upload_handles_mixed_valid_and_invalid_files(
    e2e_cli: SimpleNamespace,
) -> None:
    _write_resume(
        e2e_cli,
        "mixed-valid.pdf",
        "Bob Mixed\nbob.mixed@example.com\nSkills: Go",
    )
    (e2e_cli.paths.resumes / "mixed-invalid.pdf").write_bytes(b"not a pdf")

    result = _run_upload(e2e_cli)

    assert result.exit_code == 0
    assert "1 imported" in result.output
    assert "1 failed" in result.output
    records = _records_by_file_name(e2e_cli)
    assert "mixed-valid.pdf" in records
    assert "mixed-invalid.pdf" not in records


def test_upload_imports_multiple_resumes_in_one_batch(
    e2e_cli: SimpleNamespace,
) -> None:
    _write_resume(
        e2e_cli,
        "batch-alpha.pdf",
        "Alpha Batch\nalpha.batch@example.com\nSkills: Python",
    )
    _write_resume(
        e2e_cli,
        "batch-beta.pdf",
        "Beta Batch\nbeta.batch@example.com\nSkills: SQL",
    )

    result = _run_upload(e2e_cli)

    assert result.exit_code == 0
    assert "2 imported" in result.output
    records = _records_by_file_name(e2e_cli)
    assert records["batch-alpha.pdf"].parsed_data.personal_info.email == (
        "alpha.batch@example.com"
    )
    assert records["batch-beta.pdf"].parsed_data.personal_info.email == (
        "beta.batch@example.com"
    )


def test_upload_imports_multiple_resumes_across_runs(
    e2e_cli: SimpleNamespace,
) -> None:
    _write_resume(
        e2e_cli,
        "sequential-first.pdf",
        "Carol First\ncarol.first@example.com\nSkills: Java",
    )

    first_result = _run_upload(e2e_cli)

    assert first_result.exit_code == 0
    assert "1 imported" in first_result.output
    first_record = _records_by_file_name(e2e_cli)["sequential-first.pdf"]

    _write_resume(
        e2e_cli,
        "sequential-second.pdf",
        "Dave Second\ndave.second@example.com\nSkills: Rust",
    )

    second_result = _run_upload(e2e_cli)

    assert second_result.exit_code == 0
    assert "1 imported" in second_result.output
    assert "1 duplicates" in second_result.output
    records = _records_by_file_name(e2e_cli)
    assert records["sequential-first.pdf"].resume_id == first_record.resume_id
    assert records["sequential-second.pdf"].parsed_data.personal_info.email == (
        "dave.second@example.com"
    )


def test_upload_reports_duplicate_on_reimport(e2e_cli: SimpleNamespace) -> None:
    _write_resume(
        e2e_cli,
        "duplicate.pdf",
        "Eve Duplicate\neve.duplicate@example.com\nSkills: TypeScript",
    )

    first_result = _run_upload(e2e_cli)

    assert first_result.exit_code == 0
    first_record = _records_by_file_name(e2e_cli)["duplicate.pdf"]
    before_count = len(e2e_cli.resume_service.list_resumes())

    second_result = _run_upload(e2e_cli)

    assert second_result.exit_code == 0
    assert "0 imported" in second_result.output
    assert "1 duplicates" in second_result.output
    assert len(e2e_cli.resume_service.list_resumes()) == before_count
    current_record = _records_by_file_name(e2e_cli)["duplicate.pdf"]
    assert current_record.resume_id == first_record.resume_id
