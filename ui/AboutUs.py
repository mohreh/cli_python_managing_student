from textual.app import ComposeResult  # type: ignore
from textual.widgets import Static  # type: ignore


class AboutUs(Static):
    def compose(self) -> ComposeResult:
        yield Static("AboutUs")
