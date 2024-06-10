import pygame
import sys
import pygame
from chess_module import *
from chess_game_utils import *
from AIEngine import engine 

class Game:
    def __init__(self):
        self.board = Board()
        self.engine = Engine(self.board, maxDepth=5, color='black')
        self.selected_piece = None
        self.selected_square = None
        self.valid_moves = []
        self.white_king_pos = None
        self.black_king_pos = None
        self.white_in_check = False
        self.black_in_check = False

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                row, col = pos[1] // SQSIZE, pos[0] // SQSIZE
                square = self.board.squares[row][col]
                if self.selected_piece and not self.valid_moves:
                    if square.has_piece() and square.piece.color != self.selected_piece.color:
                        self.valid_moves = self.selected_piece.get_valid_moves()
                        for move in self.valid_moves:
                            if move.final == square:
                                self.board.move(self.selected_piece, move)
                                self.selected_piece = None
                                self.selected_square = None
                                self.valid_moves = []
                                self.update_game_state()
                                break
                    else:
                        self.selected_piece = None
                        self.selected_square = None
                        self.valid_moves = []
                elif not self.selected_piece and square.has_piece() and square.piece.color == self.current_player():
                    self.selected_piece = square.piece
                    self.selected_square = square
                    self.valid_moves = self.selected_piece.get_valid_moves()
                elif self.selected_piece and square == self.selected_square:
                    self.selected_piece = None
                    self.selected_square = None
                    self.valid_moves = []

    def update_game_state(self):
        self.white_king_pos = self.get_king_pos('white')
        self.black_king_pos = self.get_king_pos('black')
        self.white_in_check = self.in_check('white')
        self.black_in_check = self.in_check('black')

    def current_player(self):
        if self.board.turn == WHITE:
            return 'white'
        else:
            return 'black'

    def get_king_pos(self, color):
        for row in range(ROWS):
            for col in range(COLS):
                if self.board.squares[row][col].has_piece() and self.board.squares[row][col].piece.type == KING and self.board.squares[row][col].piece.color == color:
                    return (row, col)

    def in_check(self, color):
        if color == 'white':
            king_pos = self.white_king_pos
        else:
            king_pos = self.black_king_pos
        return self.board.in_check(self.board.squares[king_pos[0]][king_pos[1]].piece, king_pos)

    def ai_move(self):
        best_move = self.engine.getBestMove()
        self.board.move(self.board.squares[best_move.start.row][best_move.start.col].piece, best_move)
        self.board.set_true_en_passant(self.board.squares[best_move.start.row][best_move.start.col].piece)
        self.update_game_state()

    def draw(self, screen):
        screen.fill(BG_COLOR)
        self.board.draw(screen)
        if self.selected_piece:
            self.selected_piece.draw_valid_moves(screen, self.valid_moves)
        pygame.display.flip()

    def mainloop(self):
        screen = pygame.display.set_mode((WIDTH, HEIGHT))
        clock = pygame.time.Clock()
        while True:
            self.handle_events()
            self.draw(screen)
            if self.board.turn == BLACK and not self.valid_moves:
                self.ai_move()
            clock.tick(60)

if __name__ == '__main__':
    game = Game()
    game.mainloop()
