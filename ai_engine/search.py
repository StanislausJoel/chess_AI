import chess
import time

# Transposition table to store previously evaluated positions
transposition_table = {}

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
        score = evaluate(board)  # Quick evaluation
        board.pop()
        move_scores.append((move, score))
    move_scores.sort(key=lambda x: x[1], reverse=True)
    return [move for move, _ in move_scores]

# Minimax with Alpha-Beta Pruning and Transposition Table
def minimax(board, depth, maximizing_player, alpha, beta):
    board_hash = hash(board.fen())
    if board_hash in transposition_table:
        return transposition_table[board_hash]

    if depth == 0 or board.is_game_over():
        evaluation = evaluate(board)
        transposition_table[board_hash] = evaluation
        return evaluation

    legal_moves = list(board.legal_moves)
    legal_moves = order_moves(board, legal_moves)

    if maximizing_player:
        max_eval = float('-inf')
        for move in legal_moves:
            board.push(move)
            eval = -minimax(board, depth - 1, False, -beta, -alpha)
            board.pop()
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break  # Beta cut-off
        transposition_table[board_hash] = max_eval
        return max_eval
    else:
        min_eval = float('inf')
        for move in legal_moves:
            board.push(move)
            eval = -minimax(board, depth - 1, True, -beta, -alpha)
            board.pop()
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break  # Alpha cut-off
        transposition_table[board_hash] = min_eval
        return min_eval

def iterative_deepening(board, max_depth, time_limit):
    best_move = None
    start_time = time.time()

    for depth in range(1, max_depth + 1):
        alpha, beta = -float('inf'), float('inf')
        current_best_move = None
        legal_moves = list(board.legal_moves)
        legal_moves = order_moves(board, legal_moves)

        for move in legal_moves:
            if time.time() - start_time >= time_limit:
                return best_move

            board.push(move)
            score = -minimax(board, depth - 1, False, -beta, -alpha)
            board.pop()

            if score > alpha:
                alpha = score
                current_best_move = move

        best_move = current_best_move

        if time.time() - start_time >= time_limit:
            break

    return best_move