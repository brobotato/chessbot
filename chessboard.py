# create the backdrop of the board
import functools, re


def checker(square1, square2):
    board = []
    for x in range(0, 8, 2):
        for y in range(0, 8, 2):
            board.append([x, y, square1])
    for x in range(1, 9, 2):
        for y in range(1, 9, 2):
            board.append([x, y, square1])
    for x in range(0, 8, 2):
        for y in range(1, 9, 2):
            board.append([x, y, square2])
    for x in range(1, 9, 2):
        for y in range(0, 8, 2):
            board.append([x, y, square2])
    return board


# fill the board with pieces
def fill_pieces(color1, color2):
    piece_set = [
        [-100, -100, color2 + 'rook'],
        [4, 0, color2 + 'king'],
        [0, 0, color2 + 'rook'],
        [1, 0, color2 + 'knight'],
        [2, 0, color2 + 'bishop'],
        [3, 0, color2 + 'queen'],
        [5, 0, color2 + 'bishop'],
        [6, 0, color2 + 'knight'],
        [7, 0, color2 + 'rook'],
        [0, 1, color2 + 'pawn'],
        [1, 1, color2 + 'pawn'],
        [2, 1, color2 + 'pawn'],
        [3, 1, color2 + 'pawn'],
        [4, 1, color2 + 'pawn'],
        [5, 1, color2 + 'pawn'],
        [6, 1, color2 + 'pawn'],
        [7, 1, color2 + 'pawn'],
        [4, 7, color1 + 'king'],
        [0, 7, color1 + 'rook'],
        [1, 7, color1 + 'knight'],
        [2, 7, color1 + 'bishop'],
        [3, 7, color1 + 'queen'],
        [5, 7, color1 + 'bishop'],
        [6, 7, color1 + 'knight'],
        [7, 7, color1 + 'rook'],
        [0, 6, color1 + 'pawn'],
        [1, 6, color1 + 'pawn'],
        [2, 6, color1 + 'pawn'],
        [3, 6, color1 + 'pawn'],
        [4, 6, color1 + 'pawn'],
        [5, 6, color1 + 'pawn'],
        [6, 6, color1 + 'pawn'],
        [7, 6, color1 + 'pawn'],
    ]
    return piece_set


# search for a piece that matches a set of coordinates and color
def search_piece(coords, color, pieces):
    piece_set = [piece[0:2] for piece in pieces]
    if coords in piece_set:
        if pieces[piece_set.index(coords)][2][0] == color:
            return piece_set.index(coords)
    return False


# format a move to algebraic notation
def format_move(move, capture, check, checkmate):
    formatted_move = ''
    end = ''
    if 'king' in move[0]:
        formatted_move += 'K'
    elif 'queen' in move[0]:
        formatted_move += 'Q'
    elif 'rook' in move[0]:
        formatted_move += 'R'
    elif 'bishop' in move[0]:
        formatted_move += 'B'
    elif 'knight' in move[0]:
        formatted_move += 'N'
    elif 'pawn' in move[0]:
        pass
    if capture:
        formatted_move += 'x'
    if check:
        end += '+'
        if checkmate:
            end += '+'
    formatted_move += ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h'][move[1][0]] + str(8 - move[1][1]) + end
    return formatted_move


# log moves in algebraic notation
def log_moves(move_set):
    if len(move_set) % 2 == 0:
        message = ''
        message += str(len(move_set) / 2)[:-1] + ' ' + move_set[-2] + ' ' + move_set[-1]
        return message
    return None


# checks for colliding pieces and deletes them
def check_collision(current_board, current_player):
    for piece in current_board:
        for piece2 in current_board:
            if piece[0:2] == piece2[0:2] and piece[2] != piece2[2]:
                if current_player == 0:
                    if piece[2][0] == 'w':
                        current_board.remove(piece)
                    elif piece2[2][0] == 'w':
                        current_board.remove(piece2)
                if current_player == 1:
                    if piece[2][0] == 'b':
                        current_board.remove(piece)
                    elif piece2[2][0] == 'b':
                        current_board.remove(piece2)
                return True
    return False


def board_to_url(current_board):
    fen = []
    fen_rename = {'b_rook': 'r', 'b_knight': 'n', 'b_bishop': 'b', 'b_queen': 'q', 'b_king': 'k', 'b_pawn': 'p',
                  'w_rook': 'R', 'w_knight': 'N', 'w_bishop': 'B', 'w_queen': 'Q', 'w_king': 'K', 'w_pawn': 'P'}
    for x in range(8):
        fen.append(['1', '1', '1', '1', '1', '1', '1', '1'])
    for x in current_board[1:]:
        fen[x[1]][x[0]] = fen_rename[x[2]]
    for row in fen:
        rowstring = re.split('(\d+)', functools.reduce(lambda x, y: x + y, row))
        for group in rowstring:
            if group.isdigit():
                rowstring[rowstring.index(group)] = str(functools.reduce(lambda x, y: x + y, [int(b) for b in group]))
        fen[fen.index(row)] = functools.reduce(lambda x, y: x + y, rowstring)
    fenurl = str()
    for row in fen:
        fenurl += row + '/'
    fenurl = 'http://www.fen-to-image.com/image/36/double/coords/' + fenurl[0:-1]
    return fenurl
