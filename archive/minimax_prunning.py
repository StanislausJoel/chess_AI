from ai_engine import eval
from core.board import ChessBoard

def minimax(depth, node_index, maximizing_player, values, alpha, beta):
    if depth == 3:
        return eval.evaluate(ChessBoard())

    if maximizing_player:
        best = float('-inf')

        for i in range(0, 2):
            val = minimax(depth + 1, node_index * 2 + i, False, values, alpha, beta)
            best = max(best, val)
            alpha = max(alpha, best)

            if beta <= alpha:
                break
        return best
    else:
        best = float('inf')

        for i in range(0, 2):

            val = minimax(depth + 1, node_index * 2 + i, True, values, alpha, beta)
            best = min(best, val)
            beta = min(beta, best)

            if beta <= alpha:
                break
        return best