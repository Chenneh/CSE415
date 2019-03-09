''' chenb24_TTS_agent.py by Chen Bai(chenb24, 1560405)
An automatic Toro-Tile straight game agent
    Version 0.2, February 10, 2019.
    Chen Bai, Univ. of Washington.
    Electronic and Computer Engineering

 Usage:
 python3 timed_tts_game_master.py YOUR_GAME_BOARD WHITE_AGENT BLACK_AGENT TIME
 python3 _game_master.py YOUR_GAME_BOARD WHITE_AGENT BLACK_AGENT TIME


This implementation is extended from PlayerSkeleton.py to make a Toro-Tile game agent.
This file include both basic evaluation and my custom evaluation function.
Basic evaluation is to count C(W, 2) - C(B, 2)
My custom evaluation is to try to make next step block opponent's way while considering less on winning the game.
The main algorithm is to use minimax search along with evaluation to find optimal move.

Most of the print statements have been commented out, but can be
useful for a closer look at execution, or if preparing some
debugging infrastructure before adding extensions.
'''

# Note: I have implemented both options under Interesting utterances, for the extra credit.
#       Decide to take part in tournament, for the extra credit.

from TTS_State import TTS_State
import math
import time
import copy
# import Gold_Rush_Game_Type as Game
import test_board as Game

# import test_search as Game

name = "Mean_to_Block"
creator = "chenb24"
opponent = "Myself"
normal_utterance = ["Waiting for blocking", "Well, no block maybe next time", "Just some random move without block",
                    "Watching for any block chance", "Nothing block? ok",
                    "No need to block this time :(", "Please make a move so I can do some block",
                    "This is not the time for block", "Boring, no block this turn!",
                    "You better let me block next turn", "No block... Going on"]
normal_u_order = 0
block_utterance = ["Gonna block you!", "Not this time, Block!", "I must block you!",
                   "I don't want to win but block your way!",
                   "No matter what just block!", "Block! Block! Block!", "You know what... Block!", "Hahaha, Block",
                   "Just block you, so sad!", "Blocker! it's me!", "BBBBBBBlock!!!"]
block_u_order = 0
if_block = 0
INITIAL_STATE = None
my_side = None
op_side = None
opponent = None
K = None
USE_CUSTOM_STATIC_EVAL_FUNCTION = False
check_direction = [(1, 0), (1, -1), (0, 1), (1, 1)]  # S,  SW, E, SE
depth_count = 0
state_count = 0
eval_count = 0
ab_count = 0
all_direction = [(1, 1), (-1, -1), (1, 0), (0, 1), (-1, 0), (0, -1), (1, -1), (-1, 1)]
direct_str = {(1, 1): "SE", (-1, -1): "NE", (1, 0): "NW", (1, 0): "S",
              (0, 1): "E", (-1, 0): "N", (0, -1): "W", (1, -1): "SW", (-1, 1): "NE"}


