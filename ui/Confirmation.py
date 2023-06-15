from ast import literal_eval
from typing import Any, List
from textual import on  # type: ignore
from textual.app import ComposeResult  # type: ignore
from textual.widgets import Button, DataTable, Pretty, Static  # type: ignore

from data.lesson import Lesson
from data.selection import Selection as LessonSelection
from ui.utils.BaseTableLoader import BaseTableLoader
from utils.print_exam_card import printـexam_card  # type: ignore


class Confirmation(BaseTableLoader):
    def compose(self) -> ComposeResult:
        yield Static("Selected Lessons", classes="m-1")
        yield DataTable(id="selected", classes="m-1")
        yield Button("Reload", id="reload")

        yield Pretty("", id="confirmation_error", classes="m-1")

        yield Static("Available Lessons", classes="m-1")
        yield DataTable(id="available", classes="m-1")
        yield Button("Print Your Exam Card", id="print_exam_card")
        yield Pretty("", id="print_errors")

    @on(Button.Pressed, "#print_exam_card")
    def print_exam_card(self):
        try:
            printـexam_card(self.user["id"])
        except Exception as err:
            self.query_one("#print_errors", expect_type=Pretty).update(str(err))

    @on(Button.Pressed, "#reload")
    def reload(self):
        self.load_selected_lessons()

    def load_selected_lessons(self):
        selected_table = self.query_one("#selected", expect_type=DataTable)
        selected_table.clear()

        selection_service = LessonSelection()

        selected_lessons = selection_service.all_selected_lessons(self.user["id"])

        selected_lessons_array = []
        if not selected_lessons or not len(selected_lessons):
            self.query_one("#confirmation_error", expect_type=Pretty).update(
                "you have not select lessons yet"
            )
            return

        for lesson in selected_lessons:
            del lesson["time_id"]
            del lesson["id"]
            del lesson["teacher_id"]

            selected_lessons_array.append(lesson.values())

        lesson_service = Lesson()
        headers = lesson_service.headers

        headers.remove("time_id")
        headers.remove("teacher_id")
        headers.remove("id")

        headers.append("time")
        headers.append("perofessor")

        if not len(selected_table.columns.values()):
            selected_table.add_columns(*headers)

        selected_table.add_rows(selected_lessons_array)
        selected_table.cursor_type = "row"
        selected_table.zebra_stripes = True

    def on_mount(self):
        available_table = self.query_one("#available", expect_type=DataTable)

        lesson_service = Lesson()

        all_lessons: List[dict[str, Any]] = lesson_service.all_lessons()  # type: ignore
        available_lessons = []
        for lesson in all_lessons:
            time_str = []
            for time in lesson["time"]:
                time_str.append(
                    "{} {} {}".format(time["week"], time["day"], time["hour"])
                )

            lesson["time"] = " - ".join(time_str)
            del lesson["id"]
            available_lessons.append(lesson.values())

        headers = lesson_service.headers
        headers.remove("time_id")
        headers.remove("teacher_id")
        headers.remove("id")
        headers.append("time")
        headers.append("perofessor")

        self.load_table(available_table, headers, available_lessons)
        self.load_selected_lessons()
