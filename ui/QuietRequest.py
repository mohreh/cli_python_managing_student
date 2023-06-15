import time
from textual import on  # type: ignore
from textual.app import ComposeResult  # type: ignore
from textual.widgets import Button, Input, Pretty, Static  # type: ignore

from data.quit_request import QuitRequest as QuitRequestService
from ui.utils.Base import Base
from utils.error import RefreshPage


class QuitRequest(Base):
    def compose(self) -> ComposeResult:
        yield Pretty("", id="quit_log")
        yield Static("Submit Quiet Request")
        yield Input(placeholder="Quiet Request Message", id="quit_message")
        yield Button("Submit Quit Request", id="submit_quit_request", disabled=True)

    @on(Input.Changed, "#quit_message")
    def toggle_disable(self):
        input_box = self.query_one("#quit_message", expect_type=Input)
        button = self.query_one("#submit_quit_request", expect_type=Button)

        if len(input_box.value):
            button.disabled = False
        else:
            button.disabled = True

    @on(Button.Pressed, "#submit_quit_request")
    def submit_quit_request(self):
        message = self.query_one("#quit_message", expect_type=Input).value

        quit_service = QuitRequestService()
        quit_service.submit_quit_request(message, self.user["id"])

        self.app.exit(
            {
                "message": "refresh",
                "username": self.user["username"],
                "password": self.user["password"],
            }
        )
