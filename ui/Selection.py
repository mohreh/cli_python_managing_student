from typing import Any, List
from textual import on  # type: ignore
from textual.app import ComposeResult  # type: ignore
from textual.widgets import Button, DataTable, Input, Pretty, Static  # type: ignore


from data.lesson import Lesson
from data.selection import Selection as LessonSelection
from ui.utils.BaseTableLoader import BaseTableLoader  # type: ignore


class Selection(BaseTableLoader):
    def compose(self) -> ComposeResult:
        yield Static("To see selected lesson go to confirmation page", classes="m-1")
        yield Static("Select New Lesson", id="select_label")
        yield Input(placeholder="Lesson Code", id="lesson_code")
        yield Button(
            "Select Lesson", disabled=True, id="select_lesson", variant="primary"
        )
        yield Pretty("", classes="m-1", id="selection_errors")
        yield Static("Available Lessons", classes="m-1")
        yield DataTable(id="available", classes="m-1")

    @on(Input.Changed, "#lesson_code")
    def toggle_disable(self):
        input_box = self.query_one("#lesson_code", expect_type=Input)
        button = self.query_one("#select_lesson", expect_type=Button)
        if len(input_box.value):
            button.disabled = False
        else:
            button.disabled = True

    @on(Button.Pressed, "#select_lesson")
    def select_lesson(self):
        selection_service = LessonSelection()
        code = self.query_one("#lesson_code", expect_type=Input).value
        try:
            code = int(code)
            selection_service.select(self.user["id"], str(code))
            self.query_one("#selection_errors", expect_type=Pretty).update(
                "Lesson added successfully"
            )

        except ValueError:
            self.query_one("#selection_errors", expect_type=Pretty).update(
                "make sure entered code is a number"
            )
        except Exception as err:
            self.query_one("#selection_errors", expect_type=Pretty).update(str(err))

    def on_mount(self):
        table = self.query_one("#available", expect_type=DataTable)

        lesson_service = Lesson()
        all_lessons: List[dict[str, Any]] = lesson_service.all_lessons()  # type: ignore
        all = []
        for lesson in all_lessons:
            time_str = []
            for time in lesson["time"]:
                time_str.append(
                    "{} {} {}".format(time["week"], time["day"], time["hour"])
                )

            lesson["time"] = " - ".join(time_str)
            del lesson["id"]
            all.append(lesson.values())

        headers = lesson_service.headers
        headers.remove("time_id")
        headers.remove("id")
        headers.append("time")

        self.load_table(table, headers, all)
