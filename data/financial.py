from data.data import Data


class Financial(Data):
    def __init__(self):
        super().__init__("financial", ["student_id", "inventory", "debt"])
