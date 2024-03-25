import chess
import random

class Engine:
    def __init__(self, board, maxDepth, color):
        self.board = board
        self.color = color
        self.maxDepth = maxDepth

    def getBestMove(self):
        print("Current board position FEN:", self.board.fen())  # Hash it afterwards
        return self.engine(None, 1)

    def evalFunct(self):
        compt = 0
        # Sums up the material values
        for i in range(64):
            compt += self.squareResPoints(chess.SQUARES[i])
        compt += self.mateOpportunity() + self.openning() + 0.001 * random.random()
        return compt

    def mateOpportunity(self):
        if self.board.is_checkmate():
            if self.board.turn == self.color:
                return -999
            else:
                return 999
        elif self.board.is_check():
            return -50 if self.board.turn == self.color else 50
        else:
            return 0
        
    # to make the engine develop in the first moves        
    def openning(self):
        if self.board.fullmove_number < 10:
            # Select a random move from legal moves
            legal_moves = list(self.board.legal_moves)
            if legal_moves:
                random_move = random.choice(legal_moves)
                self.board.push(random_move)
                value = self.evalFunct()
                self.board.pop()
                return value
        return 0
    
    # to make the engine develop in the first moves
    '''def openning(self):
        if self.board.fullmove_number < 10:
            if self.board.turn == self.color:
                return 1 / 30 * self.board.legal_moves.count()
            else:
                return -1 / 30 * self.board.legal_moves.count()
        else:
            return 0'''

    # Takes a square as input and
    # returns the corresponding Hans Berliner's
    # system value of its resident
    def squareResPoints(self, square):
        pieceValue = 0
        if self.board.piece_type_at(square) == chess.PAWN:
            pieceValue = 1
        elif self.board.piece_type_at(square) == chess.ROOK:
            pieceValue = 5.1
        elif self.board.piece_type_at(square) == chess.BISHOP:
            pieceValue = 3.33
        elif self.board.piece_type_at(square) == chess.KNIGHT:
            pieceValue = 3.2
        elif self.board.piece_type_at(square) == chess.QUEEN:
            pieceValue = 8.8

        if self.board.color_at(square) != self.color:
            return -pieceValue
        else:
            return pieceValue

    def engine(self, candidate, depth):
        # reached max depth of search or no possible moves
        if depth == self.maxDepth or self.board.legal_moves.count() == 0:
            return self.evalFunct()
        else:
            # get list of legal moves of the current position
            moveListe = list(self.board.legal_moves)

            # initialise newCandidate
            newCandidate = None
            # (uneven depth means engine's turn)
            if depth % 2 != 0:
                newCandidate = float("-inf")
            else:
                newCandidate = float("inf")

            # analyse board after deeper moves
            for i in moveListe:

                # Play move i
                self.board.push(i)

                # Get value of move i (by exploring the repercussions)
                value = self.engine(newCandidate, depth + 1)

                # Basic minmax algorithm:
                # if maximizing (engine's turn)
                if value > newCandidate and depth % 2 != 0:
                    # need to save move played by the engine
                    if depth == 1:
                        move = i
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
                return move
