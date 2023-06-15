from typing import Any, Type
from textual.app import App, CSSPathType, ComposeResult  # type: ignore
from textual.driver import Driver  # type: ignore
from textual.widgets import Pretty, TabPane, TabbedContent  # type: ignore
from ui.AboutUs import AboutUs
from ui.AddOrRemove import AddOrRemove
from ui.ChangePassword import ChangePasswordUsername
from ui.Confirmation import Confirmation
from ui.Financial import Financial
from ui.QuietRequest import QuitRequest  # type: ignore

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
                if self.user["study_status"] == "quited":
                    yield Pretty(
                        "You have quited studying and cant select lessons",
                        classes="bold",
                    )
                yield Selection(self.user)

            with TabPane("Add or remove", id="add_or_remove"):
                if self.user["study_status"] == "quited":
                    yield Pretty(
                        "You have quited studying and cant select lessons",
                        classes="bold",
                    )
                yield AddOrRemove(self.user)

            with TabPane("Confirmation", id="confirmation"):
                if self.user["study_status"] == "quited":
                    yield Pretty(
                        "You have quited studying and cant select lessons",
                        classes="bold",
                    )
                yield Confirmation(self.user)

            with TabPane("Financial", id="financial"):
                yield Financial(self.user)

            with TabPane("Quiet Request", id="quiet_request"):
                yield QuitRequest(self.user)

            with TabPane("About Us", id="about_us"):
                if self.user["study_status"] == "quited":
                    yield Pretty("Kasteh Shodam Dige Baste", classes="bold")
                yield AboutUs(self.user)

            with TabPane("Chagne Username/Password", id="change_username_password"):
                yield ChangePasswordUsername(self.user)

    def action_show_tab(self, tab: str) -> None:
        self.get_child_by_type(TabbedContent).active = tab
