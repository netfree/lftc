from typing import List


class SymbolTable(object):
    def __init__(self, size):
        self.size = size
        self.hashmap: List[List[str]] = [[] for _ in range(size)]

    def hash_function(self, token: str):
        ascii_sum = sum(ord(char) for char in token)
        return ascii_sum % self.size

    def pos(self, token: str):
        position = self.hash_function(token)
        try:
            index = self.hashmap[position].index(token)
            return position, index
        except ValueError:
            self.hashmap[position].append(token)
            return position, len(self.hashmap[position]) - 1

    def __str__(self):
        s = ""
        for key, lst in enumerate(self.hashmap):
            if len(lst):
                s += f"key: {key}, values: {lst}\n"
        return s[:-1]


def test_symbol_table(st: SymbolTable, token: str):
    print(token, st.pos(token))


if __name__ == "__main__":
    st = SymbolTable(13)
    [test_symbol_table(st, token) for token in ["andrei", "ana", "mirela", "paul", "andrei", "ana", "istvan", "sergiu", "sergiu", "andrei"]]