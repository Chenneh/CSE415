'''chenb24_EightPuzzleWithManhattan.py by Chen Bai(chenb24, 1560405)
EightPuzzle game with Hamming heuristic.
Modified from starter code FranceWithDXHeuristic.py
    Version 0.2, January 30, 2019.
    Chen Bai, Univ. of Washington.
    Electronic and Computer Engineering.
This file augments EightPuzzle.py with heuristic information,
so that it can be used by an A* implementation.
The particular heuristic is the sum of total difference of x and y coordinate, or
"Manhattan heuristic".

'''

from EightPuzzle import *


def h(s):
    '''Manhattan heuristic function'''
    b = s.b
    h_total = 0
    # print("len b is " + str(len(b)))
    # print("len b[i] is " + str(len(b[0])))
    for i in range(len(b)):
        for j in range(len(b[i])):
            current = b[i][j]
            if current != 0:
                i_dest = int(current / len(b))
                j_dest = current % len(b[i])
                d_i = abs(i - i_dest)
                d_j = abs(j - j_dest)
                h_total += (d_i + d_j)
    return h_total
