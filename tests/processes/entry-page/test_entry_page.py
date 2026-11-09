from typer.testing import CliRunner

from cli.app import app


def test_entry_page_displays_title_and_exits_after_enter() -> None:
    runner = CliRunner()

    result = runner.invoke(app, [], input="\n")

    assert result.exit_code == 0
    assert "CVBrewer" in result.output
