# import chess
# import concurrent.futures
#
# transposition_table = {}
#
# def quiescence(board, alpha, beta):
#     stand_pat = evaluate(board)
#     if stand_pat >= beta:
#         return beta
#     if alpha < stand_pat:
#         alpha = stand_pat
#
#     legal_moves = list(board.legal_moves)
#     # Prioritize captures and checks for more effective pruning
#     legal_moves.sort(key=lambda move: (board.is_capture(move) or board.gives_check(move), move), reverse=True)
#
#     for move in legal_moves:
#         if board.is_capture(move) or board.gives_check(move):
#             board.push(move)
#             score = -quiescence(board, -beta, -alpha)
#             board.pop()
#             if score >= beta:
#                 return beta
#             if score > alpha:
#                 alpha = score
#     return alpha
#
#
# def minimax(board, depth, maximizing_player, alpha, beta, transposition_table):
#     # Check for previously evaluated positions
#     board_hash = hash(board.fen())  # Unique key for the board's FEN string
#     if board_hash in transposition_table:
#         entry = transposition_table[board_hash]
#         if entry['depth'] >= depth:
#             return entry['value']
#
#     if depth == 0 or board.is_game_over():
#         evaluation = evaluate(board)
#         transposition_table[board_hash] = {'value': evaluation, 'depth': depth}  # Store in transposition table
#         return evaluation
#
#     legal_moves = list(board.legal_moves)
#     best_move = None
#     if maximizing_player:
#         max_eval = float('-inf')
#         for move in legal_moves:
#             board.push(move)
#             eval = -minimax(board, depth - 1, False, -beta, -alpha, transposition_table)
#             board.pop()
#             max_eval = max(max_eval, eval)
#             alpha = max(alpha, eval)
#             if beta <= alpha:
#                 break
#         transposition_table[board_hash] = {'value': max_eval, 'depth': depth}  # Store the evaluation
#         return max_eval
#     else:
#         min_eval = float('inf')
#         for move in legal_moves:
#             board.push(move)
#             eval = -minimax(board, depth - 1, True, -beta, -alpha, transposition_table)
#             board.pop()
#             min_eval = min(min_eval, eval)
#             beta = min(beta, eval)
#             if beta <= alpha:
#                 break
#         transposition_table[board_hash] = {'value': min_eval, 'depth': depth}  # Store the evaluation
#         return min_eval
#
#
# def evaluate(board):
#     piece_values = {
#         chess.PAWN: 100,
#         chess.KNIGHT: 320,
#         chess.BISHOP: 330,
#         chess.ROOK: 500,
#         chess.QUEEN: 900,
#         chess.KING: 20000
#     }
#     value = 0
#     for piece in board.piece_map().values():
#         piece_value = piece_values.get(piece.piece_type, 0)
#         value += piece_value if piece.color == chess.WHITE else -piece_value
#     return value
#
#
# def negaScout(board, depth, maximizing_player, alpha, beta, transposition_table):
#     # NegaScout (Principal Variation Search)
#     # Try to get the best move first and then use the normal alpha-beta pruning
#     board_hash = hash(board.fen())
#     if board_hash in transposition_table:
#         entry = transposition_table[board_hash]
#         if entry['depth'] >= depth:
#             return entry['value']
#
#     if depth == 0 or board.is_game_over():
#         evaluation = evaluate(board)
#         transposition_table[board_hash] = {'value': evaluation, 'depth': depth}
#         return evaluation
#
#     legal_moves = list(board.legal_moves)
#     best_move = None
#     if maximizing_player:
#         max_eval = float('-inf')
#         first_move = True
#         for move in legal_moves:
#             board.push(move)
#             if first_move:
#                 eval = -negaScout(board, depth - 1, False, -beta, -alpha, transposition_table)
#                 first_move = False
#             else:
#                 eval = -negaScout(board, depth - 1, False, -alpha - 1, -alpha, transposition_table)
#                 if alpha < eval < beta:
#                     eval = -negaScout(board, depth - 1, False, -beta, -alpha, transposition_table)
#             board.pop()
#             max_eval = max(max_eval, eval)
#             alpha = max(alpha, eval)
#             if beta <= alpha:
#                 break
#         transposition_table[board_hash] = {'value': max_eval, 'depth': depth}
#         return max_eval
#     else:
#         min_eval = float('inf')
#         first_move = True
#         for move in legal_moves:
#             board.push(move)
#             if first_move:
#                 eval = -negaScout(board, depth - 1, True, -beta, -alpha, transposition_table)
#                 first_move = False
#             else:
#                 eval = -negaScout(board, depth - 1, True, -alpha - 1, -alpha, transposition_table)
#                 if alpha < eval < beta:
#                     eval = -negaScout(board, depth - 1, True, -beta, -alpha, transposition_table)
#             board.pop()
#             min_eval = min(min_eval, eval)
#             beta = min(beta, eval)
#             if beta <= alpha:
#                 break
#         transposition_table[board_hash] = {'value': min_eval, 'depth': depth}
#         return min_eval
#
#
# def iterative_deepening(board, max_depth):
#     best_move = None
#     transposition_table.clear()  # Clear transposition table for each search
#     for depth in range(1, max_depth + 1):
#         alpha, beta = -float('inf'), float('inf')
#         legal_moves = list(board.legal_moves)
#         # Use parallelization to explore multiple moves concurrently
#         with concurrent.futures.ThreadPoolExecutor() as executor:
#             futures = []
#             for move in legal_moves:
#                 board.push(move)
#                 futures.append(executor.submit(negaScout, board, depth - 1, False, -beta, -alpha, transposition_table))
#                 board.pop()
#
#             for future in futures:
#                 result = future.result()
#                 if result > alpha:
#                     alpha = result
#                     best_move = legal_moves[futures.index(future)]
#     return best_move




