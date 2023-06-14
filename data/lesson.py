import csv
import typing
from ast import literal_eval
from data.data import Data
from random import randint

from data.time import LESSON_TIME, WEEK, WEEK_DAYS, Time


class Lesson(Data):
    def __init__(self):
        # time_id is a tuple
        super().__init__("lesson", ["name", "code", "time_id", "credit"])

    def insert_many(self, data: typing.List[dict[str, typing.Any]]):
        for d in data:
            self.insert(d)

    def all_lessons(self):
        time = Time()
        all = []
        with open(self.filename, "r") as f:
            reader = csv.DictReader(f, fieldnames=self.headers)
            for row in reader:
                row["time"] = []
                for time_id in literal_eval(row["time_id"]):
                    lesson_time = time.find_with_id(time_id)
                    row["time"].append(lesson_time)
                all.append(all)
        return all

    def find(self, code: str):
        lesson = self.find_all(code=code)
        if len(lesson):
            return lesson[0]
        return None

    def check_for_conflict(
        self,
        lesson: dict[str, typing.Any],
        with_lessons: typing.List[dict[str, typing.Any]],
    ):
        result = []
        time = Time()
        for time_id in literal_eval(lesson["time_id"]):
            lesson_time = time.find_with_id(str(time_id))

            for other in with_lessons:
                print(other["name"])
                for time_id_ in literal_eval(other["time_id"]):
                    other_time = time.find_with_id(str(time_id_))
                    if lesson_time["hour"] == other_time["hour"]:
                        if lesson_time["day"] == other_time["day"]:
                            if (
                                lesson_time["week"] == WEEK.ALL.name
                                or other_time["week"] == WEEK.ALL.name
                            ) or lesson_time["week"] == other_time["week"]:
                                result.append(other)
        return result


def lesson_seed():
    lesson = Lesson()
    time = Time()

    lesson.insert_many(
        [
            # insert PHYSICS 1
            {
                "name": "PHYSICS 1",
                "code": randint(100, 999),
                "time_id": [
                    time.find(
                        WEEK.ALL.name,
                        WEEK_DAYS.SATURDAY.name,
                        LESSON_TIME["8AM-10AM"].name,
                    ),
                    time.find(
                        WEEK.EVEN.name,
                        WEEK_DAYS.SUNDAY.name,
                        LESSON_TIME["2PM-4PM"].name,
                    ),
                ],
                "credit": 3,
            },
            # insert PHYSICS 2, PHYSICS 1 and 2 has confilicts
            {
                "name": "PHYSICS 2",
                "code": randint(100, 999),
                "time_id": [
                    time.find(
                        WEEK.ALL.name,
                        WEEK_DAYS.SATURDAY.name,
                        LESSON_TIME["10AM-12PM"].name,
                    ),
                    time.find(
                        WEEK.EVEN.name,
                        WEEK_DAYS.SUNDAY.name,
                        LESSON_TIME["2PM-4PM"].name,
                    ),
                ],
                "credit": 3,
            },
            # insert data structure
            {
                "name": "DATA STRUCTURE",
                "code": randint(100, 999),
                "time_id": [
                    time.find(
                        WEEK.ALL.name,
                        WEEK_DAYS.TUESDAY.name,
                        LESSON_TIME["10AM-12PM"].name,
                    ),
                    time.find(
                        WEEK.ALL.name,
                        WEEK_DAYS.WEDNESDAY.name,
                        LESSON_TIME["2PM-4PM"].name,
                    ),
                ],
                "credit": 4,
            },
            # insert ALGORITHMS
            {
                "name": "ALGORITHMS",
                "code": randint(100, 999),
                "time_id": [
                    time.find(
                        WEEK.ALL.name,
                        WEEK_DAYS.SATURDAY.name,
                        LESSON_TIME["8AM-10AM"].name,
                    ),
                    time.find(
                        WEEK.ODD.name,
                        WEEK_DAYS.SATURDAY.name,
                        LESSON_TIME["2PM-4PM"].name,
                    ),
                ],
                "credit": 3,
            },
            # insert OS, OS and ALGORITHMS has confilicts
            {
                "name": "ALGORITHMS",
                "code": randint(100, 999),
                "time_id": [
                    time.find(
                        WEEK.ALL.name,
                        WEEK_DAYS.WEDNESDAY.name,
                        LESSON_TIME["8AM-10AM"].name,
                    ),
                    time.find(
                        WEEK.ODD.name,
                        WEEK_DAYS.MONDAY.name,
                        LESSON_TIME["2PM-4PM"].name,
                    ),
                ],
                "credit": 3,
            },
            # insert Compiler
            {
                "name": "COMPILER",
                "code": randint(100, 999),
                "time_id": [
                    time.find(
                        WEEK.ALL.name,
                        WEEK_DAYS.SATURDAY.name,
                        LESSON_TIME["2PM-4PM"].name,
                    ),
                ],
                "credit": 2,
            },
            # insert Network
            {
                "name": "NETWORK",
                "code": randint(100, 999),
                "time_id": [
                    time.find(
                        WEEK.ALL.name,
                        WEEK_DAYS.TUESDAY.name,
                        LESSON_TIME["10AM-12PM"].name,
                    ),
                    time.find(
                        WEEK.ALL.name,
                        WEEK_DAYS.WEDNESDAY.name,
                        LESSON_TIME["10AM-12PM"].name,
                    ),
                ],
                "credit": 4,
            },
        ]
    )
