MOVES = [(-1,-1), (-1,0), (-1,1),(0,-1),(0,1),(1,-1), (1,0), (1,1)]
PAWN_MOVES = [(-1,0), (0,-1),(0,1), (1,0)]

INIT_TO_CODE = {'p':2, 'P':3, 'c':4, 'C':5, 'l':6, 'L':7, 'i':8, 'I':9,
  'w':10, 'W':11, 'k':12, 'K':13, 'f':14, 'F':15, '-':0}

# Used in printing out states:

CODE_TO_INIT = {0:'-',2:'p',3:'P',4:'c',5:'C',6:'l',7:'L',8:'i',9:'I',
  10:'w',11:'W',12:'k',13:'K',14:'f',15:'F'}
REGULARS = [2,3,4,5,10,11,14,15]
ALL_CAPTURE = {}

SCORES = {0: 0,2: 200, 3: 200, 4: 200, 5: 200, 6: 300, 7: 300, 8: 500, 9: 500,
          10: 300, 11: 300,12: 800,13: 800,14: 100, 15: 100}

def parse(bs): # bs is board string
  '''Translate a board string into the list of lists representation.'''
  b = [[0,0,0,0,0,0,0,0] for r in range(8)]
  rs9 = bs.split("\n")
  rs8 = rs9[1:] # eliminate the empty first item.
  for iy in range(8):
    rss = rs8[iy].split(' ')
    for jx in range(8):
      b[iy][jx] = INIT_TO_CODE[rss[jx]]
  return b

INITIAL = parse('''
c l i w k i l f
p p p p p p p p
- - - - - - - -
- - - - - - - -
- - - - - - - -
- - - - - - - -
P P P P P P P P
F L I W K I L C
''')

V1 = parse('''
- - - - - - - -
- - - k - - - -
- - - P - C - -
- - - p w - - -
- K f - - - P -
- - - i - - l -
- - - - - - P -
- - - W - - - -
''')


def static_eval(board, whose_turn):
    global ALL_CAPTURE
    ALL_CAPTURE = {}
    score = 0
    total_count = 0
    king_position = (0,0)
    king_op_position = (0,0)
    # traverse through the board
    for i in range(8):
        for j in range(8):
            # adding count and piece priority to total score
            # check possible new captures or new losses
            curr_piece = board[i][j]
            if curr_piece != 0:
                if curr_piece % 2 == whose_turn:
                    if curr_piece - whose_turn in REGULARS:
                        regular_move(board, i, j, whose_turn)
                    if curr_piece - whose_turn == 6:
                        leaper(board, i, j, whose_turn)
                    if curr_piece - whose_turn == 8:
                        imitator(board, i, j, whose_turn)
                    if curr_piece - whose_turn == 12:
                        king_cap = king_capture(board, i, j, whose_turn)
                        king_position = (i, j)
                        if king_cap:
                            for cap in king_cap:
                                ALL_CAPTURE[cap] = king_cap[cap]
                    if ALL_CAPTURE:
                        print((i,j))
                        print(ALL_CAPTURE)
                        for each_cap in ALL_CAPTURE:
                            cap_piece = ALL_CAPTURE[each_cap]
                            score += SCORES[cap_piece]
                    score += SCORES[curr_piece]
                    score += 50 + 6.25 * abs(i - 4) + 6.25 * abs(j - 4) # center control
                    ALL_CAPTURE = {}
                else:
                    if curr_piece - whose_turn + 1 in REGULARS:
                        regular_move(board, i, j, 1-whose_turn)
                    if curr_piece - whose_turn + 1 == 6:
                        leaper(board, i, j, 1-whose_turn)
                    if curr_piece - whose_turn + 1 == 8:
                        imitator(board, i, j, 1-whose_turn)
                    if curr_piece - whose_turn + 1 == 12:
                        king_cap = king_capture(board, i, j, 1-whose_turn)
                        king_op_position = (i, j)
                        if king_cap:
                            for cap in king_cap:
                                ALL_CAPTURE[cap] = king_cap[cap]
                    if ALL_CAPTURE:
                        print((i, j))
                        print(ALL_CAPTURE)
                        for each_cap in ALL_CAPTURE:
                            cap_piece = ALL_CAPTURE[each_cap]
                            score -= SCORES[cap_piece]
                    score -= SCORES[curr_piece]
                    score -= 50 + 6.25 * abs(i - 4) + 6.25 * abs(j - 4)
                    ALL_CAPTURE = {}
                # check king position and
                if curr_piece == 12 + whose_turn:
                    king_position = (i, j)
                if curr_piece == 12 + 1 - whose_turn:
                    king_op_position = (i, j)
                total_count += 1
    # increase the score if the king is close to the center when not many pieces left
    if total_count < 16:
        score += 200 - 25*abs(king_position[0]-4) - 25*abs(king_position[1]-4)
        score -= 200 - 25*abs(king_op_position[0]-4) - 25*abs(king_op_position[1]-4)
    ALL_CAPTURE = {}
    return score

