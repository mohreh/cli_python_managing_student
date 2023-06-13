from textual.app import ComposeResult  # type: ignore
from textual.widgets import Static  # type: ignore


class AddOrRemove(Static):
    def compose(self) -> ComposeResult:
        yield Static("AddOrRemove")
