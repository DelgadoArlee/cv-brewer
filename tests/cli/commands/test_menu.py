import ast
from pathlib import Path
from types import SimpleNamespace

from typer.testing import CliRunner

from cli.app import create_app
from cli.commands.menu import _OPTIONS
from cli.commands.options import _OPTIONS_MENU_OPTIONS
from cli.modules.context import CLIDependencies
from cli.modules.paths import StartupPaths


class _NoopProcessor:
    def process(self, resume_input, *, on_stage=None):
        raise AssertionError("The resume processor should not be called.")


def _dependencies(tmp_path: Path) -> CLIDependencies:
    paths = StartupPaths(
        database=tmp_path / "cvbrewer.db",
        resumes=tmp_path / "resumes",
        generated=tmp_path / "generated",
    )
    return CLIDependencies(
        paths,
        _NoopProcessor(),
        SimpleNamespace(list_resumes=lambda: []),
    )


def test_main_menu_options_include_required_items() -> None:
    assert _OPTIONS == ["Import Resumes", "Options", "Exit"]


def test_options_menu_options_include_required_items() -> None:
    assert _OPTIONS_MENU_OPTIONS == ["Imported Resume", "Back"]


def test_main_menu_exits_on_enter(tmp_path: Path) -> None:
    runner = CliRunner()
    app = create_app(_dependencies(tmp_path))

    result = runner.invoke(app, [], input="\n")

    assert result.exit_code == 0
    assert "Exiting CVBrewer." in result.output


def test_main_menu_can_open_options_and_return(tmp_path: Path) -> None:
    runner = CliRunner()
    app = create_app(_dependencies(tmp_path))

    result = runner.invoke(app, [], input="2\n2\n3\n")

    assert result.exit_code == 0
    assert "Options" in result.output
    assert "Exiting CVBrewer." in result.output


def test_main_menu_can_run_import_resumes_on_empty_folder(tmp_path: Path) -> None:
    runner = CliRunner()
    app = create_app(_dependencies(tmp_path))

    result = runner.invoke(app, [], input="1\n3\n")

    assert result.exit_code == 0
    assert "No resume files found" in result.output
    assert "Exiting CVBrewer." in result.output


def test_cli_app_does_not_import_database_or_llm() -> None:
    module_path = Path(__file__).resolve().parents[3] / "app" / "cli" / "app.py"
    tree = ast.parse(module_path.read_text(encoding="utf-8"))

    imported_modules: list[str] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imported_modules.extend(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module is not None:
            imported_modules.append(node.module)

    assert all(
        not module.startswith(("database", "llm"))
        for module in imported_modules
    )


def test_cli_app_has_no_global_dependency_accessors() -> None:
    module_path = Path(__file__).resolve().parents[3] / "app" / "cli" / "app.py"
    tree = ast.parse(module_path.read_text(encoding="utf-8"))

    function_names = {
        node.name for node in tree.body if isinstance(node, ast.FunctionDef)
    }

    assert "configure_application" not in function_names
    assert "get_resume_processor" not in function_names
    assert "get_startup_paths" not in function_names
