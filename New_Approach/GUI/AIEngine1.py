import random
from board import Board
from display import GUI
from pieces import PieceImage

class Engine:
    def __init__(self, board: Board, maxDepth: int, color: str):
        self.board = board
        self.color = color
        self.maxDepth = maxDepth

    def getBestMove(self):
        print("Current board position FEN:", self.board.set_fen())  # Hash it afterwards
        return self.engine(None, 1)

    def evalFunct(self):
        compt = 0
        # Sums up the material values
        for square in self.board.get_all_squares():
            compt += self.squareResPoints(square)
        compt += self.mateOpportunity() + self.openning() + 0.001 * random.random()
        return compt

    def mateOpportunity(self):
        if self.board.is_checkmate():
            if self.board.get_turn() == self.color:
                return -999
            else:
                return 999
        elif self.board.is_check():
            return -50 if self.board.get_turn() == self.color else 50
        else:
            return 0

    # to make the engine develop in the first moves
    def openning(self):
        if self.board.get_fullmove_number() < 10:
            if self.board.get_turn() == self.color:
                return 1 / 30 * len(self.board.get_legal_moves())
            else:
                return -1 / 30 * len(self.board.get_legal_moves())
        else:
            return 0

    # Takes a square as input and
    # returns the corresponding Hans Berliner's
    # system value of its resident
    def squareResPoints(self, square: tuple) -> int:
        piece = self.board.get_piece_at(square)
        pieceValue = 0
        if piece:
            if piece.piece_type == 'pawn':
                pieceValue = 1
            elif piece.piece_type == 'rook':
                pieceValue = 5.1
            elif piece.piece_type == 'bishop':
                pieceValue = 3.33
            elif piece.piece_type == 'knight':
                pieceValue = 3.2
            elif piece.piece_type == 'queen':
                pieceValue = 8.8

            if piece.color != self.color:
                return -pieceValue
            else:
                return pieceValue
        return 0

    def engine(self, candidate, depth):
        # reached max depth of search or no possible moves
        if depth == self.maxDepth or len(self.board.get_legal_moves()) == 0:
            return self.evalFunct()
        else:
            # get list of legal moves of the current position
            moveListe = self.board.get_legal_moves()

            # initialise newCandidate
            newCandidate = None
            # (uneven depth means engine's turn)
            if depth % 2 != 0:
                newCandidate = float("-inf")
            else:
                newCandidate = float("inf")

            # analyse board after deeper moves
            for move in moveListe:

                # Play move i
                self.board.push(move)

                # Get value of move i (by exploring the repercussions)
                value = self.engine(newCandidate, depth + 1)

                # Basic minmax algorithm:
                # if maximizing (engine's turn)
                if value > newCandidate and depth % 2 != 0:
                    # need to save move played by the engine
                    if depth == 1:
                        best_move = move
                    newCandidate = value
                # if minimizing (human player's turn)
                elif value < newCandidate and depth % 2 == 0:
                    newCandidate = value

                # Alpha-beta pruning cuts:
                # (if previous move was made by the engine)
                if candidate is not None and value < candidate and depth % 2 == 0:
                    self.board.pop()
                    break
                # (if previous move was made by the human player)
                elif candidate is not None and value > candidate and depth % 2 != 0:
                    self.board.pop()
                    break

                # Undo last move
                self.board.pop()

            # Return result
            if depth > 1:
                # Return value of a move in the tree
                return newCandidate
            else:
                # Return the move (only on the first move)
                return best_move
