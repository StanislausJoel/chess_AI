from core.board import ChessBoard

pawn_value = 100
knight_value = 300
bishop_value = 320
rook_value = 500
queen_value = 900

def evaluate(board : ChessBoard):
    white_eval = 0
    black_eval = 0

    white_material, black_material = count_pieces(board)

    white_eval = white_material
    black_eval = black_material

    evaluation_score = white_eval - black_eval
    perspective = 1 if board.turn else -1

    return evaluation_score * perspective

def count_pieces(board : ChessBoard):
    white = 0
    black = 0

    for row in board.grid:
        for col in row:
            score = 0
            match col[1]:
                case 'p':
                    score = pawn_value
                case 'n':
                    score = knight_value
                case 'b':
                    score = bishop_value
                case 'r':
                    score = rook_value
                case 'q':
                    score = queen_value

            if col[0] == 'b': black += score
            else: white += score

    return white, black