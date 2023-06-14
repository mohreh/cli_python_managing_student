from typing import Any, Type
from textual.app import App, CSSPathType, ComposeResult  # type: ignore
from textual.driver import Driver  # type: ignore
from textual.widgets import TabPane, TabbedContent  # type: ignore
from ui.AboutUs import AboutUs
from ui.AddOrRemove import AddOrRemove
from ui.Confirmation import Confirmation
from ui.Financial import Financial
from ui.QuietRequest import QuietRequest  # type: ignore

from ui.Selection import Selection


class MainApp(App):
    CSS_PATH = "style/app.css"

    def __init__(
        self,
        user: dict[str, Any],
        driver_class: Type[Driver] | None = None,
        css_path: CSSPathType | None = None,
        watch_css: bool = False,
    ):
        super().__init__(driver_class, css_path, watch_css)
        self.user = user

    def compose(self) -> ComposeResult:
        with TabbedContent(initial="about_us"):
            with TabPane("Selection", id="selection"):
                yield Selection(self.user)

            with TabPane("Add or remove", id="add_or_remove"):
                yield AddOrRemove()

            with TabPane("Confirmation", id="confirmation"):
                yield Confirmation(self.user)

            with TabPane("Financial", id="financial"):
                yield Financial()

            with TabPane("Quiet Request", id="quiet_request"):
                yield QuietRequest()

            with TabPane("About Us", id="about_us"):
                yield AboutUs(self.user)

    def action_show_tab(self, tab: str) -> None:
        self.get_child_by_type(TabbedContent).active = tab