# import chess
# import concurrent.futures
#
# transposition_table = {}
#
# def quiescence(board, alpha, beta):
#     stand_pat = evaluate(board)
#     if stand_pat >= beta:
#         return beta
#     if alpha < stand_pat:
#         alpha = stand_pat
#
#     legal_moves = list(board.legal_moves)
#     # Prioritize captures and checks for more effective pruning
#     legal_moves.sort(key=lambda move: (board.is_capture(move) or board.gives_check(move), move), reverse=True)
#
#     for move in legal_moves:
#         if board.is_capture(move) or board.gives_check(move):
#             board.push(move)
#             score = -quiescence(board, -beta, -alpha)
#             board.pop()
#             if score >= beta:
#                 return beta
#             if score > alpha:
#                 alpha = score
#     return alpha
#
#
# def minimax(board, depth, maximizing_player, alpha, beta, transposition_table):
#     # Check for previously evaluated positions
#     board_hash = hash(board.fen())  # Unique key for the board's FEN string
#     if board_hash in transposition_table:
#         entry = transposition_table[board_hash]
#         if entry['depth'] >= depth:
#             return entry['value']
#
#     if depth == 0 or board.is_game_over():
#         evaluation = evaluate(board)
#         transposition_table[board_hash] = {'value': evaluation, 'depth': depth}  # Store in transposition table
#         return evaluation
#
#     legal_moves = list(board.legal_moves)
#     best_move = None
#     if maximizing_player:
#         max_eval = float('-inf')
#         for move in legal_moves:
#             board.push(move)
#             eval = -minimax(board, depth - 1, False, -beta, -alpha, transposition_table)
#             board.pop()
#             max_eval = max(max_eval, eval)
#             alpha = max(alpha, eval)
#             if beta <= alpha:
#                 break
#         transposition_table[board_hash] = {'value': max_eval, 'depth': depth}  # Store the evaluation
#         return max_eval
#     else:
#         min_eval = float('inf')
#         for move in legal_moves:
#             board.push(move)
#             eval = -minimax(board, depth - 1, True, -beta, -alpha, transposition_table)
#             board.pop()
#             min_eval = min(min_eval, eval)
#             beta = min(beta, eval)
#             if beta <= alpha:
#                 break
#         transposition_table[board_hash] = {'value': min_eval, 'depth': depth}  # Store the evaluation
#         return min_eval
#
#
# def evaluate(board):
#     piece_values = {
#         chess.PAWN: 100,
#         chess.KNIGHT: 320,
#         chess.BISHOP: 330,
#         chess.ROOK: 500,
#         chess.QUEEN: 900,
#         chess.KING: 20000
#     }
#     value = 0
#     for piece in board.piece_map().values():
#         piece_value = piece_values.get(piece.piece_type, 0)
#         value += piece_value if piece.color == chess.WHITE else -piece_value
#     return value
#
#
# def negaScout(board, depth, maximizing_player, alpha, beta, transposition_table):
#     # NegaScout (Principal Variation Search)
#     # Try to get the best move first and then use the normal alpha-beta pruning
#     board_hash = hash(board.fen())
#     if board_hash in transposition_table:
#         entry = transposition_table[board_hash]
#         if entry['depth'] >= depth:
#             return entry['value']
#
#     if depth == 0 or board.is_game_over():
#         evaluation = evaluate(board)
#         transposition_table[board_hash] = {'value': evaluation, 'depth': depth}
#         return evaluation
#
#     legal_moves = list(board.legal_moves)
#     best_move = None
#     if maximizing_player:
#         max_eval = float('-inf')
#         first_move = True
#         for move in legal_moves:
#             board.push(move)
#             if first_move:
#                 eval = -negaScout(board, depth - 1, False, -beta, -alpha, transposition_table)
#                 first_move = False
#             else:
#                 eval = -negaScout(board, depth - 1, False, -alpha - 1, -alpha, transposition_table)
#                 if alpha < eval < beta:
#                     eval = -negaScout(board, depth - 1, False, -beta, -alpha, transposition_table)
#             board.pop()
#             max_eval = max(max_eval, eval)
#             alpha = max(alpha, eval)
#             if beta <= alpha:
#                 break
#         transposition_table[board_hash] = {'value': max_eval, 'depth': depth}
#         return max_eval
#     else:
#         min_eval = float('inf')
#         first_move = True
#         for move in legal_moves:
#             board.push(move)
#             if first_move:
#                 eval = -negaScout(board, depth - 1, True, -beta, -alpha, transposition_table)
#                 first_move = False
#             else:
#                 eval = -negaScout(board, depth - 1, True, -alpha - 1, -alpha, transposition_table)
#                 if alpha < eval < beta:
#                     eval = -negaScout(board, depth - 1, True, -beta, -alpha, transposition_table)
#             board.pop()
#             min_eval = min(min_eval, eval)
#             beta = min(beta, eval)
#             if beta <= alpha:
#                 break
#         transposition_table[board_hash] = {'value': min_eval, 'depth': depth}
#         return min_eval
#
#
# def iterative_deepening(board, max_depth):
#     best_move = None
#     transposition_table.clear()  # Clear transposition table for each search
#     for depth in range(1, max_depth + 1):
#         alpha, beta = -float('inf'), float('inf')
#         legal_moves = list(board.legal_moves)
#
#         # Use parallelization to explore multiple moves concurrently
#         with concurrent.futures.ProcessPoolExecutor() as executor:  # Using ProcessPoolExecutor instead of ThreadPoolExecutor for CPU-bound tasks
#             futures = []
#             for move in legal_moves:
#                 board.push(move)
#                 futures.append(executor.submit(negaScout, board, depth - 1, False, -beta, -alpha, transposition_table))
#                 board.pop()
#
#             for future in futures:
#                 result = future.result()
#                 if result > alpha:
#                     alpha = result
#                     best_move = legal_moves[futures.index(future)]
#     return best_move

