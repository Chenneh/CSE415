# <METADATA>
QUIET_VERSION = "0.2"
PROBLEM_NAME = "Eight Puzzle"
PROBLEM_VERSION = "0.2"
PROBLEM_AUTHORS = ['S. Tanimoto']
PROBLEM_CREATION_DATE = "8-JAN-2018"
PROBLEM_DESC = \
    '''This formulation of the Eight Puzzle uses generic
Python 3 constructs and has been tested with Python 3.6.
It is designed to work according to the QUIET2 tools interface.
'''
import numpy as np
import random
faces = ['F', 'B', 'U', 'D', 'L', 'R']

class State:
    def __init__(self, b):
        self.b = b

    def __eq__(self, s2):
        for i in range(6):
            for j in range(2):
                for k in range(2):
                    if self.b[i][j][k] != s2.b[i][j][k]:
                        return False
        return True

    def __str__(self):
        return str(self.b)

    def __hash__(self):
        return (self.__str__()).__hash__()

    def copy(self):
        # Performs an appropriately deep copy of a state,
        # for use by operators in creating new states.
        news = State({})
        news.b = [row[:] for row in self.b]
        return news

    def find_void_location(self):
        '''Return the (vi, vj) coordinates of the void.
    vi is the row index of the void, and vj is its column index.'''
        for i in range(3):
            for j in range(3):
                if self.b[i][j] == 0:
                    return (i, j)
        raise Exception("No void location in state: " + str(self))

    def can_move(self, dir):
        return True

    def move(self, dir):
        news = self.copy()  # start with a deep copy.
        b = news.b
        if dir == 'F':
            b[0] = rotate(0, b)
        if dir == 'B':
            b[1] = rotate(1, b)
        if dir == 'U':
            b[2] = rotate(2, b)
        if dir == 'D':
            b[3] = rotate(3, b)
        if dir == 'L':
            b[4] = rotate(4, b)
        if dir == 'R':
            b[5] = rotate(5, b)

        return news  # return new state

    def edge_distance(self, s2):
        return 1.0  # Warning, this is only correct when
        # self and s2 are neighboring states.
        # We assume that is the case.  This method is
        # provided so that problems having all move costs equal to
        # don't have to be handled as a special case in the algorithms.


def goal_test(s):
    goal = np.array([[[i] * 2] * 2 for i in range(6)])
    return s == State(goal)


def goal_message(s):
    return "All faces are set. Great!"


class Operator:
    def __init__(self, name, precond, state_transf):
        self.name = name
        self.precond = precond
        self.state_transf = state_transf

    def is_applicable(self, s):
        return self.precond(s)

    def apply(self, s):
        return self.state_transf(s)


faces = ['F', 'B', 'U', 'D', 'L', 'R']
# even: no + 1
# odd: no -1
f_b = [2, 5, 3, 4]
l_r = [2, 1, 3, 0]
u_d = [1, 5, 0, 4]
f_to_change = {0: f_b, 1: f_b, 4: l_r, 5: l_r, 2: u_d, 3: u_d}
# s_to_change = {}


def odd(i):
    return i % 2


def zero_one(i):
    if i == 1:
        return 0
    elif i == 0:
        return 1


def rotate(dir, cube):
    new_cube = cube.copy()
    new_cube_re = cube.copy()
    f = new_cube[dir]
    p_0 = f[0][0]
    p_1 = f[0][1]
    p_2 = f[1][0]
    p_3 = f[1][1]
    main_face = np.array([[p_0, p_1], [p_2, p_3]])
    new_cube_re[dir] = main_face
    faces_r = f_to_change[dir]
    n = odd(dir)
    for i in range(4):
        if i == 0:
            new_face = new_cube[faces_r[0]].copy()
            n_come = zero_one(n)
            face_come = new_cube[faces_r[3]].copy
            for j in range(2):
                new_face[n][j] = face_come[j][n_come]
            new_cube_re[0] = new_face
        else:
            new_face = new_cube[faces_r[i]].copy()
            face_come = new_cube[faces_r[i - 1]].copy()
            for j in range(2):
                if odd(i):
                    new_face[j][n] = face_come[n][j]
                else:
                    new_face[n][j] = face_come[j][n]
            new_cube_re[i] = new_face
    return new_cube_re


init_state_list = [[[0, 1]] * 2,
                   [[2, 3]] * 2,
                   [[4, 5]] * 2,
                   [[1, 0]] * 2,
                   [[3, 2]] * 2,
                   [[5, 4]] * 2]
init_state_list = np.array(init_state_list)
CREATE_INITIAL_STATE = lambda: State(init_state_list)
# </INITIAL_STATE>

# <OPERATORS>

OPERATORS = [Operator("Move a tile " + str(dir) + " into the void",
                      lambda s, dir1=dir: s.can_move(dir1),
                      # The default value construct is needed
                      # here to capture the value of dir
                      # in each iteration of the list comp. iteration.
                      lambda s, dir1=dir: s.move(dir1))
             for dir in faces]
# </OPERATORS>

# <GOAL_TEST> (optional)
GOAL_TEST = lambda s: goal_test(s)
# </GOAL_TEST>

# <GOAL_MESSAGE_FUNCTION> (optional)
GOAL_MESSAGE_FUNCTION = lambda s: goal_message(s)
# </GOAL_MESSAGE_FUNCTION>


# goal = [[[i] * 2] * 2 for i in range(6)]
# goal = np.array(goal)
# test = np.array([[0]*2]*2)
# print(test)