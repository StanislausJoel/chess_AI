import chess
import time
from stockfish import Stockfish

transposition_table = {}
stockfish = Stockfish("stockfish/stockfish-windows-x86-64-avx2.exe")

# Evaluation Function with Pawn Promotion Consideration
def evaluate(board):
    piece_values = {
        chess.PAWN: 100,
        chess.KNIGHT: 320,
        chess.BISHOP: 330,
        chess.ROOK: 500,
        chess.QUEEN: 900,
        chess.KING: 20000
    }

    # Positional Evaluation Factors
    king_safety = 0
    for square in board.pieces(chess.KING, chess.WHITE):
        king_safety += evaluate_king_safety(board, chess.WHITE)
    for square in board.pieces(chess.KING, chess.BLACK):
        king_safety -= evaluate_king_safety(board, chess.BLACK)

    # Central Control
    center_control = 0
    center_squares = [chess.D4, chess.D5, chess.E4, chess.E5]
    for square in center_squares:
        if board.piece_at(square):
            piece = board.piece_at(square)
            center_control += 50 if piece.color == chess.WHITE else -50

    # Piece Development
    development_bonus = 0
    for square in board.pieces(chess.KNIGHT, chess.WHITE):
        if square not in [chess.B1, chess.G1]:
            development_bonus += 10
    for square in board.pieces(chess.KNIGHT, chess.BLACK):
        if square not in [chess.B8, chess.G8]:
            development_bonus -= 10

    # Piece Mobility
    mobility_score = len(list(board.legal_moves))  # Simple mobility score

    # Passed Pawn Bonus
    passed_pawn_bonus = 0
    promotion_bonus = 0  # New promotion bonus
    for square in board.pieces(chess.PAWN, chess.WHITE):
        if is_passed_pawn(board, square, chess.WHITE):
            passed_pawn_bonus += 50
        if chess.square_rank(square) == 6:  # 7th rank
            promotion_bonus += 100
    for square in board.pieces(chess.PAWN, chess.BLACK):
        if is_passed_pawn(board, square, chess.BLACK):
            passed_pawn_bonus -= 50
        if chess.square_rank(square) == 1:  # 2nd rank
            promotion_bonus -= 100

    # Piece Values
    value = 0
    for piece in board.piece_map().values():
        piece_value = piece_values.get(piece.piece_type, 0)
        value += piece_value if piece.color == chess.WHITE else -piece_value

    # Combine all evaluation factors
    return value + center_control + development_bonus + king_safety + mobility_score + passed_pawn_bonus + promotion_bonus

# Check if a pawn is passed
def is_passed_pawn(board, pawn_square, color):
    direction = 1 if color == chess.WHITE else -1
    file = chess.square_file(pawn_square)
    rank = chess.square_rank(pawn_square)

    # Check if no opposing pawns are in the way
    for offset in [-1, 1]:
        check_square = chess.square(file + offset, rank + direction)
        if board.piece_at(check_square) and board.piece_at(check_square).color != color:
            return False
    return True

# King Safety Evaluation (simple version)
def evaluate_king_safety(board, color):
    safety_score = 0
    king_square = board.king(color)
    if king_square:
        # Check for nearby pieces and structure
        if board.is_attacked_by(not color, king_square):
            safety_score -= 50  # Penalize if the king is under attack
        else:
            safety_score += 10  # Reward if the king is safe
    return safety_score

# Move Ordering (enhanced for development, center control, etc.)
def order_moves(board, legal_moves):
    move_scores = []
    for move in legal_moves:
        board.push(move)
        score = evaluate_stockfish(board)
        board.pop()
        move_scores.append((move, score))
    move_scores.sort(key=lambda x: x[1], reverse=True)
    return [move for move, _ in move_scores]

def evaluate_stockfish(board):
    stockfish.set_fen_position(board.fen())
    eval = stockfish.get_evaluation()

    if eval['type'] == 'cp':
        return eval['value'] / 100.0
    elif eval['type'] == 'mate':
        return 10000 if eval['value'] > 0 else -10000

    return 0

def minimax(board, depth, maximizing_player, alpha, beta, ai_type):
    board_hash = hash(board.fen())

    if board_hash in transposition_table:
        return transposition_table[board_hash]

    if depth == 0 or board.is_game_over():
        evaluation = None

        if ai_type == "custom":
            evaluation = evaluate(board)
        elif ai_type == "stockfish":
            evaluation = evaluate_stockfish(board)
        transposition_table[board_hash] = evaluation
        return evaluation

    legal_moves = list(board.legal_moves)
    legal_moves = order_moves(board, legal_moves)

    if maximizing_player:
        max_eval = float('-inf')
        for move in legal_moves:
            board.push(move)
            eval = minimax(board, depth - 1, False, alpha, beta, ai_type)
            board.pop()
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        transposition_table[board_hash] = max_eval
        return max_eval
    else:
        min_eval = float('inf')
        for move in legal_moves:
            board.push(move)
            eval = minimax(board, depth - 1, True, alpha, beta, ai_type)
            board.pop()
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break
        transposition_table[board_hash] = min_eval
        return min_eval

