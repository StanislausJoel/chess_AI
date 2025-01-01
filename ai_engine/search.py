# # import chess
# #
# # class Eval:
# #     @staticmethod
# #     def evaluate(board):
# #         piece_values = {
# #             chess.PAWN: 1,
# #             chess.KNIGHT: 3,
# #             chess.BISHOP: 3,
# #             chess.ROOK: 5,
# #             chess.QUEEN: 9,
# #             chess.KING: 0
# #         }
# #         value = 0
# #
# #         for square in chess.SQUARES:
# #             piece = board.piece_at(square)
# #             if piece:
# #                 piece_value = piece_values[piece.piece_type]
# #                 if piece.color:  # White piece
# #                     value += piece_value
# #                 else:  # Black piece
# #                     value -= piece_value
# #         return value
# #
# # def minimax(board : chess.Board, depth, maximizing_player, alpha, beta):
# #     if depth == 0 or board.is_game_over():
# #         return Eval.evaluate(board)
# #
# #     moves = board.generate_legal_moves()
# #
# #     if not moves:
# #         if board.is_checkmate():
# #             return float('-inf')
# #         return 0
# #
# #     for move in moves:
# #         board.push(move)
# #         evaluation = -minimax(board, depth - 1, -maximizing_player, -beta, -alpha)
# #         board.pop()
# #
# #         if evaluation >= beta:
# #             return beta
# #
# #         alpha = max(alpha, evaluation)
# #
# #     return alpha
# #
#
#
# import chess
#
# class Eval:
#     @staticmethod
#     def evaluate(board):
#         piece_values = {
#             chess.PAWN: 1,
#             chess.KNIGHT: 3,
#             chess.BISHOP: 3,
#             chess.ROOK: 5,
#             chess.QUEEN: 9,
#             chess.KING: 0
#         }
#
#         pst_pawn = [
#             0, 0, 0, 0, 0, 0, 0, 0,
#             50, 50, 50, 50, 50, 50, 50, 50,
#             10, 10, 20, 30, 30, 20, 10, 10,
#             5, 5, 10, 25, 25, 10, 5, 5,
#             0, 0, 0, 20, 20, 0, 0, 0,
#             5, -5, -10, 0, 0, -10, -5, 5,
#             5, 5, 10, 15, 15, 10, 5, 5,
#             0, 0, 0, 0, 0, 0, 0, 0
#         ]
#
#         pst_knight = [
#             -50, -40, -30, -30, -30, -30, -40, -50,
#             -40, -20, 0, 10, 10, 0, -20, -40,
#             -30, 10, 20, 30, 30, 20, 10, -30,
#             -30, 10, 30, 40, 40, 30, 10, -30,
#             -30, 10, 30, 40, 40, 30, 10, -30,
#             -30, 10, 20, 30, 30, 20, 10, -30,
#             -40, -20, 0, 10, 10, 0, -20, -40,
#             -50, -40, -30, -30, -30, -30, -40, -50
#         ]
#
#         pst_bishop = [
#             -50, -40, -30, -20, -20, -30, -40, -50,
#             -40, -20, 0, 10, 10, 0, -20, -40,
#             -30, 0, 10, 20, 20, 10, 0, -30,
#             -20, 10, 20, 30, 30, 20, 10, -20,
#             -20, 0, 10, 30, 30, 10, 0, -20,
#             -30, -20, 0, 10, 10, 0, -20, -30,
#             -40, -30, -20, -20, -20, -20, -30, -40,
#             -50, -40, -30, -20, -20, -30, -40, -50
#         ]
#
#         pst_rook = [
#             0, 0, 0, 5, 5, 0, 0, 0,
#             0, 5, 10, 10, 10, 10, 5, 0,
#             0, 5, 10, 15, 15, 10, 5, 0,
#             0, 5, 10, 20, 20, 10, 5, 0,
#             0, 5, 10, 20, 20, 10, 5, 0,
#             0, 5, 10, 20, 20, 10, 5, 0,
#             0, 0, 0, 15, 15, 0, 0, 0,
#             0, 0, 0, 5, 5, 0, 0, 0
#         ]
#
#         pst_queen = [
#             -20, -10, 0, 5, 5, 0, -10, -20,
#             -10, 0, 10, 15, 15, 10, 0, -10,
#             0, 10, 20, 25, 25, 20, 10, 0,
#             5, 15, 25, 30, 30, 25, 15, 5,
#             5, 15, 25, 30, 30, 25, 15, 5,
#             0, 10, 20, 25, 25, 20, 10, 0,
#             -10, 0, 10, 15, 15, 10, 0, -10,
#             -20, -10, 0, 5, 5, 0, -10, -20
#         ]
#
#         pst_king = [
#             -30, -40, -50, -60, -60, -50, -40, -30,
#             -40, -50, -60, -70, -70, -60, -50, -40,
#             -50, -60, -70, -80, -80, -70, -60, -50,
#             -60, -70, -80, -90, -90, -80, -70, -60,
#             -60, -70, -80, -90, -90, -80, -70, -60,
#             -50, -60, -70, -80, -80, -70, -60, -50,
#             -40, -50, -60, -70, -70, -60, -50, -40,
#             -30, -40, -50, -60, -60, -50, -40, -30
#         ]
#
#         # Initialize total evaluation value
#         value = 0
#
#         for square in chess.SQUARES:
#             piece = board.piece_at(square)
#
#             if piece:
#                 piece_value = piece_values[piece.piece_type]
#                 if piece.color:  # White piece
#                     value += piece_value
#                 else:  # Black piece
#                     value -= piece_value
#
#                 # Add positional value for each piece type
#                 if piece.piece_type == chess.PAWN:
#                     value += pst_pawn[square]
#                 elif piece.piece_type == chess.KNIGHT:
#                     value += pst_knight[square]
#                 elif piece.piece_type == chess.BISHOP:
#                     value += pst_bishop[square]
#                 elif piece.piece_type == chess.ROOK:
#                     value += pst_rook[square]
#                 elif piece.piece_type == chess.QUEEN:
#                     value += pst_queen[square]
#                 elif piece.piece_type == chess.KING:
#                     value += pst_king[square]
#
#         return value
#
# def minimax(board : chess.Board, depth, maximizing_player, alpha, beta):
#     if depth == 0 or board.is_game_over():
#         return Eval.evaluate(board)
#
#     moves = board.generate_legal_moves()
#
#     if not moves:
#         if board.is_checkmate():
#             return float('-inf') if maximizing_player else float('inf')  # Assign appropriate values for checkmate
#         return 0
#
#     if maximizing_player:
#         max_eval = float('-inf')
#         for move in moves:
#             board.push(move)
#             evaluation = minimax(board, depth - 1, False, alpha, beta)
#             board.pop()
#
#             max_eval = max(max_eval, evaluation)
#             alpha = max(alpha, evaluation)
#             if beta <= alpha:
#                 break
#
#         return max_eval
#     else:
#         min_eval = float('inf')
#         for move in moves:
#             board.push(move)
#             evaluation = minimax(board, depth - 1, True, alpha, beta)
#             board.pop()
#
#             min_eval = min(min_eval, evaluation)
#             beta = min(beta, evaluation)
#             if beta <= alpha:
#                 break
#
#         return min_eval

