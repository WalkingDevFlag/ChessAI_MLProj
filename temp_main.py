from ChessBoard import ChessBoard
from HumanMove import playHumanMove
from CheckGame import check_game_end, resolve_check
from AIEngine import Engine
from Chess_Rep import get_board_array, create_rep_layer, move_and_board_to_rep, create_movelist, move_to_string, append_to_csv, evaluate_board_state, evaluate_move
from AIEngine_1 import Engine as AIEngine_1
from AIEngine_2 import Engine as AIEngine_2
from ExitGame import exit_game
import chess
import numpy as np
import sys


def check_only_two_kings(board):
    if len(board.piece_map().values()) == 2 and all(piece.piece_type == chess.KING for piece in board.piece_map().values()):
        return True
    else:
        return False
    
def evaluate_move_material(board, move):
    # Make a copy of the board
    board_copy = board.copy()
    
    # Apply the move to the board copy
    board_copy.push(move)
    
    # Evaluate the material balance after the move
    material_after_move = sum(piece_value(piece) for piece in board_copy.piece_map().values())
    material_before_move = sum(piece_value(piece) for piece in board.piece_map().values())
    material_difference = material_after_move - material_before_move
    
    return material_difference

def piece_value(piece):
    # Assign numerical values to pieces
    values = {'P': 1, 'N': 3, 'B': 3, 'R': 5, 'Q': 9}
    piece_symbol = piece.symbol().upper()
    return values.get(piece_symbol, 0)  # Return 0 for unrecognized pieces (e.g., kings)



    
def main():
    print("Welcome to Chess Game!")
    print("Would you like to watch AI self-play? (Self-play)")
    game_mode = input("Enter your choice: ").lower()
    
    # Create a chessboard instance
    game = ChessBoard()

    # Initialize move list
    move_list = ""

    if game_mode == "self-play":
        print("You have chosen to watch AI self-play.")
        ai_difficulty = int(input("Choose AI difficulty level (1-5): "))
        if ai_difficulty < 1 or ai_difficulty > 5:
            print("Invalid difficulty level. Defaulting to level 3.")
            ai_difficulty = 3

        # Print the initial chessboard
        game.print_board()
        
        # Game loop i.e Start self-play
        while True:
            # Check if there are only two kings left on the board
            if check_only_two_kings(game.board):
                print("Only two kings left on the board. Exiting the program.")
                sys.exit()
                
            # White engine (AIEngine_1) makes a move
            print("The White AI is thinking...")
            white_engine = AIEngine_1(game.board, ai_difficulty, chess.WHITE)
            best_move = white_engine.getBestMove()
            game.board.push(best_move)
            print("White's move:")
            print(best_move)
            game.print_board()
            result = check_game_end(game.board)
            if result:
                if "Checkmate" in result:
                    print(result)
                    break  # Break if it's a checkmate
                elif "Check" in result:
                    print(result)
                    print("Make a move to get out of check")
                continue

            # Board Evaluation:
            board_evaluation = evaluate_board_state(game.board)
            print("Board Evaluation after Whites's move:", board_evaluation)
            # Move Evaluation:
            move_evaluation = evaluate_move_material(game.board, best_move)
            print("Evaluation after playing move", best_move, ":", move_evaluation)

            
            # Black engine (AIEngine_2) makes a move
            print("The Black AI is thinking...")
            black_engine = AIEngine_2(game.board, ai_difficulty, chess.BLACK)
            best_move = black_engine.getBestMove()
            game.board.push(best_move)
            print("Black's move:")
            print(best_move)
            game.print_board()
            result = check_game_end(game.board)
            if result:
                if "Checkmate" in result:
                    print(result)
                    break  # Break if it's a checkmate
                elif "Check" in result:
                    print(result)
                    print("Make a move to get out of check")
                continue
            
            # Board Evaluation:
            board_evaluation = evaluate_board_state(game.board)
            print("Board Evaluation after Black's move:", board_evaluation)
            # Move Evaluation:
            move_evaluation = evaluate_move_material(game.board, best_move)
            print("Evaluation after playing move", best_move, ":", move_evaluation)



    else:
        print("Invalid choice. Exiting the game.")

if __name__ == "__main__":
    main()
