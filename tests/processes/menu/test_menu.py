from typer.testing import CliRunner

from cli.app import app
from cli.commands.menu import _OPTIONS, _OPTIONS_MENU_OPTIONS


def test_main_menu_options_include_required_items() -> None:
    assert _OPTIONS == ["Import Resumes", "Options", "Exit"]


def test_options_menu_options_include_required_items() -> None:
    assert _OPTIONS_MENU_OPTIONS == ["Imported Resume", "Back"]


def test_main_menu_exits_on_enter() -> None:
    runner = CliRunner()

    result = runner.invoke(app, [], input="\n")

    assert result.exit_code == 0
    assert "Exiting CVBrewer." in result.output


def test_main_menu_can_open_options_and_return() -> None:
    runner = CliRunner()

    result = runner.invoke(app, [], input="2\n2\n3\n")

    assert result.exit_code == 0
    assert "Options" in result.output
    assert "Exiting CVBrewer." in result.output


def test_main_menu_can_run_import_resumes_on_empty_folder(tmp_path, monkeypatch) -> None:
    from cli.modules.paths import StartupPaths

    paths = StartupPaths(
        database=tmp_path / "cvbrewer.db",
        resumes=tmp_path / "resumes",
        generated=tmp_path / "generated",
    )
    monkeypatch.setattr("cli.app.get_startup_paths", lambda: paths)
    monkeypatch.setattr("cli.app.get_resume_processor", lambda: None)

    runner = CliRunner()
    result = runner.invoke(app, [], input="1\n3\n")

    assert result.exit_code == 0
    assert "No resume files found" in result.output
    assert "Exiting CVBrewer." in result.output
