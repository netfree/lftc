from typing import Tuple, List

from constants import RESERVED_WORDS, OPERATORS, SEPARATORS, IDENTIFIER_FA_FILE, INTEGER_FA_FILE, BOOLEAN_FA_FILE, \
    CHAR_FA_FILE, STRING_FA_FILE
from exceptions.lexical_error import LexicalError
from finite_automata_package.finite_automata_parser import FiniteAutomataParser
from program_internal_form import ProgramInternalForm
from symbol_table import SymbolTable


class ScannerParams(object):
    def __init__(self):
        self.st_size = 13


class Scanner(object):
    def __init__(self, params=ScannerParams()):
        self.params = params
        self.identifier_fa = FiniteAutomataParser.from_file(IDENTIFIER_FA_FILE)
        self.integer_fa = FiniteAutomataParser.from_file(INTEGER_FA_FILE)
        self.boolean_fa = FiniteAutomataParser.from_file(BOOLEAN_FA_FILE)
        self.char_fa = FiniteAutomataParser.from_file(CHAR_FA_FILE)
        self.string_fa = FiniteAutomataParser.from_file(STRING_FA_FILE)


    @staticmethod
    def advanced_splitting(token: str) -> List[str]:
        all_separators = SEPARATORS + OPERATORS
        rosetta_stone = {}
        answer = []
        all_separators.sort(key=lambda x: len(x))
        for separator in all_separators:
            positions = [i for i in range(len(token)) if token.startswith(separator, i)]
            for position in positions:
                rosetta_stone[position] = len(separator)
        i = 0
        acumulator = ""
        while i < len(token):
            if i in rosetta_stone.keys():
                if len(acumulator):
                    answer.append(acumulator)
                    acumulator = ""
                answer.append(token[i:i + rosetta_stone[i]])
                i += rosetta_stone[i]
            else:
                acumulator += token[i]
                i += 1
        if len(acumulator):
            answer.append(acumulator)
        return answer

    @staticmethod
    def accumulate_constants(line_number, line, constant_separators=("\"", "\'")) -> List[Tuple[bool, str]]:
        answer = []
        acumulator = ""
        i = 0
        while i < len(line):
            if line[i] in constant_separators:
                separator = line[i]
                if len(acumulator):
                    answer.append((False, acumulator))
                acumulator = f"{line[i]}"
                mda = True
                while mda:
                    i += 1

                    if i == len(line):
                        print(answer)
                        raise LexicalError(line_number, f"could not find ending for separator {separator}")

                    acumulator += line[i]

                    if line[i] == separator:
                        answer.append((True, acumulator))
                        acumulator = ""
                        mda = False
                i += 1
            else:
                acumulator += line[i]
                i += 1
        if len(acumulator):
            answer.append((False, acumulator))
        return answer

    @staticmethod
    def detect_tokens(line_number, line) -> List[str]:
        ans = []
        parts = Scanner.accumulate_constants(line_number, line)
        for part in parts:
            if part[0] is True:
                ans.append(part[1])
            else:
                for token in part[1].split():
                    tokens = Scanner.advanced_splitting(token)
                    ans = ans + tokens
        return ans

    def is_identifier(self, token) -> bool:
        return self.identifier_fa.accept_sequence(token)

    def is_constant(self, token) -> bool:
        return self.integer_fa.accept_sequence(token) or \
               self.boolean_fa.accept_sequence(token) or \
               self.char_fa.accept_sequence(token) or \
               self.string_fa.accept_sequence(token)

    def scan(self, file) -> Tuple[ProgramInternalForm, SymbolTable]:
        st = SymbolTable(self.params.st_size)
        pif = ProgramInternalForm()

        with open(file) as f:
            lines = f.readlines()
            for line_number, line in enumerate(lines):
                try:
                    tokens = self.detect_tokens(line_number, line)
                except LexicalError as le:
                    raise LexicalError(line_number + 1, le.get_additional_info())
                for token in tokens:
                    if token in RESERVED_WORDS + OPERATORS + SEPARATORS:
                        pif.add(token, (-1, -1))
                    elif self.is_identifier(token):
                        idx = st.pos(token)
                        pif.add("id", idx)
                    elif self.is_constant(token):
                        idx = st.pos(token)
                        pif.add("const", idx)
                    else:
                        raise LexicalError(line_number + 1, f"\"{token}\" is not a valid identifier or constant")
        return pif, st


class ScannerTest(object):
    def __init__(self, scanner: Scanner):
        self.scanner = scanner

    def test_constant(self):
        assert self.scanner.is_constant("+12")
        assert self.scanner.is_constant("-10")
        assert self.scanner.is_constant("0")
        assert self.scanner.is_constant("\"ubbcluj\"")
        assert self.scanner.is_constant("\"ub00luj\"")
        assert self.scanner.is_constant("\"ub%(*^%(^)(&^$luj\"")
        assert self.scanner.is_constant("True")
        assert self.scanner.is_constant("False")

        assert not self.scanner.is_constant("qFalse")
        assert not self.scanner.is_constant("Falsew")
        assert not self.scanner.is_constant("+1w2")
        assert not self.scanner.is_constant("w12")
        assert not self.scanner.is_constant("12q")
        print("constants tests passed")

    def test_identifier(self):
        assert self.scanner.is_identifier("__ana12")
        assert self.scanner.is_identifier("__ana12ana")

        assert not self.scanner.is_identifier("1ana")
        assert not self.scanner.is_identifier("#na")
        assert not self.scanner.is_identifier("n#a")
        print("identifer tests passed")

    def test_all(self):
        self.test_constant()
        self.test_identifier()


scanner = Scanner()
scanner_test = ScannerTest(scanner)
scanner_test.test_all()