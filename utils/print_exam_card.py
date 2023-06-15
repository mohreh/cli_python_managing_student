import webbrowser
from fpdf import FPDF
from tabulate import tabulate

from data.selection import Selection
from data.student import Student


def printـexam_card(student_id: str):
    selection = Selection()
    student = Student()

    user = student.find_with_id(student_id)
    selected_lessons = selection.all_selected_lessons(student_id)

    if not user:
        raise Exception("There is not any user with this id")

    if not selected_lessons or not len(selected_lessons):
        raise Exception("You have not yet select any lessons")

    headers = ["Lesson Name", "Credit", "Time", "Perofessor"]

    rows = []
    for lesson in selected_lessons:
        rows.append(
            [
                lesson["name"],
                lesson["credit"],
                lesson["time"],
                lesson["perofessor"],
            ]
        )

    with open("{}.pdf".format(user["username"]), "w") as f:
        f.write(
            "Name: {}\t Last Name: {}\n\n".format(user["first_name"], user["last_name"])
        )
        f.write(
            "Student Code: {}\t National Code: {}\n".format(
                user["student_code"], user["national_code"]
            )
        )
        f.write(
            "College Name: {}\t Study Field: {}\n".format(
                user["college_name"], user["study_field"]
            )
        )
        f.write("\n\n")
        f.write("Selected Lessons: \n")
        f.write(tabulate(rows, headers))

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Courier", size=9)

    with open("{}.pdf".format(user["username"]), "r") as f:
        text = f.read()
        for index, row in enumerate(text.split("\n")):
            pdf.cell(0, 0 + (index + 1) * 1, txt=row, ln=1)

    pdf.output("{}.pdf".format(user["username"]))
    webbrowser.open_new_tab("./{}.pdf".format(user["username"]))
