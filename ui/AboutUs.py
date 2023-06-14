from typing import List
from textual.app import ComposeResult  # type: ignore
from textual.containers import Container, Vertical  # type: ignore
from textual.widgets import DataTable, Static  # type: ignore

from data import student
from data.entry_exit_time import EntryExitTime
from ui.utils.Base import Base  # type: ignore


class AboutUs(Base):
    def compose(self) -> ComposeResult:
        yield Static("Your Data", classes="p-2")
        yield Static(id="container", classes="p-2")
        yield Static("Your Entry Exit Times", classes="p-2")
        yield DataTable(id="entry_exit", classes="p-2")

    def on_mount(self) -> None:
        container = self.query_one("#container", expect_type=Static)
        for index, header in enumerate(student.headers):
            container._add_children(
                Static(
                    header + ": " + self.user[header],
                    classes="even" if index % 2 == 0 else "odd",
                )
            )

        table = self.query_one("#entry_exit", expect_type=DataTable)

        entry_exit_service = EntryExitTime()

        entry_exit_times = entry_exit_service.find_for_student_id(self.user["id"])
        rows = []
        for time in entry_exit_times:
            del time["student_id"]
            del time["id"]
            rows.append(time.values())

        headers: List[str] = entry_exit_service.headers
        headers.remove("student_id")
        headers.remove("id")

        table.add_columns(*headers)
        table.add_rows(rows)
        table.cursor_type = "row"
        table.zebra_stripes = True
