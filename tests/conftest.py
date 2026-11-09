import shutil
from pathlib import Path

import pytest

from cli.modules.paths import StartupPaths, startup_paths

TEST_DATA_PATH = Path(__file__).resolve().parent / "data"


def pytest_sessionstart(session: pytest.Session) -> None:
    if session.config.option.collectonly:
        return

    _reset_test_data()


def pytest_collection_modifyitems(
    config: pytest.Config,
    items: list[pytest.Item],
) -> None:
    startup_items = [
        item for item in items if item.get_closest_marker("application_startup")
    ]
    other_items = [
        item for item in items if not item.get_closest_marker("application_startup")
    ]
    items[:] = startup_items + other_items


@pytest.fixture(scope="session")
def test_environment_path() -> Path:
    return TEST_DATA_PATH


@pytest.fixture(scope="session")
def test_startup_paths(test_environment_path: Path) -> StartupPaths:
    return startup_paths(test_environment_path)


def _reset_test_data() -> None:
    if TEST_DATA_PATH.exists():
        if TEST_DATA_PATH.is_dir():
            shutil.rmtree(TEST_DATA_PATH)
        else:
            TEST_DATA_PATH.unlink()

    TEST_DATA_PATH.mkdir(parents=True)
