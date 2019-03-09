'''PlayerSkeletonA.py
The beginnings of an agent that might someday play Baroque Chess.

'''

from BC_state_etc import BC_state
import time
import copy
import math
import numpy as np
import random
import sys

DEPTH = 2
TIME = 1.0
ALPHA_BETA = 1
ZOBRIST_TABLE = np.zeros([8, 8, 12], dtype=int)
Y_BOARD = 8
X_BOARD = 8
NUM_PIECE = 12
WHITE_LIST = ["P", "L", "I", "W", "K", "C", "F"]
BLACK_LIST = ["p", "l", "i", "w", "k", "c", "f"]
# PIECE_LIST = ["P", "L", "I", "W", "K", "C", "F",
#              "p", "l", "i", "w", "k", "c", "f"]
PIECE_LIST = WHITE_LIST + BLACK_LIST
VISTED_BOARD = {}


class MY_BC_STATE(BC_state):
    def static_evalation(self, rule):
        evalu = 0
        if rule == 0:
            evalu = self.rule_0()
        return evalu

    def rule_0(self):
        sum = 0
        for i in range(Y_BOARD):
            for j in range(X_BOARD):
                piece = self.board[i][j]
                if piece in WHITE_LIST:
                    sum += 1
                if piece in BLACK_LIST:
                    sum -= 1
        return sum


def children_states(state, piece):
    children_list = []
    return children_list


def searcher(current, depth, time_limit, alpha_beta):
    time_limit = time.time() + time_limit * 0.9
    who = current.whose_turn
    new_who = 1 - who
    # if who == 1: who = True
    # else: who = False
    best_eval, new_position = minimax_a_b_search(current, -math.inf, math.inf, depth, 0, who, time_limit, alpha_beta)
    new_board = copy.deepcopy(current.board)
    if new_position is not None:
        new_board[new_position[0]][new_position[1]] = who
    # new_state = TTS_State(new_board, new_who)
    # new_state.__class__ = MY_TTS_State
    new_state = MY_BC_STATE(new_board, new_who)
    new_state.whose_move = new_who
    # print(new_position)
    return best_eval, new_state, new_position


# helper function for searcher
# return next move position, and its state evaluation
def minimax_a_b_search(current, a, b, depth, d, white, time_limit, a_b):
    global depth_count, state_count, eval_count, ab_count, my_side
    new_move = None
    depth_count = max(depth_count, d)  # update depth count
    children = children_states(current, white)
    if depth == d or len(children) == 0:  # base case
        eval_count += 1
        return current.static_eval(), new_move
    state_count += 1  # update state count

    if white:  # maximizer
        max_eval = -math.inf

        for child in children:

            if time.time() >= time_limit:
                if new_move is None:
                    new_move = children[child]
                break
            child_hash = board_hash_value(child.board)
            evalu = 0
            if child_hash not in VISTED_BOARD:
                evalu, _ = minimax_a_b_search(child, a, b, depth, d + 1, False, time_limit, a_b)
                VISTED_BOARD[child_hash] = evalu
                # print("evalu {}; max_eval {}".format(evalu, max_eval))
                # print("white {} d {}; child {}".format(white, d, child))
                # eval_count += 1  # update eval count
            else:
                evalu = VISTED_BOARD[child_hash]

            # evalu = recur_eval(children, child, new_move, a, b, depth, d, white, time_limit, a_b)
            if evalu > max_eval:  # update evaluation and returned state
                max_eval = evalu
                new_move = children[child]
                if time.time() >= time_limit:
                    break
                # print("it's a pick the value is " + str(max_eval))
            if a_b:
                a = max(a, evalu)  # update alpha
                if a >= b:
                    ab_count += 1  # update a_b_cut counter
                    break
        return max_eval, new_move
    else:  # minimizer
        min_eval = math.inf
        # children = children_states(current)
        for child in children:

            if time.time() >= time_limit:
                if new_move is None:
                    new_move = children[child]
                break
            child_hash = board_hash_value(child.board)
            evalu = 0
            if child_hash not in VISTED_BOARD:
                evalu, _ = minimax_a_b_search(child, a, b, depth, d + 1, True, time_limit, a_b)
                # eval_count += 1  # update eval count
                # print("evalu {}; min_eval{}".format(evalu, min_eval))
                # print("black {} d {}; child {}".format(white, d, child))
            else:
                evalu = VISTED_BOARD[child_hash]
            if evalu < min_eval:  # update evaluation and returned state
                min_eval = evalu
                new_move = children[child]
                if time.time() >= time_limit:
                    break

            # evalu = recur_eval(children, child, new_move, a, b, depth, d, white, time_limit, a_b)
            if a_b:
                b = min(b, evalu)
                if a >= b:
                    ab_count += 1  # update a_b_cut counter
                    break
        return min_eval, new_move

'''
def recur_eval(children, child, new_move, a, b, depth, d, white, time_limit, a_b):
    evalu = 0
    if time.time() >= time_limit:
        if new_move is None:
            new_move = children[child]
        return new_move
    child_hash = board_hash_value(child.board)
    evalu = 0
    if child_hash not in VISTED_BOARD:
        evalu, _ = minimax_a_b_search(child, a, b, depth, d + 1, white, time_limit, a_b)
        VISTED_BOARD[child_hash] = evalu
        # print("evalu {}; max_eval {}".format(evalu, max_eval))
        # print("white {} d {}; child {}".format(white, d, child))
        # eval_count += 1  # update eval count
    else:
        evalu = VISTED_BOARD[child_hash]
    return evalu
'''

def makeMove(currentState, currentRemark, timelimit):
    # Construct a representation of the move that goes from the
    # currentState to the newState.
    # Here is a placeholder in the right format but with made-up
    # numbers:
    best_eval, newState, move = searcher(currentState, DEPTH, TIME, ALPHA_BETA)
    # move = ((6, 4), (3, 4))

    # Make up a new remark
    newRemark = "I'll think harder in some future game. Here's my move"

    return [[move, newState], newRemark]


def nickname():
    return "Newman"


def introduce():
    return "I'm Newman Barry, a newbie Baroque Chess agent."


def prepare(player2Nickname):
    make_hash_table()
    pass


def piece_index(piece):
    for i in range(len(PIECE_LIST)):
        if piece == piece[i]:
            return i


# make a hash table that indicate the hash value for each piece laying on each grid
def make_hash_table():
    global ZOBRIST_TABLE
    for i in range(Y_BOARD):
        for j in range(X_BOARD):
            for k in range(NUM_PIECE):
                ZOBRIST_TABLE[i][j][k] = random.randint(0, 4294967296)  # might be changed "sys.maxsize"


# calucate the hash value for a given board
def board_hash_value(board):
    total_hash = 0
    for i in range(Y_BOARD):
        for j in range(X_BOARD):
            piece = board[i][j]
            if piece != '-':
                hash_piece = ZOBRIST_TABLE[i][j][piece_index(piece)]
                total_hash ^= hash_piece
    return total_hash

