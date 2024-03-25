from ChessBoard import ChessBoard
from HumanMove import playHumanMove
from CheckGame import check_game_end
from AIEngine import Engine
from ExitGame import exit_game 

def main():
    print("Welcome to Chess Game!")
    print("Would you like to play against the AI or with another player? (AI/Multiplayer)")
    game_mode = input("Enter your choice: ").lower()

    if game_mode == "ai":
        # Play against AI
        print("You have chosen to play against the AI.")
        ai_difficulty = int(input("Choose AI difficulty level (1-5): "))
        if ai_difficulty < 1 or ai_difficulty > 5:
            print("Invalid difficulty level. Defaulting to level 3.")
            ai_difficulty = 3

        # Create a chessboard instance
        game = ChessBoard()

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
                print(result)
                break

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
                print(result)
                break

    elif game_mode == "multiplayer":
        # Play multiplayer game
        print("You have chosen to play a multiplayer game.")
        # Create a chessboard instance
        game = ChessBoard()

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
                print(result)
                break

            # Player 2 (Black) makes a move
            print("Player 2 (Black) move:")
            if playHumanMove(game.board):
                exit_game()  # Call exit_game function if playHumanMove returns True
            game.print_board()
            result = check_game_end(game.board)
            if result:
                print(result)
                break

    else:
        print("Invalid choice. Exiting the game.")

if __name__ == "__main__":
    main()
