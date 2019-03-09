from TTS_State import TTS_State
import random
import time
import copy
import Gold_Rush_Game_Type as Game

INIT = \
    [['W', 'W', ' ', 'B'],
     [' ', ' ', ' ', '-'],
     ['-', ' ', ' ', ' '],
     [' ', ' ', ' ', 'B']]
K = 4
STATE = None
my_side = 'W'
op_side = 'B'
OPPONENT = ''
USE_CUSTOM_STATIC_EVAL_FUNCTION = False
MAX_DEPTH_REACHED = 0
CURRENT_STATE_DYNAMIC_VAL = 0
USE_DEFAULT_MOVE = False
num_expand = 0
num_eval = 0
max_depth = 0
num_cutoff = 0
start_time = None
table = {}
count_op = 0
global_w = 0
global_b = 0
last_move = (0, 0)
utterances = ["Nice move, but mine's better!", "That's not so smart bro!", "Here you go"]
bad_utterances = ["Oh wow! That was nice!", "Great Move! But mine's gonna be better!", "I am still gonna win"]


class MY_TTS_State(TTS_State):

    def static_eval(self):
        if USE_CUSTOM_STATIC_EVAL_FUNCTION:
            return self.custom_static_eval()
        else:
            return self.basic_static_eval()

    def basic_static_eval(self):
        board = self.board
        H = len(board)  # height of board = num. of rows
        W = len(board[0])  # width of board = num. of cols.
        count_w = 0
        count_b = 0
        for i in range(H):
            for j in range(W):
                count_w += self.basic_helper(board, (i, j), 'W')
                count_b += self.basic_helper(board, (i, j), 'B')
        return count_w - count_b

    def custom_static_eval(self):
        global global_b, global_w, count_op
        board = self.copy().board
        score = 0
        H = len(board)  # height of board = num. of rows
        W = len(board[0])  # width of board = num. of cols.
        for i in range(H):
            for j in range(W):
                position = (i, j)
                score += self.custom_helper(board, position)
        if my_side == 'W':
            count_op = global_b
        elif my_side == 'B':
            count_op = global_w
        return score

    def basic_helper(self, board, position, side):
        px, py = position
        H = len(board)  # height of board = num. of rows
        W = len(board[0])  # width of board = num. of cols.
        directions = [(1, -1), (1, 0), (1, 1), (0, 1)]  # SW, S, SE, E
        total_count = 0
        for d in directions:
            dx = d[0]
            dy = d[1]
            count = 0
            i = px
            j = py
            for step in range(K - 1):
                i += dx
                if i < 0 or i >= H: i = ((i + H) % H)  # toroidal wrap
                j += dy
                if j < 0 or j >= W: j = ((j + W) % W)  # toroidal wrap
                if board[i][j] == '-':
                    break
                elif board[i][j] == side:
                    count += 1
            if count == 2: total_count += 1
        return total_count

    def custom_helper(self, board, position):
        global count_op, global_w, global_b
        score = 0
        count_w = 0
        count_b = 0
        px, py = position
        directions = [(1, -1), (1, 0), (1, 1), (0, 1)]  # SW, S, SE, E
        H = len(board)  # height of board = num. of rows
        W = len(board[0])  # width of board = num. of cols.
        for d in directions:
            dx = d[0]
            dy = d[1]
            i = px
            j = py
            prev = board[i][j]
            for step in range(K - 1):
                i += dx
                if i < 0 or i >= H:
                    i = ((i + H) % H)  # toroidal wrap
                j += dy
                if j < 0 or j >= W:
                    j = ((j + W) % W)  # toroidal wrap
                curr = board[i][j]
                if board[i][j] == '-':
                    score = score - 50  # deduct more if a block is closer
                elif curr == 'W':
                    score += 5
                    if curr == prev:
                        count_w += 1  # increment more if white is closer
                elif curr == 'B':
                    score -= 5
                    if curr == prev:
                        count_b += 1  # increment more if white is closer
                prev = curr
        score += 10 * count_w ** 4 - 10 * count_b ** 4
        global_w += count_w
        global_b += count_b
        return score


