from ast import literal_eval
import typing

from data.data import Data
from data.lesson import Lesson
from data.student import Student
from utils.error import ConfilictError


class Selection(Data):
    def __init__(self):
        super().__init__("selection", ["student_id", "lesson_ids"])

    def find_with_student_id(self, student_id: str):
        data = self.find_all(student_id=student_id)
        if len(data):
            return data[0]
        return None

    def remove_selected_lesson(self, student_id: str, lesson_id: str):
        data = self.find_with_student_id(student_id)
        if not data:
            raise Exception("There is not data for student")

        lesson_ids: typing.List[str] = literal_eval(data["lesson_ids"])

        if lesson_id not in lesson_ids:
            raise Exception(
                "You have not selected lesson with code {}".format(lesson_id)
            )
        lesson_ids.remove(lesson_id)

        self.update_selection(data["student_id"], lesson_ids)

    def remove(self, student_id: str):
        self.remove_row("student_id", student_id)

    def update_selection(self, student_id: str, lesson_ids: typing.List[str]):
        self.update_row("student_id", student_id, lesson_ids=lesson_ids)

    def select(self, student_id: str, new_lesson_code: str):
        student = Student()
        user = student.find_with_id(student_id)
        if not user:
            raise Exception("There is not any student with this id")

        if user["study_status"] == "quited":
            raise Exception(
                "You have quited studying and can't have financial information"
            )

        lesson = Lesson()

        new_lesson = lesson.find(new_lesson_code)
        if not new_lesson:
            raise Exception(
                "there is not any lesson with code: {}".format(new_lesson_code)
            )

        other_lessons = []

        data = self.find_with_student_id(student_id)
        if not data:
            self.insert({"student_id": student_id, "lesson_ids": [new_lesson["code"]]})
            return

        for lesson_code in literal_eval(data["lesson_ids"]):
            other_lessons.append(lesson.find(lesson_code))

        conflicts = lesson.check_for_conflict(new_lesson, other_lessons)
        if len(conflicts):
            error = "{} has conflict with {}".format(
                new_lesson["name"],
                ", ".join(conflict["name"] for conflict in conflicts),
            )
            raise ConfilictError(error)

        other_lessons.append(new_lesson)

        self.update_selection(
            data["student_id"],
            lesson_ids=[lesson["code"] for lesson in other_lessons],
        )
