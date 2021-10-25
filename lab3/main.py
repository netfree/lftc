from argparse import ArgumentParser

from exceptions.lexical_error import LexicalError
from program_internal_form import ProgramInternalForm
from scanner import Scanner
from symbol_table import SymbolTable


def parse():
    parser = ArgumentParser()
    parser.add_argument("-input", "--input", required=True, help="Input file for scanning")
    parser.add_argument("-outputSt", "--outputSt", required=True, help="Output file for Symbol Table")
    parser.add_argument("-outputPif", "--outputPif", required=True, help="Output file for Program Internal Form")
    args = parser.parse_args()
    return args

def print_helper(pif, st, pif_file, st_file):
    # pif
    f = open(pif_file, "w")
    f.write(str(pif))
    f.close()

    # st
    f = open(st_file, "w")
    f.write(str(st))
    f.close()

if __name__ == '__main__':
    args = parse()
    scanner = Scanner()
    try:
        pif, st = scanner.scan(args.input)
    except LexicalError as e:
        print(f"A lexical error was detected at line: {e.get_line()}")
        print(f"Additional info: {e.get_additional_info()}")
    else:
        print("Lexically correct")
        print_helper(pif, st, args.outputPif, args.outputSt)
