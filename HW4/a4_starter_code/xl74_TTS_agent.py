'''
xl74_TTS_agent.py
xl74, 1561102

Artificial Idiot written by Xuedeliang Li
'''

from TTS_State import TTS_State
import math
import time
import random
import test_board as Game
USE_CUSTOM_STATIC_EVAL_FUNCTION = False
USE_ITERATIVE_DEEPENING_AND_TIME = False
MAX_PLY = 2
ALPHA_BETA = False
TIME_LIMIT = 1.0
K = 5
WHO_I_PLAY = ""
PLAYER_2_NAME = ""


STATIC_EVAL_PERFORMED = 0
STATES_EXPANDED = 0
AB_CUTOFFS = 0
TIME_USED = 0
MAX_DEPTH_VISITED = 0


class xl74_TTS_State(TTS_State):
    ROW_NUMBER, COL_NUMBER = 0, 0

    def static_eval(self):
        global USE_CUSTOM_STATIC_EVAL_FUNCTION
        if USE_CUSTOM_STATIC_EVAL_FUNCTION:
            return self.custom_static_eval()
        else:
            return self.basic_static_eval()

    def basic_static_eval(self):
        return self.count("W", 2) - self.count("B", 2)

    def custom_static_eval(self):
        global K, WHO_I_PLAY
        result = 0
        for i in range(1, K - 1):
            result += pow(10, i) * (self.count("W", i + 1) - self.count("B", i + 1))

        return result

    def get_dimension(self):
        global ROW_NUMBER, COL_NUMBER
        ROW_NUMBER = len(self.board)
        COL_NUMBER = len(self.board[0])

    #   Take row number, column number, neighbor direction
    #   Return (row, col) of that neighbor
    def get_neighbor(self, row, col, drc):
        row_number = len(self.board)
        col_number = len(self.board[0])

        return {0: ((row - 1) % row_number, col),
                1: ((row + 1) % row_number, col),
                2: (row, (col - 1) % col_number),
                3: (row, (col + 1) % col_number),
                4: ((row - 1) % row_number, (col - 1) % col_number),
                5: ((row - 1) % row_number, (col + 1) % col_number),
                6: ((row + 1) % row_number, (col - 1) % col_number),
                7: ((row + 1) % row_number, (col + 1) % col_number)}.get(drc)

    def count(self, target, length):
        row_number = len(self.board)
        col_number = len(self.board[0])

        loop, normal = 0, 0
        for row in range(row_number):
            for col in range(col_number):
                #   Check every entry of the board
                if self.board[row][col] == target:
                    for drc in range(0, 8):
                        form_line = True
                        current = (row, col)

                        #   n-1 neighbor on that direction to be checked
                        for num in range(1, length):
                            neighbor = self.get_neighbor(current[0], current[1], drc)
                            #   Encounter none-target entry in a line
                            if self.board[neighbor[0]][neighbor[1]] != target:
                                form_line = False
                                break
                            #   Encounter the start point before finishing length-n line
                            elif neighbor[0] == row and neighbor[1] == col:
                                form_line = False
                                break
                            else:
                                current = neighbor

                        if form_line:
                            current = self.get_neighbor(current[0], current[1], drc)
                            if current[0] == row and current[1] == col:
                                loop += 1
                            elif self.board[current[0]][current[1]] != target:
                                normal += 1
                            #   Otherwise it is a sub-line of a longer line

        return (loop / length) + (normal / 2)


def take_turn(current_state, last_utterance, time_limit=10):
    # Compute the new state for a move.
    # Start by copying the current state.
    new_state = TTS_State(current_state.board)
    # Fix up whose turn it will be.
    who = current_state.whose_turn
    new_who = 'B'
    if who == 'B': new_who = 'W'
    new_state.whose_turn = new_who

    global TIME_LIMIT, TIME_USED
    TIME_LIMIT = time_limit
    TIME_USED = 0

    # Make up a new remark
    new_utterance = _random_utterance()
    result = [_find_next_vacancy(new_state.board)]

    temp_time = time.perf_counter()
    for current_max_depth in range(0, 5):
        time_inloop = time.perf_counter()
        TIME_USED += time_inloop - temp_time
        if TIME_USED > 0.9995 * TIME_LIMIT:
            break

        result = _minimax_id_abp_changed_move(
            current_state, current_max_depth, 0, who, (-math.inf, math.inf))
        temp_time = time_inloop


    move = result[0]
    if move is None:
        return [[False, current_state], "No place to go. GGWP."]
    else:
        new_state.board[move[0]][move[1]] = who
        return [[move, new_state], new_utterance]