# import chess
# import concurrent.futures
# import hashlib
#
# transposition_table = {}
#
# def quiescence(board, alpha, beta):
#     stand_pat = evaluate(board)
#     if stand_pat >= beta:
#         return beta
#     if alpha < stand_pat:
#         alpha = stand_pat
#
#     legal_moves = list(board.legal_moves)
#     legal_moves.sort(key=lambda move: (board.is_capture(move) or board.gives_check(move), move), reverse=True)
#
#     for move in legal_moves:
#         if board.is_capture(move) or board.gives_check(move):
#             board.push(move)
#             score = -quiescence(board, -beta, -alpha)
#             board.pop()
#             if score >= beta:
#                 return beta
#             if score > alpha:
#                 alpha = score
#     return alpha
#
#
# def evaluate(board):
#     piece_values = {
#         chess.PAWN: 100,
#         chess.KNIGHT: 320,
#         chess.BISHOP: 330,
#         chess.ROOK: 500,
#         chess.QUEEN: 900,
#         chess.KING: 20000
#     }
#     value = 0
#     for piece in board.piece_map().values():
#         piece_value = piece_values.get(piece.piece_type, 0)
#         value += piece_value if piece.color == chess.WHITE else -piece_value
#     return value
#
#
# def get_board_hash(board):
#     # Return a unique hash for the board using the FEN string
#     return hashlib.sha256(board.fen().encode('utf-8')).hexdigest()
#
#
# def minimax(board, depth, maximizing_player, alpha, beta, transposition_table):
#     board_hash = get_board_hash(board)
#     if board_hash in transposition_table:
#         entry = transposition_table[board_hash]
#         if entry['depth'] >= depth:
#             return entry['value']
#
#     if depth == 0 or board.is_game_over():
#         evaluation = evaluate(board)
#         transposition_table[board_hash] = {'value': evaluation, 'depth': depth}
#         return evaluation
#
#     legal_moves = list(board.legal_moves)
#     best_move = None
#     if maximizing_player:
#         max_eval = float('-inf')
#         for move in legal_moves:
#             board.push(move)
#             eval = -minimax(board, depth - 1, False, -beta, -alpha, transposition_table)
#             board.pop()
#             max_eval = max(max_eval, eval)
#             alpha = max(alpha, eval)
#             if beta <= alpha:
#                 break
#         transposition_table[board_hash] = {'value': max_eval, 'depth': depth}
#         return max_eval
#     else:
#         min_eval = float('inf')
#         for move in legal_moves:
#             board.push(move)
#             eval = -minimax(board, depth - 1, True, -beta, -alpha, transposition_table)
#             board.pop()
#             min_eval = min(min_eval, eval)
#             beta = min(beta, eval)
#             if beta <= alpha:
#                 break
#         transposition_table[board_hash] = {'value': min_eval, 'depth': depth}
#         return min_eval
#
#
# def negaScout(board, depth, maximizing_player, alpha, beta, transposition_table):
#     board_hash = get_board_hash(board)
#     if board_hash in transposition_table:
#         entry = transposition_table[board_hash]
#         if entry['depth'] >= depth:
#             return entry['value']
#
#     if depth == 0 or board.is_game_over():
#         evaluation = evaluate(board)
#         transposition_table[board_hash] = {'value': evaluation, 'depth': depth}
#         return evaluation
#
#     legal_moves = list(board.legal_moves)
#     best_move = None
#     if maximizing_player:
#         max_eval = float('-inf')
#         first_move = True
#         for move in legal_moves:
#             board.push(move)
#             if first_move:
#                 eval = -negaScout(board, depth - 1, False, -beta, -alpha, transposition_table)
#                 first_move = False
#             else:
#                 eval = -negaScout(board, depth - 1, False, -alpha - 1, -alpha, transposition_table)
#                 if alpha < eval < beta:
#                     eval = -negaScout(board, depth - 1, False, -beta, -alpha, transposition_table)
#             board.pop()
#             max_eval = max(max_eval, eval)
#             alpha = max(alpha, eval)
#             if beta <= alpha:
#                 break
#         transposition_table[board_hash] = {'value': max_eval, 'depth': depth}
#         return max_eval
#     else:
#         min_eval = float('inf')
#         first_move = True
#         for move in legal_moves:
#             board.push(move)
#             if first_move:
#                 eval = -negaScout(board, depth - 1, True, -beta, -alpha, transposition_table)
#                 first_move = False
#             else:
#                 eval = -negaScout(board, depth - 1, True, -alpha - 1, -alpha, transposition_table)
#                 if alpha < eval < beta:
#                     eval = -negaScout(board, depth - 1, True, -beta, -alpha, transposition_table)
#             board.pop()
#             min_eval = min(min_eval, eval)
#             beta = min(beta, eval)
#             if beta <= alpha:
#                 break
#         transposition_table[board_hash] = {'value': min_eval, 'depth': depth}
#         return min_eval
#
#
# def iterative_deepening(board, max_depth):
#     best_move = None
#     transposition_table.clear()  # Clear transposition table for each search
#     for depth in range(1, max_depth + 1):
#         alpha, beta = -float('inf'), float('inf')
#         legal_moves = list(board.legal_moves)
#
#         # Parallelize search at the root level
#         with concurrent.futures.ProcessPoolExecutor() as executor:
#             futures = []
#             for move in legal_moves:
#                 board.push(move)
#                 futures.append(executor.submit(negaScout, board, depth - 1, False, -beta, -alpha, transposition_table))
#                 board.pop()
#
#             for future in futures:
#                 result = future.result()
#                 if result > alpha:
#                     alpha = result
#                     best_move = legal_moves[futures.index(future)]
#     return best_move

