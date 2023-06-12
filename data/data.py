import csv
import typing


class Data:
    def __init__(self, name: str, headers: list):
        headers.insert(0, "id")

        self.filename = "./tmp/{}.csv".format(name)
        self.headers = headers

        with open(self.filename, "a") as f:
            writer = csv.DictWriter(f, fieldnames=self.headers)

            # write headers if file not exists before
            if not f.tell():
                writer.writeheader()

        self.length = len(list(csv.reader(open(self.filename)))) - 1

    def insert(self, data: dict[str, typing.Any]):
        data["id"] = self.length + 1

        with open(self.filename, "a") as f:
            writer = csv.DictWriter(f, fieldnames=self.headers)
            writer.writerow(data)

        self.length += 1
