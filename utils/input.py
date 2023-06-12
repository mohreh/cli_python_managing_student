from enum import Enum
from pynput.keyboard import Listener, Key
import os


Action = Enum("Action", ["DELETE", "INSERT", "COMPLETE"])


class Input:
    action: Action = Action.INSERT
    word = ""

    def __init__(
        self, width: int, height: int, fullname: str, student_code: str
    ) -> None:
        self.lisenter = Listener(on_release=self.on_release)
        self.width = width
        self.height = height
        self.fullname = fullname
        self.student_code = student_code
        self.complete_hits = 0

        print_star_input_box(self.width, self.height, self.fullname, self.student_code)

    def on_press(self, key):
        pass

    def on_release(self, key):
        if key == Key.enter:
            self.action = Action.COMPLETE
        elif key == Key.backspace:
            self.word = self.word[:-1]
        elif key == Key.space:
            self.word = self.word + " "
        else:
            self.word = self.word + "{}".format(key)[1:2]

        if self.complete_hits == 0:
            self.fullname = self.word
            if self.action == Action.COMPLETE:
                self.complete_hits = 1
                self.word = ""
                self.student_code = self.word
                self.action = Action.INSERT
        else:
            self.student_code = self.word
            if self.action == Action.COMPLETE:
                self.lisenter.stop()

        print_star_input_box(self.width, self.height, self.fullname, self.student_code)


def clear():
    os.system("cls" if os.name == "nt" else "clear")


def print_star_input_box(width: int, height: int, fullname, student_code):
    clear()
    print("*" * width)

    for _ in range(int(height / 2 - 1)):
        print("*" + " " * (width - 2) + "*")

    print(
        "*"
        + " " * (int(width / 2 - 1) - int(len(fullname) / 2))
        + fullname
        + " "
        * (
            int(width / 2 - 1)
            - int(len(fullname) / 2)
            - (1 if len(fullname) % 2 == 1 else 0)
        )
        + "*"
    )

    print(
        "*"
        + " " * (int(width / 2 - 1) - int(len(student_code) / 2))
        + student_code
        + " "
        * (
            int(width / 2 - 1)
            - int(len(student_code) / 2)
            - (1 if len(student_code) % 2 == 1 else 0)
        )
        + "*"
    )

    for _ in range(int(height / 2 - 1)):
        print("*" + " " * (width - 2) + "*")

    print("*" * width)
