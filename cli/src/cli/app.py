from pathlib import Path
from typing import Any

import typer
from rich.console import Console

from cli.modules.paths import StartupPaths, development_startup_paths

app = typer.Typer(add_completion=False, no_args_is_help=False)

_startup_paths: StartupPaths | None = None
_resume_processor: Any = None


def configure_application(
    paths: StartupPaths,
    resume_processor: Any,
) -> None:
    global _startup_paths, _resume_processor
    _startup_paths = paths
    _resume_processor = resume_processor


def get_startup_paths() -> StartupPaths:
    global _startup_paths
    if _startup_paths is None:
        _startup_paths = development_startup_paths()
    return _startup_paths


def get_resume_processor() -> Any:
    global _resume_processor, _startup_paths
    if _resume_processor is not None:
        return _resume_processor

    paths = get_startup_paths()
    from database import create_resume_service, initialize_database
    from llm import create_llm_service
    from core.pipeline import ResumeProcessor

    try:
        initialize_database(paths.database)
    except Exception:  # noqa: BLE001
        pass

    resume_service = create_resume_service(paths.database)
    llm_service = create_llm_service()
    _resume_processor = ResumeProcessor(resume_service, llm_service)
    return _resume_processor


@app.command("upload")
@app.command("upload-resumes", hidden=True)
def upload_command() -> None:
    from cli.processes.resume_upload import ResumeUploadError, run_resume_upload

    console = Console()
    try:
        run_resume_upload(
            get_startup_paths(),
            get_resume_processor(),
            console=console,
        )
    except ResumeUploadError as exc:
        console.print(f"[red]Error:[/red] {exc}")
        raise typer.Exit(code=1) from exc


@app.callback(invoke_without_command=True)
def main(ctx: typer.Context) -> None:
    from cli.processes.menu import run_menu

    console = Console()
    run_menu(
        get_startup_paths(),
        get_resume_processor(),
        console=console,
    )
