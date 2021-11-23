from grammar import *

grammar = GrammarFileParser.parse("g1.txt")
grammar.print_terminals()
grammar.print_non_terminals()
grammar.print_productions()
