def minimax_search(current, depth, d, side, max_time, custom):
    global depth_count, state_count, eval_count, ab_count, new_position
    depth_count = max(depth_count, d)  # update depth count
    if depth == d:  # base case
        return current.static_eval(), current
    state_count += 1  # update state count

    next_state = None
    if side:  # maximizer
        max_eval = -math.inf
        children = children_states(current, side)
        # print(next_position)
        # next_state = current
        for child in children:
            evalu, result_child = minimax_search(child, depth, d + 1, False)

            eval_count += 1  # update eval count
            if evalu > max_eval:
                max_eval = evalu
                next_state = result_child
                if d == 0:
                    new_position = children[child]
                    print("position is " + str(new_position))
                # print("determined W" + str(next_state))
                # print(max_eval)
            print(max_eval, evalu)
            print("child is " + str(child))

        return max_eval, next_state

    else:  # minimizer
        min_eval = math.inf
        opp = "B"
        if side == "B":
            opp = "W"
        children = children_states(current, opp)
        # next_state = current
        for child in children:
            # print("determined B" + str(child))
            evalu, result_child = minimax_search(child, depth, d + 1, True)
            # next_state = prev_state
            eval_count += 1
            if evalu < min_eval:
                min_eval = evalu
                next_state = result_child
                if d == 0:
                    children[child]
                # print("determined B" + str(next_state))
                # print(min_eval)
        return min_eval, next_state


def children_states(current, w_b):
    children_dict = {}
    current_cp = current.copy()
    who = current.whose_turn
    next_position = _find_next_vacancy(current_cp.board)
    # print("inner1 " + str(next_position))
    while next_position is not None:
        i, j = next_position[0], next_position[1]
        current_cp.board[i][j] = w_b  # record the iteration
        next_state = current.copy()  # make a new child state
        next_state.board[i][j] = w_b
        next_state.__class__ = MY_TTS_State
        children_dict[next_state] = next_position
        next_position = _find_next_vacancy(current_cp.board)
    # print("inner2 " + str(children_dict))
    return children_dict


def minimax_search(current, depth, d, white, time_limit):
    global depth_count, state_count, eval_count, ab_count
    depth_count = max(depth_count, d)  # update depth count
    children = children_states(current, white)
    if depth == d or len(children) == 0:  # base case
        return current.static_eval()
    state_count += 1  # update state count

    if white:  # maximizer
        max_eval = -math.inf
        # children = children_states(current, "W")
        for child in children:
            if time.time() >= time_limit:
                break
            evalu = minimax_search(child, depth, d + 1, False, time_limit)  # recurrsion
            eval_count += 1  # update eval count
            if evalu >= max_eval:
                max_eval = evalu
                if d == 0:
                    new_position = children[child]
                    # print("position is " + str(new_position))

        return max_eval

    else:  # minimizer
        min_eval = math.inf
        # children = children_states(current, "B")
        for child in children:
            if time.time() >= time_limit:
                break
            # print("Depth-{}-child-{}".format(d, child))
            evalu = minimax_search(child, depth, d + 1, True, time_limit)  # recurrsion
            # print("Result_child-{}".format(result_child))
            eval_count += 1
            if evalu <= min_eval:
                # print("Minimizer  evalu:{} min_eval:{}".format(evalu, min_eval))
                min_eval = evalu
                if d == 0:
                    new_position = children[child]
                    # print("NEW position is " + str(new_position) + "\n")
        return min_eval


def minimax_a_b_search(current, a, b, depth, d, white, time_limit, a_b):
    global depth_count, state_count, eval_count, ab_count, my_side
    new_position = None
    depth_count = max(depth_count, d)  # update depth count
    children = children_states(current, white)
    if depth == d or len(children) == 0:  # base case
        return current.static_eval(), new_position
    state_count += 1  # update state count
    if white:  # maximizer
        max_eval = -math.inf
        # children = children_states(current)
        for child in children:
            if time.time() >= time_limit:
                break
            evalu, temp_position = minimax_a_b_search(child, a, b, depth, d + 1, False, time_limit, a_b)
            eval_count += 1  # update eval count
            # max_eval = max(evalu, max_eval)
            if evalu > max_eval:  # update evaluation and returned state
                max_eval = evalu
                new_position = children[child]
            if a_b:
                a = max(a, evalu)  # update alpha
                if a >= b:
                    ab_count += 1
                    break
        # print("mark " + str(new_position))
        return max_eval, new_position
    else:  # minimizer
        min_eval = math.inf
        # children = children_states(current)
        for child in children:
            if time.time() >= time_limit:
                break
            evalu, temp_position = minimax_a_b_search(child, a, b, depth, d + 1, True, time_limit, a_b)
            # print("black evalu {}, min eval {}".format(evalu, min_eval))
            if evalu < min_eval:  # update evaluation and returned state
                min_eval = evalu
                # print("a {}; b{}".format(a, b))
                # print("updated black evalu {}, min eval {}".format(evalu, min_eval))
                new_position = children[child]
            if a_b:
                b = min(b, evalu)
                if a >= b:
                    ab_count += 1
                    break
        return min_eval, new_position

