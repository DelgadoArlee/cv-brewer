import io
from types import SimpleNamespace

from rich.console import Console

from cli.commands import options as options_module
from core.models import ResumeProcessingStatus


def _record_console() -> Console:
    return Console(record=True, file=io.StringIO())


def _empty_resume_processor() -> SimpleNamespace:
    return SimpleNamespace(
        _resume_service=SimpleNamespace(list_resumes=lambda: []),
    )


def test_options_menu_constant() -> None:
    assert options_module._OPTIONS_MENU_OPTIONS == ["Imported Resume", "Back"]


def test_options_menu_back_returns(monkeypatch) -> None:
    console = _record_console()
    monkeypatch.setattr(options_module, "_select_option", lambda _console, _options: 1)

    options_module.run_options_menu(
        console=console,
        resume_processor=_empty_resume_processor(),
    )

    assert "Options" in console.export_text()


def test_options_menu_imported_resume_then_back(monkeypatch) -> None:
    console = _record_console()
    selections = iter([0, 1])
    monkeypatch.setattr(options_module, "_select_option", lambda _console, _options: next(selections))

    options_module.run_options_menu(
        console=console,
        resume_processor=_empty_resume_processor(),
    )

    output = console.export_text()
    print(output)
    assert "Options" in output
    assert "No imported resumes found." in output


def test_run_imported_resume_empty_service() -> None:
    console = _record_console()

    options_module.run_imported_resume(
        console=console,
        resume_processor=_empty_resume_processor(),
    )

    assert "No imported resumes found." in console.export_text()


def test_run_imported_resume_lists_resumes() -> None:
    console = _record_console()
    resume = SimpleNamespace(
        resume_id="abc-123",
        metadata=SimpleNamespace(file_name="resume.pdf"),
        created_at="2026-01-01",
    )
    service = SimpleNamespace(list_resumes=lambda: [resume])
    processor = SimpleNamespace(_resume_service=service)

    options_module.run_imported_resume(console=console, resume_processor=processor)

    output = console.export_text()
    assert "Imported Resumes" in output
    assert "resume.pdf" in output
    assert "abc-123" not in output
