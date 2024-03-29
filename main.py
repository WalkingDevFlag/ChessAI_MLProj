from ChessBoard import ChessBoard
from HumanMove import playHumanMove
from CheckGame import check_game_end, resolve_check
from AIEngine import Engine
from Chess_Rep import board_to_3d_matrix, create_rep_layer, move_and_board_to_rep, create_movelist, move_to_string, append_to_csv, evaluate_board_state
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

    
def main():
    print("Welcome to Chess Game!")
    print("Would you like to play against the AI or watch AI self-play? (AI/Self-play)")
    game_mode = input("Enter your choice: ").lower()
    
    # Create a chessboard instance
    game = ChessBoard()
    move_list = ""

    if game_mode == "ai":
        print("You have chosen to play against the AI.")
        ai_difficulty = int(input("Choose AI difficulty level (1-5): "))
        if ai_difficulty < 1 or ai_difficulty > 5:
            print("Invalid difficulty level. Defaulting to level 3.")
            ai_difficulty = 3

        # Print the initial chessboard
        game.print_board()

        while True:
            # Check if there are only two kings left on the board
            if len(game.board.pieces(chess.KING)) == 2:
                print("Only two kings left on the board. Exiting the program.")
                sys.exit()
                
            # Player (Human) makes a move
            print("Your move:")
            human_move = playHumanMove(game.board)  
            if human_move:
                exit_game()  
            game.print_board()
            result = check_game_end(game.board)
            if result:
                if "Checkmate" in result:
                    print(result)
                    break  
                continue

            move_rep = move_and_board_to_rep(human_move, game.board)
            move_list += str(human_move) + " "
            d = create_movelist(move_list)
            b = create_rep_layer(game.board)
            a = board_to_3d_matrix(game.board)
            c = move_rep
            e = evaluate_board_state(game.board)

            data_to_append=(a,b,c,d,e)
            file_path='C:\\Users\\Lenovo\\Desktop\\Chess AI\\WhiteDataset.csv' #xlsx
            append_to_csv(file_path, data_to_append)

            
            # AI makes a move
            print("AI is thinking...")
            engine = Engine(game.board, ai_difficulty, game.board.turn)
            best_move = engine.getBestMove()
            game.board.push(best_move)
            print("AI's move:")
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

            move_rep = move_and_board_to_rep(best_move, game.board)
            move_list += str(best_move) + " "
            d = create_movelist(move_list)
            b = create_rep_layer(game.board)
            a = board_to_3d_matrix(game.board)
            c = move_rep
            e = evaluate_board_state(game.board)

            data_to_append=(a,b,c,d,e)
            file_path='C:\\Users\\Lenovo\\Desktop\\Chess AI\\WhiteDataset.csv' #xlsx
            append_to_csv(file_path, data_to_append)


    elif game_mode == "self-play":
        print("You have chosen to watch AI self-play.")
        ai_difficulty = int(input("Choose AI difficulty level (1-5): "))
        if ai_difficulty < 1 or ai_difficulty > 5:
            print("Invalid difficulty level. Defaulting to level 3.")
            ai_difficulty = 3

        game.print_board()
        while True:
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
                    break  
                elif "Check" in result:
                    print(result)
                    print("Make a move to get out of check")
                continue

            move_rep = move_and_board_to_rep(best_move, game.board)
            move_list += str(best_move) + " "
            d = create_movelist(move_list)
            b = create_rep_layer(game.board)
            a = board_to_3d_matrix(game.board)
            c = move_rep
            e = evaluate_board_state(game.board)

            data_to_append=(a,b,c,d,e)
            file_path='C:\\Users\\Lenovo\\Desktop\\Chess AI\\WhiteDataset.csv' #xlsx
            append_to_csv(file_path, data_to_append)
            

    
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

            move_rep = move_and_board_to_rep(best_move, game.board)
            move_list += str(best_move) + " "
            z = create_movelist(move_list)
            w = create_rep_layer(game.board)
            v = board_to_3d_matrix(game.board)
            y = move_rep
            u = evaluate_board_state(game.board)


            data_to_append=(v,w,y,z,u)
            file_path='C:\\Users\\Lenovo\\Desktop\\Chess AI\\BlackDataset.csv' #xlsx
            append_to_csv(file_path, data_to_append)


    else:
        print("Invalid choice. Exiting the game.")

if __name__ == "__main__":
    main()
