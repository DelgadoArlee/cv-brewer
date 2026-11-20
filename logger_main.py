from collections.abc import Mapping
from functools import partial
from pathlib import Path
import webbrowser

from rich.console import Console

from cli.commands.application_startup import initialize_application
from cli.logger_app import create_logger_app
from cli.modules.logger_context import (
    LoggerCLIDependencies,
    LoggerDependenciesFactory,
    LoggerEnvironment,
    LoggerSources,
)
from cli.modules.paths import StartupPaths, development_startup_paths, startup_paths
from core.services.llm.log_port import LLMLogRepository
from database import (
    create_llm_log_service,
    create_processing_log_service,
    initialize_database,
)

_REPOSITORY_ROOT = Path(__file__).resolve().parent
_ENVIRONMENT_DATA_DIRS: Mapping[LoggerEnvironment, Path] = {
    "dev": development_startup_paths().database.parent,
    "e2e": _REPOSITORY_ROOT / "tests" / "e2e" / "data",
    "test": _REPOSITORY_ROOT / "tests" / "data",
}


def build_dependencies(
    paths: StartupPaths,
    source: LoggerEnvironment,
) -> LoggerCLIDependencies:
    prepared_paths = initialize_application(paths, initialize_database)
    log_repository: LLMLogRepository = create_llm_log_service(prepared_paths.database)
    processing_log_service = create_processing_log_service(prepared_paths.database)
    return LoggerCLIDependencies(
        prepared_paths,
        log_repository,
        processing_log_service,
        source,
        _REPOSITORY_ROOT / "logs",
        webbrowser.open,
    )


def available_log_sources() -> LoggerSources:
    sources: dict[LoggerEnvironment, LoggerDependenciesFactory] = {}
    for environment, data_dir in _ENVIRONMENT_DATA_DIRS.items():
        paths = startup_paths(data_dir)
        if paths.database.is_file():
            sources[environment] = partial(build_dependencies, paths, environment)
    return sources


def main() -> None:
    console = Console()
    sources = available_log_sources()
    if not sources:
        console.print("[red]Error:[/red] No log databases found.")
        raise SystemExit(1)
    create_logger_app(sources)()


if __name__ == "__main__":
    main()
