from enum import Enum
from time import localtime
from data.data import Data

ACT = Enum("ACT", ["ENTRY", "EXIT"])


class EntryExitTime(Data):
    def __init__(self):
        super().__init__("entry_exit_time", ["action", "time", "student_id"])

    def record(self, student_id: str, act: ACT):
        local_time = localtime()
        time_str = (
            "/".join(
                [
                    str(local_time.tm_year),
                    str(local_time.tm_mon),
                    str(local_time.tm_mday),
                ]
            )
            + "-"
            + ":".join(
                [
                    str(local_time.tm_hour),
                    str(local_time.tm_min),
                    str(local_time.tm_sec),
                ]
            )
        )
        self.insert({"action": act.name, "time": time_str, "student_id": student_id})

    def find_for_student_id(self, student_id: str):
        data = self.find_all(student_id=student_id)
        return data
