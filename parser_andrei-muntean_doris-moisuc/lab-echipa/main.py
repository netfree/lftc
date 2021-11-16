from grammar import *

grammar = GrammarFileParser.parse("grammar.in")
grammar.print_terminals()
grammar.print_non_terminals()
grammar.print_productions()

