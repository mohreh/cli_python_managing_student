import csv
import shutil
from tempfile import NamedTemporaryFile
import typing


class Data:
    def __init__(self, name: str, headers: typing.List[str]):
        headers.insert(0, "id")

        self.filename = "./tmp/{}.csv".format(name)
        self.headers = headers

        with open(self.filename, "a") as f:
            writer = csv.DictWriter(f, fieldnames=self.headers)

            # write headers if file not exists before
            if not f.tell():
                writer.writeheader()

        self.length = len(list(csv.reader(open(self.filename)))) - 1

    def update_row(self, key_name: str, key_val: str, **update_kwargs):
        tempfile = NamedTemporaryFile(mode="w+t", delete=False)
        with open(self.filename, "r") as f, tempfile:
            reader = csv.DictReader(f)
            writer = csv.DictWriter(tempfile, fieldnames=self.headers)
            writer.writeheader()

            for row in reader:
                if row[key_name] == key_val:
                    for key, val in update_kwargs.items():
                        row[key] = val

                writer.writerow(row)

        shutil.move(tempfile.name, self.filename)

    def remove_row(self, key_name: str, key_val: str):
        tempfile = NamedTemporaryFile(mode="w+t", delete=False)
        with open(self.filename, "r") as f, tempfile:
            reader = csv.DictReader(f)
            writer = csv.DictWriter(tempfile, fieldnames=self.headers)
            writer.writeheader()

            for row in reader:
                if not row[key_name] == key_val:
                    writer.writerow(row)

        shutil.move(tempfile.name, self.filename)

    def insert(self, data: dict[str, typing.Any]):
        data["id"] = self.length + 1

        with open(self.filename, "a") as f:
            writer = csv.DictWriter(f, fieldnames=self.headers)
            writer.writerow(data)

        self.length += 1

    def find_all(self, **kwargs) -> typing.List[dict[str, typing.Any]]:
        results = []
        with open(self.filename, "r") as f:
            reader = csv.DictReader(f, delimiter=",")
            for row in reader:
                for key, val in kwargs.items():
                    if row[key] == val:
                        results.append(row)

        return results