def _find_next_vacancy(b):
    for i in range(len(b)):
        for j in range(len(b[0])):
            if b[i][j] == ' ': return (i, j)
    return False


def _random_utterance():
    return random.choice([
        "That was a good move by you.",
        "This game requires lots of observation and thinking, doesn't it?",
        "I hope I just made a good choice.",
        "Take your time.",
        "It's just a game, relax.",
        "That was an aggressive move.",
        "The clock is ticking.",
        "Are you sure about that?",
        "I sometimes think if I can play some games other than this one.",
        "I am not perfect; I make mistakes eventually.",
        "It is hard to make a move in this situation.",
        "The board is so complicated.",
        "May I ask how much time do I have?"
    ])


def moniker():
    return "LXDL"


def who_am_i():
    return """My name is LXDL, and I am created by Xuedeliang Li. XD?"""


def get_ready(initial_state, k, who_i_play, player2Nickname):
    # do any prep, like eval pre-calculation, here.
    global K, WHO_I_PLAY, PLAYER_2_NAME
    K = k
    WHO_I_PLAY = who_i_play
    PLAYER_2_NAME = player2Nickname

    return "OK"


# The following is a skeleton for the function called parameterized_minimax,
# which should be a top-level function in each agent file.
# A tester or an autograder may do something like
# import ABC_TTS_agent as player, call get_ready(),
# and then it will be able to call tryout using something like this:
# results = player.parameterized_minimax(**kwargs)

def parameterized_minimax(
        current_state=None,
        use_iterative_deepening_and_time=False,
        max_ply=2,
        use_default_move_ordering=False,
        alpha_beta=False,
        time_limit=1.0,
        use_custom_static_eval_function=False):
    # All students, add code to replace these default
    # values with correct values from your agent (either here or below).
    global STATIC_EVAL_PERFORMED, STATES_EXPANDED, AB_CUTOFFS, TIME_USED, \
        TIME_LIMIT, USE_CUSTOM_STATIC_EVAL_FUNCTION, WHO_I_PLAY, MAX_DEPTH_VISITED

    USE_CUSTOM_STATIC_EVAL_FUNCTION = use_custom_static_eval_function
    STATIC_EVAL_PERFORMED = 0
    STATES_EXPANDED = 0
    AB_CUTOFFS = 0
    TIME_USED = 0
    TIME_LIMIT = time_limit
    MAX_DEPTH_VISITED = 0

    current_state_static_val = -1000.0
    n_states_expanded = 0
    n_static_evals_performed = 0
    max_depth_reached = 0
    n_ab_cutoffs = 0

    # STUDENTS: You may create the rest of the body of this function here.
    current_state.__class__ = xl74_TTS_State
    temp_result = [None, current_state.static_eval()]
    depth_limit = max_ply

    if not use_iterative_deepening_and_time:
        if not alpha_beta:
            if not use_default_move_ordering:
                temp_result = _minimax_default_move(current_state, depth_limit, WHO_I_PLAY)
            else:
                temp_result = _minimax_changed_move(current_state, depth_limit, WHO_I_PLAY)
            n_ab_cutoffs = 0
        else:
            if not use_default_move_ordering:
                temp_result = _minimax_abp_default_move(current_state, depth_limit, WHO_I_PLAY, (-math.inf, math.inf))

            else:
                temp_result = _minimax_abp_changed_move(current_state, depth_limit, WHO_I_PLAY, (-math.inf, math.inf))
            n_ab_cutoffs = AB_CUTOFFS

        max_depth_reached = depth_limit
        current_state_static_val = temp_result[1]
    else:
        temp_time = time.perf_counter()
        for current_max_depth in range(0, depth_limit + 1):
            time_inloop = time.perf_counter()
            TIME_USED += time_inloop - temp_time
            if TIME_USED > 0.9995 * TIME_LIMIT:
                break

            if not alpha_beta:
                if not use_default_move_ordering:
                    temp_result = _minimax_id_default_move(current_state, current_max_depth, 0, WHO_I_PLAY)
                else:
                    temp_result = _minimax_id_changed_move(current_state, current_max_depth, 0, WHO_I_PLAY)
                n_ab_cutoffs = 0
            else:
                if not use_default_move_ordering:
                    temp_result = _minimax_id_abp_default_move(
                        current_state, current_max_depth, 0, WHO_I_PLAY, (-math.inf, math.inf))
                else:
                    temp_result = _minimax_id_abp_changed_move(
                        current_state, current_max_depth, 0, WHO_I_PLAY, (-math.inf, math.inf))
                n_ab_cutoffs = AB_CUTOFFS

        current_state_static_val = temp_result[1]
        max_depth_reached = MAX_DEPTH_VISITED

    n_states_expanded = STATES_EXPANDED
    n_static_evals_performed = STATIC_EVAL_PERFORMED

    # Prepare to return the results, don't change the order of the results
    results = []
    results.append(current_state_static_val)
    results.append(n_states_expanded)
    results.append(n_static_evals_performed)
    results.append(max_depth_reached)
    results.append(n_ab_cutoffs)
    # Actually return the list of all results...
    print(temp_result)
    return results