# import chess
# import concurrent.futures
# import hashlib
# import cupy as cp
#
# # This will hold transposition information.
# transposition_table = {}
#
#
# def quiescence(board, alpha, beta):
#     stand_pat = evaluate(board)
#     if stand_pat >= beta:
#         return beta
#     if alpha < stand_pat:
#         alpha = stand_pat
#
#     legal_moves = list(board.legal_moves)
#     legal_moves.sort(key=lambda move: (board.is_capture(move) or board.gives_check(move), move), reverse=True)
#
#     for move in legal_moves:
#         if board.is_capture(move) or board.gives_check(move):
#             board.push(move)
#             score = -quiescence(board, -beta, -alpha)
#             board.pop()
#             if score >= beta:
#                 return beta
#             if score > alpha:
#                 alpha = score
#     return alpha
#
#
# def evaluate(board):
#     piece_values = {
#         chess.PAWN: 100,
#         chess.KNIGHT: 320,
#         chess.BISHOP: 330,
#         chess.ROOK: 500,
#         chess.QUEEN: 900,
#         chess.KING: 20000
#     }
#
#     # We will use Cupy arrays to accelerate evaluation
#     piece_map = board.piece_map()
#     pieces = cp.array(
#         [piece_values.get(piece.piece_type, 0) if piece.color == chess.WHITE else -piece_values.get(piece.piece_type, 0)
#          for piece in piece_map.values()])
#
#     # Return the sum of the pieces values
#     return cp.sum(pieces).item()
#
#
# def get_board_hash(board):
#     return hashlib.sha256(board.fen().encode('utf-8')).hexdigest()
#
#
# def minimax(board, depth, maximizing_player, alpha, beta, transposition_table):
#     board_hash = get_board_hash(board)
#     if board_hash in transposition_table:
#         entry = transposition_table[board_hash]
#         if entry['depth'] >= depth:
#             return entry['value']
#
#     if depth == 0 or board.is_game_over():
#         evaluation = evaluate(board)
#         transposition_table[board_hash] = {'value': evaluation, 'depth': depth}
#         return evaluation
#
#     legal_moves = list(board.legal_moves)
#     best_move = None
#     if maximizing_player:
#         max_eval = float('-inf')
#         for move in legal_moves:
#             board.push(move)
#             eval = -minimax(board, depth - 1, False, -beta, -alpha, transposition_table)
#             board.pop()
#             max_eval = max(max_eval, eval)
#             alpha = max(alpha, eval)
#             if beta <= alpha:
#                 break
#         transposition_table[board_hash] = {'value': max_eval, 'depth': depth}
#         return max_eval
#     else:
#         min_eval = float('inf')
#         for move in legal_moves:
#             board.push(move)
#             eval = -minimax(board, depth - 1, True, -beta, -alpha, transposition_table)
#             board.pop()
#             min_eval = min(min_eval, eval)
#             beta = min(beta, eval)
#             if beta <= alpha:
#                 break
#         transposition_table[board_hash] = {'value': min_eval, 'depth': depth}
#         return min_eval
#
#
# def negaScout(board, depth, maximizing_player, alpha, beta, transposition_table):
#     board_hash = get_board_hash(board)
#     if board_hash in transposition_table:
#         entry = transposition_table[board_hash]
#         if entry['depth'] >= depth:
#             return entry['value']
#
#     if depth == 0 or board.is_game_over():
#         evaluation = evaluate(board)
#         transposition_table[board_hash] = {'value': evaluation, 'depth': depth}
#         return evaluation
#
#     legal_moves = list(board.legal_moves)
#     best_move = None
#     if maximizing_player:
#         max_eval = float('-inf')
#         first_move = True
#         for move in legal_moves:
#             board.push(move)
#             if first_move:
#                 eval = -negaScout(board, depth - 1, False, -beta, -alpha, transposition_table)
#                 first_move = False
#             else:
#                 eval = -negaScout(board, depth - 1, False, -alpha - 1, -alpha, transposition_table)
#                 if alpha < eval < beta:
#                     eval = -negaScout(board, depth - 1, False, -beta, -alpha, transposition_table)
#             board.pop()
#             max_eval = max(max_eval, eval)
#             alpha = max(alpha, eval)
#             if beta <= alpha:
#                 break
#         transposition_table[board_hash] = {'value': max_eval, 'depth': depth}
#         return max_eval
#     else:
#         min_eval = float('inf')
#         first_move = True
#         for move in legal_moves:
#             board.push(move)
#             if first_move:
#                 eval = -negaScout(board, depth - 1, True, -beta, -alpha, transposition_table)
#                 first_move = False
#             else:
#                 eval = -negaScout(board, depth - 1, True, -alpha - 1, -alpha, transposition_table)
#                 if alpha < eval < beta:
#                     eval = -negaScout(board, depth - 1, True, -beta, -alpha, transposition_table)
#             board.pop()
#             min_eval = min(min_eval, eval)
#             beta = min(beta, eval)
#             if beta <= alpha:
#                 break
#         transposition_table[board_hash] = {'value': min_eval, 'depth': depth}
#         return min_eval
#
#
# def iterative_deepening(board, max_depth):
#     best_move = None
#     transposition_table.clear()  # Clear transposition table for each search
#     for depth in range(1, max_depth + 1):
#         alpha, beta = -float('inf'), float('inf')
#         legal_moves = list(board.legal_moves)
#
#         # Parallelize search at the root level using CUDA
#         with concurrent.futures.ProcessPoolExecutor() as executor:
#             futures = []
#             for move in legal_moves:
#                 board.push(move)
#                 futures.append(executor.submit(negaScout, board, depth - 1, False, -beta, -alpha, transposition_table))
#                 board.pop()
#
#             for future in futures:
#                 result = future.result()
#                 if result > alpha:
#                     alpha = result
#                     best_move = legal_moves[futures.index(future)]
#     return best_move
#

