import discord
from chessboard import *
from valid_moves import *

api_key = open('./api_key.txt').read()

def normalize(position):
    return [ord(position[0]) - 97, 8 - int(position[1])]


class game_data:
    chessboard = [[-1, -1, 'board']] + checker('w_square', 'b_square')

    pieces = fill_pieces('w_', 'b_')
    pieces_last = deepcopy(pieces)


    current_piece = False
    current_player = 0
    players = {0: 'w', 1: 'b'}

    check = [0, 0]
    checking_pieces = []
    checked = False
    checkmated = False
    captured = False

    moves = []
    moves_formatted = []
    moves_processed = []

    def reset(self):
        self.chessboard = [[-1, -1, 'board']] + checker('w_square', 'b_square')

        self.pieces = fill_pieces('w_', 'b_')
        self.pieces_last = deepcopy(self.pieces)

        self.current_piece = False
        self.current_player = 0
        self.players = {0: 'w', 1: 'b'}

        self.check = [0, 0]
        self.checking_pieces = []
        self.checked = False
        self.checkmated = False
        self.captured = False

        self.moves = []
        self.moves_formatted = []
        self.moves_processed = []


client = discord.Client()


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')


global data_global
data_global = game_data()


@client.event
async def on_message(message):
    if message.content.startswith('!newgame'):
        data_global.reset()
        data = data_global
        await client.send_message(message.channel, board_to_url(data.pieces))
    if message.content.startswith('!move '):
        data = data_global
        message_data = message.content.split()
        move = [message_data[1], message_data[2]]
        try:
            if move[0][0] in ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h'] and int(move[0][1]) in range(1, 9) and \
                            move[1][0] in ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h'] and int(move[1][1]) in range(1, 9):
                if not data.checkmated:
                    pos1 = normalize(move[0])
                    pos2 = normalize(move[1])
                    data.current_piece = search_piece(pos1, data.players[data.current_player], data.pieces)
                    if pos2 in valid_moves(data.pieces[data.current_piece], data.pieces):
                        data.pieces[data.current_piece][0:2] = pos2
                        if check_collision(data.pieces, (data.current_player + 1) % 2):
                            data.captured = True
                        else:
                            data.captured = False
                        check, checking_pieces = in_check(data.pieces)
                        if check[data.current_player]:
                            data.pieces = deepcopy(data.pieces_last)
                        else:
                            if check[(data.current_player + 1) % 2]:
                                data.checked = True
                                data.checkmated = in_checkmate(data.pieces, data.check)
                            else:
                                data.checked = False
                            data.moves.append([data.pieces[data.current_piece][2], pos2, data.current_piece])
                            data.moves_formatted.append(
                                format_move(data.moves[-1], data.captured, data.checked, data.checkmated))
                            data.moves_processed.append(log_moves(data.moves_formatted))
                            data.current_player = (data.current_player + 1) % 2
                            data.current_piece = False
                            data.pieces_last = deepcopy(data.pieces)
                            await client.send_message(message.channel, board_to_url(data.pieces))
        except ValueError:
            pass
    if message.content.startswith('!data'):
        data = data_global
        if data.checked:
            if data.checkmated:
                await client.send_message(message.channel, 'Gameover! {} won through checkmate!'.format(
                    ['White', 'Black'][(data.current_player + 1) % 2]))
            else:
                await client.send_message(message.channel,
                                          '{} is in check!'.format(['White', 'Black'][data.current_player]))
        else:
            await client.send_message(message.channel, 'Neither player is currently in check.')
    if message.content.startswith('!movelist'):
        data = data_global
        for move in data.moves_processed:
            if move != None:
                await client.send_message(message.channel, '{}'.format(move))


client.run(api_key)