#   No timing, no iterative deepening, no ab-pruning, default move generator
#   max_depth_visited always given depth
#   Return [(i, j), state-value]
#   Will change STATIC_EVAL_PERFORMED, STATES_EXPANDED
def _minimax_default_move(current_state, depth, move):
    current_state.__class__ = xl74_TTS_State
    global STATIC_EVAL_PERFORMED, STATES_EXPANDED

    if depth == 0:
        STATIC_EVAL_PERFORMED += 1
        return [None, current_state.static_eval()]

    STATES_EXPANDED += 1

    new_board = [r[:] for r in current_state.board]

    if move == 'W':
        provisional = - math.inf
        next_move = 'B'
    else:
        provisional = math.inf
        next_move = 'W'

    available_location = []

    for i in range(len(new_board)):
        for j in range(len(new_board[i])):
            if new_board[i][j] == ' ':
                available_location.append((i, j))

    #   No more moves can be made
    if len(available_location) == 0:
        return [None, current_state.static_eval()]

    best_move = None
    for moves in available_location:
        new_board[moves[0]][moves[1]] = move
        result = _minimax_default_move(TTS_State(new_board), depth - 1, next_move)
        if ((move == 'W' and result[1] > provisional) or
                (move == 'B' and result[1] < provisional)):
            best_move = moves
            provisional = result[1]

        new_board[moves[0]][moves[1]] = ' '

    return [best_move, provisional]


#   No timing, no iterative depending, ab-pruning, default move generator
#   ab = [alpha, beta]
#   max_depth_visited always given depth
#   Return [(i, j), state-value]
#   Will change STATIC_EVAL_PERFORMED, STATES_EXPANDED, AB_CUTOFFS
def _minimax_abp_default_move(current_state, depth, move, ab):
    current_state.__class__ = xl74_TTS_State
    global STATIC_EVAL_PERFORMED, STATES_EXPANDED, AB_CUTOFFS

    if depth == 0:
        STATIC_EVAL_PERFORMED += 1
        return [None, current_state.static_eval()]

    STATES_EXPANDED += 1

    new_board = [r[:] for r in current_state.board]
    current_ab = [r for r in ab]
    best_move = None

    for i in range(len(new_board)):
        for j in range(len(new_board[i])):
            if new_board[i][j] == ' ':
                if move == 'W':
                    new_board[i][j] = 'W'
                    result = _minimax_abp_default_move(TTS_State(new_board), depth - 1, 'B', current_ab)
                    #   For max, if returned value larger than or equal to beta
                    #   return therefore pruning all other child states
                    if result[1] >= current_ab[1]:
                        AB_CUTOFFS += 1
                        return [(i, j), result[1]]
                    #   Else if returned value larger than alpha
                    #   update alpha for other child state
                    #   current move might be the best
                    elif result[1] >= current_ab[0]:
                        current_ab[0] = result[1]
                        best_move = (i, j)
                else:
                    new_board[i][j] = 'B'
                    result = _minimax_abp_default_move(TTS_State(new_board), depth - 1, 'W', current_ab)
                    #   For min, if returned value smaller than alpha
                    #   return therefore pruning all other child states
                    if result[1] <= current_ab[0]:
                        AB_CUTOFFS += 1
                        return [(i, j), result[1]]
                    #   Else if returned value smaller than beta
                    #   update beta for other child state
                    #   current move might be the best
                    elif result[1] <= current_ab[1]:
                        current_ab[1] = result[1]
                        best_move = (i, j)

                new_board[i][j] = ' '

    #   No possible move found
    if best_move is None:
        return [None, current_state.static_eval()]
    #   No pruning made
    else:
        #   Return alpha as value if max, beta as value if min
        if move == 'W':
            return [best_move, current_ab[0]]
        else:
            return [best_move, current_ab[1]]


