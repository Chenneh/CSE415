'''chenb24_EightPuzzleWithHamming.py by Chen Bai(chenb24, 1560405)
EightPuzzle game with Hamming heuristic.
Modified from starter code FranceWithDXHeuristic.py
    Version 0.2, January 30, 2019.
    Chen Bai, Univ. of Washington.
    Electronic and Computer Engineering.
This file augments EightPuzzle.py with heuristic information,
so that it can be used by an A* implementation.
The particular heuristic is total number misplaced grids, or
"Hamming heuristic".

'''

from EightPuzzle import *


def h(s):
    '''Hamming heuristic function'''
    b = s.b
    h_total = 0
    for i in range(len(b)):
        for j in range(len(b[i])):
            current = b[i][j]
            if current != 0:
                i_dest = int(current / 3)
                j_dest = current % 3
                d_i = abs(i - i_dest)
                d_j = abs(j - j_dest)
                if d_i != 0 or d_j != 0:
                    h_total += 1
    return h_total
