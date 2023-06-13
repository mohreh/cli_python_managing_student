from textual.app import ComposeResult  # type: ignore
from textual.widgets import Static  # type: ignore


class Selection(Static):
    def compose(self) -> ComposeResult:
        yield Static("Selection")