class MY_TTS_State(TTS_State):
    def static_eval(self):
        if USE_CUSTOM_STATIC_EVAL_FUNCTION:
            return self.custom_static_eval()
        else:
            return self.basic_static_eval()

    def basic_static_eval_helper(self, grid):
        # print("enter")
        board = self.board
        height = len(board)  # height of the board
        width = len(board[0])  # width of the board
        w_eval = 0
        b_eval = 0
        (i, j) = grid
        # print("i, j is " + str((i, j)))
        if board[i][j] != '-':
            for direct in check_direction:
                i_c = i
                j_c = j
                num_w = 0
                num_b = 0
                num_f = 0
                i_move = direct[0]
                j_move = direct[1]
                if board[i_c][j_c] == 'W':  # white counter
                    num_w += 1
                if board[i_c][j_c] == 'B':  # black counter
                    num_b += 1
                if board[i_c][j_c] == '-':  # forbidden counter
                    num_f += 1
                    continue
                for k in range(K - 1):
                    i_c += i_move
                    j_c += j_move
                    if i_c < 0 or i_c >= height:  # L-R case
                        i_c = ((i_c + height) % height)
                    if j_c < 0 or j_c >= width:  # T-B case
                        j_c = ((j_c + width) % width)
                    if board[i_c][j_c] == 'W':  # white counter
                        num_w += 1
                    if board[i_c][j_c] == 'B':  # black counter
                        num_b += 1
                    if board[i_c][j_c] == '-':
                        num_f += 1
                if (num_w > 0 and num_b > 0) or num_f > 0:  # block situation
                    continue
                if num_w == 2:
                    # print("W++ and direction is " + str(direct))
                    w_eval += 1
                if num_b == 2:
                    # print("B++ and direction is " + str(direct))
                    b_eval += 1
        # print("return: " + str(w_eval) + ", " + str(b_eval))
        return w_eval, b_eval

    # basic evaluation function
    # instead of implementing C(W, 2) - C(B, 2), I traversed the board only once in order to speed up.
    def basic_static_eval(self):
        board = self.board
        height = len(board)  # height of the board
        width = len(board[0])  # width of the board
        win_w = 0
        win_b = 0
        for i in range(height):
            for j in range(width):
                if board[i][j] != '-':
                    w_eval, b_eval = self.basic_static_eval_helper((i, j))
                    # print("return2: " + str(w_eval) + ", " + str(b_eval))
                    win_w += w_eval
                    win_b += b_eval
                    # print("sum: " + str(win_w) + ", " + str(win_b))
        win_sum = win_w - win_b
        return win_sum

    # my own custom evaluation function
    # Just trying to block other agent's move while considering less on aggressively winning the game.
    def custom_static_eval(self):
        global check_direction, if_block
        if_block = 0
        board = self.board
        height = len(board)  # height of the board
        width = len(board[0])  # width of the board
        win_w = 0
        win_b = 0
        w_eval = 0
        b_eval = 0
        for i in range(height):
            for j in range(width):
                if board[i][j] != '-':
                    for direct in check_direction:
                        i_c = i
                        j_c = j
                        num_w = 0
                        num_b = 0
                        num_f = 0
                        i_move = direct[0]
                        j_move = direct[1]
                        if board[i_c][j_c] == 'W':  # white counter
                            num_w += 1
                        if board[i_c][j_c] == 'B':  # black counter
                            num_b += 1
                        if board[i_c][j_c] == '-':  # forbidden counter
                            num_f += 1
                            continue
                        for k in range(K - 1):
                            i_c += i_move
                            j_c += j_move
                            if i_c < 0 or i_c >= height:  # L-R case
                                i_c = ((i_c + height) % height)
                            if j_c < 0 or j_c >= width:  # T-B case
                                j_c = ((j_c + width) % width)
                            if board[i_c][j_c] == 'W':  # white counter
                                num_w += 1
                            if board[i_c][j_c] == 'B':  # black counter
                                num_b += 1
                            if board[i_c][j_c] == '-':
                                num_f += 1
                        if (num_w > 0 and num_b > 0) or num_f > 0:  # block situation
                            continue
                        if num_w == int(K / 2):
                            w_eval += 1
                        if num_b == int(K / 2):
                            b_eval += 1
                        if num_w >= K - 1:
                            w_eval += 100
                            return 100
                        if num_b >= K - 1:
                            b_eval += 100
                            return -100
                win_w += w_eval
                win_b += b_eval
        win_sum = win_w - win_b
        return win_sum


def get_ready(initial_state, k, what_side_i_play, opponent_moniker):
    global my_side, op_side, opponent, K, INITIAL_STATE
    INITIAL_STATE = initial_state
    K = k
    my_side = what_side_i_play
    op_side = 'B'
    if my_side == 'B':
        op_side = 'W'
    opponent = opponent_moniker
    return "OK"


def who_am_i():
    intro = "Hi, my name is " + name + " who is programmed by " + creator + "\n" + \
            "I don't care if I gonna win. I just want to block your way."
    return intro


def moniker():
    return name


