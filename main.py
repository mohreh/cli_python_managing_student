from typing import List
import time

from data.lesson import Lesson, lesson_seed
from data.selection import Selection
from ui.App import MainApp


if __name__ == "__main__":
    from data.time import time_seed

    from utils import get_fullname_and_student_number
    from utils.input import clear
    from ui import SingUp
    from data import student

    errors: List[str] = []

    while True:
        data = get_fullname_and_student_number(60, 14)
        if len(data["username"].split(" ")) > 1:
            errors.append("username must not contain spaces")

        try:
            user = student.login(data["username"], data["password"])
            if user is None and not data["password"].isdigit():
                errors.append(
                    """you are loging is for first time,
your password is your student code, and must be number"""
                )

            if len(errors) != 0:
                clear()

                for err in errors:
                    print(err)

                print("waiting 5 secons, you will be back to login page")
                time.sleep(5)
                continue

            if user is None:
                sign_up = SingUp()
                signup_data: dict[str, str] = sign_up.run()  # type: ignore

                signup_data.update(data)

                student.sign_up(signup_data)
            else:
                app = MainApp(user)
                app.run()
                break

        except Exception as err:
            clear()
            print(err)
            print("\n \nwaiting 5 secons, you will be back to login page")
            time.sleep(5)
