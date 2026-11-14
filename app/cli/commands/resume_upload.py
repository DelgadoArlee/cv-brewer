from pathlib import Path

from rich.console import Console
from rich.progress import (
    BarColumn,
    Progress,
    SpinnerColumn,
    TaskProgressColumn,
    TextColumn,
    TimeElapsedColumn,
)

from core.models import ResumeInput, ResumeProcessingOutcome, ResumeProcessingStatus
from core.pipeline import ResumeProcessor

from cli.modules.paths import StartupPaths
from cli.ui.resume_upload import (
    format_stage_description,
    render_empty_folder,
    render_upload_results,
)


class ResumeUploadError(Exception):
    pass


def _resolve_folder(paths: str | Path | StartupPaths) -> Path:
    if isinstance(paths, (str, Path)):
        return Path(paths)
    return Path(paths.resumes)


def ensure_input_folder(path: Path) -> None:
    resolved = Path(path)
    try:
        resolved.mkdir(parents=True, exist_ok=True)
    except OSError as exc:
        raise ResumeUploadError(f"Failed to create the input folder at {resolved}.") from exc

    if not resolved.is_dir():
        raise ResumeUploadError(f"Expected a directory at {resolved}.")


def discover_resume_files(input_folder: Path) -> list[Path]:
    folder = Path(input_folder)
    if not folder.is_dir():
        raise ResumeUploadError(f"Input folder is not accessible: {folder}")

    try:
        entries = sorted(folder.iterdir(), key=lambda path: path.name)
    except OSError as exc:
        raise ResumeUploadError(f"Failed to read the input folder at {folder}.") from exc

    return [path for path in entries if path.is_file()]


def build_resume_inputs(paths: list[Path]) -> list[ResumeInput]:
    resume_inputs: list[ResumeInput] = []
    for path in paths:
        try:
            content = path.read_bytes()
        except OSError as exc:
            raise ResumeUploadError(f"Failed to read {path}.") from exc
        resume_inputs.append(
            ResumeInput(
                file_name=path.name,
                original_file_path=str(path),
                content=content,
            )
        )
    return resume_inputs


def run_resume_upload(
    paths: str | Path | StartupPaths,
    resume_processor: ResumeProcessor,
    *,
    console: Console | None = None,
) -> list[ResumeProcessingOutcome]:
    folder = _resolve_folder(paths)

    try:
        ensure_input_folder(folder)
    except ResumeUploadError:
        raise

    files = discover_resume_files(folder)

    active_console = console
    if files and active_console is None:
        active_console = Console()

    if not files:
        if console is not None:
            render_empty_folder(console, folder)
        return []

    if resume_processor is None:
        raise ResumeUploadError("A resume processor is required to import resumes.")

    outcomes: list[ResumeProcessingOutcome] = []
    file_contents: list[tuple[Path, bytes | OSError]] = []

    for path in files:
        try:
            file_contents.append((path, path.read_bytes()))
        except OSError as exc:
            file_contents.append((path, exc))

    if active_console is not None:
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TaskProgressColumn(),
            TimeElapsedColumn(),
            console=active_console,
        ) as progress:
            task = progress.add_task("Importing resumes", total=len(file_contents))
            for index, (path, content) in enumerate(file_contents, start=1):
                progress.update(
                    task,
                    description=f"Importing {path.name} ({index}/{len(file_contents)})",
                )
                if isinstance(content, OSError):
                    outcomes.append(
                        ResumeProcessingOutcome(
                            file_name=path.name,
                            status=ResumeProcessingStatus.PROCESSING_FAILURE,
                            message=f"Could not read file: {content}",
                        )
                    )
                else:
                    resume_input = ResumeInput(
                        file_name=path.name,
                        original_file_path=str(path),
                        content=content,
                    )

                    def on_stage(stage: str) -> None:
                        progress.update(
                            task,
                            description=format_stage_description(
                                path.name,
                                stage,
                                index,
                                len(file_contents),
                            ),
                        )

                    outcomes.append(
                        resume_processor.process(resume_input, on_stage=on_stage)
                    )
                progress.advance(task)
    else:
        for path, content in file_contents:
            if isinstance(content, OSError):
                outcomes.append(
                    ResumeProcessingOutcome(
                        file_name=path.name,
                        status=ResumeProcessingStatus.PROCESSING_FAILURE,
                        message=f"Could not read file: {content}",
                    )
                )
            else:
                resume_input = ResumeInput(
                    file_name=path.name,
                    original_file_path=str(path),
                    content=content,
                )
                outcomes.append(resume_processor.process(resume_input))

    if console is not None:
        render_upload_results(console, folder, outcomes)

    return outcomes
