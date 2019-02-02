'''BFS.py
by Chen Bai

Assignment 2, in CSE 415, Winter 2019.
1560405 chenb24
This file contains my implementation of bread-first search.
'''
import sys

if sys.argv == [''] or len(sys.argv) < 2:
    # import EightPuzzle as Problem
    #import TowersOfHanoi.TowersOfHanoi as Problem
    # import Missionaries.Missionaries as Problem
     import FarmerFox.chenb24_Farmer_Fox as Problem
else:
    import importlib

    Problem = importlib.import_module(sys.argv[1])

print("\nWelcome to BFS")
COUNT = None
BACKLINKS = {}


def runBFS():
    initial_state = Problem.CREATE_INITIAL_STATE()
    print("initial state is ")
    print(initial_state)
    global COUNT, BACKLINKS, MAX_OPEN_LENGTH
    COUNT = 0
    BACKLINKS = {}
    MAX_OPEN_LENGTH = 0
    BFS(initial_state)
    print(str(COUNT) + " states expanded.")
    print('MAX_OPEN_LENGTH = ' + str(MAX_OPEN_LENGTH))


def BFS(initial_state):
    global COUNT, BACKLINKS, MAX_OPEN_LENGTH

    # STEP 1: put the start state on the list OPEN
    OPEN = [initial_state]
    CLOSED = []
    BACKLINKS[initial_state] = None

    # STEP 2: if OPEN is empty, output DONE and stop
    while OPEN != []:
        report(OPEN, CLOSED, COUNT)
        if len(OPEN) > MAX_OPEN_LENGTH:
            MAX_OPEN_LENGTH = len(OPEN)

        # STEP 3:
        S = OPEN.pop(0)  # select the first element of open list and call it S and delete S from open list
        CLOSED.append(S)  # put S into closed list

        if Problem.GOAL_TEST(S):
            print(Problem.goal_message(S))  # output description
            path = backtrace(S)
            print('Length of solution path found: ' + str(len(path) - 1) + ' edges')
            return
        COUNT += 1

        # STEP 4: generate the list L of successors of S and delete from L those states already appearing on CLOSED
        L = []
        for op in Problem.OPERATORS:
            if op.precond(S):
                new_state = op.state_transf(S)
                if not (new_state in CLOSED) and not (new_state in OPEN):
                    L.append(new_state)
                    BACKLINKS[new_state] = S


        # Insert all members in L at the end of OPEN
        OPEN = OPEN + L
        print_state_list("OPEN", OPEN)


def print_state_list(name, lst):
    print(name + " is now: ", end='')
    for state in lst[:-1]:
        print(str(state), end=", ")
    print(str(lst[-1]))


def backtrace(s):
    global BACKLINKS
    path = []
    while s:
        path.append(s)
        s = BACKLINKS[s]
    path.reverse()
    print("Solution path: ")
    for s in path:
        print(s)
    return path


def report(open, closed, count):
    print("len(OPEN) = " + str(len(open)))
    print("len(CLOSED) = " + str(len(closed)))
    print("COUNT = " + str(count))


if __name__ == '__main__':
    runBFS()
