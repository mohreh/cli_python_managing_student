from typing import Any, List
from rich.console import RenderableType  # type: ignore
from rich.text import Text  # type: ignore
from textual.app import ComposeResult
from textual.containers import Horizontal  # type: ignore
from textual.widgets import DataTable, Label, ProgressBar, Static, TextLog  # type: ignore

from data import student  # type: ignore

ROWS = [
    ["lane", "swimmer", "country", "time"],
    [4, "Joseph Schooling", "Singapore", 50.39],
    [2, "Michael Phelps", "United States", 51.14],
    [5, "Chad le Clos", "South Africa", 51.14],
    [6, "László Cseh", "Hungary", 51.14],
    [3, "Li Zhuhao", "China", 51.26],
    [8, "Mehdy Metella", "France", 51.58],
    [7, "Tom Shields", "United States", 51.73],
    [1, "Aleksandr Sadovnikov", "Russia", 51.84],
    [10, "Darren Burns", "Scotland", 51.84],
]


class AboutUs(Static):
    def __init__(
        self,
        user: dict[str, Any],
        renderable: RenderableType = "",
        *,
        expand: bool = False,
        shrink: bool = False,
        markup: bool = True,
        name: str | None = None,
        id: str | None = None,
        classes: str | None = None,
        disabled: bool = False
    ) -> None:
        super().__init__(
            renderable,
            expand=expand,
            shrink=shrink,
            markup=markup,
            name=name,
            id=id,
            classes=classes,
            disabled=disabled,
        )
        self.user = user

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
