from typing import Tuple


class ProgramInternalForm(object):
    def __init__(self):
        self.pif = []

    def add(self, token: str, pos: Tuple[int, int]):
        self.pif.append((token, pos))

    def __str__(self):
        s = ""
        for item in self.pif:
            s += str(item) + "\n"
        return s[:-1]
