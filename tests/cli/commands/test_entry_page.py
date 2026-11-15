from pathlib import Path
from types import SimpleNamespace

from typer.testing import CliRunner

from cli.app import create_app
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


def test_entry_page_displays_title_and_exits_after_enter(tmp_path: Path) -> None:
    runner = CliRunner()
    app = create_app(_dependencies(tmp_path))

    result = runner.invoke(app, [], input="\n")

    assert result.exit_code == 0
    assert "CVBrewer" in result.output
