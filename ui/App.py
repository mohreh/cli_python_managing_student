from textual.app import App, ComposeResult  # type: ignore
from textual.widgets import Static, TabPane, TabbedContent  # type: ignore
from ui.AboutUs import AboutUs
from ui.AddOrRemove import AddOrRemove
from ui.Confirmation import Confirmation
from ui.Financial import Financial
from ui.QuietRequest import QuietRequest  # type: ignore

from ui.Selection import Selection


class MainApp(App):
    CSS_PATH = "style/app.css"

    def compose(self) -> ComposeResult:
        with TabbedContent(initial="selection"):
            with TabPane("Selection", id="selection"):
                yield Selection()

            with TabPane("Add or remove", id="add_or_remove"):
                yield AddOrRemove()

            with TabPane("Confirmation", id="confirmation"):
                yield Confirmation()

            with TabPane("Financial", id="financial"):
                yield Financial()

            with TabPane("Quiet Request", id="quiet_request"):
                yield QuietRequest()

            with TabPane("About Us", id="about_us"):
                yield AboutUs()

    def action_show_tab(self, tab: str) -> None:
        self.get_child_by_type(TabbedContent).active = tab
