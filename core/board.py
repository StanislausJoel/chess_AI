from warnings import catch_warnings

import pygame
import chess
from ai_engine.search import minimax

class ChessGame:
    def __init__(self, square_size=80):
        pygame.init()
        self.square_size = square_size
        self.rows = 8
        self.cols = 8
        self.screen = pygame.display.set_mode((self.cols * self.square_size, self.rows * self.square_size))
        pygame.display.set_caption("Chess Game")
        self.font = pygame.font.SysFont("Arial", 24, bold=True)
        self.clock = pygame.time.Clock()
        self.running = True

        self.board = chess.Board()
        self.piece_images = self.load_piece_images()
        self.selected_square = None
        self.valid_moves = []

    def load_piece_images(self):
        pieces = ["bp", "br", "bn", "bb", "bq", "bk", "wp", "wr", "wn", "wb", "wq", "wk"]
        images = {}
        for piece in pieces:
            images[piece] = pygame.image.load(f"../assets/{piece}.png")
        return images

    def square_to_coords(self, square):
        """Convert a chess square (e.g., 'e4') to pygame coordinates."""
        col = chess.square_file(square)
        row = chess.square_rank(square)
        return 7 - row, col

    def coords_to_square(self, row, col):
        """Convert pygame coordinates to a chess square."""
        return chess.square(col, 7 - row)

    def draw_board(self):
        """Render the chessboard and pieces."""
        for row in range(self.rows):
            for col in range(self.cols):
                is_white_tile = (row + col) % 2 == 0
                tile_color = "#F0D9B5" if is_white_tile else "#B58863"
                pygame.draw.rect(
                    self.screen, tile_color,
                    (col * self.square_size, row * self.square_size, self.square_size, self.square_size)
                )

                square = self.coords_to_square(row, col)
                piece = self.board.piece_at(square)
                if piece:
                    piece_color = "w" if piece.color else "b"
                    piece_type = piece.symbol().lower()
                    piece_key = f"{piece_color}{piece_type}"
                    piece_image = self.piece_images.get(piece_key)
                    if piece_image:
                        piece_image = pygame.transform.scale(piece_image, (self.square_size, self.square_size))
                        self.screen.blit(piece_image, (col * self.square_size, row * self.square_size))

        for move in self.valid_moves:
            target_row, target_col = self.square_to_coords(move.to_square)
            pygame.draw.circle(
                self.screen, (255, 255, 255, 150),
                (target_col * self.square_size + self.square_size // 2,
                 target_row * self.square_size + self.square_size // 2),
                self.square_size // 6
            )

    def handle_click(self, pos):
        col = pos[0] // self.square_size
        row = pos[1] // self.square_size
        square = self.coords_to_square(row, col)

        if self.selected_square is None:
            piece = self.board.piece_at(square)
            if piece and (piece.color == self.board.turn):
                self.selected_square = square
                self.valid_moves = [move for move in self.board.legal_moves if move.from_square == square]
        else:
            move = chess.Move(self.selected_square, square)
            if move in self.board.legal_moves:
                self.board.push(move)
            else:
                for legal_move in self.board.legal_moves:
                    if move.from_square == legal_move.from_square and move.to_square == legal_move.to_square:
                        if legal_move.promotion:
                            promotion_move = chess.Move(self.selected_square, square, promotion=legal_move.promotion)
                            if promotion_move in self.board.legal_moves:
                                self.board.push(promotion_move)

            self.selected_square = None
            self.valid_moves = []

    def ai_move(self):
        """Make the best move for the AI using minimax."""
        best_move = None
        best_value = float('-inf') if self.board.turn else float('inf')
        alpha = float('-inf')
        beta = float('inf')

        for move in self.board.legal_moves:
            self.board.push(move)
            board_value = minimax(self.board, 3, not self.board.turn, alpha, beta)
            self.board.pop()

            if self.board.turn:  # Maximizing player
                if board_value > best_value:
                    best_value = board_value
                    best_move = move
            else:  # Minimizing player
                if board_value < best_value:
                    best_value = board_value
                    best_move = move

        if best_move:
            self.board.push(best_move)

    def run(self):
        """Main game loop."""
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.MOUSEBUTTONDOWN and self.board.turn:
                    self.handle_click(event.pos)

            # If it's AI's turn, make a move
            if not self.board.turn:
                self.ai_move()

            self.screen.fill((0, 0, 0))
            self.draw_board()
            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()


if __name__ == "__main__":
    game = ChessGame()
    game.run()