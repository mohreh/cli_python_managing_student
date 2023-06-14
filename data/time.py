import csv
from enum import Enum
from data.data import Data


class Time(Data):
    def __init__(self):
        # week is all, even or odd
        super().__init__("time", ["week", "day", "hour"])

    def find(self, week: str, day: str, hour: str):
        with open(self.filename, "r") as f:
            reader = csv.DictReader(f, delimiter=",")
            for row in reader:
                if row["week"] == week and row["day"] == day and row["hour"] == hour:
                    return int(row["id"])
        return None

    def find_with_id(self, id: str):
        time = self.find_all(id=id)
        return time[0]


WEEK = Enum("WEEK", ["ALL", "EVEN", "ODD"])

WEEK_DAYS = Enum(
    "DAYS",
    [
        "SATURDAY",
        "SUNDAY",
        "MONDAY",
        "TUESDAY",
        "WEDNESDAY",
    ],
)

LESSON_TIME = Enum("HOUR", ["8AM-10AM", "10AM-12PM", "2PM-4PM", "4PM-6PM"])


# for insert datas manually
def time_seed() -> None:
    time = Time()
    time_data = {}
    for day in WEEK_DAYS:
        time_data["day"] = day.name
        for week in WEEK:
            time_data["week"] = week.name
            for hour in LESSON_TIME:
                time_data["hour"] = hour.name
                time.insert(time_data)
