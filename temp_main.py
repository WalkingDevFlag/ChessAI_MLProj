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

        # Print the initial chessboard
        game.print_board()

        move_list = ""

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

            move_rep = move_and_board_to_rep(best_move, game.board)
            move_list += str(best_move) + " "
            a = board_to_3d_matrix(game.board)
            b = create_rep_layer(game.board)
            c = move_rep
            d = create_movelist(move_list)
            e = evaluate_board_state(game.board)

            save_variable(a, 'w_board_matrix.npz')
            save_variable(b, 'w_board_representation.npz')
            save_variable(c, 'w_move_rep.npz')
            save_variable(d, 'w_move_list.npz')
            save_variable(e, 'w_board_evaluation.npz')


            
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
            v = board_to_3d_matrix(game.board)
            w = create_rep_layer(game.board)
            x = move_rep
            y = create_movelist(move_list)
            z = evaluate_board_state(game.board)

            save_variable(a, 'b_board_matrix.npz')
            save_variable(b, 'b_board_representation.npz')
            save_variable(c, 'b_move_rep.npz')
            save_variable(d, 'b_move_list.npz')
            save_variable(e, 'b_board_evaluation.npz')


    else:
        print("Invalid choice. Exiting the game.")

if __name__ == "__main__":
    main()



    
'''piece_values = {
    chess.PAWN: 1,
    chess.KNIGHT: 3,
    chess.BISHOP: 3,
    chess.ROOK: 5,
    chess.QUEEN: 9
}

# Piece-square tables (PST) for evaluation
pst_values = {
    chess.PAWN: [
        [ 0,  0,  0,  0,  0,  0,  0,  0],
        [50, 50, 50, 50, 50, 50, 50, 50],
        [10, 10, 20, 30, 30, 20, 10, 10],
        [ 5,  5, 10, 25, 25, 10,  5,  5],
        [ 0,  0,  0, 20, 20,  0,  0,  0],
        [ 5, -5,-10,  0,  0,-10, -5,  5],
        [ 5, 10, 10,-20,-20, 10, 10,  5],
        [ 0,  0,  0,  0,  0,  0,  0,  0]
    ],
    chess.KNIGHT: [
        [-50,-40,-30,-30,-30,-30,-40,-50],
        [-40,-20,  0,  0,  0,  0,-20,-40],
        [-30,  0, 10, 15, 15, 10,  0,-30],
        [-30,  5, 15, 20, 20, 15,  5,-30],
        [-30,  0, 15, 20, 20, 15,  0,-30],
        [-30,  5, 10, 15, 15, 10,  5,-30],
        [-40,-20,  0,  5,  5,  0,-20,-40],
        [-50,-40,-30,-30,-30,-30,-40,-50],
    ],
    chess.BISHOP: [
        [-20,-10,-10,-10,-10,-10,-10,-20],
        [-10,  0,  0,  0,  0,  0,  0,-10],
        [-10,  0,  5, 10, 10,  5,  0,-10],
        [-10,  5,  5, 10, 10,  5,  5,-10],
        [-10,  0, 10, 10, 10, 10,  0,-10],
        [-10, 10, 10, 10, 10, 10, 10,-10],
        [-10,  5,  0,  0,  0,  0,  5,-10],
        [-20,-10,-10,-10,-10,-10,-10,-20],
    ],
    chess.ROOK: [
        [ 0,  0,  0,  0,  0,  0,  0,  0],
        [ 5, 10, 10, 10, 10, 10, 10,  5],
        [-5,  0,  0,  0,  0,  0,  0, -5],
        [-5,  0,  0,  0,  0,  0,  0, -5],
        [-5,  0,  0,  0,  0,  0,  0, -5],
        [-5,  0,  0,  0,  0,  0,  0, -5],
        [-5,  0,  0,  0,  0,  0,  0, -5],
        [ 0,  0,  0,  5,  5,  0,  0,  0]
],
    chess.QUEEN: [
        [-20,-10,-10, -5, -5,-10,-10,-20],
        [-10,  0,  0,  0,  0,  0,  0,-10],
        [-10,  0,  5,  5,  5,  5,  0,-10],
        [ -5,  0,  5,  5,  5,  5,  0, -5],
        [  0,  0,  5,  5,  5,  5,  0, -5],
        [-10,  5,  5,  5,  5,  5,  0,-10],
        [-10,  0,  5,  0,  0,  0,  0,-10],
        [-20,-10,-10, -5, -5,-10,-10,-20],
]
}

# Evaluate pawn structure
def evaluate_pawn_structure(board):
    # Sample implementation: count the number of pawn islands
    pawn_islands = 0
    for file in range(8):
        for rank in range(7):
            if board.piece_at(chess.square(file, rank)) == chess.PAWN:
                # Check if the pawn has no pawns adjacent to it
                if not any(board.piece_at(sq) == chess.PAWN for sq in chess.SquareSet(chess.square(file, rank)).neighbors()):
                    pawn_islands += 1
    return -pawn_islands  # Negative score for pawn islands

# Evaluate king safety
def evaluate_king_safety(board):
    # Sample implementation: count the number of attackers near the king
    king_square = board.king(chess.WHITE)  # Assuming white king
    attackers = len(board.attackers(chess.BLACK, king_square))
    return -attackers  # Negative score for more attackers near the king

# Evaluate a move score
def evaluate_move_score(board, move):
    evaluation = 0
    
    # Make the move on a copy of the board
    board_copy = board.copy()
    board_copy.push(move)
    
    # Material evaluation
    for square in chess.SQUARES:
        piece = board_copy.piece_at(square)
        if piece:
            piece_value = piece_values[piece.piece_type]
            evaluation += piece_value
            
            # Add piece-square table value
            pst_value = pst_values[piece.piece_type - 1][square]
            evaluation += pst_value
    
    # Evaluate pawn structure
    evaluation += evaluate_pawn_structure(board_copy)
    
    # Evaluate king safety
    evaluation += evaluate_king_safety(board_copy)
    
    return evaluation'''
