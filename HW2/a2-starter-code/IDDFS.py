'''IDDFS.py
by Chen Bai

Assignment 2, in CSE 415, Winter 2019.
1560405 chenb24
This file contains my implementation of Iterative Deepening Depth First Search.
'''
import sys

if sys.argv == [''] or len(sys.argv) < 2:
    # import EightPuzzle as Problem
    # import FarmerFox.chenb24_Farmer_Fox as Problem
    # import Missionaries.Missionaries as Problem
     import TowersOfHanoi.TowersOfHanoi as Problem

else:
    import importlib

    Problem = importlib.import_module(sys.argv[1])

print("\nWelcome to IDDFS")
COUNT = None
CLOSED = []
BACKLINKS = {}


def runIDDFS():
    initial_state = Problem.CREATE_INITIAL_STATE()
    print("initial state is ")
    # print(initial_state)
    global COUNT, CLOSED, BACKLINKS, MAX_OPEN_LENGTH
    COUNT = 0
    BACKLINKS = {}
    CLOSED = []
    MAX_OPEN_LENGTH = 0
    max_depth = 50
    if IDDFS(initial_state, max_depth):
        print(str(COUNT) + " states expanded.")
        # print('MAX_OPEN_LENGTH = ' + str(MAX_OPEN_LENGTH))
    else:
        print("Target not reachable!")


def IDDFS(initial_state, max_depth):
    global COUNT, BACKLINKS, CLOSED, MAX_OPEN_LENGTH
    OPEN = [initial_state]
    BACKLINKS[initial_state] = None
    for i in range(max_depth):
        if DLS(initial_state, i):
            return True
        CLOSED = []
    return False


def DLS(S, max_depth):
    global COUNT, BACKLINKS, CLOSED, MAX_OPEN_LENGTH
    print("This state is: " + str(S))

    if S not in CLOSED:
        CLOSED.append(S)  # put S into closed list
        if Problem.GOAL_TEST(S):
            print(Problem.goal_message(S))  # output description
            path = backtrace(S)
            print('Length of solution path found: ' + str(len(path) - 1) + ' edges')
            return True

        if max_depth <= 0:
            return False
        else:
            COUNT += 1

            for op in Problem.OPERATORS:
                if op.precond(S):
                    new_state = op.state_transf(S)
                    if new_state not in BACKLINKS:
                        BACKLINKS[new_state] = S
                    temp = DLS(new_state, max_depth - 1)
                    if temp:
                        return True
    return False


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
    runIDDFS()
