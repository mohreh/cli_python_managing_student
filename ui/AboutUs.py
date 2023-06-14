from textual.app import ComposeResult  # type: ignore
from textual.widgets import Static  # type: ignore

from data import student
from ui.utils.Base import Base  # type: ignore


class AboutUs(Base):
    def compose(self) -> ComposeResult:
        yield Static("Your Data", id="title")

    def on_mount(self) -> None:
        for index, header in enumerate(student.headers):
            self._add_children(
                Static(
                    header + ": " + self.user[header],
                    classes="even" if index % 2 == 0 else "odd",
                )
            )
