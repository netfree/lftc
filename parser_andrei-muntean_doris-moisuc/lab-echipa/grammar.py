from typing import List, Dict


class SymbolType(object):
    @staticmethod
    def is_terminal(s: str) -> bool:
        return s.isupper()

    @staticmethod
    def is_non_terminal(s: str) -> bool:
        return not s.isupper()

class Prod(object):
    def __init__(self, id: int, symbol: str, result: List[str]):
        self.id = id
        self.symbol = symbol
        self.result = result

    def __str__(self):
        return self.symbol + str(self.id)

    def __repr__(self):
        return self.__str__()
class NonTerminalProductions(object):
    def __init__(self, symbol, prods: List[Prod]):
        self.symbol = symbol
        self.prods = prods

class Grammar(object):
    def __init__(self, terminals, non_terminals, productions):
        self.terminals: List[str] = terminals
        self.non_terminals: List[str] = non_terminals
        self.non_terminal_productions: Dict[str, NonTerminalProductions] = productions # Dict[symbol, productions]

    def find_productions(self, symbol: str):
        return self.non_terminal_productions[symbol]

    def print_terminals(self):
        print("\nTerminals: ")
        s = ""
        for ter in self.terminals:
            s += str(ter) + " "
        print(s)

    def print_non_terminals(self):
        print("\nNonterminals: ")
        s = ""
        for ter in self.non_terminals:
            s += str(ter) + " "
        print(s)

    def print_productions(self):
        print("\nProductions:")
        for symbol, non_terminal_productions in self.non_terminal_productions.items():
            s = f"{symbol} -> "
            for i, prod in enumerate(non_terminal_productions.prods):
                for p in prod.result:
                    s += str(p)
                if i != len(non_terminal_productions.prods) - 1:
                    s += " | "
            print(s)


    def check_context_free_grammar(self):
        for key, ntps in self.non_terminal_productions.items():
            if not SymbolType.is_terminal(key):
                return False
        return True


class GrammarFileParser(object):
    @staticmethod
    def parse(path: str) -> Grammar:
        terminals: List[str] = []
        non_terminals: List[str] = []
        productions: Dict[str, NonTerminalProductions] = {}

        line_number = 0

        with open(path) as f:
            for line in f:
                line_number += 1
                line = line.strip(" \n")

                if line_number == 1:
                    non_terminals = line.split()
                if line_number == 2:
                    terminals = line.split()
                else:
                    splitted = line.split("=>")
                    if len(splitted) != 2:
                        continue
                    starting_symbol, prod = splitted[0], splitted[1]
                    starting_symbol = starting_symbol.strip(" \n")
                    # if starting_symbol != starting_symbol.strip(" ")[0]:
                    #     raise Exception("the grammar is not context free")
                    pds = [p.strip(" \n") for p in prod.split("|")]

                    mda = []

                    for id, p in enumerate(pds):
                        l = []
                        if p == "\" \"":
                            mda.append(Prod(id, starting_symbol, [" "]))
                            continue
                        if p == "\"eps\"":
                            mda.append(Prod(id, starting_symbol, [""]))
                            continue
                        symbols = p.split(" ")
                        symbols = [s.strip(" ") for s in symbols]
                        mda.append(Prod(id, starting_symbol, symbols))
                    productions[starting_symbol] = NonTerminalProductions(starting_symbol, mda)

        return Grammar(terminals, non_terminals, productions)

