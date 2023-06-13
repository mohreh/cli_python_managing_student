import csv
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
