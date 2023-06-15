import typing

from data.financial import Financial
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

    def update_data(self, id: str, **kwargs):
        self.update_row("id", id, **kwargs)

    def find_with_id(self, id: str):
        data = self.find_all(id=id)
        if len(data):
            return data[0]
        else:
            return None

    def find(self, username: str) -> dict[str, typing.Any] | None:
        data = self.find_all(username=username)
        if len(data):
            return data[0]
        else:
            return None

    def login(self, username: str, password: str) -> dict[str, typing.Any] | None:
        user = self.find(username)
        if not user:
            return None
        elif user["password"] != password:
            raise Exception("password is incorrect")

        return user

    def sign_up(self, data: dict[str, str]):
        data["study_status"] = "studying"
        self.insert(data)

        financial = Financial()
        financial.insert_base_financial(data)