# will be called by game master to make a move based on current_state
# time_limit is default 1.0 but will be set during usage
# opponents_utterance can be used for determining my utterance, but not used in my case
# my utterance have 10 selections for each normal and blocking behavior
# my agent will utter if it made a move that block opponent's way as well as knowing the blocking direction.
# able to tell when to win and give utterance
def take_turn(current_state, opponents_utterance, time_limit=10.0):
    global USE_CUSTOM_STATIC_EVAL_FUNCTION, normal_u_order, block_u_order, if_block
    current_state.__class__ = MY_TTS_State
    who = current_state.whose_turn
    new_who = 'B'
    if who == 'B':
        new_who = 'W'

    # Place a new tile
    location = _find_next_vacancy(current_state.board)
    if location is None:
        return [[False, current_state], "I don't have any moves!"]
    USE_CUSTOM_STATIC_EVAL_FUNCTION = True
    best_eval, new_state, new_location = searcher(current=current_state,
                                                  depth=2,
                                                  a=-math.inf,
                                                  b=math.inf,
                                                  alpha_beta=True,
                                                  time_limit=time_limit)
    new_state.whose_turn = new_who
    board = new_state.board
    height = len(board)  # height of the board
    width = len(board[0])  # width of the board
    i, j = new_location
    if i < 0 or i >= height:  # L-R case
        i = ((i + height) % height)
    if j < 0 or j >= width:  # T-B case
        j = ((j + width) % width)
    new_location = (i, j)
    win = get_win_local(new_state, new_location, K)
    block, direct = get_block(board, new_location)

    # block_utterance = ["3", "4"]
    # normal_utterance = ["1", "2"]

    if win:
        new_utterance = "Well I win... I didn't expect this, but I will take it..."
    elif block:
        new_utterance = block_utterance[block_u_order] + " Direction to " + str(direct)
        block_u_order += 1
        if block_u_order >= len(block_utterance):
            block_u_order = 0

    else:
        new_utterance = normal_utterance[normal_u_order]
        normal_u_order += 1
        if normal_u_order >= len(normal_utterance):
            normal_u_order = 0

    # print("new pos " + str(new_location))
    return [[new_location, new_state], new_utterance]


def get_win_local(s, move, k):
    board, who = s.board, s.whose_turn
    moveI, moveJ = move
    whoWent = board[moveI][moveJ]
    H = len(board)  # height of board = num. of rows
    W = len(board[0])  # width of board = num. of cols.
    plusDirections = [(0, 1), (1, 1), (1, 0), (-1, 1)]  # E, NE, N, NW
    minusDirections = [(0, -1), (-1, -1), (-1, 0), (1, -1)]  # W, SW, S, SE
    for di in range(4):
        dp = plusDirections[di]
        dm = minusDirections[di]
        # count number of Ws (or Bs) in plusDirection:
        count = 1
        i = moveI
        j = moveJ
        for step in range(k - 1):
            i += dp[0]
            if i < 0 or i >= H:
                i = ((i + H) % H)  # toroidal wrap
            j += dp[1]
            if j < 0 or j >= W:
                j = ((j + W) % W)  # toroidal wrap
            if board[i][j] != whoWent:
                break  # the run ends.
            count += 1
        # add in the number of Ws (or Bs) in minusDirection:
        i = moveI
        j = moveJ
        for step in range(k - 1):
            i += dm[0]
            if i < 0 or i >= H:
                i = ((i + H) % H)  # toroidal wrap
            j += dm[1]
            if j < 0 or j >= W:
                j = ((j + W) % W)  # toroidal wrap
            if board[i][j] != whoWent:
                break  # the run ends.
            count += 1
            if count == k:
                break
        if count >= k:
            iWin = i - dm[0]
            jWin = j - dm[1]
            return True

    return False


def get_block(board, new_location):
    height = len(board)  # height of the board
    width = len(board[0])  # width of the board
    for direct in all_direction:
        no_check = 0
        i_c, j_c = new_location
        num_w = 0
        num_b = 0
        i_move = direct[0]
        j_move = direct[1]
        i_c += i_move
        j_c += j_move
        if i_c < 0 or i_c >= height:  # L-R case
            i_c = ((i_c + height) % height)
        if j_c < 0 or j_c >= width:  # T-B case
            j_c = ((j_c + width) % width)
        if board[i_c][j_c] == my_side or board[i_c][j_c] == "-":
            continue
        for k in range(K - 1):
            i_c += i_move
            j_c += j_move
            if i_c < 0 or i_c >= height:  # L-R case
                i_c = ((i_c + height) % height)
            if j_c < 0 or j_c >= width:  # T-B case
                j_c = ((j_c + width) % width)
            if board[i_c][j_c] == 'W':  # white counter
                num_w += 1
            if board[i_c][j_c] == 'B':  # black counter
                num_b += 1
            # if board[i_c][j_c] == "-" and num_b < K - 2:
            # no_check = 1
            # break
        if my_side == "W":
            if num_b >= K - 2:
                # print("do a block")
                return True, direct_str[direct]
        if my_side == "B":
            if num_w >= K - 2:
                return True, direct_str[direct]
    return False, None


