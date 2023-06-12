from .input import Input


def get_fullname_and_student_number(width: int, height: int):
    fullname = "Enter your fullname first"
    student_code = "Enter your student_code then"

    input = Input(width, height, fullname, student_code)

    input.lisenter.start()
    input.lisenter.join()

    return (input.fullname, input.student_code)
