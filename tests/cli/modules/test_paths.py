from pathlib import Path

from cli.modules.paths import StartupPaths, development_startup_paths, startup_paths


def test_startup_paths_builds_expected_paths(tmp_path: Path) -> None:
    paths = startup_paths(tmp_path)

    assert isinstance(paths, StartupPaths)
    assert paths.database == tmp_path / "cvbrewer.db"
    assert paths.resumes == tmp_path / "local" / "resumes"
    assert paths.generated == tmp_path / "local" / "generated"


def test_development_startup_paths_are_under_cli_data() -> None:
    paths = development_startup_paths()

    assert paths.database.name == "cvbrewer.db"
    assert paths.database.parent.name == "data"
    assert paths.resumes.parts[-2:] == ("local", "resumes")
    assert paths.generated.parts[-2:] == ("local", "generated")