# get all children for a state
def all_children(board, whose_turn):
    res = []
    # check each piece for a side
    for i in range(8):
        for j in range(8):
            curr_piece = board[i][j]
            # eliminate pieces to check
            if curr_piece == 0:
                continue  # try to move empty space
            elif (curr_piece - whose_turn) % 2 != 0:
                continue  # try to move other player's piece
            elif isFrozen(board, i, j, whose_turn):
                continue
            else:
                # get children for each position
                curr_res = get_children(board, i, j, whose_turn)
                if curr_res:
                    for each_child in curr_res:
                        res.append(each_child)
    return res

def get_children(board, row, col, whose_turn):
    res = []
    moves = MOVES
    curr_piece = board[row][col]
    # if the piece is a pawn, coordinator, withdrawer, freezer
    # not allowed to go over and only can land in empty space
    if curr_piece in REGULARS:
        res = regular_move(board, row, col, whose_turn)
    elif curr_piece == 12 or curr_piece == 13:
        res = king(board, row, col, whose_turn)
    elif curr_piece == 6 or curr_piece == 7:
        res = leaper(board, row, col, whose_turn)
    elif curr_piece == 8 or curr_piece == 9:
        res = imitator(board, row, col, whose_turn)
    return res

def regular_move(board, row, col, whose_turn):
    global ALL_CAPTURE
    res = []
    curr_piece = board[row][col]
    moves = MOVES
    if curr_piece == 2 or curr_piece == 3:
        moves = PAWN_MOVES
    for move in moves:
        for multi in range(8):
            mx = move[0] * (1 + multi)
            my = move[1] * (1 + multi)
            new_row = row + mx
            new_col = col + my
            if new_row < 0 or new_row > 7 or new_col < 0 or new_col > 7:
                break
            elif board[new_row][new_col] != 0:
                break
            else:
                new_board = copy(board)  # new board to make changes
                # check captures
                capture_dict = {}
                if curr_piece == 2 or curr_piece == 3: # pawn case
                    capture_dict = pawn_capture(board, new_row, new_col, whose_turn)
                elif curr_piece == 4 or curr_piece == 5: # coordinator case
                    capture_dict = coordinator_capture(board, new_row, new_col, whose_turn)
                elif curr_piece == 10 or curr_piece == 11:    # withdrawer case
                    capture_dict = withdrawer_capture(board, row, col, move[0], move[1], whose_turn)
                # freezer cannot capture
                if capture_dict:
                    for cap_coord in capture_dict:
                        x, y = cap_coord
                        new_board[x][y] = 0
                        ALL_CAPTURE[cap_coord] = capture_dict[cap_coord]
                # set original pawn position to empty
                new_board[row][col] = 0
                # set new position to pawn
                new_board[new_row][new_col] = curr_piece
                #new_state = BC_state(new_board, 1 - whose_turn)
                #res.append(new_state)
                res.append(new_board)
    return res


def pawn_capture(board, new_row, new_col, whose_turn):
    capture = {}
    for ad in PAWN_MOVES:
        adx, ady = ad
        if new_row+2*adx >= 0 and new_row+2*adx < 8 and new_col+2*ady >= 0 and new_col+2*ady < 8:
            # check if opponent is in between curr piece and friendly piece
            ad = board[new_row + adx][new_col + ady]
            if board[new_row + adx][new_col + ady] % 2 != whose_turn and board[new_row + adx][new_col + ady] != 0:
                if board[new_row + 2 * adx][new_col + 2 * ady] % 2 == whose_turn and board[new_row + 2 * adx][new_col + 2 * ady] != 0:
                    capture[(new_row + adx, new_col + ady)] = board[new_row + adx][new_col + ady]
    return capture


def coordinator_capture(board, new_row, new_col, whose_turn):
    # check if there are any opponent pieces on current row
    capture = {}
    for i in range(8):
        # opponent on current row
        if board[new_row][i] != 0:
            if i != new_col and board[new_row][i] % 2 != whose_turn:
                # check if king is on this column
                for j in range(8):
                    if board[j][i] == 12 + whose_turn:
                        capture[(new_row, i)] = board[new_row][i]
    # check if there are any opponent pieces on current column
    for i in range(8):
        # opponent on current row
        new_piece = board[i][new_col]
        same = new_piece % 2
        if board[i][new_col] != 0:
            if i != new_row and board[i][new_col] % 2 != whose_turn:
                # check if king is on this column
                for j in range(8):
                    if board[i][j] == 12 + whose_turn:
                        capture[(i, new_col)] = board[i][new_col]
    return capture