#   No timing, no iterative deepening, no ab-pruning, custom move generator
#   max_depth_visited always given depth
#   Return [(i, j), state-value]
#   Will change STATIC_EVAL_PERFORMED, STATES_EXPANDED
def _minimax_changed_move(current_state, depth, move):
    current_state.__class__ = xl74_TTS_State
    global STATIC_EVAL_PERFORMED, STATES_EXPANDED

    if depth == 0:
        STATIC_EVAL_PERFORMED += 1
        return [None, current_state.static_eval()]

    STATES_EXPANDED += 1

    new_board = [r[:] for r in current_state.board]

    if move == 'W':
        provisional = - math.inf
        next_move = 'B'
    else:
        provisional = math.inf
        next_move = 'W'

    available_location = _custom_order(new_board, move)
    if len(available_location) == 1:
        if available_location[0][2] == math.inf:
            STATIC_EVAL_PERFORMED += 1
            return [(available_location[0][0], available_location[0][1]), current_state.static_eval()]

    #   No more moves can be made
    if len(available_location) == 0:
        return [None, current_state.static_eval()]

    best_move = None
    for moves in available_location:
        new_board[moves[0]][moves[1]] = move
        result = _minimax_changed_move(TTS_State(new_board), depth - 1, next_move)
        if ((move == 'W' and result[1] > provisional) or
                (move == 'B' and result[1] < provisional)):
            best_move = (moves[0], moves[1])
            provisional = result[1]

        new_board[moves[0]][moves[1]] = ' '

    return [best_move, provisional]


#   No timing, no iterative deepening, ab-pruning, custom move generator
#   ab = [alpha, beta]
#   max_depth_visited always given depth
#   Return [(i, j), state-value]
#   Will change STATIC_EVAL_PERFORMED, STATES_EXPANDED, AB_CUTOFFS
def _minimax_abp_changed_move(current_state, depth, move, ab):
    current_state.__class__ = xl74_TTS_State
    global STATIC_EVAL_PERFORMED, STATES_EXPANDED, AB_CUTOFFS

    if depth == 0:
        STATIC_EVAL_PERFORMED += 1
        return [None, current_state.static_eval()]

    STATES_EXPANDED += 1

    new_board = [r[:] for r in current_state.board]
    current_ab = [r for r in ab]
    best_move = None

    #   Use custom ordering
    available_location = _custom_order(new_board, move)
    if len(available_location) == 1:
        if available_location[0][2] == math.inf:
            STATIC_EVAL_PERFORMED += 1
            return [(available_location[0][0], available_location[0][1]), current_state.static_eval()]

    for moves in available_location:
        row = moves[0]
        col = moves[1]
        if move == 'W':
            new_board[row][col] = 'W'
            result = _minimax_abp_changed_move(TTS_State(new_board), depth - 1, 'B', current_ab)
            #   For max, if returned value larger than or equal to beta
            #   return therefore pruning all other child states
            if result[1] >= current_ab[1]:
                AB_CUTOFFS += 1
                return [(row, col), result[1]]
            #   Else if returned value larger than alpha
            #   update alpha for other child state
            #   current move might be the best
            elif result[1] >= current_ab[0]:
                current_ab[0] = result[1]
                best_move = (row, col)
        else:
            new_board[row][col] = 'B'
            result = _minimax_abp_changed_move(TTS_State(new_board), depth - 1, 'W', current_ab)
            #   For min, if returned value smaller than alpha
            #   return therefore pruning all other child states
            if result[1] <= current_ab[0]:
                AB_CUTOFFS += 1
                return [(row, col), result[1]]
            #   Else if returned value smaller than beta
            #   update beta for other child state
            #   current move might be the best
            elif result[1] <= current_ab[1]:
                current_ab[1] = result[1]
                best_move = (row, col)

        new_board[row][col] = ' '

    #   No possible move found
    if best_move is None:
        return [None, current_state.static_eval()]
    #   No pruning made
    else:
        #   Return alpha as value if max, beta as value if min
        if move == 'W':
            return [best_move, current_ab[0]]
        else:
            return [best_move, current_ab[1]]


