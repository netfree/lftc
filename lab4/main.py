from finite_automata import FiniteAutomata
from finite_automata_parser import FiniteAutomataParser

if __name__ == '__main__':
    finite_automata = FiniteAutomataParser.from_file("FA.in")

    not_exit = True
    while not_exit:
        print("1. Display all FA properties\n" +
              "2. Verify sequence\n" +
              "3. Exit")
        choice = input("Please input a number: ")
        if choice == "1":
            pass
        elif choice == "2":
            pass
        elif choice == "3":
            print("Goodbye")
            not_exit = False
        else:
            print("Invalid choice")
