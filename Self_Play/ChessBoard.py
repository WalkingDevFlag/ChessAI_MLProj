import chess

class ChessBoard:
    def __init__(self, board=None):
        if board is None:
            self.board = chess.Board()
        else:
            self.board = board

    def print_board(self):
        print(self.board)

    def fen(self):
        return self.board.fen()

    def get_legal_moves(self):
        return list(self.board.legal_moves)