#   Timing, iterative deepening, no ab-pruning, default move generator
#   Return [(i, j), state-value]
#   Will change MAX_DEPTH_VISITED, STATIC_EVAL_PERFORMED, STATES_EXPANDED, TIME_USED
def _minimax_id_default_move(current_state, depth, max_depth, move):
    current_state.__class__ = xl74_TTS_State
    global STATIC_EVAL_PERFORMED, STATES_EXPANDED, MAX_DEPTH_VISITED, TIME_USED, TIME_LIMIT
    MAX_DEPTH_VISITED = max(max_depth, MAX_DEPTH_VISITED)

    time1 = time.perf_counter()

    if depth == 0 or TIME_USED > 0.9995 * TIME_LIMIT:
        STATIC_EVAL_PERFORMED += 1
        return [None, current_state.static_eval()]

    STATES_EXPANDED += 1

    new_board = [r[:] for r in current_state.board]

    if move == 'W':
        provisional = - math.inf
        next_move = 'B'
    else:
        provisional = math.inf
        next_move = 'W'

    available_location = []

    for i in range(len(new_board)):
        for j in range(len(new_board[i])):
            if new_board[i][j] == ' ':
                available_location.append((i, j))

    #   No more moves can be made
    if len(available_location) == 0:
        STATIC_EVAL_PERFORMED += 1
        return [None, current_state.static_eval()]

    time2 = time.perf_counter()
    TIME_USED += (time2 - time1)
    if TIME_USED > 0.9995 * TIME_LIMIT:
        STATIC_EVAL_PERFORMED += 1
        return [None, current_state.static_eval()]

    temp_time = time2
    best_move = None
    for moves in available_location:
        time_inloop = time.perf_counter()
        TIME_USED += time_inloop - temp_time

        if TIME_USED > 0.9995 * TIME_LIMIT:
            return [best_move, provisional]

        new_board[moves[0]][moves[1]] = move
        result = _minimax_id_default_move(TTS_State(new_board),
                                          depth - 1, max_depth + 1, next_move)
        if ((move == 'W' and result[1] > provisional) or
                (move == 'B' and result[1] < provisional)):
            best_move = moves
            provisional = result[1]

        new_board[moves[0]][moves[1]] = ' '

        temp_time = time_inloop
        TIME_USED += time.perf_counter() - temp_time
        if TIME_USED > 0.9995 * TIME_LIMIT:
            return [best_move, provisional]

    return [best_move, provisional]


#   Timing, iterative deepening, ab-pruning, default move generator
#   ab = [alpha, beta]
#   Return [(i, j), state-value]
#   Will change MAX_DEPTH_VISITED, STATIC_EVAL_PERFORMED, STATES_EXPANDED, AB_CUTOFFS, TIME_USED
def _minimax_id_abp_default_move(current_state, depth, max_depth, move, ab):
    current_state.__class__ = xl74_TTS_State
    global MAX_DEPTH_VISITED, STATIC_EVAL_PERFORMED, STATES_EXPANDED, AB_CUTOFFS, TIME_USED, TIME_LIMIT
    MAX_DEPTH_VISITED = max(max_depth, MAX_DEPTH_VISITED)

    if depth == 0 or TIME_USED > 0.9995 * TIME_LIMIT:
        STATIC_EVAL_PERFORMED += 1
        return [None, current_state.static_eval()]

    STATES_EXPANDED += 1

    new_board = [r[:] for r in current_state.board]
    current_ab = [r for r in ab]
    best_move = None

    result = [None, current_state.static_eval()]

    temp_time = time.perf_counter()

    for i in range(len(new_board)):
        for j in range(len(new_board[i])):
            if new_board[i][j] == ' ':
                time_inloop = time.perf_counter()
                TIME_USED += time_inloop - temp_time
                if TIME_USED > 0.9995 * TIME_LIMIT:
                    return [(i, j), result[1]]

                if move == 'W':
                    new_board[i][j] = 'W'
                    result = _minimax_id_abp_default_move(TTS_State(new_board),
                                                          depth - 1, max_depth + 1, 'B', current_ab)
                    #   For max, if returned value larger than or equal to beta
                    #   return therefore pruning all other child states
                    if result[1] >= current_ab[1]:
                        AB_CUTOFFS += 1
                        return [(i, j), result[1]]
                    #   Else if returned value larger than alpha
                    #   update alpha for other child state
                    #   current move might be the best
                    elif result[1] >= current_ab[0]:
                        current_ab[0] = result[1]
                        best_move = (i, j)
                else:
                    new_board[i][j] = 'B'
                    result = _minimax_id_abp_default_move(TTS_State(new_board),
                                                          depth - 1, max_depth + 1, 'W', current_ab)
                    #   For min, if returned value smaller than alpha
                    #   return therefore pruning all other child states
                    if result[1] <= current_ab[0]:
                        AB_CUTOFFS += 1
                        return [(i, j), result[1]]
                    #   Else if returned value smaller than beta
                    #   update beta for other child state
                    #   current move might be the best
                    elif result[1] <= current_ab[1]:
                        current_ab[1] = result[1]
                        best_move = (i, j)

                new_board[i][j] = ' '
                temp_time = time_inloop
                TIME_USED += time.perf_counter() - temp_time
                if TIME_USED > 0.9995 * TIME_LIMIT:
                    return [best_move, result[1]]

    #   No possible move found
    if best_move is None:
        STATIC_EVAL_PERFORMED += 1
        return [None, current_state.static_eval()]
    #   No pruning made
    else:
        #   Return alpha as value if max, beta as value if min
        if move == 'W':
            return [best_move, current_ab[0]]
        else:
            return [best_move, current_ab[1]]


