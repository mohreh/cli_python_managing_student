from textual import on  # type: ignore
from textual.app import ComposeResult  # type: ignore
from textual.widgets import Button, Input  # type: ignore
from data.student import Student  # type: ignore
from ui.utils.Base import Base


class ChangePasswordUsername(Base):
    def compose(self) -> ComposeResult:
        yield Input(
            value=self.user["username"],
            placeholder="username",
            id="username",
        )
        yield Input(
            value=self.user["password"],
            placeholder="password",
            id="password",
        )
        yield Button("change password/username", id="change")

    @on(Button.Pressed, "#change")
    def change(self):
        username_input = self.query_one("#username", expect_type=Input)
        password_input = self.query_one("#password", expect_type=Input)

        student_service = Student()
        student_service.update_data(
            self.user["id"],
            username=username_input.value,
            password=password_input.value,
        )

        self.user = student_service.find(username_input.value) or self.user
        username_input.value = self.user["username"]
        password_input.value = self.user["password"]

        self.app.exit(
            {
                "message": "refresh",
                "username": self.user["username"],
                "password": self.user["password"],
            }
        )
