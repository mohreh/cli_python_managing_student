from ast import literal_eval
from tempfile import NamedTemporaryFile
import shutil
import csv
import typing

from data.data import Data
from data.lesson import Lesson
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
        data: dict[str, typing.Any] = self.find_with_student_id(student_id)  # type: ignore

        lesson_ids: typing.List[str] = literal_eval(data["lesson_ids"])

        if lesson_id not in lesson_ids:
            raise Exception(
                "You have not selected lesson with code {}".format(lesson_id)
            )
        lesson_ids.remove(lesson_id)

        self.update_selection(data["student_id"], lesson_ids)

    def update_selection(self, student_id: str, lesson_ids: typing.List[str]):
        tempfile = NamedTemporaryFile(mode="w+t", delete=False)
        with open(self.filename, "r") as f, tempfile:
            reader = csv.DictReader(f)
            writer = csv.DictWriter(tempfile, fieldnames=self.headers)
            writer.writeheader()

            for row in reader:
                if row["student_id"] == student_id:
                    new_row = {
                        "id": row["id"],
                        "student_id": row["student_id"],
                        "lesson_ids": lesson_ids,
                    }
                    writer.writerow(new_row)

        shutil.move(tempfile.name, self.filename)

    def select(self, student_id: str, new_lesson_code: str):
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
            conflicts_names = ""
            for conflict in conflicts:
                conflicts_names += ", " + conflict["name"]

            error = "{} has conflict with {}".format(
                new_lesson["name"], conflicts_names
            )
            raise ConfilictError(error)

        other_lessons.append(new_lesson)

        self.update_selection(
            data["student_id"],
            lesson_ids=[lesson["code"] for lesson in other_lessons],
        )
