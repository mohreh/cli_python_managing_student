from enum import Enum
from pynput.keyboard import Listener, Key
import os


Action = Enum("Action", ["INSERT", "COMPLETE"])


class Input:
    action: Action = Action.INSERT
    word = ""

    def __init__(self, width: int, height: int, **kwargs) -> None:
        self.lisenter = Listener(on_release=self.on_release)

        self.width = width
        self.height = height

        # self.fullname = fullname
        # self.student_code = student_code
        self.__dict__.update(kwargs)
        self.to_input = list(kwargs.keys())

        self.hits = 0

        print_star_input_box(self.width, self.height, **kwargs)

    def on_release(self, key):
        if key == Key.enter:
            self.action = Action.COMPLETE
        elif key == Key.backspace:
            self.word = self.word[:-1]
        elif key == Key.space:
            self.word = self.word + " "
        else:
            self.word = self.word + "{}".format(key)[1:2]

        if self.action == Action.COMPLETE and self.hits == len(self.to_input) - 1:
            return False

        for index, key in enumerate(self.to_input):
            if self.hits == index:
                self.__dict__[key] = self.word
                if self.action == Action.COMPLETE:
                    self.hits += 1
                    self.word = ""
                    self.__dict__[self.to_input[self.hits]] = self.word
                    self.action = Action.INSERT

        values = []
        for key in self.to_input:
            values.append(self.__dict__[key])

        print_star_input_box(
            self.width, self.height, **dict(zip(self.to_input, values))
        )


def clear():
    os.system("cls" if os.name == "nt" else "clear")


def print_star_input_box(width: int, height: int, **kwargs):
    clear()
    print("*" * width)

    for _ in range(int(height / 2 - 1)):
        print("*" + " " * (width - 2) + "*")

    for val in kwargs.values():
        print(
            "*"
            + " " * (int(width / 2 - 1) - int(len(val) / 2))
            + val
            + " "
            * (int(width / 2 - 1) - int(len(val) / 2) - (1 if len(val) % 2 == 1 else 0))
            + "*"
        )

    for _ in range(int(height / 2 - 1)):
        print("*" + " " * (width - 2) + "*")

    print("*" * width)
