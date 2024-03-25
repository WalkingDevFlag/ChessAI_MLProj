from ChessBoard import ChessBoard
from HumanMove import playHumanMove
from CheckGame import check_game_end, resolve_check
from AIEngine import Engine
from AIEngine_1 import Engine as AIEngine_1
from AIEngine_2 import Engine as AIEngine_2
from ExitGame import exit_game 
import chess

def main():
    print("Welcome to Chess Game!")
    print("Would you like to play against the AI, with another player, or watch AI self-play? (AI/Multiplayer/Self-play)")
    game_mode = input("Enter your choice: ").lower()
    # Create a chessboard instance
    game = ChessBoard()

    if game_mode == "ai":
        # Play against AI
        print("You have chosen to play against the AI.")
        ai_difficulty = int(input("Choose AI difficulty level (1-5): "))
        if ai_difficulty < 1 or ai_difficulty > 5:
            print("Invalid difficulty level. Defaulting to level 3.")
            ai_difficulty = 3

        # Print the initial chessboard
        game.print_board()

        # Game loop
        while True:
            # Player (Human) makes a move
            print("Your move:")
            if playHumanMove(game.board):
                exit_game()  # Call exit_game function if playHumanMove returns True
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
                    break  # Break if it's a checkmate
                continue 

    elif game_mode == "multiplayer":
        # Play multiplayer game
        print("You have chosen to play a multiplayer game.")

        # Print the initial chessboard
        game.print_board()

        # Game loop
        while True:
            # Player 1 (White) makes a move
            print("Player 1 (White) move:")
            if playHumanMove(game.board):
                exit_game()  # Call exit_game function if playHumanMove returns True
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

            # Player 2 (Black) makes a move
            print("Player 2 (Black) move:")
            if playHumanMove(game.board):
                exit_game()  # Call exit_game function if playHumanMove returns True
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


    elif game_mode == "self-play":
        print("You have chosen to watch AI self-play.")
        ai_difficulty = int(input("Choose AI difficulty level (1-5): "))
        if ai_difficulty < 1 or ai_difficulty > 5:
            print("Invalid difficulty level. Defaulting to level 3.")
            ai_difficulty = 3

        # Print the initial chessboard
        game.print_board()
        
        # Game loop i.e Start self-play
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
                    break  # Break if it's a checkmate
                elif "Check" in result:
                    print(result)
                    print("Make a move to get out of check")
                continue 
                
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
    else:
        print("Invalid choice. Exiting the game.")

if __name__ == "__main__":
    main()
