import copy
from enum import Enum
from typing import List, Tuple
from tabulate import tabulate
from grammar import Grammar, SymbolType, GrammarFileParser, Prod

def parse_sequence(file):
    with open(file, 'r') as file:
        data = file.read().replace('\n', '')
    return data

class StateType(Enum):
    Q = "normal state"
    B = "back state"
    F = "final state (success)"
    E = "error state"

class Configuration(object):
    def __init__(self, state: StateType, pos: int, working_stack: List[object], input_stack: List[str]):
        self.state: StateType = state #
        self.pos = pos # position of current symbol in the sequence
        self.working_stack: List[object] = working_stack # alpha
        self.input_stack: List[str] = input_stack # beta

    def __str__(self):
        str_working_stack = ""
        for w in self.working_stack:
            if type(w) is str:
                str_working_stack += w
            else:
                str_working_stack += w.symbol + str(w.id + 1)
        str_input_stack = ""
        for w in self.input_stack[::-1]:
                str_input_stack += w

        if str_input_stack == "":
            str_input_stack = "eps"

        if str_working_stack == "":
            str_working_stack = "eps"
        return f"({self.state.name}, {self.pos+1}, {str_working_stack}, {str_input_stack})"

class RecursiveDescent(object):
    def __init__(self, grammar: Grammar):
        self.grammar = grammar

    def expand(self, config: Configuration):
        ntps = self.grammar.find_productions(config.input_stack[-1])
        config.input_stack.pop()
        A1 = ntps.prods[0]
        config.working_stack.append(A1)
        config.input_stack = A1.result + config.input_stack[::-1]
        config.input_stack = config.input_stack[::-1]

    def advance(self, config: Configuration):
        config.pos += 1
        config.working_stack += config.input_stack[-1]
        config.input_stack.pop()

    def momentary_insuccess(self, config: Configuration):
        config.state = StateType.B

    def back(self, config: Configuration):
        config.pos -= 1
        config.input_stack.append(config.working_stack[-1])
        config.working_stack.pop()

    def another_try(self, config: Configuration):
        last_prod: Prod = config.working_stack[-1]

        # undo the last production
        last_result = last_prod.result
        for i, item in enumerate(last_result):
            if item == config.input_stack[-1]:
                config.input_stack.pop()
            else:
                raise Exception("cannot undo the last operation")


        all_prods = grammar.find_productions(last_prod.symbol)
        config.working_stack.pop()
        if last_prod.id + 1 < len(all_prods.prods): # verify if there are no longer any productions
            config.working_stack.append(all_prods.prods[last_prod.id+1])
            A1 = config.working_stack[-1]
            config.input_stack = A1.result + config.input_stack[::-1]
            config.input_stack = config.input_stack[::-1]
            config.state = StateType.Q
        else: # tried all possibilities
            if last_prod.symbol == "S" and config.pos == 0:
                config.state = StateType.E
            else:
                config.input_stack.append(all_prods.symbol)

    def success(self, config: Configuration):
        config.state = StateType.F

    def parse(self, sequence, verbose=True):
        config = Configuration(StateType.Q, 0, [], ["S"])
        while config.state not in [StateType.F, StateType.E]:
            print(sequence[0:config.pos+1])
            if verbose:
                print(config)
            if config.state is StateType.Q:
                if config.pos == len(sequence) and len(config.input_stack) == 0:
                    self.success(config)
                else:
                    if len(config.input_stack) == 0:
                        self.momentary_insuccess(config)
                    else:
                        if SymbolType.is_terminal(config.input_stack[-1]):
                            self.expand(config)
                        else:
                            if config.pos < len(sequence) and config.input_stack[-1] == sequence[config.pos]:
                                self.advance(config)
                            else:
                                self.momentary_insuccess(config)
            elif config.state == StateType.B:
                if type(config.working_stack[-1]) is str:
                    self.back(config)
                else:
                    self.another_try(config)
        if verbose:
            print(config)
        if config.state is StateType.E:
            return config
        else:
            return config


class TreeConverter(object):
    def __init__(self):
        self.parsing_tree: List[Tuple[int,str,int,int]] = [] # index, info, parent, sibling
    def get_tree_recursive(self, working_stack, parent_idx):
        idx = len(self.parsing_tree) + 1
        left = 0
        indexes = []
        print(working_stack)
        prod: Prod = working_stack.pop(0)
        if type(prod) is not str:
            for s in prod.result:
                self.parsing_tree.append((idx, s, parent_idx, left))
                indexes.append(idx)
                left = idx
                idx += 1

            for i, s in enumerate(prod.result):
                if s.isupper():
                    self.get_tree_recursive(working_stack, indexes[i])
        else:
            self.get_tree_recursive(working_stack, parent_idx)

    def get_tree(self, working_stack):
        self.parsing_tree.append((1, "S", 0, 0))
        self.get_tree_recursive(working_stack, 1)
        return self.parsing_tree


grammar = GrammarFileParser().parse("g1.txt")
sequence = parse_sequence("input1.txt")
grammar.print_productions()
recursive_descent = RecursiveDescent(grammar)
final_config = recursive_descent.parse("acbc", verbose=False)
print(final_config)
if final_config.state == StateType.F:
    print("success. reached final state")
    print(tabulate(TreeConverter().get_tree(final_config.working_stack), ["idx", "info", "parent", "left"], tablefmt='orgtbl'))
else:
    print("error. sequence is not accepted")