def get_ready(initial_state, k, what_side_i_play, opponent_moniker):
    global STATE, K, my_side, op_side, OPPONENT
    STATE = initial_state
    K = k
    my_side = what_side_i_play
    if my_side == 'W':
        op_side = 'B'
    else:
        op_side = 'W'
    OPPONENT = opponent_moniker


def who_am_i():
    return " I am a very talented player which smacks every opponent away"


def moniker():
    return 'smart peppa'


def take_turn(current_state, opponents_utterance, time_limit=10):
    # Compute the new state for a move.
    # Start by copying the current state.
    global count_op, last_move

    new_state = MY_TTS_State(current_state.board)
    l = parameterized_minimax(current_state=current_state, max_ply=2,
                              use_iterative_deepening=True,
                              use_default_move_ordering=True,
                              alpha_beta=True,
                              timed=True,
                              time_limit=time_limit,
                              use_custom_static_eval_function=True)

    best_val = l[0]
    new_state = table[best_val]
    # Fix up whose turn it will be.
    who = current_state.whose_turn
    new_who = 'B'
    if who == 'B': new_who = 'W'
    new_state.whose_turn = new_who

    board = current_state.board
    move = None

    for i in range(len(board)):
        for j in range(len(board[0])):
            if new_state.board[i][j] != board[i][j]:
                move = (i, j)
    if move == None: return [[False, current_state], "I don't have any moves!"]

    last_move = move

    print(count_op)
    new_utterance = random.choice(utterances)
    if count_op > 30000:
        new_utterance = random.choice(bad_utterances)

    count_op = 0

    return [[move, new_state], new_utterance]


def parameterized_minimax(current_state=None,
                          max_ply=2,
                          use_iterative_deepening=False,
                          use_default_move_ordering=False,
                          alpha_beta=False,
                          timed=False,
                          time_limit=1.0,
                          use_custom_static_eval_function=False):
    global num_expand, num_eval, max_depth, num_cutoff, my_side, CURRENT_STATE_DYNAMIC_VAL, \
        USE_CUSTOM_STATIC_EVAL_FUNCTION, USE_DEFAULT_MOVE, start_time
    current_state.__class__ = MY_TTS_State
    result = []
    num_expand = 0
    num_eval = 0
    max_depth = 0
    num_cutoff = 0
    if use_custom_static_eval_function:
        USE_CUSTOM_STATIC_EVAL_FUNCTION = True
    if not use_iterative_deepening:
        max_ply = 5
    if not timed:
        time_limit = 10000
    if use_default_move_ordering:
        USE_DEFAULT_MOVE = True
    start_time = time.time()
    if alpha_beta == False:
        value = minimax(current_state, my_side, max_ply, 0, time_limit)
    elif alpha_beta == True:
        value = alpha_beta_srch(current_state, max_ply, 0, -100000, 100000, my_side, time_limit)
    result.append(value)
    result.append(num_expand)
    result.append(num_eval)
    result.append(max_depth)
    result.append(num_cutoff)
    return result