#   No timing, no iterative deepening, no ab-pruning, custom move generator
#   Return [(i, j), state-value]
#   Will change MAX_DEPTH_VISITED, STATIC_EVAL_PERFORMED, STATES_EXPANDED, TIME_USED
def _minimax_id_changed_move(current_state, depth, max_depth, move):
    current_state.__class__ = xl74_TTS_State
    global STATIC_EVAL_PERFORMED, STATES_EXPANDED, MAX_DEPTH_VISITED, TIME_USED, TIME_LIMIT
    MAX_DEPTH_VISITED = max(max_depth, MAX_DEPTH_VISITED)

    time1 = time.perf_counter()

    if depth == 0 or TIME_USED > 0.9995 * TIME_LIMIT:
        STATIC_EVAL_PERFORMED += 1
        return [None, current_state.static_eval()]

    STATES_EXPANDED += 1

    new_board = [r[:] for r in current_state.board]

    if move == 'W':
        provisional = - math.inf
        next_move = 'B'
    else:
        provisional = math.inf
        next_move = 'W'

    available_location = _custom_order(new_board, move)
    if len(available_location) == 1:
        if available_location[0][2] == math.inf:
            STATIC_EVAL_PERFORMED += 1
            return [(available_location[0][0], available_location[0][1]), current_state.static_eval()]

    #   No more moves can be made
    if len(available_location) == 0:
        STATIC_EVAL_PERFORMED += 1
        return [None, current_state.static_eval()]

    time2 = time.perf_counter()
    TIME_USED += (time2 - time1)
    if TIME_USED > 0.9995 * TIME_LIMIT:
        STATIC_EVAL_PERFORMED += 1
        return [None, current_state.static_eval()]

    temp_time = time2
    best_move = None
    for moves in available_location:
        time_inloop = time.perf_counter()
        TIME_USED += time_inloop - temp_time

        if TIME_USED > 0.9995 * TIME_LIMIT:
            return [best_move, provisional]

        new_board[moves[0]][moves[1]] = move
        result = _minimax_id_changed_move(TTS_State(new_board),
                                          depth - 1, max_depth + 1, next_move)
        if ((move == 'W' and result[1] > provisional) or
                (move == 'B' and result[1] < provisional)):
            best_move = moves
            provisional = result[1]

        new_board[moves[0]][moves[1]] = ' '

        temp_time = time_inloop
        TIME_USED += time.perf_counter() - temp_time
        if TIME_USED > 0.9995 * TIME_LIMIT:
            return [best_move, provisional]

    return [best_move, provisional]


