from typing import Any, List
from rich.console import RenderableType  # type: ignore
from textual import on  # type: ignore
from textual.app import ComposeResult  # type: ignore
from textual.widgets import Button, DataTable, Input, Pretty, Static  # type: ignore


from data.lesson import Lesson
from data.selection import Selection as LessonSelection


class Selection(Static):
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
        yield Static("To see selected lesson go to confirmation page", classes="m-1")
        yield Pretty([], classes="m-1", id="selection_errors")
        yield Static("Select New Lesson", id="select_label")
        yield Input(placeholder="Lesson Code", id="lesson_code")
        yield Button(
            "Select Lesson", disabled=True, id="select_lesson", variant="primary"
        )
        yield Static("Available Courses")
        yield DataTable(id="available")

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
            r = selection_service.select(self.user["id"], str(code))
            self.query_one("#selection_errors", expect_type=Pretty).update(r)

        except ValueError:
            self.query_one("#selection_errors", expect_type=Pretty).update(
                "make sure entered code in a number"
            )
        except Exception as err:
            self.query_one("#selection_errors", expect_type=Pretty).update(str(err))

    def on_mount(self):
        table = self.query_one("#available", expect_type=DataTable)

        lesson_service = Lesson()
        all_lessons: List[dict[str, Any]] = lesson_service.all_lessons()
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

        table.add_columns(*headers)
        table.add_rows(all)
        table.cursor_type = "row"
        table.zebra_stripes = True