import chess


class Eval:
    @staticmethod
    def evaluate(board):
        piece_values = {
            chess.PAWN: 1,
            chess.KNIGHT: 3,
            chess.BISHOP: 3,
            chess.ROOK: 5,
            chess.QUEEN: 9,
            chess.KING: 1000  # King has the highest value
        }

        pst_pawn = [
            0, 0, 0, 0, 0, 0, 0, 0,
            50, 50, 50, 50, 50, 50, 50, 50,
            10, 10, 20, 30, 30, 20, 10, 10,
            5, 5, 10, 25, 25, 10, 5, 5,
            0, 0, 0, 20, 20, 0, 0, 0,
            5, -5, -10, 0, 0, -10, -5, 5,
            5, 5, 10, 15, 15, 10, 5, 5,
            0, 0, 0, 0, 0, 0, 0, 0
        ]

        pst_knight = [
            -50, -40, -30, -30, -30, -30, -40, -50,
            -40, -20, 0, 10, 10, 0, -20, -40,
            -30, 10, 20, 30, 30, 20, 10, -30,
            -30, 10, 30, 40, 40, 30, 10, -30,
            -30, 10, 30, 40, 40, 30, 10, -30,
            -30, 10, 20, 30, 30, 20, 10, -30,
            -40, -20, 0, 10, 10, 0, -20, -40,
            -50, -40, -30, -30, -30, -30, -40, -50
        ]

        pst_bishop = [
            -50, -40, -30, -20, -20, -30, -40, -50,
            -40, -20, 0, 10, 10, 0, -20, -40,
            -30, 0, 10, 20, 20, 10, 0, -30,
            -20, 10, 20, 30, 30, 20, 10, -20,
            -20, 0, 10, 30, 30, 10, 0, -20,
            -30, -20, 0, 10, 10, 0, -20, -30,
            -40, -30, -20, -20, -20, -20, -30, -40,
            -50, -40, -30, -20, -20, -30, -40, -50
        ]

        pst_rook = [
            0, 0, 0, 5, 5, 0, 0, 0,
            0, 5, 10, 10, 10, 10, 5, 0,
            0, 5, 10, 15, 15, 10, 5, 0,
            0, 5, 10, 20, 20, 10, 5, 0,
            0, 5, 10, 20, 20, 10, 5, 0,
            0, 5, 10, 20, 20, 10, 5, 0,
            0, 0, 0, 15, 15, 0, 0, 0,
            0, 0, 0, 5, 5, 0, 0, 0
        ]

        pst_queen = [
            -20, -10, 0, 5, 5, 0, -10, -20,
            -10, 0, 10, 15, 15, 10, 0, -10,
            0, 10, 20, 25, 25, 20, 10, 0,
            5, 15, 25, 30, 30, 25, 15, 5,
            5, 15, 25, 30, 30, 25, 15, 5,
            0, 10, 20, 25, 25, 20, 10, 0,
            -10, 0, 10, 15, 15, 10, 0, -10,
            -20, -10, 0, 5, 5, 0, -10, -20
        ]

        pst_king = [
            -30, -40, -50, -60, -60, -50, -40, -30,
            -40, -50, -60, -70, -70, -60, -50, -40,
            -50, -60, -70, -80, -80, -70, -60, -50,
            -60, -70, -80, -90, -90, -80, -70, -60,
            -60, -70, -80, -90, -90, -80, -70, -60,
            -50, -60, -70, -80, -80, -70, -60, -50,
            -40, -50, -60, -70, -70, -60, -50, -40,
            -30, -40, -50, -60, -60, -50, -40, -30
        ]

        # Initialize total evaluation value
        value = 0

        for square in chess.SQUARES:
            piece = board.piece_at(square)

            if piece:
                piece_value = piece_values[piece.piece_type]
                if piece.color:  # White piece
                    value += piece_value
                else:  # Black piece
                    value -= piece_value

                # Add positional value for each piece type
                if piece.piece_type == chess.PAWN:
                    value += pst_pawn[square]
                elif piece.piece_type == chess.KNIGHT:
                    value += pst_knight[square]
                elif piece.piece_type == chess.BISHOP:
                    value += pst_bishop[square]
                elif piece.piece_type == chess.ROOK:
                    value += pst_rook[square]
                elif piece.piece_type == chess.QUEEN:
                    value += pst_queen[square]
                elif piece.piece_type == chess.KING:
                    value += pst_king[square]

        return value

    @staticmethod
    def evaluate_piece(piece_type):
        piece_values = {
            chess.PAWN: 1,
            chess.KNIGHT: 3,
            chess.BISHOP: 3,
            chess.ROOK: 5,
            chess.QUEEN: 9,
            chess.KING: 1000  # King has the highest value
        }
        return piece_values.get(piece_type, 0)  # Default to 0 if no piece matches

    @staticmethod
    def evaluate_move(move, board):
        evaluation = 0

        if move.promotion:  # Handle promoted pieces (like promoted pawn to queen)
            evaluation += 9  # Add value for promoted queen
        elif board.is_capture(move):  # If the move captures a piece
            captured_piece = board.piece_at(move.to_square)
            captured_value = Eval.evaluate_piece(captured_piece.piece_type)
            if captured_piece.color != board.turn:  # Capturing opponent's piece
                evaluation += captured_value * 2  # Give extra value for capturing an opponent's piece
            else:  # Capturing own piece (this is not a good move, subtract value)
                evaluation -= captured_value

        return evaluation


def minimax(board: chess.Board, depth, maximizing_player, alpha, beta):
    if depth == 0 or board.is_game_over():
        return Eval.evaluate(board)

    moves = board.legal_moves

    if not moves:
        if board.is_checkmate():
            return float('-inf') if maximizing_player else float('inf')
        return 0

    best_eval = float('-inf') if maximizing_player else float('inf')

    for move in moves:
        board.push(move)

        move_eval = Eval.evaluate_move(move, board)

        evaluation = Eval.evaluate(board) + move_eval

        if maximizing_player:
            best_eval = max(best_eval, evaluation)
            alpha = max(alpha, best_eval)
        else:
            best_eval = min(best_eval, evaluation)
            beta = min(beta, best_eval)

        board.pop()

        if beta <= alpha:
            break

    return best_eval