#   No timing, no iterative deepening, ab-pruning, custom move generator
#   ab = [alpha, beta]
#   Return [(i, j), state-value]
#   Will change MAX_DEPTH_VISITED, STATIC_EVAL_PERFORMED, STATES_EXPANDED, AB_CUTOFFS, TIME_USED
def _minimax_id_abp_changed_move(current_state, depth, max_depth, move, ab):
    current_state.__class__ = xl74_TTS_State
    global MAX_DEPTH_VISITED, STATIC_EVAL_PERFORMED, STATES_EXPANDED, AB_CUTOFFS, TIME_USED, TIME_LIMIT, K
    MAX_DEPTH_VISITED = max(max_depth, MAX_DEPTH_VISITED)
    current_stat_eval = current_state.static_eval()

    if depth == 0 or TIME_USED > 0.9995 * TIME_LIMIT:
        STATIC_EVAL_PERFORMED += 1
        return [None, current_stat_eval]

    STATES_EXPANDED += 1

    new_board = [r[:] for r in current_state.board]
    current_ab = [r for r in ab]
    best_move = None

    result = [None, current_stat_eval]

    available_location = _custom_order(new_board, move)
    if len(available_location) == 1:
        position = available_location[0]
        if position[2] == math.inf:
            STATIC_EVAL_PERFORMED += 1
            if move == 'W':
                return [(position[0], position[1]), math.inf]
            else:
                return [(position[0], position[1]), - math.inf]

    temp_time = time.perf_counter()

    for moves in available_location:
        row = moves[0]
        col = moves[1]

        time_inloop = time.perf_counter()
        TIME_USED += time_inloop - temp_time
        if TIME_USED > 0.9995 * TIME_LIMIT:
            return [(row, col), result[1]]

        if move == 'W':
            new_board[row][col] = 'W'
            result = _minimax_id_abp_changed_move(TTS_State(new_board),
                                                  depth - 1, max_depth + 1, 'B', current_ab)
            #   For max, if returned value larger than or equal to beta
            #   return therefore pruning all other child states
            if result[1] >= current_ab[1]:
                AB_CUTOFFS += 1
                return [(row, col), result[1]]
            #   Else if returned value larger than alpha
            #   update alpha for other child state
            #   current move might be the best
            elif result[1] >= current_ab[0]:
                current_ab[0] = result[1]
                best_move = (row, col)
        else:
            new_board[row][col] = 'B'
            result = _minimax_id_abp_changed_move(TTS_State(new_board),
                                                  depth - 1, max_depth + 1, 'W', current_ab)
            #   For min, if returned value smaller than alpha
            #   return therefore pruning all other child states
            if result[1] <= current_ab[0]:
                AB_CUTOFFS += 1
                return [(row, col), result[1]]
            #   Else if returned value smaller than beta
            #   update beta for other child state
            #   current move might be the best
            elif result[1] <= current_ab[1]:
                current_ab[1] = result[1]
                best_move = (row, col)

        new_board[row][col] = ' '
        temp_time = time_inloop
        TIME_USED += time.perf_counter() - temp_time

        if TIME_USED > 0.9995 * TIME_LIMIT:
            return [best_move, result[1]]

    #   No possible move found
    if best_move is None:
        STATIC_EVAL_PERFORMED += 1
        return [None, current_stat_eval]
    #   No pruning made
    else:
        #   Return alpha as value if max, beta as value if min
        if move == 'W':
            return [best_move, current_ab[0]]
        else:
            return [best_move, current_ab[1]]


#   Return something like [(row, col, p_value)]
#   Only checks for available slots
def _custom_order(board, who):
    global K

    if who == 'W':
        coeff = (1, 10)
    else:
        coeff = (10, 1)
    result = []
    row_num = len(board)
    col_num = len(board[0])

    for row in range(row_num):
        for col in range(col_num):
            if board[row][col] == ' ':
                p_value = 0
                for drc in range(0, 8):
                    count = _find_cont(drc, row, col, board)
                    if count[1] == 'W':
                        if who == 'W' and count[0] == K - 1:
                            return [(row, col, math.inf)]
                        elif who == 'B' and count[0] >= math.floor(K / 2):
                            return [(row, col, math.inf)]
                        else:
                            p_value += (count[0] - 1) * coeff[0]
                    elif count[1] == 'B':
                        if who == 'B' and count[0] == K - 1:
                            return [(row, col, math.inf)]
                        elif who == 'W' and count[0] >= math.floor(K / 2):
                            return [(row, col, math.inf)]
                        else:
                            p_value += (count[0] - 1) * coeff[1]
                    elif count[1] == '-':
                        p_value += -20
                    else:
                        p_value += 0
                result.append((row, col, p_value))

    #   Higher p_value has higher priority
    #   and therefore will be at the front
    for i in range(1, len(result)):
        temp = result[i]
        j = i - 1
        while j >= 0 and temp[2] > result[j][2]:
            result[j + 1] = result[j]
            j -= 1
        result[j + 1] = temp

    return result


