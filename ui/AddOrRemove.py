from textual import on  # type: ignore
from textual.app import ComposeResult  # type: ignore
from textual.widgets import Button, Input, Pretty, Static  # type: ignore

from data.selection import Selection as LessonSelection
from ui.utils.Base import Base  # type: ignore


class AddOrRemove(Base):
    def compose(self) -> ComposeResult:
        yield Static(
            "After you add or remove a lesson go to Confirmation tab and press reload",
            classes="m-1",
        )
        yield Pretty("", id="add_remove_errors", classes="m-1")
        yield Input(placeholder="lesson code to select", id="add_lesson_code")
        yield Button("Select Lesson", id="add_lesson", disabled=True, variant="primary")

        yield Input(placeholder="lesson code to remove", id="remove_lesson_code")
        yield Button(
            "Remove Lesson", id="remove_lesson", disabled=True, variant="warning"
        )

    @on(Input.Changed, "#add_lesson_code")
    def toggle_disable_add(self):
        input_box = self.query_one("#add_lesson_code", expect_type=Input)
        button = self.query_one("#add_lesson", expect_type=Button)

        if len(input_box.value):
            button.disabled = False
        else:
            button.disabled = True

    @on(Input.Changed, "#remove_lesson_code")
    def toggle_disable_remove(self):
        input_box = self.query_one("#remove_lesson_code", expect_type=Input)
        button = self.query_one("#remove_lesson", expect_type=Button)

        if len(input_box.value):
            button.disabled = False
        else:
            button.disabled = True

    @on(Button.Pressed, "#add_lesson")
    def add_lesson(self):
        selection_service = LessonSelection()
        code = self.query_one("#add_lesson_code", expect_type=Input).value
        try:
            code = int(code)
            selection_service.select(self.user["id"], str(code))
            self.query_one("#add_remove_errors", expect_type=Pretty).update(
                "Lesson added successfully"
            )

        except ValueError:
            self.query_one("#add_remove_errors", expect_type=Pretty).update(
                "make sure entered code is a number"
            )
        except Exception as err:
            self.query_one("#add_remove_errors", expect_type=Pretty).update(str(err))

    @on(Button.Pressed, "#remove_lesson")
    def remove_lesson(self):
        selection_service = LessonSelection()
        code = self.query_one("#remove_lesson_code", expect_type=Input).value
        try:
            code = int(code)
            selection_service.remove_selected_lesson(self.user["id"], str(code))
            self.query_one("#add_remove_errors", expect_type=Pretty).update(
                "Lesson removed successfully"
            )

        except ValueError:
            self.query_one("#add_remove_errors", expect_type=Pretty).update(
                "make sure entered code in a number"
            )
        except Exception as err:
            self.query_one("#add_remove_errors", expect_type=Pretty).update(str(err))