def withdrawer_capture(board, row, col, move_x, move_y, whose_turn):
    capture = {}
    opposite_x = row - move_x
    opposite_y = col - move_y
    if opposite_x >= 0 and opposite_x < 8 and opposite_y >= 0 and opposite_y < 8:
        # check if opponent in opposite direction and is not a freezer
        if board[opposite_x][opposite_y] % 2 != whose_turn and board[opposite_x][opposite_y] % 2 != 0 \
                and board[opposite_x][opposite_y] != 14 + (1 - whose_turn):
            capture[(opposite_x, opposite_y)] = board[opposite_x][opposite_y]
    return capture


def king_capture(board, row, col, whose_turn):
    capture = {}
    for move in MOVES:
        new_row = row + move[0]
        new_col = col + move[1]
        if new_row >= 0 and new_row < 8 and new_col >= 0 and new_col < 8:
            if board[new_row][new_col] % 2 != whose_turn and board[new_row][new_col] % 2 != 0:
                capture[(new_row, new_col)] = board[new_row][new_col]
                ALL_CAPTURE[(new_row, new_col)] = board[new_row][new_col]
    return capture


def king(board, row, col, whose_turn):
    global ALL_CAPTURE
    capture_dict = {}
    res = []
    possible_pos = []
    for move in MOVES:
        new_row = row + move[0]
        new_col = col + move[1]
        if new_row >= 0 and new_row < 8 and new_col >= 0 and new_col < 8:
        # if new space empty or opposite piece, can move to that position
            if board[new_row][new_col] == 0 or board[new_row][new_col] % 2 != whose_turn:
                # check if king will be captured if moved to new position
                possible_pos.append((new_row, new_col))
                for i in range(8):
                    for j in range(8):
                        if board[i][j] % 2 != whose_turn:
                            capture_dict = {}
                            if board[i][j] in REGULARS:
                                regular_move(board, i, j, 1-whose_turn)
                                capture_dict = ALL_CAPTURE
                            elif board[i][j] == 12 + (1 - whose_turn):
                                capture_dict = king_capture(board, i, j, 1 - whose_turn)
                            elif board[i][j] == 6 + (1 - whose_turn):
                                leaper(board, i, j, 1-whose_turn)
                                capture_dict = ALL_CAPTURE
                            for capture_coord in capture_dict:
                                if capture_coord == (new_row, new_col):
                                    if capture_dict[capture_coord] == 12 + whose_turn:
                                        possible_pos.remove((new_row, new_col))
    if possible_pos:
        for each_coor in possible_pos:
            new_board = copy(board)
            x,y = each_coor
            new_board[x][y] = 12 + whose_turn
            new_board[row][col] = 0
            # new_state = BC_state(new_board, 1 - whose_turn)
            # res.append(new_state)
            res.append(new_board)
    ALL_CAPTURE = {}
    return res

def leaper(board, row, col, whose_turn):
    capture_dict = {}
    res = []
    encounter = False
    capture = (0, 0)
    for move in MOVES:
        for multi in range(8):
            mx = move[0] * (1 + multi)
            my = move[1] * (1 + multi)
            new_row = row + mx
            new_col = col + my
            # new position within board
            if new_row >= 0 and new_row < 8 and new_col >= 0 and new_col < 8:
                new_board = copy(board)
                # if new position is not empty
                if not board[new_row][new_col] == 0:
                    # if new position is friendly piece, break
                    if board[new_row][new_col] % 2 == whose_turn:
                        break
                    # if new position opposite piece
                    elif board[new_row][new_col] % 2 != whose_turn:
                        # if already encountered an opposite piece, break
                        if encounter:
                            break
                        # else set encounter to true, set capture coordinate and continue
                        else:
                            encounter = True
                            capture = (new_row, new_col)
                            continue
                # if new position is empty
                else:
                    # if have encountered an opposite piece, perform capture
                    if encounter:
                        capture_dict[capture] = board[capture[0]][capture[1]]
                        ALL_CAPTURE[capture] = board[capture[0]][capture[1]]
                        new_board[capture[0]][capture[1]] = 0
                    # set new position to leaper
                    new_board[new_row][new_col] = 6 + whose_turn
                    new_board[row][col] = 0
                    # new_state = BC_state(new_board, 1 - whose_turn)
                    # res.append(new_state)
                    res.append(new_board)
        encounter = False
    return res

def leaper_capture(board, row, col, new_row, new_col, whose_turn):
    capture = {}
    mx = new_row - row
    my = new_col - col
    multi = max(abs(mx), abs(my))
    move_x = round(mx/multi)
    move_y = round(my/multi)
    encounter = False
    nx = row
    ny = col
    for i in range(multi):
        nx += move_x
        ny += move_y
        # if new position is not empty
        if not board[nx][ny] == 0:
            # if new position is friendly piece, break
            if board[nx][ny] % 2 == whose_turn:
                break
            # if new position opposite piece
            elif board[nx][ny] % 2 != whose_turn:
                # if already encountered an opposite piece, break
                if encounter:
                    return {}
                # else set encounter to true, set capture coordinate and continue
                else:
                    encounter = True
                    capture[(nx, ny)] = board[nx][ny]
    return capture

    # if new position is empty



