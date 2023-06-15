from typing import Any, List
import time


def run_app(user: dict[str, Any]):
    from ui.App import MainApp
    from data.student import Student

    result = None
    student = Student()

    while True:
        if result:
            if result["message"] == "refresh":
                user = student.login(result["username"], result["password"]) or user
                result["message"] = "exit"
            else:
                break

        app = MainApp(user)
        result = app.run()
        if result is None:
            result = {"message": "exit"}


if __name__ == "__main__":
    from data.entry_exit_time import ACT
    from utils import get_fullname_and_student_number
    from utils.input import clear
    from ui import SingUp
    from data.student import Student
    from data.entry_exit_time import EntryExitTime

    student = Student()

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
                sign_up = SingUp(data["password"])
                signup_data: dict[str, str] = sign_up.run()  # type: ignore

                signup_data.update(data)

                student.sign_up(signup_data)
                user = student.login(signup_data["username"], signup_data["password"])
                if user:
                    entry_exit.record(user["id"], ACT.ENTRY)
                    run_app(user)
                    entry_exit.record(user["id"], ACT.EXIT)
                    break
                else:
                    errors.append("something wrong happened.")
                    errors.append(str(user))
                    continue
            else:
                entry_exit.record(user["id"], ACT.ENTRY)
                run_app(user)
                entry_exit.record(user["id"], ACT.EXIT)
                break

        except Exception as err:
            clear()
            print(err)
            print("\n \nwaiting 5 secons, you will be back to login page")
            time.sleep(5)