# the testing function
# current state will be checked
# use_iterative_deepening_and_time: boolean value that determines if the minimax search will use elastic search methods
# max_ply: max depth
# use_default_move_ordering: boolean value telling if use standard move generation method
# alpha_beta: This field determines if the search should use alpha-beta pruning or not
# time_limit:  This field specifies the time limit (in seconds) my search is under.
# use_custom_static_eval_function: boolean value telling if use the basic eval or my own custom eval function
def parameterized_minimax(current_state=None,
                          use_iterative_deepening_and_time=False,
                          max_ply=2,
                          use_default_move_ordering=False,
                          alpha_beta=False,
                          time_limit=1.0,
                          use_custom_static_eval_function=False):
    # All students, add code to replace these default
    # values with correct values from your agent (either here or below).
    current_state_static_val = -1000.0
    n_states_expanded = 0
    n_static_evals_performed = 0
    max_depth_reached = 0
    n_ab_cutoffs = 0

    # STUDENTS: You may create the rest of the body of this function here.
    global USE_CUSTOM_STATIC_EVAL_FUNCTION

    if use_custom_static_eval_function:
        USE_CUSTOM_STATIC_EVAL_FUNCTION = True
    else:
        USE_CUSTOM_STATIC_EVAL_FUNCTION = False

    current_state.__class__ = MY_TTS_State
    use_default_move_ordering = True
    if not use_iterative_deepening_and_time:  # prepare time limit default t = 10
        time_limit = 10.0
        # max_ply = math.inf
    # print("inner whose " + str(current_state.whose_turn))
    best_eval, new_state, new_location = searcher(current=current_state,
                                                  depth=max_ply,
                                                  a=-math.inf,
                                                  b=math.inf,
                                                  alpha_beta=alpha_beta,
                                                  time_limit=time_limit)
    # print("new move is {} and the basic eval is {}".format(new_location, new_state_static_val))
    # Prepare to return the results, don't change the order of the results
    results = [best_eval, state_count, eval_count, depth_count, ab_count]
    refresh_para()
    # extra

    # Actually return the list of all results...
    return results


# refresh all the global value that will be used by for recording results return by parameterized_minimax
def refresh_para():
    global depth_count, state_count, eval_count, ab_count
    depth_count = 0
    state_count = 0
    eval_count = 0
    ab_count = 0


# Implement searching alogrithm
# current is the root state for searching
# depth is the max_depth that will be reached
# time_limit limit the time that the function will run
# a and b are alpha and beta value what will be applied to pruning
# alpha_beta determines if pruning will be applied
def searcher(current, depth, time_limit, a, b, alpha_beta):
    time_limit = time.time() + time_limit * 0.9
    who = current.whose_turn
    new_who = 'B'
    if who == 'B':
        new_who = 'W'
    white = True
    if who == "B":
        white = False
    best_eval, new_position = minimax_a_b_search(current, a, b, depth, 0, white, time_limit, alpha_beta)
    new_board = copy.deepcopy(current.board)
    if new_position is not None:
        new_board[new_position[0]][new_position[1]] = who
    new_state = TTS_State(new_board, new_who)
    new_state.__class__ = MY_TTS_State
    # print(new_position)
    return best_eval, new_state, new_position


