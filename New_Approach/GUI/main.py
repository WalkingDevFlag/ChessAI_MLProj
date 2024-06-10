import pygame
import chess

from display import GUI
from board import Board
from pieces import PieceImage
from AIEngine1 import Engine

# Constants
WINDOWWIDTH = 800  
WINDOWHEIGHT = 800  
FEN = chess.STARTING_FEN  
PLAYER_TURN = True  

def main():
    pygame.init()
    pygame.font.init()

    # Initialize the GUI
    gui = GUI(WINDOWWIDTH, WINDOWHEIGHT, PLAYER_TURN, FEN)

    # Initialize the AI engine
    engine = Engine(gui.gameboard.board, maxDepth=3, color=chess.BLACK)

    best_move = engine.getBestMove()
    print("Best Move:", best_move)

    # Run the main game loop
    while True:
        if not gui.player:
            # AI's turn
            best_move = engine.getBestMove()
            gui.make_move(best_move)
            gui.draw()
        else:
            # Player's turn
            gui.draw()

        # Handle any game events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

if __name__ == "__main__":
    main()
