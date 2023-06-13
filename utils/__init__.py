from .input import Input


def get_fullname_and_student_number(width: int, height: int) -> dict[str, str]:
    input = Input(
        width,
        height,
        fullname="Enter your fullname first",
        username="Enter your username then",
        password="Enter your student_code/password then",
    )

    input.lisenter.start()
    input.lisenter.join()

    return {
        # "fullname": input.fullname,  # type: ignore
        "password": input.password,  # type: ignore
        "username": input.username,  # type: ignore
    }
