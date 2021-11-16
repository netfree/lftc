from typing import List


class Production:
    def __init__(self, starting_symbol, productions):
        self.starting_symbol: Terminal = starting_symbol
        self.productions: List[List[object]] = productions

    def __str__(self):
        s = f"{str(self.starting_symbol)} -> "
        for i, production in enumerate(self.productions):
            for p in production:
                s += str(p)
            if i != len(self.productions) - 1:
                s += " | "
        return s

class NonTerminal:
    def __init__(self, name):
        self.name = name
    def __str__(self):
        return str(self.name)

class Terminal:
    def __init__(self, name: str):
        self.name = name

    def __str__(self):
        return str(self.name)

class Grammar(object):
    def __init__(self, terminals, non_terminals, productions):
        self.terminals: List[str] = terminals
        self.non_terminals: List[str] = non_terminals
        self.productions: List[Production] = productions

    def print_terminals(self):
        print("terminals: ")
        s = ""
        for ter in self.terminals:
            s += str(ter) + " "
        print(s)

    def print_non_terminals(self):
        print("nonterminals: ")
        s = ""
        for ter in self.non_terminals:
            s += str(ter) + " "
        print(s)

    def print_productions(self):
        print("productions:")
        for p in self.productions:
            print(str(p))

    def check_context_free_grammar(self):
        for production in self.productions:
            if not production.starting_symbol.name.isupper():
                return False
        return True


class GrammarFileParser(object):
    @staticmethod
    def parse(path: str) -> Grammar:
        terminals: List[str] = []
        non_terminals: List[str] = []
        productions: List[Production] = []

        line_number = 0

        with open(path) as f:
            for line in f:
                line_number += 1
                line = line.strip(" \n")

                if line_number == 1:
                    non_terminals = line.split()
                if line_number == 2:
                    terminals = line.split()
                else: # inseamna ca e production
                    splitted = line.split("=>")
                    if len(splitted) != 2:
                        continue
                    starting_symbol, prod = splitted[0], splitted[1]
                    if len(starting_symbol):
                        print()
                    starting_symbol = starting_symbol.strip(" \n")
                    pds = [p.strip(" \n") for p in prod.split("|")]

                    all_prods = []

                    for p in pds:
                        l = []
                        symbols = p.split(" ")
                        symbols = [s.strip(" ") for s in symbols]
                        for s in symbols:
                            if s.isupper():
                                l.append(NonTerminal(s))
                            else:
                                l.append(Terminal(s))
                        all_prods.append(l)

                    productions.append(Production(NonTerminal(starting_symbol), all_prods))

        return Grammar(terminals, non_terminals, productions)


grammar = GrammarFileParser.parse("grammar.in")
grammar.print_terminals()
grammar.print_non_terminals()
grammar.print_productions()



