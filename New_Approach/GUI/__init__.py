import pygame
import chess

from display import GUI
from board import Board
from pieces import PieceImage

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

    # Run the main game loop
    while True:
        gui.draw()

        # Handle any game events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

if __name__ == "__main__":
    main()
