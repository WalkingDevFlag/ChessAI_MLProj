import chess
import numpy as np
import re
import chess.engine
import pandas as pd
import csv
import os

'''def save_variable(variable, filename):
    if isinstance(variable, np.ndarray):
        np.savez(filename, data=variable)
    elif isinstance(variable, list):
        np.savez(filename, data=np.array(variable))
    elif isinstance(variable, dict):
        np.savez(filename, **variable)
    else:
        np.savez(filename, data=np.array([variable]))
'''

def save_variable(variable, filename):
    if isinstance(variable, np.ndarray):
        if os.path.isfile(filename + ".npz"):
            with np.load(filename + ".npz") as existing_data:
                merged_data = {**existing_data, "data": variable}
                np.savez(filename, **merged_data)
        else:
            np.savez(filename, data=variable)
    elif isinstance(variable, list):
        if os.path.isfile(filename + ".npz"):
            with np.load(filename + ".npz") as existing_data:
                existing_list = existing_data["data"]
                merged_list = existing_list + variable
                np.savez(filename, data=np.array(merged_list))
        else:
            np.savez(filename, data=np.array(variable))
    elif isinstance(variable, dict):
        if os.path.isfile(filename + ".npz"):
            with np.load(filename + ".npz") as existing_data:
                merged_data = {**existing_data, **variable}
                np.savez(filename, **merged_data)
        else:
            np.savez(filename, **variable)
    else:
        if os.path.isfile(filename + ".npz"):
            with np.load(filename + ".npz") as existing_data:
                existing_variable = existing_data["data"]
                merged_variable = np.concatenate((existing_variable, np.array([variable])))
                np.savez(filename, data=merged_variable)
        else:
            np.savez(filename, data=np.array([variable]))
            

def append_to_csv(file_path, data):
    # Check if the file exists
    try:
        with open(file_path, 'r') as file:
            reader = csv.reader(file)
            # Check if the file is empty
            if not any(row for row in reader):
                write_mode = 'w'  # If the file is empty, write mode is used
            else:
                write_mode = 'a'  # If the file has existing data, append mode is used
    except FileNotFoundError:
        write_mode = 'w'  # If the file doesn't exist, create a new file

    with open(file_path, write_mode, newline='') as file:
        writer = csv.writer(file)
        if isinstance(data, dict):
            if write_mode == 'w':  # Write header if it's a new file
                writer.writerow(data.keys())
            writer.writerow(data.values())
        elif isinstance(data, tuple):
            writer.writerow(data)


'''def get_board_array(board):
    board_array = np.zeros((8, 8, 17))  # Initialize a 3D array to represent the board
    pieces = board.piece_map()  # Get the pieces on the board

    for square, piece in pieces.items():
        piece_color = piece.color  # Get the color of the piece (True for white, False for black)
        piece_value = piece.piece_type - 1  # Get the piece type and convert it to index (0-5)

        # Map the piece to its position on the board array
        rank = chess.square_rank(square)
        file = chess.square_file(square)
        board_array[rank][file][piece_value] = 1 if piece_color else -1  # Set the piece value at the position

    return board_array
'''


'''def board_to_array(board):
    board_array = np.zeros((1, 8, 8, 17))
    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece is not None:
            piece_index = piece.piece_type - 1
            if piece.color == chess.WHITE:
                piece_value = 1
            else:
                piece_value = -1
            rank = chess.square_rank(square)
            file = chess.square_file(square)
            board_array[0][rank][file][piece_index] = piece_value
    
    return board_array
'''

def board_to_3d_matrix(board):
    board_matrix = np.zeros((14, 8, 8))
    piece_to_channel = {'p': 0, 'r': 1, 'n': 2, 'b': 3, 'q': 4, 'k': 5,
                        'P': 6, 'R': 7, 'N': 8, 'B': 9, 'Q': 10, 'K': 11}
    for row in range(8):
        for col in range(8):
            square = chess.square(col, 7 - row)  
            piece = board.piece_at(square)
            if piece is not None:
                piece_channel = piece_to_channel[piece.symbol()]
                if piece.color == chess.WHITE:
                    board_matrix[piece_channel, row, col] = 1
                else:
                    board_matrix[piece_channel + 6, row, col] = 1

    # Channel 12: 1 if it's white's turn, 0 if it's black's turn
    board_matrix[12] = 1 if board.turn == chess.WHITE else 0
    # Channel 13: 1 if white can kingside castle, 0 otherwise
    board_matrix[13, 0 if board.turn == chess.WHITE else 7, 7] = 1 if board.castling_rights & chess.BB_H1 != 0 else 0
    # Channel 14: 1 if white can queenside castle, 0 otherwise
    board_matrix[13, 0 if board.turn == chess.WHITE else 7, 0] = 1 if board.castling_rights & chess.BB_A1 != 0 else 0

    return board_matrix



