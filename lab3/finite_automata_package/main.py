from finite_automata_package.constants import bcolors
from finite_automata_parser import FiniteAutomataParser

if __name__ == '__main__':
    finite_automata = FiniteAutomataParser.from_file("FA.in")

    not_exit = True
    while not_exit:
        print("0. Display all\n" +
              "1. Display set of states\n" +
              "2. Display alphabet\n" +
              "3. Display all the transitions\n" +
              "4. Display the set of final states\n" +
              "5. For a DFA, verify if a sequence is accepted by the FA\n" +
              "6. Exit")
        choice = input("Please input a number: ")
        if choice == "0":
            print("M = (Q,Σ,δ,q0,F)")
            print(finite_automata.states_to_string())
            print(finite_automata.alphabet_to_string())
            print(finite_automata.transitions_to_string())
            print(finite_automata.initial_state_to_string())
            print(finite_automata.final_states_to_string())
        elif choice == "1":
            print(finite_automata.initial_state_to_string())
            print(finite_automata.states_to_string())
        elif choice == "2":
            print(finite_automata.alphabet_to_string())
        elif choice == "3":
            print(finite_automata.transitions_to_string())
        elif choice == "4":
            print(finite_automata.final_states_to_string())
        elif choice == "5":
            seq = input("Please give sequence: ")
            if finite_automata.accept_sequence(seq):
                print(f"{bcolors.OKGREEN}sequence '{seq}' is accepted{bcolors.ENDC}")
            else:
                print(f"{bcolors.FAIL}sequence '{seq}' is NOT accepted{bcolors.ENDC}")
        elif choice == "6":
            print("Goodbye")
            not_exit = False
        else:
            print("Invalid choice")