import chess
import concurrent.futures
import hashlib
import tensorflow as tf

# This will hold transposition information.
transposition_table = {}

if tf.config.list_physical_devices('GPU'):
    print("GPU is available.")
else:
    print("GPU is not available.")

def quiescence(board, alpha, beta):
    stand_pat = evaluate(board)
    if stand_pat >= beta:
        return beta
    if alpha < stand_pat:
        alpha = stand_pat

    legal_moves = list(board.legal_moves)
    legal_moves.sort(key=lambda move: (board.is_capture(move) or board.gives_check(move), move), reverse=True)

    for move in legal_moves:
        if board.is_capture(move) or board.gives_check(move):
            board.push(move)
            score = -quiescence(board, -beta, -alpha)
            board.pop()
            if score >= beta:
                return beta
            if score > alpha:
                alpha = score
    return alpha


def evaluate(board):
    piece_values = {
        chess.PAWN: 100,
        chess.KNIGHT: 320,
        chess.BISHOP: 330,
        chess.ROOK: 500,
        chess.QUEEN: 900,
        chess.KING: 20000
    }

    piece_map = board.piece_map()

    # Specify that the tensor should be created on the GPU
    with tf.device('/GPU:0'):  # Explicitly tell TensorFlow to use the GPU
        pieces = tf.constant(
            [piece_values.get(piece.piece_type, 0) if piece.color == chess.WHITE else -piece_values.get(piece.piece_type, 0)
             for piece in piece_map.values()], dtype=tf.float32)

        # Sum all pieces and return the result
        return tf.reduce_sum(pieces).numpy()  # Convert tensor back to numpy for return value


