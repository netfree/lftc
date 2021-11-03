from typing import List

from constants import SET_OF_STATES_KEYWORD, FINITE_ALPHABET_KEYWORD, TRANSITIONS_KEYWORD, INITIAL_STATE_KEYWORD
from finite_automata import FiniteAutomata, State, Transition


class FiniteAutomataParser(object):
    @staticmethod
    def from_file(path: str) -> FiniteAutomata:
        q: List[State] = []
        sigma: List[str] = []
        delta: List[Transition] = []
        q0: State = None

        keywords = [SET_OF_STATES_KEYWORD, FINITE_ALPHABET_KEYWORD, TRANSITIONS_KEYWORD, INITIAL_STATE_KEYWORD]
        last_keyword: str = ""

        with open(path) as f:
            for line in f:
                print(line)

        return FiniteAutomata(q, sigma, delta, q0)