# minimax search for searching the best value without ant cutoffs
# each value is put in to the "table" dictionary with corresponding state for referencing later
def minimax(state, side, depth, curr_depth, time_limit):
    global my_side, op_side, num_eval, num_expand, max_depth, \
        CURRENT_STATE_DYNAMIC_VAL, start_time, BEST_DEPTH
    max_depth = max(max_depth, curr_depth)
    state.__class__ = MY_TTS_State
    while time.time() - start_time <= time_limit:
        if depth == 0 or _find_next_vacancy(state.board) == False:
            num_eval += 1
            if my_side == 'W':
                value = state.static_eval()
            else:
                value = -1 * state.static_eval()
            return value
        if side == my_side:
            value = -100000
            states = next_states(state, side, USE_DEFAULT_MOVE)
            for s in states:
                num_expand += 1
                value = max(value, minimax(s, op_side, depth - 1, curr_depth + 1, time_limit))
                table[value] = s
            return value
        elif side == op_side:
            value = 100000
            states = next_states(state, side, USE_DEFAULT_MOVE)
            for s in states:
                num_expand += 1
                value = min(value, minimax(s, my_side, depth - 1, curr_depth + 1, time_limit))
                if value < CURRENT_STATE_DYNAMIC_VAL:
                    CURRENT_STATE_DYNAMIC_VAL = value
                table[value] = s
            if value > CURRENT_STATE_DYNAMIC_VAL and curr_depth == 1:  # select max value from top minimizing layer
                CURRENT_STATE_DYNAMIC_VAL = value
                table[CURRENT_STATE_DYNAMIC_VAL] = state
                BEST_DEPTH = curr_depth
            return value
    return CURRENT_STATE_DYNAMIC_VAL  # return current best when out of time


# alpha_beta search for searching the best value without ant cutoffs
# each value is put in to the "table" dictionary with corresponding state for referencing later
def alpha_beta_srch(state, depth, curr_depth, alpha, beta, side, time_limit):
    global my_side, op_side, num_eval, num_expand, num_cutoff, max_depth, \
        CURRENT_STATE_DYNAMIC_VAL, start_time
    max_depth = max(max_depth, curr_depth)
    curr_time = time.time()
    num_expand += 1
    state.__class__ = MY_TTS_State
    while curr_time - start_time <= time_limit:
        if depth == 0 or not _find_next_vacancy(state.board):
            num_eval += 1
            if my_side == 'W':
                value = state.static_eval()
            else:
                value = -1 * state.static_eval()
            return value
        if side == my_side:
            value = -100000
            states = next_states(state, my_side, USE_DEFAULT_MOVE)
            for s in states:
                value = max(value, alpha_beta_srch(s, depth - 1, curr_depth + 1, alpha, beta, op_side, time_limit))
                alpha = max(alpha, value)
                if alpha >= beta:
                    num_cutoff += 1
                    break
                if value == -100000:
                    table[value] = s
            return value
        elif side == op_side:
            value = 100000
            states = next_states(state, op_side, USE_DEFAULT_MOVE)
            for s in states:
                value = min(value, alpha_beta_srch(s, depth - 1, curr_depth + 1, alpha, beta, my_side, time_limit))
                beta = min(beta, value)
                if alpha >= beta:
                    num_cutoff += 1
                    break
                if curr_depth == 1:
                    table[value] = s
            if value > CURRENT_STATE_DYNAMIC_VAL and curr_depth == 1:
                CURRENT_STATE_DYNAMIC_VAL = value
                table[CURRENT_STATE_DYNAMIC_VAL] = state
            return value
    return CURRENT_STATE_DYNAMIC_VAL  # return current best when out of time


def _find_next_vacancy(b):
    for i in range(len(b)):
        for j in range(len(b[0])):
            if b[i][j] == ' ': return (i, j)
    return False


def next_states(state, side, default):
    global last_move
    mx, my = last_move
    board = state.copy().board
    l = []
    H = len(board)
    W = len(board[0])
    if not default:
        H = 2
        W = 2
    for i in range(H):
        for j in range(W):
            i += mx
            if i < 0 or i >= H:
                i = ((i + H) % H)  # toroidal wrap
            j += my
            if j < 0 or j >= W:
                j = ((j + W) % W)  # toroidal wrap
            if board[i][j] == ' ':
                new_state = state.copy()
                new_state.board[i][j] = side
                l.append(new_state)
    return l


INIT = \
    [['W', ' ', ' ', 'W'],
     [' ', ' ', ' ', '-'],
     ['-', ' ', ' ', 'B'],
     ['W', ' ', ' ', 'B']]
K = 4

curr = TTS_State(board=INIT)

l = take_turn(curr, '')
print(l)
