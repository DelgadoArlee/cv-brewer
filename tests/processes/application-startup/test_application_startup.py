import ast
from pathlib import Path

import pytest

from cli.modules.paths import StartupPaths, development_startup_paths
from cli.processes.application_startup import StartupError, initialize_application
from database import initialize_database as initialize_database_from_path

pytestmark = pytest.mark.application_startup


def _isolated_startup_paths(tmp_path: Path) -> StartupPaths:
    return StartupPaths(
        database=tmp_path / "data" / "cvbrewer.db",
        resumes=tmp_path / "data" / "local" / "resumes",
        generated=tmp_path / "data" / "local" / "generated",
    )


def test_startup_initializes_database_and_creates_folders(
    test_startup_paths: StartupPaths,
) -> None:
    initialized: list[Path] = []

    def initialize_database(database_path: Path) -> None:
        initialized.append(database_path)
        initialize_database_from_path(database_path)

    result = initialize_application(test_startup_paths, initialize_database)

    assert result == test_startup_paths
    assert initialized == [test_startup_paths.database]
    assert test_startup_paths.database.is_file()
    assert test_startup_paths.resumes.is_dir()
    assert test_startup_paths.generated.is_dir()


def test_test_startup_paths_match_development_structure(
    test_environment_path: Path,
    test_startup_paths: StartupPaths,
) -> None:
    development_paths = development_startup_paths()
    development_root = development_paths.database.parent

    assert (
        test_startup_paths.database.relative_to(test_environment_path)
        == development_paths.database.relative_to(development_root)
    )
    assert (
        test_startup_paths.resumes.relative_to(test_environment_path)
        == development_paths.resumes.relative_to(development_root)
    )
    assert (
        test_startup_paths.generated.relative_to(test_environment_path)
        == development_paths.generated.relative_to(development_root)
    )


def test_startup_stops_when_database_initialization_fails(tmp_path: Path) -> None:
    paths = _isolated_startup_paths(tmp_path)

    def initialize_database(_database_path: Path) -> None:
        raise RuntimeError("database failure")

    with pytest.raises(StartupError, match="database"):
        initialize_application(paths, initialize_database)

    assert not paths.resumes.exists()
    assert not paths.generated.exists()


def test_startup_stops_when_folder_path_is_a_file(tmp_path: Path) -> None:
    paths = _isolated_startup_paths(tmp_path)
    paths.resumes.parent.mkdir(parents=True)
    paths.resumes.touch()

    def initialize_database(database_path: Path) -> None:
        database_path.parent.mkdir(parents=True, exist_ok=True)
        database_path.touch()

    with pytest.raises(StartupError, match="directory"):
        initialize_application(paths, initialize_database)

    assert not paths.generated.exists()


def test_development_startup_paths_are_under_cli_data() -> None:
    paths = development_startup_paths()

    assert paths.database.name == "cvbrewer.db"
    assert paths.database.parent.name == "data"
    assert paths.database.parent.parent.name == "cli"
    assert paths.resumes.parts[-2:] == ("local", "resumes")
    assert paths.resumes.parents[2].name == "cli"
    assert paths.generated.parts[-2:] == ("local", "generated")
    assert paths.generated.parents[2].name == "cli"


def test_startup_module_does_not_import_database_implementation() -> None:
    module_path = (
        Path(__file__).resolve().parents[3]
        / "cli"
        / "src"
        / "cli"
        / "processes"
        / "application_startup.py"
    )
    tree = ast.parse(module_path.read_text())

    imported_modules: list[str] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imported_modules.extend(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            imported_modules.append(node.module)

    assert all(
        not module.startswith(("database", "sqlalchemy", "sqlite3"))
        for module in imported_modules
    )
