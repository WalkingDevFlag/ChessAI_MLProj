import chess


def check_game_end(board):
    if board.is_checkmate():
        return "Checkmate! You win!"
    elif board.is_stalemate():
        return "Stalemate! It's a draw."
    elif board.is_insufficient_material():
        return "Insufficient material! It's a draw."
    elif board.is_check():
        return "Check!"
    return None
