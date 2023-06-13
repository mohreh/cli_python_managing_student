from .data import Data


class Student(Data):
    def __init__(self):
        super().__init__(
            "students",
            [
                "first_name",
                "last_name",
                "student_code",
                "gender",
                "marital_status",
                "phone_number",
                "father_name",
                "mother_name",
                "national_code",
                "address",
                "admission",
                "college_name",
                "study_field",
                "study_status",
                "password",
                "username",
            ],
        )

    def login(self, data: dict[str, str]):
        self.insert(data)
