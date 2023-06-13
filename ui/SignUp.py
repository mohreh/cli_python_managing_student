from textual import on  # type: ignore
from textual.app import App, ComposeResult  # type: ignore
from textual.containers import Container, VerticalScroll  # type: ignore
from textual.validation import Number  # type: ignore
from textual.widgets import (  # type: ignore
    Button,
    Header,
    Input,
    Label,
    Checkbox,
    OptionList,
    Pretty,
    Select,
)


class SingUp(App):
    CSS_PATH = "style/signup.css"

    def compose(self) -> ComposeResult:
        yield Header(name="Sign up")
        with Container():
            with VerticalScroll():
                yield Label("First Name", name="First Name")
                yield Input(placeholder="First Name", id="first_name")

                yield Label("Last Name", name="Last Name")
                yield Input(placeholder="Last Name", id="last_name")

                yield Label("Student Code", name="Student Code")
                yield Input(
                    placeholder="Student Code",
                    id="student_code",
                    validators=Number(),
                )
                yield Pretty([], id="student_code_result")

                yield Label("National Code", name="National Code")
                yield Input(
                    placeholder="National Code",
                    id="national_code",
                    validators=Number(),
                )
                yield Pretty([], id="national_code_result")

                yield Label("gender", name="gender")
                gender = ["Male", "Female"]
                yield Select(((line, line) for line in gender), id="gender")

                yield Label("Phone Number", name="Phone Number")
                yield Input(
                    placeholder="Phone Number",
                    id="phone_number",
                    validators=Number(),
                )
                yield Pretty([], id="phone_number_result")

                yield Label("Address", name="Address")
                yield Input(placeholder="Address", id="address")

                yield Label("College Name", name="College Name")
                yield Input(placeholder="College Name", id="college_name")

                yield Label("Study Field", name="Study Field")
                yield Input(placeholder="Study Field", id="study_field")

                yield Label("Admission", name="Admission")
                admission = ["Shabane", "Rouzane"]
                yield Select(((line, line) for line in admission), id="admission")

                yield Label("Father Name", name="Father Name")
                yield Input(placeholder="Father Name", id="father_name")

                yield Label("Mother Name", name="Mother Name")
                yield Input(placeholder="Mother Name", id="mother_name")

                yield Checkbox(label="Are you married?", id="marital_status")

                yield Button("Sign up", variant="primary", id="signup")

    def on_button_pressed(self, _: Button.Pressed):
        data = {}

        for nput in list(self.query(Input)):
            data[nput.id] = nput.value

        for nput in list(self.query(Select)):
            data[nput.id] = nput.value

        marital_status = self.query_one(Checkbox)
        data[marital_status.id] = marital_status.value

        self.exit(data)

    @on(Input.Changed)
    def show_invalid_reasons(self, event: Input.Changed) -> None:
        if event.input.id:
            if event.validation_result and not event.validation_result.is_valid:
                self.query_one(
                    "#" + event.input.id + "_result", expect_type=Pretty
                ).update(event.validation_result.failure_descriptions)
            elif event.validation_result and event.validation_result.is_valid:
                self.query_one(
                    "#" + event.input.id + "_result", expect_type=Pretty
                ).update([])
