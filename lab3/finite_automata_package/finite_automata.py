from typing import List, Dict, Tuple


class State(object):
    def __init__(self, name: str):
        self.name = name
        self.final: bool = False


class FiniteAutomata(object):
    def __init__(self, states: Dict[str, State], alphabet: List[str], transitions: Dict[State, Dict[str, State]],
                 initial_state: State):
        self.states: Dict[str, State] = states
        self.alphabet: List[str] = alphabet
        self.transitions: Dict[State, Dict[str, State]] = transitions
        self.initial_state: State = initial_state

    def accept_sequence(self, seq: str):
        current_state = self.initial_state
        for letter in seq:
            if letter in self.transitions[current_state].keys():
                current_state = self.transitions[current_state][letter]
            else:
                return False
        if current_state.final:
            return True
        return False

    def initial_state_to_string(self):
        return f"q0 = {self.initial_state.name}"

    def states_to_string(self):
        s = "Q = {"
        for i, state_name in enumerate(self.states.keys()):
            s += state_name
            if i == len(self.states.keys()) - 1:
                s += "}"
            else:
                s += ", "
        return s

    def alphabet_to_string(self):
        s = "Σ = {"
        for i, letter in enumerate(self.alphabet):
            s += letter
            if i == len(self.alphabet) - 1:
                s += "}"
            else:
                s += ", "
        return s

    def final_states_to_string(self):
        final_states = list(filter(lambda x: x[1].final is True, self.states.items()))
        s = "F = {"
        for i, state_name in enumerate(final_states):
            s += state_name[0]
            if i == len(final_states) - 1:
                s += "}"
            else:
                s += ", "
        return s

    def transitions_to_string(self):
        s = ""
        for t in self.transitions.items():
            s1, dict = t
            for item in dict.items():
                s += f"δ({s1.name}, {item[0]}) = {item[1].name}\n"
        return s[:-1]


