from data.data import Data
from data.financial import Financial
from data.selection import Selection
from data.student import Student


class QuitRequest(Data):
    def __init__(
        self,
    ):
        super().__init__("QuitRequest", ["req_text", "student_id"])

    def submit_quit_request(self, req_text: str, student_id: str):
        self.insert(
            {
                "req_text": req_text,
                "student_id": student_id,
            }
        )

        financial = Financial()
        selection = Selection()
        student = Student()

        financial.remove(student_id)
        selection.remove(student_id)
        student.update_data(student_id, study_status="quited")