def create_rep_layer(board):
    piece_mapping = {
        'P': -1, 'N': -2, 'B': -3, 'R': -4, 'Q': -5, 'K': -6,
        'p': 1, 'n': 2, 'b': 3, 'r': 4, 'q': 5, 'k': 6
    }
    
    board_rep = np.zeros((8, 8, 17))  # Initialize a 3D array to represent the board

    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece is not None:
            piece_idx = piece_mapping[piece.symbol()]
            piece_color = piece.color
            rank = chess.square_rank(square)
            file = chess.square_file(square)
            board_rep[rank][file][abs(piece_idx) - 1] = 1 if piece_color else -1  # Set the piece value at the position

    return board_rep

def move_to_string(move):
    # Convert move object to string
    move_str = str(move)

    # Convert move string to desired format
    move_str = move_str.replace(' ', '')  # Remove any spaces
    move_str = move_str.lower()           # Convert to lowercase

    return move_str

def move_and_board_to_rep(move, board):
    # Convert move to string
    move_str = move_to_string(move)

    # Get the piece type that was moved
    #piece_type = board.piece_at(move.from_square).symbol()
    piece = board.piece_at(move.from_square)
    if piece is not None:
        piece_type = piece.symbol()
    else:
        piece_type = None

    # Convert move string to representation
    from_output_layer = np.zeros((8, 8))
    from_row = 8 - int(move_str[1])
    from_column = ord(move_str[0]) - ord('a')
    from_output_layer[from_row, from_column] = 1

    to_output_layer = np.zeros((8, 8))
    to_row = 8 - int(move_str[3])
    to_column = ord(move_str[2]) - ord('a')
    to_output_layer[to_row, to_column] = 1

    move_representation = np.stack([from_output_layer, to_output_layer])

    return move_representation

def create_movelist(s):
    moves = s.strip().split()
    movelist = []
    for i in range(0, len(moves), 2):
        white_move = moves[i]
        black_move = moves[i + 1] if i + 1 < len(moves) else None
        if black_move:
            movelist.append(f"{i // 2 + 1}. {white_move} {black_move}")
        else:
            movelist.append(f"{i // 2 + 1}. {white_move}")
    return movelist

def evaluate_board_state(board):
    with chess.engine.SimpleEngine.popen_uci("C:\\Users\\Lenovo\\Desktop\\Sid Folder\\Chess Project\\stockfish\\stockfish-windows-x86-64-avx2.exe") as engine:
        result = engine.analyse(board, chess.engine.Limit(time=5))  # Adjust time limit as needed
        evaluation_score = result["score"].relative.score(mate_score=10000)  # Convert to centipawns
    return evaluation_score


'''def evaluate_move(board, move):
    # Make the move on a copy of the board
    board_copy = (board.pop()).copy()
    
    board_copy.push(move)  # Don't need to convert 'move' to UCI format
    
    # Evaluate the resulting board position using Stockfish
    return evaluate_board_state(board_copy)'''


'''class ChessDataset(Dataset):

    def __init__(self, games):
        super(ChessDataset, self).__init__()
        self.games = games

    def __len__(self):
        return 40_000

    def __getitem__(self,index):
        game_i = np.random.randint(self.games.shape[0])
        random_game = chess_dataset['AN'].values[games_i]
        moves = create_move_list(random_game)
        game_state_i = np.random.randint(len(moves)-1)
        next_move = moves[game_state_i]
        moves = moves[:game_state_i]
        board = chess.Board()
        for move in moves:
            board.push_san(move)
        x = board_2_rep(board)
        y = move_2_rep(next_move, board)
        if game_state_i % 2 == 1:
            x *= -1
        return x, y'''
