from .input import Input


def get_fullname_and_student_number(width: int, height: int) -> tuple[str, str, str]:
    input = Input(
        width,
        height,
        fullname="Enter your fullname first",
        password="Enter your student_code/password then",
        username="Enter your username then",
    )

    input.lisenter.start()
    input.lisenter.join()

    return (input.fullname, input.password, input.username)  # type: ignore
