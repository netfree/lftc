from typing import List, Dict

from finite_automata_package.constants import SET_OF_STATES_KEYWORD, FINITE_ALPHABET_KEYWORD, TRANSITIONS_KEYWORD, INITIAL_STATE_KEYWORD, \
    FINAL_STATES_KEYWORD
from finite_automata_package.finite_automata import FiniteAutomata, State
from finite_automata_package.parser_exception import ParserException


class FiniteAutomataParser(object):
    @staticmethod
    def read_transition(line: str, line_number=0):
        try:
            p, a, q = line.split(" ")
            if a == "\"\"":
                a = " "
            return p, a, q
        except:
            raise ParserException(line_number, "cannot read transition")

    @staticmethod
    def from_file(path: str) -> FiniteAutomata:
        states: Dict[str, State] = {}
        alphabet: List[str] = []
        transitions: Dict[State, Dict[str, State]] = {}
        initial_state: State = None

        keywords = [SET_OF_STATES_KEYWORD, FINITE_ALPHABET_KEYWORD, TRANSITIONS_KEYWORD, INITIAL_STATE_KEYWORD,
                    FINAL_STATES_KEYWORD]
        last_keyword: str = ""

        line_number = 0

        with open(path) as f:
            for line in f:
                line_number += 1
                line = line.strip(" \n")
                if line == "":
                    continue
                if line in keywords:
                    last_keyword = line
                else:
                    if last_keyword == SET_OF_STATES_KEYWORD:
                        if line in states.keys():
                            raise ParserException(line_number, f"{line} state cannot be redeclared")
                        states[line] = State(line)
                        transitions[states[line]] = {}
                    elif last_keyword == FINITE_ALPHABET_KEYWORD:
                        if line in alphabet:
                            raise ParserException(line_number, f"{line} appears twice in {FINITE_ALPHABET_KEYWORD}")
                        alphabet.append(line)
                    elif last_keyword == TRANSITIONS_KEYWORD:
                        p, a, q = FiniteAutomataParser.read_transition(line, line_number)
                        try:
                            p, q = states[p], states[q]
                        except:
                            raise ParserException(line_number, "invalid states")
                        transitions[p][a] = q
                    elif last_keyword == INITIAL_STATE_KEYWORD:
                        if initial_state is not None:
                            raise ParserException(line_number, "too many initial states")
                        else:
                            try:
                                initial_state = states[line]
                            except:
                                raise ParserException(line_number, f"{line} is not a valid state")
                    elif last_keyword == FINAL_STATES_KEYWORD:
                        try:
                            states[line].final = True
                        except:
                            raise ParserException(line_number, f"{line} is not a valid state")

        if initial_state is None:
            raise ParserException(0, "no initial state was declared")

        return FiniteAutomata(states, alphabet, transitions, initial_state)