def iterative_deepening(board, max_depth, time_limit, player, ai_type):
    best_move = None
    start_time = time.time()

    for depth in range(1, max_depth):
        alpha, beta = -float('inf'), float('inf')
        current_best_move = None
        legal_moves = list(board.legal_moves)
        legal_moves = order_moves(board, legal_moves)

        for move in legal_moves:
            if time.time() - start_time >= time_limit:
                return current_best_move

            board.push(move)
            score = minimax(board, depth, player, alpha, beta, ai_type)
            # score = minimax(board, depth, alpha, beta, player, ai_type)
            board.pop()

            if score > alpha:
                alpha = score
                current_best_move = move

            if alpha >= beta:  # Prune the remaining moves
                break

        best_move = current_best_move

        if time.time() - start_time >= time_limit:
            break

    return best_move

# def minimax(board, depth, alpha, beta, maximizing_player, ai_type):
#     board_hash = hash(board.fen)
#
#     if board_hash in transposition_table:
#         return transposition_table[board_hash]
#
#     if depth == 0 or board.is_game_over():
#         evaluation = None
#
#         if ai_type == "custom":
#             evaluation = evaluate(board)
#         elif ai_type == "stockfish":
#             evaluation = evaluate_stockfish(board)
#
#         transposition_table[board_hash] = evaluation
#         return evaluation
#
#     legal_moves = list(board.legal_moves)
#
#     if maximizing_player:
#         max_eval = float('-inf')
#
#         for move in legal_moves:
#             board.push(move)
#             evaluation = minimax(board, depth - 1, alpha, beta, False, ai_type)
#             current_hash = hash(board.fen)
#             board.pop()
#             transposition_table[current_hash] = evaluation
#             max_eval = max(max_eval, evaluation)
#             alpha = max(alpha, evaluation)
#
#             if beta <= alpha:
#                 break
#
#         return max_eval
#     else:
#         min_eval = float('inf')
#
#         for move in legal_moves:
#             board.push(move)
#             evaluation = minimax(board, depth - 1, alpha, beta, True, ai_type)
#             current_hash = hash(board.fen)
#             board.pop()
#             transposition_table[current_hash] = evaluation
#             min_eval = min(min_eval, evaluation)
#             beta = min(beta, evaluation)
#
#             if beta <= alpha:
#                 break
#
#         return min_eval

# def iterative_deepening(board, max_depth, time_limit, player, ai_type):
#     maximizing = True if player == chess.WHITE else False
#     best_score = float('-inf') if maximizing else float('-inf')
#     best_move = None
#
#     start_time = time.time()
#
#     for depth in range(1, max_depth):
#         current_best_score = float('-inf') if maximizing else float('-inf')
#         current_best_move = None
#         legal_moves = list(board.legal_moves)
#         # legal_moves = order_moves(board, legal_moves)
#         # print(legal_moves)
#
#         for move in legal_moves:
#             # print(move)
#             if time.time() - start_time >= time_limit:
#                 print("break")
#                 return best_move
#
#             board.push(move)
#             score = minimax(board, depth, float('-inf'), float('inf'), maximizing, ai_type)
#             # print(score)
#             board.pop()
#
#             if (maximizing and (score > current_best_score)) or (not maximizing and (score < current_best_score)):
#                 current_best_score, current_best_move = score, move
#                 print("current bm: ", move)
#
#         if (maximizing and (current_best_score > best_score)) or (not maximizing and (current_best_score < best_score)):
#             best_score, best_move = current_best_score, current_best_move
#             print("best_move: ", best_move)
#
#         if time.time() - start_time >= time_limit:
#             return best_move
#
#     return best_move

# def iterative_deepening(board, max_depth, time_limit, player, ai_type):
#     best_score = float('-inf') if player else float('inf')
#     best_move = None
#
#     start_time = time.time()
#
#     for depth in range(1, max_depth + 1):
#         current_best_score = float('-inf') if player else float('inf')
#         current_best_move = None
#         legal_moves = list(board.legal_moves)
#
#         if not legal_moves:  # No legal moves
#             return None
#
#         for move in legal_moves:
#             if time.time() - start_time >= time_limit:
#                 return best_move if best_move else current_best_move
#
#             board.push(move)
#             score = minimax(board, depth, float('-inf'), float('inf'), player, ai_type)
#             board.pop()
#
#             if (player and score > current_best_score) or (not player and score < current_best_score):
#                 current_best_score, current_best_move = score, move
#
#         if (player and current_best_score > best_score) or (not player and current_best_score < best_score):
#             best_score, best_move = current_best_score, current_best_move
#
#         if time.time() - start_time >= time_limit:
#             return best_move
#
#     return best_move

