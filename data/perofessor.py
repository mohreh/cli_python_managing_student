from data.data import Data


class Perofessor(Data):
    def __init__(self):
        super().__init__("perofessor", ["name"])

    def find(self, id: str):
        data = self.find_all(id=id)
        if not len(data):
            return None

        return data[0]


def perofessor_seed():
    prof_service = Perofessor()
    for i in range(10):
        prof_service.insert({"name": "teacher_{}".format(i)})
