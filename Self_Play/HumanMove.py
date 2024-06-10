import chess

def playHumanMove(board):
    try:
        print(board.legal_moves)
        print("""To undo your last move, type "undo".""")
        print("""To exit the game, type "exit".""")
        # get human move
        play = input("Your move: ")
        if play == "undo":
            board.pop()
            board.pop()
            print(board)  # Print the board after undoing the move
            playHumanMove(board)
            return
        elif play == "exit":
            return True
        board.push_san(play)
    except:
        playHumanMove(board)
