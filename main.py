from typing import List
import time
from data import entry_exit_time
from data.entry_exit_time import ACT

from data.lesson import Lesson, lesson_seed
from data.selection import Selection
from ui.App import MainApp


if __name__ == "__main__":
    from data.time import time_seed

    from utils import get_fullname_and_student_number
    from utils.input import clear
    from ui import SingUp
    from data import student
    from data.entry_exit_time import EntryExitTime

    errors: List[str] = []

    while True:
        entry_exit = EntryExitTime()

        if len(errors) != 0:
            clear()

            for err in errors:
                print(err)

            print("\n waiting 5 secons, you will be back to login page")
            time.sleep(5)
            errors = []

        data = get_fullname_and_student_number(60, 14)
        if len(data["username"].split(" ")) > 1:
            errors.append("username must not contain spaces")

        try:
            user = student.login(data["username"], data["password"])
            if user is None and (
                not data["password"].isdigit() or len(data["password"]) < 7
            ):
                errors.append(
                    """you are loging is for first time,
your password is your student code, and must be number"""
                )
                continue

            if user is None:
                sign_up = SingUp()
                signup_data: dict[str, str] = sign_up.run()  # type: ignore

                signup_data.update(data)

                student.sign_up(signup_data)
                user = student.login(signup_data["username"], signup_data["password"])
                if user:
                    app = MainApp(user)
                    entry_exit.record(user["id"], ACT.ENTRY)
                    app.run()
                    entry_exit.record(user["id"], ACT.EXIT)
                    break
                else:
                    errors.append("something wrong happened.")
                    errors.append(str(user))
                    continue
            else:
                app = MainApp(user)
                entry_exit.record(user["id"], ACT.ENTRY)
                app.run()
                entry_exit.record(user["id"], ACT.EXIT)
                break

        except Exception as err:
            clear()
            print(err)
            print("\n \nwaiting 5 secons, you will be back to login page")
            time.sleep(5)
