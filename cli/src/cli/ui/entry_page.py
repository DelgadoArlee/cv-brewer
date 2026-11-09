from rich.console import Console
from rich.panel import Panel
from rich.rule import Rule
from rich.text import Text

BEER_COLOR = "#D9A441"


def render_entry_page(console: Console) -> None:
    console.print(
        Panel.fit(
            Text("CVBrewer", style="bold", justify="center"),
            padding=(1, 4),
            border_style=BEER_COLOR,
        )
    )
    console.print(Rule(style=BEER_COLOR))


def wait_for_enter(console: Console) -> None:
    console.input("Press Enter to exit")
