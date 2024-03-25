import chess
from alpha_zero_chess_model import AlphaZeroChessModel
from AIEngine import Engine
from CheckGame import check_game_end
from ChessBoard import ChessBoard
from ExitGame import exit_game
from HumanMove import playHumanMove
import numpy as np
import chess.engine

'''
1. Integrates various functionalities for training a chess AI using the AlphaZero algorithm.

2. Includes functions for converting board states, selecting moves based on policy and evaluation, evaluating board positions, playing games, and training the AlphaZero model.
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

def select_move_based_on_policy_and_evaluation(board, policy, engine):
    legal_moves = [str(move) for move in board.legal_moves]
    move_probs = []
    for move in legal_moves:
        move_index = chess.Move.from_uci(move).uci()
        if move_index in policy:
            move_prob = policy[move_index]
            move_probs.append(move_prob)
        else:
            # If the move is not in the policy, assign a small probability
            move_probs.append(0.0)
    
    # Evaluate each legal move and select the one with the highest combined score
    best_move = None
    best_score = float('-inf')
    for move, prob in zip(legal_moves, move_probs):
        board.push(chess.Move.from_uci(move))
        evaluation = evaluate_board(board, engine)
        score = prob * evaluation  # Combine policy probability and position evaluation
        if score > best_score:
            best_move = move
            best_score = score
        board.pop()
    
    return chess.Move.from_uci(best_move)

def evaluate_board(board, engine):
    with chess.engine.SimpleEngine.popen_uci("C:\\Users\\Lenovo\\Desktop\\Sid Folder\\Chess Project\\stockfish\\stockfish-windows-x86-64-avx2.exe") as sf:
        result = sf.analyse(board, chess.engine.Limit(time=0.1))
        score = result['score'].relative.score()
    return score

def play_game_and_generate_data(alpha_zero_model, ai_engine, num_games):
    training_data_states = []
    training_data_policies = []
    training_data_values = []

    for _ in range(num_games):
        board = ChessBoard()
        current_player = chess.WHITE

        while True:
            # Check if the game has ended
            game_result = check_game_end(board.board)
            if game_result is not None:
                print(game_result)
                break

            if current_player == chess.WHITE:
                # AlphaZero model makes a move
                input_data = convert_board_to_input(board.board)
                policy, value = alpha_zero_model(input_data)  # Remove extra arguments here
                training_data_states.append(input_data)
                training_data_policies.append(policy)
                training_data_values.append(value)
            else:
                # AI Engine makes a move
                move = ai_engine.getBestMove()  
            board.board.push(move)
            current_player = chess.WHITE if current_player == chess.BLACK else chess.BLACK

    return training_data_states, training_data_policies, training_data_values

def main():
    # Initialize AlphaZero model
    alpha_zero_model = AlphaZeroChessModel()
    # Initialize AI Engine
    board = chess.Board()
    maxdepth = 5
    color = chess.WHITE
    ai_engine = Engine(board, maxdepth, color)

    num_games = 10  # Number of self-play games to generate training data

    # Play games and generate training data
    training_data_states, training_data_policies, training_data_values = play_game_and_generate_data(alpha_zero_model, ai_engine, num_games)

    # Train AlphaZero model using generated training data
    alpha_zero_model.train(training_data_states, training_data_policies, training_data_values)

    # Save the trained model
    model_filename = "alpha_zero_chess_model_1.h5"
    model_save_path = "C:\\Users\\Lenovo\\Desktop\\Chess AI\\" + model_filename
    alpha_zero_model.save(model_save_path)
    print(f"Trained model saved to {model_save_path}")

if __name__ == "__main__":
    main()
