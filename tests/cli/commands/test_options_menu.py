import io
from pathlib import Path
from types import SimpleNamespace

from rich.console import Console

from cli.commands import options as options_module
from cli.modules.context import CLIDependencies
from cli.modules.paths import StartupPaths


def _record_console() -> Console:
    return Console(record=True, file=io.StringIO())


def _dependencies(list_resumes, delete_all_resumes=None) -> CLIDependencies:
    paths = StartupPaths(
        database=Path("/tmp/cvbrewer.db"),
        resumes=Path("/tmp/resumes"),
        generated=Path("/tmp/generated"),
    )
    return CLIDependencies(
        paths,
        SimpleNamespace(),
        SimpleNamespace(list_resumes=list_resumes),
        SimpleNamespace(delete_all_resumes=delete_all_resumes or (lambda: 0)),
    )


def test_options_menu_constant() -> None:
    assert options_module._OPTIONS_MENU_OPTIONS == [
        "Imported Resume",
        "Delete Imported Resumes",
        "Back",
    ]


def test_options_menu_back_returns(monkeypatch) -> None:
    console = _record_console()
    monkeypatch.setattr(options_module, "_select_option", lambda _console, _options: 2)

    options_module.run_options_menu(
        _dependencies(lambda: []),
        console=console,
    )

    assert "Options" in console.export_text()


def test_options_menu_imported_resume_then_back(monkeypatch) -> None:
    console = _record_console()
    selections = iter([0, 2])
    monkeypatch.setattr(options_module, "_select_option", lambda _console, _options: next(selections))

    options_module.run_options_menu(
        _dependencies(lambda: []),
        console=console,
    )

    output = console.export_text()
    assert "Options" in output
    assert "No imported resumes found." in output


def test_options_menu_delete_imported_resumes_then_back(monkeypatch) -> None:
    console = _record_console()
    deleted = []
    selections = iter([1, 2])
    monkeypatch.setattr(
        options_module,
        "_select_option",
        lambda _console, _options: next(selections),
    )
    monkeypatch.setattr(
        options_module,
        "run_delete_imported_resumes",
        lambda _dependencies, console: deleted.append(console),
    )

    options_module.run_options_menu(
        _dependencies(lambda: []),
        console=console,
    )

    assert deleted == [console]
    assert "Options" in console.export_text()


def test_run_imported_resume_empty_service() -> None:
    console = _record_console()

    options_module.run_imported_resume(
        _dependencies(lambda: []),
        console=console,
    )

    assert "No imported resumes found." in console.export_text()


def test_run_imported_resume_lists_resumes() -> None:
    console = _record_console()
    resume = SimpleNamespace(
        resume_id="abc-123",
        metadata=SimpleNamespace(file_name="resume.pdf"),
        created_at="2026-01-01",
    )

    options_module.run_imported_resume(
        _dependencies(lambda: [resume]),
        console=console,
    )

    output = console.export_text()
    assert "Imported Resumes" in output
    assert "resume.pdf" in output
    assert "abc-123" not in output
