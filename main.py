if __name__ == "__main__":
    from utils import get_fullname_and_student_number
    from ui import SingUp
    from data import student

    data = get_fullname_and_student_number(60, 14)

    sign_up = SingUp()
    signup_data: dict[str, str] = sign_up.run()  # type: ignore
    sign_up.__dict__.update(data)
    student.login(signup_data)