# helper function for searcher
# return next move position, and its state evaluation
def minimax_a_b_search(current, a, b, depth, d, white, time_limit, a_b):
    global depth_count, state_count, eval_count, ab_count, my_side
    new_position = None
    depth_count = max(depth_count, d)  # update depth count
    children = children_states(current, white)

    if depth == d or len(children) == 0:  # base case
        eval_count += 1
        return current.static_eval(), new_position
    state_count += 1  # update state count
    if white:  # maximizer
        max_eval = -math.inf
        for child in children:
            if time.time() >= time_limit:
                if new_position is None:
                    new_position = children[child]
                break
            evalu, temp_position = minimax_a_b_search(child, a, b, depth, d + 1, False, time_limit, a_b)
            # print("evalu {}; max_eval {}".format(evalu, max_eval))
            # print("white {} d {}; child {}".format(white, d, child))
            # eval_count += 1  # update eval count
            if evalu > max_eval:  # update evaluation and returned state
                max_eval = evalu
                new_position = children[child]
                if time.time() >= time_limit:
                    break
                # print("it's a pick the value is " + str(max_eval))
            if a_b:
                a = max(a, evalu)  # update alpha
                if a >= b:
                    ab_count += 1  # update a_b_cut counter
                    break
        return max_eval, new_position
    else:  # minimizer
        min_eval = math.inf
        # children = children_states(current)
        for child in children:
            if time.time() >= time_limit:
                if new_position is None:
                    new_position = children[child]
                break
            evalu, temp_position = minimax_a_b_search(child, a, b, depth, d + 1, True, time_limit, a_b)
            # eval_count += 1  # update eval count
            # print("evalu {}; min_eval{}".format(evalu, min_eval))
            # print("black {} d {}; child {}".format(white, d, child))
            if evalu < min_eval:  # update evaluation and returned state
                min_eval = evalu
                new_position = children[child]
                if time.time() >= time_limit:
                    break
            if a_b:
                b = min(b, evalu)
                if a >= b:
                    ab_count += 1  # update a_b_cut counter
                    break
        return min_eval, new_position


# return a dictionary whose key are children states of current state and value is the move was made to this child.
# white or not determines the move's color and the state's whose_turn field.
# {TTS_state: (i, j)}
def children_states(current, white):
    children_dict = {}
    board = current.board
    new_who = None
    if white:
        who = "W"
        new_who = "B"
    else:
        who = "B"
        new_who = "W"
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] == ' ':
                new_board = copy.deepcopy(board)
                new_board[i][j] = who  # make the step
                next_state = TTS_State(new_board, new_who)  # make a new child state
                # next_state.whose_turn = new_who
                next_state.__class__ = MY_TTS_State
                children_dict[next_state] = (i, j)
    return children_dict


# find next vacancy on given board b
def _find_next_vacancy(b):
    for i in range(len(b)):
        for j in range(len(b[0])):
            if b[i][j] == ' ':
                return (i, j)
    return None


# test a evaluation on a game board imported in
def test():
    get_ready(Game.INITIAL_BOARD, Game.K, 'W', 'haha')
    test_state = TTS_State(board=Game.INITIAL_BOARD, whose_turn="W")
    test_state.__class__ = MY_TTS_State
    # print(my_side)
    result = test_state.static_eval()
    print(result)


# test parameterized_minimax function on a game board imported in
def test_search():
    global USE_CUSTOM_STATIC_EVAL_FUNCTION
    test_state = TTS_State(board=Game.INITIAL_BOARD, whose_turn="W")
    get_ready(Game.INITIAL_BOARD, Game.K, test_state.whose_turn, 'haha')
    test_state.__class__ = MY_TTS_State
    # result = parameterized_minimax(test_state, False, 2, False, False, 1.0, False)
    # USE_CUSTOM_STATIC_EVAL_FUNCTION = False
    start = time.perf_counter()
    test_state.__class__ = MY_TTS_State

    result = parameterized_minimax(current_state=test_state,
                                   use_iterative_deepening_and_time=True,
                                   max_ply=2,
                                   use_default_move_ordering=True,
                                   alpha_beta=True,
                                   time_limit=20.0,
                                   use_custom_static_eval_function=False)
    end = time.perf_counter()
    runtime = end - start
    print("[current_state_static_val, state_count, eval_count, depth_count, ab_count]")
    print("result is {}; runtime is {}".format(result, runtime))
    # print("new state " + str(new_state.static_eval()))
    '''
    who = test_state.whose_turn
    new_who = 'B'
    if who == 'B':
        new_who = 'W'
    location = _find_next_vacancy(new_state.board)
    if location is False:
        return [[False, test_state], "I don't have any moves!"]
    new_state.board[location[0]][location[1]] = new_who
    '''


# print(my_side)

# if __name__ == '__main__':


# test()
# test_search()