def get_board_hash(board):
    return hashlib.sha256(board.fen().encode('utf-8')).hexdigest()


def minimax(board, depth, maximizing_player, alpha, beta, transposition_table):
    board_hash = get_board_hash(board)
    if board_hash in transposition_table:
        entry = transposition_table[board_hash]
        if entry['depth'] >= depth:
            return entry['value']

    if depth == 0 or board.is_game_over():
        evaluation = evaluate(board)
        transposition_table[board_hash] = {'value': evaluation, 'depth': depth}
        return evaluation

    legal_moves = list(board.legal_moves)
    best_move = None
    if maximizing_player:
        max_eval = float('-inf')
        for move in legal_moves:
            board.push(move)
            eval = -minimax(board, depth - 1, False, -beta, -alpha, transposition_table)
            board.pop()
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        transposition_table[board_hash] = {'value': max_eval, 'depth': depth}
        return max_eval
    else:
        min_eval = float('inf')
        for move in legal_moves:
            board.push(move)
            eval = -minimax(board, depth - 1, True, -beta, -alpha, transposition_table)
            board.pop()
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break
        transposition_table[board_hash] = {'value': min_eval, 'depth': depth}
        return min_eval


def negaScout(board, depth, maximizing_player, alpha, beta, transposition_table):
    board_hash = get_board_hash(board)
    if board_hash in transposition_table:
        entry = transposition_table[board_hash]
        if entry['depth'] >= depth:
            return entry['value']

    if depth == 0 or board.is_game_over():
        evaluation = evaluate(board)
        transposition_table[board_hash] = {'value': evaluation, 'depth': depth}
        return evaluation

    legal_moves = list(board.legal_moves)
    best_move = None
    if maximizing_player:
        max_eval = float('-inf')
        first_move = True
        for move in legal_moves:
            board.push(move)
            if first_move:
                eval = -negaScout(board, depth - 1, False, -beta, -alpha, transposition_table)
                first_move = False
            else:
                eval = -negaScout(board, depth - 1, False, -alpha - 1, -alpha, transposition_table)
                if alpha < eval < beta:
                    eval = -negaScout(board, depth - 1, False, -beta, -alpha, transposition_table)
            board.pop()
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        transposition_table[board_hash] = {'value': max_eval, 'depth': depth}
        return max_eval
    else:
        min_eval = float('inf')
        first_move = True
        for move in legal_moves:
            board.push(move)
            if first_move:
                eval = -negaScout(board, depth - 1, True, -beta, -alpha, transposition_table)
                first_move = False
            else:
                eval = -negaScout(board, depth - 1, True, -alpha - 1, -alpha, transposition_table)
                if alpha < eval < beta:
                    eval = -negaScout(board, depth - 1, True, -beta, -alpha, transposition_table)
            board.pop()
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break
        transposition_table[board_hash] = {'value': min_eval, 'depth': depth}
        return min_eval


def iterative_deepening(board, max_depth):
    best_move = None
    transposition_table.clear()  # Clear transposition table for each search
    for depth in range(1, max_depth + 1):
        alpha, beta = -float('inf'), float('inf')
        legal_moves = list(board.legal_moves)

        # Parallelize search at the root level using concurrent futures
        with concurrent.futures.ProcessPoolExecutor() as executor:
            futures = []
            for move in legal_moves:
                board.push(move)
                futures.append(executor.submit(negaScout, board, depth - 1, False, -beta, -alpha, transposition_table))
                board.pop()

            for future in futures:
                result = future.result()
                if result > alpha:
                    alpha = result
                    best_move = legal_moves[futures.index(future)]
    return best_move