#   Return something like [(row, col, p_value)]
#   Only checks for available slots
#   ***ABANDONED***
def _custom_order1(board, who):
    result = []
    row_num = len(board)
    col_num = len(board[0])

    for row in range(row_num):
        for col in range(col_num):
            if board[row][col] == ' ':
                neighbor_w, neighbor_b, neighbor_n, neighbor_f = 0, 0, 0, 0
                neighbors = [((row - 1) % row_num, col),
                             ((row + 1) % row_num, col),
                             (row, (col - 1) % col_num),
                             (row, (col + 1) % col_num),
                             ((row - 1) % row_num, (col - 1) % col_num),
                             ((row - 1) % row_num, (col + 1) % col_num),
                             ((row + 1) % row_num, (col - 1) % col_num),
                             ((row + 1) % row_num, (col + 1) % col_num)]

                for n in neighbors:
                    if board[n[0]][n[1]] == 'W':
                        neighbor_w += 1
                    elif board[n[0]][n[1]] == 'B':
                        neighbor_b += 1
                    elif board[n[0]][n[1]] == ' ':
                        neighbor_n += 1
                    else:
                        neighbor_f += 1

                if who == 'W':
                    p_value = (2 * neighbor_b + neighbor_w) - (neighbor_n + 2 * neighbor_f)
                else:
                    p_value = (2 * neighbor_w + neighbor_b) - (neighbor_n + 2 * neighbor_f)
                result.append((row, col, p_value))

    #   Higher p_value has higher priority
    #   and therefore will be at the front
    for i in range(1, len(result)):
        temp = result[i]
        j = i - 1
        while j >= 0 and temp[2] >= result[j][2]:
            result[j + 1] = result[j]
            j -= 1
        result[j + 1] = temp

    return result


def _find_cont(drc, row, col, board):
    offset = {0: (-1, 0),
              1: (1, 0),
              2: (0, -1),
              3: (0, 1),
              4: (-1, -1),
              5: (-1, 1),
              6: (1, -1),
              7: (1, 1)}.get(drc)
    temp_row = (row + offset[0]) % len(board)
    temp_col = (col + offset[1]) % len(board[0])
    temp_thing = board[temp_row][temp_col]

    if temp_thing == ' ' or temp_thing == '-':
        return [1, temp_thing]

    count = 0
    while (board[temp_row][temp_col] == temp_thing) and (temp_row != row or temp_col != col):
        count += 1
        temp_row = (temp_row + offset[0]) % len(board)
        temp_col = (temp_col + offset[1]) % len(board[0])

    return [count, temp_thing]


def test_search():
    global USE_CUSTOM_STATIC_EVAL_FUNCTION
    test_state = TTS_State(board=Game.INITIAL_BOARD, whose_turn="W")
    get_ready(Game.INITIAL_BOARD, Game.K, test_state.whose_turn, 'haha')
    test_state.__class__ = xl74_TTS_State
    # result = parameterized_minimax(test_state, False, 2, False, False, 1.0, False)
    a_b = True
    USE_CUSTOM_STATIC_EVAL_FUNCTION = False
    start = time.perf_counter()
    test_state.__class__ = xl74_TTS_State

    result = parameterized_minimax(current_state=test_state,
                                   use_iterative_deepening_and_time=True,
                                   max_ply=2,
                                   use_default_move_ordering=True,
                                   alpha_beta=a_b,
                                   time_limit=20.0,
                                   use_custom_static_eval_function=USE_CUSTOM_STATIC_EVAL_FUNCTION)
    end = time.perf_counter()
    runtime = end - start
    print("[current_state_static_val, state_count, eval_count, depth_count, ab_count]")
    print("a_b is {}; result is {}; runtime is {}".format(a_b, result, runtime))


def test():
    get_ready(Game.INITIAL_BOARD, Game.K, 'W', 'haha')
    test_state = TTS_State(board=Game.INITIAL_BOARD, whose_turn="W")
    test_state.__class__ = xl74_TTS_State
    # print(my_side)
    result = test_state.static_eval()
    print(result)

test_search()

# test()
