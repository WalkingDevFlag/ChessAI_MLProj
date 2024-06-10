import numpy as np  
import chess
import tensorflow as tf 

'''
1. Implements a custom dataset class (ChessDataset) for generating training data.

2. Defines methods for converting game data into input tensors suitable for training the neural network model.

3. Includes functions for checking checkmate, calculating move distributions, and choosing moves based on policy and value predictions.
'''

class ChessDataset(tf.keras.utils.Sequence):
    def __init__(self, games):
        self.games = games

    def __len__(self):
        return len(self.games)

    def __getitem__(self, index):
        game = self.games[index]
        moves = create_movelist(game)  # Assuming create_movelist returns a list of moves
        board = chess.Board()
        for move in moves:
            board.push_san(move)
        
        x = get_board_array(board)
        policy, value = AlphaZeroChessModel()(np.expand_dims(x, axis=0))  # Assuming AlphaZeroChessModel is the model defined earlier
        return x, {'policy': policy.numpy(), 'value': value.numpy()}

    
def check_mate_single(board):
    board = board.copy()
    legal_moves = list(board.legal_moves)
    for move in legal_moves:
        board.push_uci(str(move))
        if board.is_checkmate():
            move = board.pop()
            return move
        _ = board.pop()

def distribution_over_moves(vals):
    probs = np.array(vals)
    probs = np.exp(probs)
    probs = probs / probs.sum()
    probs = probs ** 3
    probs = probs / probs.sum()
    return probs

def choose_move(board, player, color, model):
    legal_moves = list(board.legal_moves)
    move = check_mate_single(board)
    if move is not None:
        return move

    x = tf.convert_to_tensor(board_2_rep(board), dtype=tf.float32)
    if color == chess.BLACK:
        x *= -1
    x = tf.expand_dims(x, 0)
    move = model.predict(x)

    vals = []
    froms = [str(legal_move)[:2] for legal_move in legal_moves]
    froms = list(set(froms))
    for from_ in froms:
        vals = move[0,:,:][8 - int(from_[1]), letter_2_num[from_[0]]]
        vals.append(val)

    probs = distribution_over_moves(vals)

    choosen_from = str(np.random.choice(froms, size=1, p=probs)[0])[:2]
    vals = []
    for legal_move in legal_moves:
        from_ = str(legal_moves)[:2]
        if from_ == choosen_from:
            to = str(legal_move)[:2]
            val = move[1,:,:][8 - int(to[1]), letter_2_num[to[0]]]
            vals.append(val)
        else:
            vals.append(0)
    choosen_move = legal_moves[np.argmax(vals)]
    return choosen_move
