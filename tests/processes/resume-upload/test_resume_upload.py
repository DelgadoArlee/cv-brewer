from pathlib import Path

import pytest

from cli.commands.resume_upload import (
    ResumeUploadError,
    build_resume_inputs,
    discover_resume_files,
    ensure_input_folder,
    run_resume_upload,
    _resolve_folder,
)
from cli.modules.paths import StartupPaths
from core.models import ResumeProcessingOutcome, ResumeProcessingStatus


class FakeProcessor:
    def __init__(self, outcomes=None, fail_on=None):
        self.outcomes = list(outcomes or [])
        self.fail_on = fail_on
        self.calls = []

    def process(self, resume_input, *, on_stage=None):
        self.calls.append(resume_input)
        if on_stage is not None:
            on_stage("parsing")
        if self.fail_on and resume_input.file_name in self.fail_on:
            raise RuntimeError("boom")
        if self.outcomes:
            return self.outcomes.pop(0)
        return ResumeProcessingOutcome(
            file_name=resume_input.file_name,
            status=ResumeProcessingStatus.STORED,
            message="stored",
            resume_id="resume-1",
        )


def test_resolve_folder_startup_paths() -> None:
    paths = StartupPaths(database=Path("/tmp/db"), resumes=Path("/tmp/resumes"), generated=Path("/tmp/generated"))
    assert _resolve_folder(paths) == Path("/tmp/resumes")


def test_resolve_folder_path_and_string() -> None:
    assert _resolve_folder(Path("/tmp/input")) == Path("/tmp/input")
    assert _resolve_folder("/tmp/input") == Path("/tmp/input")


def test_ensure_input_folder_creates_directory(tmp_path: Path) -> None:
    folder = tmp_path / "resumes"
    ensure_input_folder(folder)
    assert folder.is_dir()


def test_ensure_input_folder_raises_for_file(tmp_path: Path) -> None:
    file_path = tmp_path / "not-a-dir"
    file_path.write_text("x")
    with pytest.raises(ResumeUploadError, match="input folder"):
        ensure_input_folder(file_path)


def test_discover_resume_files_sorted(tmp_path: Path) -> None:
    (tmp_path / "b.txt").write_text("b")
    (tmp_path / "a.txt").write_text("a")
    (tmp_path / "nested").mkdir()

    files = discover_resume_files(tmp_path)

    assert [path.name for path in files] == ["a.txt", "b.txt"]


def test_discover_resume_files_raises_for_missing_folder(tmp_path: Path) -> None:
    with pytest.raises(ResumeUploadError, match="not accessible"):
        discover_resume_files(tmp_path / "missing")


def test_build_resume_inputs_reads_bytes(tmp_path: Path) -> None:
    file_path = tmp_path / "resume.pdf"
    file_path.write_bytes(b"%PDF-1.7")

    inputs = build_resume_inputs([file_path])

    assert len(inputs) == 1
    assert inputs[0].file_name == "resume.pdf"
    assert inputs[0].content == b"%PDF-1.7"


def test_run_resume_upload_empty_folder(tmp_path: Path) -> None:
    from rich.console import Console

    console = Console(record=True)
    folder = tmp_path / "resumes"
    folder.mkdir()

    outcomes = run_resume_upload(input_folder=folder, console=console)

    assert outcomes == []
    assert "No resume files found" in console.export_text()


def test_run_resume_upload_processes_files(tmp_path: Path) -> None:
    from rich.console import Console

    folder = tmp_path / "resumes"
    folder.mkdir()
    (folder / "a.pdf").write_bytes(b"%PDF-a")
    (folder / "b.pdf").write_bytes(b"%PDF-b")

    processor = FakeProcessor()
    console = Console(record=True)

    outcomes = run_resume_upload(input_folder=folder, processor=processor, console=console)

    assert len(outcomes) == 2
    assert {outcome.file_name for outcome in outcomes} == {"a.pdf", "b.pdf"}
    assert len(processor.calls) == 2
    output = console.export_text()
    assert "Import complete" in output
    assert "2 imported" in output


def test_run_resume_upload_requires_processor_for_nonempty_folder(tmp_path: Path) -> None:
    folder = tmp_path / "resumes"
    folder.mkdir()
    (folder / "a.pdf").write_bytes(b"%PDF-a")

    with pytest.raises(ResumeUploadError, match="resume processor is required"):
        run_resume_upload(input_folder=folder, processor=None, console=None)


def test_run_resume_upload_handles_unreadable_file(tmp_path: Path, monkeypatch) -> None:
    from rich.console import Console

    folder = tmp_path / "resumes"
    folder.mkdir()
    (folder / "bad.pdf").write_bytes(b"%PDF-bad")

    original_read_bytes = Path.read_bytes

    def fake_read_bytes(self):
        if self.name == "bad.pdf":
            raise OSError("permission denied")
        return original_read_bytes(self)

    monkeypatch.setattr(Path, "read_bytes", fake_read_bytes)

    processor = FakeProcessor()
    console = Console(record=True)

    outcomes = run_resume_upload(input_folder=folder, processor=processor, console=console)

    assert len(outcomes) == 1
    assert outcomes[0].status is ResumeProcessingStatus.PROCESSING_FAILURE
    assert "Could not read file" in outcomes[0].message


def test_run_resume_upload_shows_processing_stage(tmp_path: Path) -> None:
    from rich.console import Console

    folder = tmp_path / "resumes"
    folder.mkdir()
    (folder / "a.pdf").write_bytes(b"%PDF-a")

    processor = FakeProcessor()
    console = Console(record=True)

    outcomes = run_resume_upload(input_folder=folder, processor=processor, console=console)

    assert len(outcomes) == 1
    output = console.export_text()
    assert "Parsing resume" in output
