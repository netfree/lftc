from typing import List


class State(object):
    def __init__(self, name: str):
        self.name = name


class Transition(object):
    def __init__(self, source: State, destination: State, value: str):
        self.source = source
        self.destination = destination
        self.value = value


class FiniteAutomata(object):
    def __init__(self, q: list[State], sigma: List[str], delta: List[Transition], q0: State):
        self.q: List[State] = q
        self.sigma: List[str] = sigma
        self.delta: List[Transition] = delta
        self.q0: State = q0