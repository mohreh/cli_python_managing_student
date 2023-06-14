from ast import literal_eval
from typing import Any, List
from textual import on  # type: ignore
from textual.app import ComposeResult  # type: ignore
from textual.widgets import Button, DataTable, Pretty, Static  # type: ignore

from data.lesson import Lesson
from data.perofessor import Perofessor
from data.selection import Selection as LessonSelection
from data.time import Time
from ui.utils.BaseTableLoader import BaseTableLoader  # type: ignore


class Confirmation(BaseTableLoader):
    def compose(self) -> ComposeResult:
        yield Static("Selected Lessons", classes="m-1")
        yield DataTable(id="selected", classes="m-1")
        yield Button("Reload", id="reload")

        yield Pretty("", id="confirmation_error", classes="m-1")

        yield Static("Available Lessons", classes="m-1")
        yield DataTable(id="available", classes="m-1")

    @on(Button.Pressed, "#reload")
    def reload(self):
        self.load_selected_lessons()

    def load_selected_lessons(self):
        selected_table = self.query_one("#selected", expect_type=DataTable)
        selected_table.clear()

        selection_service = LessonSelection()
        time_service = Time()
        lesson_service = Lesson()
        perofessor = Perofessor()

        user_selection = selection_service.find_with_student_id(self.user["id"])
        if not user_selection:
            self.query_one("#confirmation_error", expect_type=Pretty).update(
                "you have not select lessons yet"
            )
            return

        selected_lesson_codes = user_selection["lesson_ids"]

        selected_lessons = []
        for code in literal_eval(selected_lesson_codes):
            lesson = lesson_service.find(code)
            if not lesson:
                return

            time_str = []
            for time_id in literal_eval(lesson["time_id"]):
                lesson_time = time_service.find_with_id(str(time_id))
                time_str.append(
                    "{} {} {}".format(
                        lesson_time["week"], lesson_time["day"], lesson_time["hour"]
                    )
                )
            del lesson["time_id"]
            del lesson["id"]
            lesson["time"] = " - ".join(time_str)

            lesson["perofessor"] = perofessor.find(lesson["teacher_id"])["name"]
            del lesson["teacher_id"]

            selected_lessons.append(lesson.values())

        headers = lesson_service.headers
        headers.remove("time_id")
        headers.remove("teacher_id")
        headers.remove("id")
        headers.append("time")
        headers.append("perofessor")

        if not len(selected_table.columns.values()):
            selected_table.add_columns(*headers)

        selected_table.add_rows(selected_lessons)
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
