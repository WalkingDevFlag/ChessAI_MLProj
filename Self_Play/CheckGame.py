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

def resolve_check(board):
    if board.is_check():
        # Check if the current player can escape from check
        if not any(board.is_checkmate(), board.is_stalemate()):
            return "You are in check. Make a move to get out of check."
    return None
