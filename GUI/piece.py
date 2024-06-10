import os

class Piece:

    def __init__(self, name, color, value, texture=None, texture_rect=None):
        self.name = name
        self.color = color
        value_sign = 1 if color == 'white' else -1
        self.value = value * value_sign
        self.moves = []
        self.moved = False
        self.texture = texture
        self.set_texture()
        self.texture_rect = texture_rect

    def set_texture(self, size=80):
        self.texture = os.path.join(
            f'assets/images/imgs-{size}px/{self.color}_{self.name}.png')

    def add_move(self, move):
        self.moves.append(move)

    def clear_moves(self):
        self.moves = []

    def fen(self):
        return self.name.capitalize() if self.color == 'white' else self.name

class Pawn(Piece):

    def __init__(self, color):
        self.dir = -1 if color == 'white' else 1
        self.en_passant = False
        super().__init__('pawn', color, 1.0)

    def fen(self):
        return 'P' if self.color == 'white' else 'p'

class Knight(Piece):

    def __init__(self, color):
        super().__init__('knight', color, 3.0)

    def fen(self):
        return 'N' if self.color == 'white' else 'n'

class Bishop(Piece):

    def __init__(self, color):
        super().__init__('bishop', color, 3.001)

    def fen(self):
        return 'B' if self.color == 'white' else 'b'

class Rook(Piece):

    def __init__(self, color):
        super().__init__('rook', color, 5.0)

    def fen(self):
        return 'R' if self.color == 'white' else 'r'

class Queen(Piece):

    def __init__(self, color):
        super().__init__('queen', color, 9.0)

    def fen(self):
        return 'Q' if self.color == 'white' else 'q'

class King(Piece):

    def __init__(self, color):
        self.left_rook = None
        self.right_rook = None
        super().__init__('king', color, 10000.0)

    def fen(self):
        return 'K' if self.color == 'white' else 'k'
