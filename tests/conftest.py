from pathlib import Path

import pytest

from cli.modules.paths import StartupPaths, startup_paths
from tests.fixtures.environment import (
    E2E_DATA_PATH,
    E2E_TESTS_PATH,
    TEST_DATA_PATH,
    reset_data_directory,
)


def pytest_sessionstart(session: pytest.Session) -> None:
    if session.config.option.collectonly:
        return

    reset_data_directory(TEST_DATA_PATH)
    reset_data_directory(E2E_DATA_PATH)


def pytest_collection_modifyitems(
    config: pytest.Config,
    items: list[pytest.Item],
) -> None:
    startup_items = [
        item for item in items if item.get_closest_marker("application_startup")
    ]
    remaining_items = [
        item for item in items if not item.get_closest_marker("application_startup")
    ]
    non_e2e_items = [item for item in remaining_items if not _is_e2e_item(item)]
    e2e_items = [item for item in remaining_items if _is_e2e_item(item)]

    items[:] = (
        startup_items
        + _empty_data_first(non_e2e_items)
        + _empty_data_first(e2e_items)
    )


def _is_e2e_item(item: pytest.Item) -> bool:
    return Path(item.path).resolve().is_relative_to(E2E_TESTS_PATH)


def _empty_data_first(items: list[pytest.Item]) -> list[pytest.Item]:
    empty_data_items = [
        item for item in items if item.get_closest_marker("requires_empty_data")
    ]
    other_items = [
        item for item in items if not item.get_closest_marker("requires_empty_data")
    ]
    return empty_data_items + other_items


@pytest.fixture(scope="session")
def test_environment_path() -> Path:
    return TEST_DATA_PATH


@pytest.fixture(scope="session")
def test_startup_paths(test_environment_path: Path) -> StartupPaths:
    return startup_paths(test_environment_path)
