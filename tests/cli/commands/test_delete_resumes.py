import io
from pathlib import Path
from types import SimpleNamespace

from rich.console import Console

from cli.commands import delete_resumes as delete_resumes_module
from cli.modules.context import CLIDependencies
from cli.modules.paths import StartupPaths


def _record_console() -> Console:
    return Console(record=True, file=io.StringIO())


def _dependencies(delete_all_resumes) -> CLIDependencies:
    paths = StartupPaths(
        database=Path("/tmp/cvbrewer.db"),
        resumes=Path("/tmp/resumes"),
        generated=Path("/tmp/generated"),
    )
    return CLIDependencies(
        paths,
        SimpleNamespace(),
        SimpleNamespace(list_resumes=lambda: []),
        SimpleNamespace(delete_all_resumes=delete_all_resumes),
    )


def test_delete_imported_resumes_cancelled(monkeypatch) -> None:
    console = _record_console()
    calls = []
    monkeypatch.setattr(
        delete_resumes_module,
        "confirm_delete_imported_resumes",
        lambda _console: False,
    )

    deleted_count = delete_resumes_module.run_delete_imported_resumes(
        _dependencies(lambda: calls.append("deleted") or 1),
        console=console,
    )

    assert deleted_count == 0
    assert calls == []
    assert "Deletion cancelled." in console.export_text()


def test_delete_imported_resumes_reports_deleted_count(monkeypatch) -> None:
    console = _record_console()
    monkeypatch.setattr(
        delete_resumes_module,
        "confirm_delete_imported_resumes",
        lambda _console: True,
    )

    deleted_count = delete_resumes_module.run_delete_imported_resumes(
        _dependencies(lambda: 3),
        console=console,
    )

    assert deleted_count == 3
    assert "Deleted 3 imported resume(s)" in console.export_text()


def test_delete_imported_resumes_reports_empty_database(monkeypatch) -> None:
    console = _record_console()
    monkeypatch.setattr(
        delete_resumes_module,
        "confirm_delete_imported_resumes",
        lambda _console: True,
    )

    deleted_count = delete_resumes_module.run_delete_imported_resumes(
        _dependencies(lambda: 0),
        console=console,
    )

    assert deleted_count == 0
    assert "No imported resumes were deleted." in console.export_text()


def test_delete_imported_resumes_propagates_failure(monkeypatch) -> None:
    console = _record_console()
    monkeypatch.setattr(
        delete_resumes_module,
        "confirm_delete_imported_resumes",
        lambda _console: True,
    )

    def fail() -> int:
        raise RuntimeError("database unavailable")

    try:
        delete_resumes_module.run_delete_imported_resumes(
            _dependencies(fail),
            console=console,
        )
    except RuntimeError as exc:
        assert "database unavailable" in str(exc)
    else:
        raise AssertionError("Expected the deletion failure to propagate.")
