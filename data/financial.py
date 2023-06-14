import csv
import shutil
from tempfile import NamedTemporaryFile
import typing
from data.data import Data


class Financial(Data):
    def __init__(self):
        super().__init__("financial", ["student_id", "inventory", "debt"])

    def update_financial(self, student_id: str, **kwargs):
        tempfile = NamedTemporaryFile(mode="w+t", delete=False)
        with open(self.filename, "r") as f, tempfile:
            reader = csv.DictReader(f)
            writer = csv.DictWriter(tempfile, fieldnames=self.headers)
            writer.writeheader()

            for row in reader:
                if row["student_id"] == student_id:
                    new_row = {}
                    for key, val in kwargs.items():
                        new_row[key] = val
                    new_row["student_id"] = row["student_id"]

                    writer.writerow(new_row)

        shutil.move(tempfile.name, self.filename)

    def increase_inventory(self, student_id: str, amount: int):
        self.update_financial(student_id, inventory=amount)

    def find(self, student_id):
        data = self.find_all(student_id=student_id)
        if len(data):
            return data[0]
        return None

    def insert_base_financial(self, student_id: str):
        data = self.find(student_id)
        if data:
            raise Exception("This user already has data")

        self.insert({"student_id": student_id, "inventory": 0, "debt": 0})

    def remove_financial_data(self, student_id: str):
        pass

    def debt(self, student_id: str):
        data = self.find(student_id)
        if not data:
            raise Exception("There is no financial data for this user")
        self.update_financial(
            student_id, inventory=int(data["inventory"]) - int(data["debt"])
        )
