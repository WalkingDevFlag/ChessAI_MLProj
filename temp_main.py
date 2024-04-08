from ChessBoard import ChessBoard
from HumanMove import playHumanMove
from CheckGame import check_game_end, resolve_check
from Chess_Rep import create_rep_layer, move_and_board_to_rep, create_movelist, move_to_string, append_to_csv, evaluate_board_state, board_to_3d_matrix, save_variable
from AIEngine_1 import Engine as AIEngine_1
from AIEngine_2 import Engine as AIEngine_2
from ExitGame import exit_game
import chess
import numpy as np
import sys


def save_board_states(board_states_list, filename):
    board_states_array = np.stack(board_states_list, axis=0)
    np.savez(filename, data=board_states_array)

    
def main():
    print("Welcome to Chess Game!")
    print("Would you like to watch AI self-play? (Self-play)")
    game_mode = input("Enter your choice: ").lower()
    
    game = ChessBoard()

    if game_mode == "self-play":
        print("You have chosen to watch AI self-play.")
        ai_difficulty = int(input("Choose AI difficulty level (1-5): "))
        if ai_difficulty < 1 or ai_difficulty > 5:
            print("Invalid difficulty level. Defaulting to level 3.")
            ai_difficulty = 3

        game.print_board()

        move_list = ""
        board_states_list = []
        rep_layer_list = []
        move_rep_list = []
        move_list_list = []
        board_evaluation_list = []

        while True:
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
                    break 
                elif "Check" in result:
                    print(result)
                    print("Make a move to get out of check")
                continue

            move_list += str(best_move) + " "
            
            board_states_list.append(board_to_3d_matrix(game.board))
            rep_layer_list.append(create_rep_layer(game.board))
            board_evaluation_list.append(evaluate_board_state(game.board))
            move_rep_list.append(move_and_board_to_rep(best_move, game.board))
            move_list_list.append(move_list.strip().split())  # Append individual moves

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
                    break  
                elif "Check" in result:
                    print(result)
                    print("Make a move to get out of check")
                continue

            move_list += str(best_move) + " "
            
            board_states_list.append(board_to_3d_matrix(game.board))
            rep_layer_list.append(create_rep_layer(game.board))
            board_evaluation_list.append(evaluate_board_state(game.board))
            move_rep_list.append(move_and_board_to_rep(best_move, game.board))
            move_list_list.append(move_list.strip().split())  # Append individual moves
               

        save_board_states(board_states_list, 'all_board_states')
        save_variable(rep_layer_list, 'rep_layer.npz')
        save_variable(move_rep_list, 'move_rep.npz')
        save_variable(board_evaluation_list, 'board_evaluation.npz')
        save_variable(move_list_list, 'move_list.npz')

    else:
        print("Invalid choice. Exiting the game.")

if __name__ == "__main__":
    main()