def children_states(current, white):
    children_dict = {}
    current_cp = current.copy()
    if white:
        who = "W"
        # new_who = "B"
    else:
        who = "B"
        # new_who = "W"
    # who = current.whose_turn
    next_position = _find_next_vacancy(current_cp.board)
    # print("inner1 " + str(next_position))
    while next_position is not None:
        i, j = next_position[0], next_position[1]
        current_cp.board[i][j] = who  # record the iteration
        next_state = current.copy()  # make a new child state
        next_state.board[i][j] = who  # make the step
        # next_state.whose_turn = new_who
        next_state.__class__ = MY_TTS_State
        children_dict[next_state] = next_position
        next_position = _find_next_vacancy(current_cp.board)
    # print("inner2 " + str(children_dict))
    return children_dict


    def custom_static_eval(self):
        global check_direction, if_block
        if_block = 0
        board = self.board
        height = len(board)  # height of the board
        width = len(board[0])  # width of the board
        win_sum = 0
        win_w = 0
        win_b = 0
        # mid_i = int(height / 2)
        # mid_j = int(width / 2)
        for i in range(height):
            for j in range(width):
                for direct in check_direction:
                    i_c = i
                    j_c = j
                    num_w = 0
                    num_b = 0
                    num_f = 0
                    single_w = 0
                    single_b = 0
                    i_move = direct[0]
                    j_move = direct[1]
                    if board[i_c][j_c] == 'W':  # white counter
                        num_w += 1
                    if board[i_c][j_c] == 'B':  # black counter
                        num_b += 1
                    if board[i_c][j_c] == '-':  # forbidden counter
                        num_f += 1
                    for k in range(K - 1):
                        i_c += i_move
                        j_c += j_move
                        if i_c < 0 or i_c >= height:  # L-R case
                            i_c = ((i_c + height) % height)
                        if j_c < 0 or j_c >= width:  # T-B case
                            j_c = ((j_c + width) % width)
                        if board[i_c][j_c] == 'W':  # white counter
                            num_w += 1
                            single_w += 1
                        if board[i_c][j_c] == 'B':  # black counter
                            num_b += 1
                            single_b += 1
                        if board[i_c][j_c] == '-':
                            num_f += 1
                            continue
                        if single_w >= K - 2:
                            if_block = 1
                            return 100
                        if single_b >= K - 2:
                            if_block = 1
                            return -100
                        win_w = num_w
                        win_b = num_b
                        single_b = 0
                        single_w = 0
        win_sum = win_w - win_b
        return win_sum

    def custom_static_eval_helper(self, grid):
        # print("enter")
        board = self.board
        height = len(board)  # height of the board
        width = len(board[0])  # width of the board
        w_eval = 0
        b_eval = 0
        w_block = 0
        b_block = 0
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
                if num_f > 0:  # block situation
                    continue
                if num_w >= 0:
                    # print("W++ and direction is " + str(direct))
                    w_eval += num_w
                if num_b >= 0:
                    # print("B++ and direction is " + str(direct))
                    b_eval += num_b
                # if my_side == "W":
                #     if num_w == K - 1:
                #         w_eval = 1000
                #         b_eval = 0
                #         break
                if num_w >= K - 3:
                    w_eval += 100
                    w_block = 1
                    b_block = 0
                    break
                if num_b >= K - 3:
                    b_eval += 100
                    w_block = 0
                    b_block = 1
                    break
        # print("return: " + str(w_eval) + ", " + str(b_eval))
        return w_eval, b_eval, w_block, b_block

    def custom_static_eval(self):
        global check_direction, if_block
        if_block = 0
        board = self.board
        height = len(board)  # height of the board
        width = len(board[0])  # width of the board
        win_sum = 0
        win_w = 0
        win_b = 0
        # mid_i = int(height / 2)
        # mid_j = int(width / 2)
        for i in range(height):
            for j in range(width):
                if board[i][j] == op_side:

        return win_sum