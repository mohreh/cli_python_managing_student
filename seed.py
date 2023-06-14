import os
from data.perofessor import perofessor_seed
from data.time import time_seed
from data.lesson import lesson_seed


def seed():
    try:
        os.remove("./tmp/lesson.csv")
        os.remove("./tmp/perofessor.csv")
        os.remove("./tmp/time.csv")
    except Exception:
        pass

    time_seed()
    lesson_seed()
    perofessor_seed()


seed()