# if have encountered an opposite piece, perform capture

def imitator(board, row, col, whose_turn):
    global ALL_CAPTURE
    res = []
    regular = True
    has_leapcap = False
    encounter = False
    for move in MOVES:
        for multi in range(8):
            mx = move[0] * (1 + multi)
            my = move[1] * (1 + multi)
            new_row = row + mx
            new_col = col + my
            if new_row < 0 or new_row > 7 or new_col < 0 or new_col > 7:
                break
            # if not empty or piece and is a friendly piece, cannot land
            elif board[new_row][new_col] != 0 and board[new_row][new_col] % 2 == whose_turn:
                break
            # if new position is opposite piece, set regular to false
            # only check leaper and king capture case
            elif not board[new_row][new_col] == 12 + 1 - whose_turn and board[new_row][new_col] % 2 != whose_turn:
                regular = False
                encounter = True
                continue
            else:
                new_board = copy(board)  # new board to make changes
                capture_dict = {}
                if regular:
                    # check captures
                    # check capture as a pawn
                    pawn_cap = pawn_capture(board, new_row, new_col, whose_turn)
                    if pawn_cap:
                        for cap_coor in pawn_cap:
                            # if capture is opposite pawn
                            if pawn_cap[cap_coor] == 2 + 1 - whose_turn:
                                capture_dict[cap_coor] = 2 + 1 - whose_turn
                                ALL_CAPTURE[cap_coor] = 2 + 1 - whose_turn
                    coordi_cap = coordinator_capture(board, new_row, new_col, whose_turn)
                    if coordi_cap:
                        for cap_coor in coordi_cap:
                            # if capture is opposite coordinator
                            if coordi_cap[cap_coor] == 4 + 1 - whose_turn:
                                capture_dict[cap_coor] = 4 + 1 - whose_turn
                                ALL_CAPTURE[cap_coor] = 4 + 1 - whose_turn
                    with_cap = withdrawer_capture(board, row, col, move[0], move[1], whose_turn)
                    if with_cap:
                        for cap_coor in with_cap:
                            # if capture is opposite withdrawer
                            if with_cap[cap_coor] == 10 + 1 - whose_turn:
                                capture_dict[cap_coor] = 10 + 1 - whose_turn
                                ALL_CAPTURE[cap_coor] = 10 + 1 - whose_turn
                # check if capture can be a king
                if multi == 0:
                    if board[new_row][new_col] == 12 + 1 - whose_turn:
                        #capture_dict[(new_row, new_col)] = 12 + 1 - whose_turn
                        ALL_CAPTURE[cap_coor] = 12 + 1 - whose_turn
                        new_board[new_row][new_col] = 8 + whose_turn
                        new_board[row][col] = 0
                        res.append(new_board)
                        break
                leaper_cap = leaper_capture(board, row, col, new_row, new_col, whose_turn)
                if leaper_cap:
                    has_leapcap = True
                    for cap_coor in leaper_cap:
                        # if capture is opposite coordinator
                        if leaper_cap[cap_coor] == 6 + 1 - whose_turn:
                            capture_dict[cap_coor] = 6 + 1 - whose_turn
                            ALL_CAPTURE[cap_coor] = 6 + 1 - whose_turn
                        else:
                            has_leapcap = False
                if regular or has_leapcap:
                    if capture_dict:
                        for each_cap in capture_dict:
                            x, y = each_cap
                            nx = x
                            ny = y
                            # this step does not work
                            new_board[nx][ny] = 0
                            #ALL_CAPTURE = capture_dict
                    new_board[row][col] = 0
                    new_board[new_row][new_col] = 8 + whose_turn
                    res.append(new_board)
                if not has_leapcap and encounter:
                    encounter = False
                    break
        regular = True
    return res

def isFrozen(board, row, col, whose_turn):
    for move in MOVES:
        mx, my = move
        curr_x = row + mx
        curr_y = col + my
        if curr_x < 0 or curr_x > 7 or curr_y < 0 or curr_y > 7:
            continue
        if board[curr_x][curr_y] - (1-whose_turn) == 14:
            return True
    return False

def copy(board):
    return [r[:] for r in board]

def to_string(board):
    s = ''
    for r in range(8):
        for c in range(8):
            s += CODE_TO_INIT[board[r][c]] + " "
        s += "\n"
    return s


list = all_children(V1, 1)
for item in list:
    print(to_string(item))


print(static_eval(V1, 1))