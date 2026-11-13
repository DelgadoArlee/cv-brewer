import shutil
from collections.abc import Iterator
from pathlib import Path
from types import SimpleNamespace

import pytest

import cli.app as app_module
from cli.app import configure_application
from cli.modules.paths import StartupPaths, startup_paths
from cli.commands.application_startup import initialize_application
from core.pipeline import ResumeProcessor
from database import create_resume_service, initialize_database
from llm import create_llm_service
from tests.fixtures.environment import E2E_DATA_PATH


@pytest.fixture(scope="session")
def e2e_environment_path() -> Path:
    return E2E_DATA_PATH


@pytest.fixture(scope="session")
def e2e_startup_paths(e2e_environment_path: Path) -> StartupPaths:
    return startup_paths(e2e_environment_path)


@pytest.fixture(scope="session")
def e2e_application(e2e_startup_paths: StartupPaths) -> SimpleNamespace:
    paths = initialize_application(e2e_startup_paths, initialize_database)
    llm_service = create_llm_service()

    if not llm_service.check_availability():
        pytest.fail(
            "The E2E tests require a running Ollama service at the default endpoint."
        )

    if not llm_service.list_models():
        pytest.fail("The E2E tests require at least one model installed in Ollama.")

    resume_service = create_resume_service(paths.database)
    processor = ResumeProcessor(resume_service, llm_service)
    return SimpleNamespace(
        paths=paths,
        processor=processor,
        resume_service=resume_service,
    )


@pytest.fixture
def e2e_cli(e2e_application: SimpleNamespace) -> Iterator[SimpleNamespace]:
    previous_paths = app_module._startup_paths
    previous_processor = app_module._resume_processor

    _clear_input_folder(e2e_application.paths.resumes)
    configure_application(e2e_application.paths, e2e_application.processor)

    try:
        yield e2e_application
    finally:
        app_module._startup_paths = previous_paths
        app_module._resume_processor = previous_processor


def _clear_input_folder(folder: Path) -> None:
    folder.mkdir(parents=True, exist_ok=True)
    for entry in folder.iterdir():
        if entry.is_dir() and not entry.is_symlink():
            shutil.rmtree(entry)
        else:
            entry.unlink()
