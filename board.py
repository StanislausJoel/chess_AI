import pygame
import chess
from ai_engine.search import iterative_deepening
from stockfish import Stockfish
import time

pygame.mixer.init()
stockfish = Stockfish("stockfish/stockfish-windows-x86-64-avx2.exe") #Stockfish binary - Buat evaluation
capture_sound = pygame.mixer.Sound("assets/sfx/capture.mp3")
move_sound = pygame.mixer.Sound("assets/sfx/move-self.mp3")

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
        self.transposition_table = {}

        self.GAME_OVER_COLOR = (255, 0, 0)
        self.BUTTON_COLOR = (0, 255, 0)
        self.BUTTON_HOVER_COLOR = (0, 200, 0)
        self.BUTTON_TEXT_COLOR = (255, 255, 255)
        self.BUTTON_WIDTH = 200
        self.BUTTON_HEIGHT = 50
        self.BUTTON_PADDING = 20

    def load_piece_images(self):
        pieces = ["bp", "br", "bn", "bb", "bq", "bk", "wp", "wr", "wn", "wb", "wq", "wk"]
        images = {}
        for piece in pieces:
            images[piece] = pygame.image.load(f"assets/{piece}.png")
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
                move_sound.play()
            else:
                for legal_move in self.board.legal_moves:
                    if move.from_square == legal_move.from_square and move.to_square == legal_move.to_square:
                        if legal_move.promotion:
                            promotion_move = chess.Move(self.selected_square, square, promotion=legal_move.promotion)
                            if promotion_move in self.board.legal_moves:
                                self.board.push(promotion_move)
                                move_sound.play()

            if self.board.is_capture(move):
                capture_sound.play()

            self.selected_square = None
            self.valid_moves = []

    def display_game_over(self, player, ai_type, loser):
        if loser == chess.BLACK:
            winner_text = f"White Wins!"
        else:
            winner_text = f"Black Wins!"

        game_over_text = self.font.render('Game Over', True, self.GAME_OVER_COLOR)
        game_over_text_rect = game_over_text.get_rect(
            center=(self.screen.get_width() // 2, self.screen.get_height() // 2 - 50))

        winner_text_render = self.font.render(winner_text, True, self.GAME_OVER_COLOR)
        winner_text_rect = winner_text_render.get_rect(
            center=(self.screen.get_width() // 2, self.screen.get_height() // 2))

        button_rect = pygame.Rect(self.screen.get_width() // 2 - self.BUTTON_WIDTH // 2,
                                  self.screen.get_height() // 2 + self.BUTTON_PADDING,
                                  self.BUTTON_WIDTH, self.BUTTON_HEIGHT)
        button_text = self.font.render('Restart', True, self.BUTTON_TEXT_COLOR)
        button_text_rect = button_text.get_rect(center=button_rect.center)

        self.screen.fill((255, 255, 255))
        self.screen.blit(game_over_text, game_over_text_rect)
        self.screen.blit(winner_text_render, winner_text_rect)

        pygame.draw.rect(self.screen, self.BUTTON_COLOR, button_rect)
        self.screen.blit(button_text, button_text_rect)
        pygame.display.flip()

        waiting_for_input = True
        while waiting_for_input:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

                # Mouse event for button hover and click
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = event.pos
                    if button_rect.collidepoint(mouse_x, mouse_y):
                        self.restart_game(player, ai_type)
                        waiting_for_input = False
                if event.type == pygame.MOUSEMOTION:
                    mouse_x, mouse_y = event.pos
                    if button_rect.collidepoint(mouse_x, mouse_y):
                        pygame.draw.rect(self.screen, self.BUTTON_HOVER_COLOR, button_rect)
                    else:
                        pygame.draw.rect(self.screen, self.BUTTON_COLOR, button_rect)

                # Keyboard event for restarting game
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        self.restart_game(player, ai_type)
                        waiting_for_input = False
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        quit()

                self.screen.blit(game_over_text, game_over_text_rect)  # Re-render "Game Over"
                self.screen.blit(winner_text_render, winner_text_rect)  # Re-render winner text
                self.screen.blit(button_text, button_text_rect)  # Re-render button text
                pygame.display.flip()

    def restart_game(self, player, ai_type):
        self.board.reset()
        game.run(player, ai_type)

    def ai_move(self, ai_type):
        time.sleep(0.5)
        max_depth = 3
        time_limit = 10

        best_move = iterative_deepening(self.board, max_depth, time_limit, self.board.turn, ai_type)
        print(best_move)

        if best_move:
            self.board.push(best_move)
            if self.board.is_capture(best_move):
                capture_sound.play()
            else:
                move_sound.play()

    def run(self, player, ai_type):
        self.clock.tick(60)
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.MOUSEBUTTONDOWN and player == "player" and self.board.turn:
                    self.handle_click(event.pos)
                elif player != "player":
                    time.sleep(0.5)
                    self.ai_move(player)

                self.screen.fill((0, 0, 0))
                self.draw_board()
                pygame.display.update()

            if not self.board.turn:
                self.ai_move(ai_type)

            self.screen.fill((0, 0, 0))
            self.draw_board()
            pygame.display.flip()

            if self.board.is_checkmate() or self.board.is_game_over():
                time.sleep(3)
                self.display_game_over(player, ai_type, self.board.turn)
                pygame.display.update()

        self.clock.tick(60)
        pygame.quit()


if __name__ == "__main__":
    current_player = "player"  # player or stockfish
    ai_type = "stockfish" #stockfish or custom
    game = ChessGame()
    game.run(current_player, ai_type)