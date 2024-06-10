import chess
import numpy as np

'''
1. Defines functions for converting chess board states into input tensors.

2. Implements a function (play_game_and_generate_data) to play games between the AlphaZero model and an AI engine, generating training data in the process.
'''

def convert_board_to_input(board):
    # Convert the chess board state to a 8x8x17 input tensor
    board_input = np.zeros((8, 8, 17), dtype=np.float32)
    for row in range(8):
        for col in range(8):
            piece = board.piece_at(chess.square(col, 7 - row))
            if piece is not None:
                piece_index = piece.piece_type - 1 + (0 if piece.color == chess.WHITE else 6)
                board_input[row, col, piece_index] = 1
    return np.expand_dims(board_input, axis=0)

def play_game_and_generate_data(alpha_zero_model, ai_engine, num_games):
    training_data_states = []
    training_data_policies = []
    training_data_values = []

    for _ in range(num_games):
        board = ChessBoard()
        current_player = chess.WHITE

        while not check_game_state(board):
            if current_player == chess.WHITE:
                # AlphaZero model makes a move
                input_data = convert_board_to_input(board)
                policy, value = alpha_zero_model.predict(input_data)
                move = select_move_based_on_policy(board, policy)
                training_data_states.append(input_data)
                training_data_policies.append(policy)
                training_data_values.append(value)
            else:
                # AI Engine makes a move
                move = ai_engine.find_best_move(board)
            board.make_move(move)
            current_player = chess.WHITE if current_player == chess.BLACK else chess.BLACK

    return training_data_states, training_data_policies, training_data_values
