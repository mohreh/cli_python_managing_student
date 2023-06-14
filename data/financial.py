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
                    for key, val in kwargs.items():
                        row[key] = val

                writer.writerow(row)

        shutil.move(tempfile.name, self.filename)

    def increase_inventory(self, student_id: str, amount: int):
        data = self.find(student_id)
        if not data:
            raise Exception("There is no financial data for this user")

        data["inventory"] = str(int(data["inventory"]) + amount)
        self.update_financial(student_id, inventory=data["inventory"])

        return data

    def find(self, student_id: str):
        data = self.find_all(student_id=student_id)
        if len(data):
            return data[0]
        return None

    def insert_base_financial(self, student_id: str):
        data = self.find(student_id)
        if data:
            raise Exception("This user already has data")

        data = {"student_id": student_id, "inventory": 0, "debt": 10}
        self.insert(data)
        return data

    def remove_financial_data(self, student_id: str):
        pass

    def checkout(self, student_id: str):
        data = self.find(student_id)
        if not data:
            raise Exception("There is no financial data for this user")

        if int(data["inventory"]) < int(data["debt"]):
            raise Exception(
                "You have not enough money in your account to checkout your debt"
            )

        data["inventory"] = int(data["inventory"]) - int(data["debt"])
        data["debt"] = 0

        self.update_financial(
            student_id, inventory=data["inventory"], debt=data["debt"]
        )

        return data
