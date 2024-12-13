import pygame
import os

class ChessBoard:
    def __init__(self, rows=8, cols=8):
        self.rows = rows
        self.cols = cols
        self.grid = [[None for _ in range(cols)] for _ in range(rows)]
        self.font = None

        self.restart = False

        # Track whose turn it is: True for White's turn, False for Black's turn
        self.turn = True  # White starts first

        # Castling variables
        self.white_king_moved = False
        self.white_queen_rook_moved = False
        self.white_king_side_rook_moved = False
        self.black_king_moved = False
        self.black_queen_rook_moved = False
        self.black_king_side_rook_moved = False

        # Variables for handling pawn promotion
        self.promotion_position = None

        # Store opposing piece position from valid moves
        self.opposing_piece_positions = []

        # Path to assets directory
        self.asset_path = os.path.join(os.getcwd(), "assets")

        # Load piece images
        self.piece_images = {
            "bb": pygame.image.load(os.path.join(self.asset_path, "bb.png")),
            "bk": pygame.image.load(os.path.join(self.asset_path, "bk.png")),
            "bn": pygame.image.load(os.path.join(self.asset_path, "bn.png")),
            "bp": pygame.image.load(os.path.join(self.asset_path, "bp.png")),
            "bq": pygame.image.load(os.path.join(self.asset_path, "bq.png")),
            "br": pygame.image.load(os.path.join(self.asset_path, "br.png")),
            "wb": pygame.image.load(os.path.join(self.asset_path, "wb.png")),
            "wk": pygame.image.load(os.path.join(self.asset_path, "wk.png")),
            "wn": pygame.image.load(os.path.join(self.asset_path, "wn.png")),
            "wp": pygame.image.load(os.path.join(self.asset_path, "wp.png")),
            "wq": pygame.image.load(os.path.join(self.asset_path, "wq.png")),
            "wr": pygame.image.load(os.path.join(self.asset_path, "wr.png")),
        }

        # Load sfx
        self.sounds = {
            "move": pygame.mixer.Sound("assets/sfx/move-self.mp3"),
            "capture": pygame.mixer.Sound("assets/sfx/capture.mp3"),
        }

        # Initial positions of pieces (simplified)
        self.initialize_pieces()

        # Variables for handling dragging
        self.dragging_piece = None
        self.dragging_pos = None
        self.drag_offset = (0, 0)

    def clear_grid(self):
        """Clears the chessboard grid by setting all squares to empty."""
        for i in range(8):
            self.grid[i] = [None] * 8  # Set each square to None (empty)


    def initialize_pieces(self):
        """Set initial positions of pieces on the chessboard."""

        self.clear_grid()

        # White pieces (pawn and major pieces)
        self.grid[6] = ["wp"] * 8  # White pawns on row 6
        self.grid[7] = ["wr", "wn", "wb", "wq", "wk", "wb", "wn", "wr"]  # Other pieces on row 7
        
        # Black pieces (pawn and major pieces)
        self.grid[1] = ["bp"] * 8  # Black pawns on row 1
        self.grid[0] = ["br", "bn", "bb", "bq", "bk", "bb", "bn", "br"]  # Other pieces on row 0

    def get_valid_moves(self, piece, row, col):
        """Return valid moves for a given piece at the specified position."""
        valid_moves = []

        # Determine the type of piece and calculate valid moves
        if piece == "wp":
            # White Pawn: Moves 1 step forward, captures diagonally, and can move 2 squares forward on its first move
            if row > 0:  # Ensure the pawn is not off the board
                if self.grid[row - 1][col] is None:  # Move one step forward
                    valid_moves.append((row - 1, col))

                # First move: Can move 2 squares forward if both are empty
                if row == 6 and self.grid[row - 1][col] is None and self.grid[row - 2][col] is None:
                    valid_moves.append((row - 2, col))

                # Diagonal captures
                if col > 0 and self.grid[row - 1][col - 1] and self.grid[row - 1][col - 1][0] == "b":
                    valid_moves.append((row - 1, col - 1))
                if col < 7 and self.grid[row - 1][col + 1] and self.grid[row - 1][col + 1][0] == "b":
                    valid_moves.append((row - 1, col + 1))

        elif piece == "bp":
            # Black Pawn: Moves 1 step forward, captures diagonally, and can move 2 squares forward on its first move
            if row < 7:  # Ensure the pawn is not off the board
                if self.grid[row + 1][col] is None:  # Move one step forward
                    valid_moves.append((row + 1, col))

                # First move: Can move 2 squares forward if both are empty
                if row == 1 and self.grid[row + 1][col] is None and self.grid[row + 2][col] is None:
                    valid_moves.append((row + 2, col))

                # Diagonal captures
                if col > 0 and self.grid[row + 1][col - 1] and self.grid[row + 1][col - 1][0] == "w":
                    valid_moves.append((row + 1, col - 1))
                if col < 7 and self.grid[row + 1][col + 1] and self.grid[row + 1][col + 1][0] == "w":
                    valid_moves.append((row + 1, col + 1))

        elif piece == "wr" or piece == "br":
            # Rook: Horizontal or vertical moves
            directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # up, down, left, right

            for direction in directions:
                step = 1  # Start moving in the current direction
                while True:
                    new_row = row + direction[0] * step
                    new_col = col + direction[1] * step

                    if 0 <= new_row < 8 and 0 <= new_col < 8:
                        # If the square is empty, the rook can move here
                        if self.grid[new_row][new_col] is None:
                            valid_moves.append((new_row, new_col))
                        # If the square is occupied by a piece of the opposite color, the rook can capture it
                        elif self.grid[new_row][new_col][0] != piece[0]:
                            valid_moves.append((new_row, new_col))
                            break  # The rook captures the piece, so stop in that direction
                        else:
                            break  # The square is blocked by a piece of the same color, stop moving in this direction
                    else:
                        break  # The rook is out of bounds, stop moving in this direction

                    step += 1  # Move to the next square in this direction


        elif piece == "wn" or piece == "bn":
            # Knight: "L" shaped moves
            knight_moves = [(-2, -1), (-1, -2), (1, -2), (2, -1), (2, 1), (1, 2), (-1, 2), (-2, 1)]
            for move in knight_moves:
                new_row = row + move[0]
                new_col = col + move[1]
                if 0 <= new_row < 8 and 0 <= new_col < 8:
                    if not self.grid[new_row][new_col] or self.grid[new_row][new_col][0] != piece[0]:
                        valid_moves.append((new_row, new_col))


        elif piece == "wb" or piece == "bb":
            # Bishop: Diagonal moves in all four diagonal directions
            directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]  # top-left, top-right, bottom-left, bottom-right

            for direction in directions:
                step = 1  # Start moving in the current direction
                while True:
                    new_row = row + direction[0] * step
                    new_col = col + direction[1] * step

                    if 0 <= new_row < 8 and 0 <= new_col < 8:
                        # If the square is empty, the bishop can move here
                        if self.grid[new_row][new_col] is None:
                            valid_moves.append((new_row, new_col))
                        # If the square is occupied by a piece of the opposite color, the bishop can capture it
                        elif self.grid[new_row][new_col][0] != piece[0]:
                            valid_moves.append((new_row, new_col))
                            break  # The bishop captures the piece, so stop in that direction
                        else:
                            break  # The square is blocked by a piece of the same color, stop moving in this direction
                    else:
                        break  # The bishop is out of bounds, stop moving in this direction

                    step += 1  # Move to the next square in this direction


        elif piece == "wq" or piece == "bq":
            # Queen: Combination of rook and bishop moves
            directions = [(-1, 0), (1, 0), (0, -1), (0, 1),  # Rook-like (vertical, horizontal)
                        (-1, -1), (-1, 1), (1, -1), (1, 1)]  # Bishop-like (diagonal)

            for direction in directions:
                step = 1  # Start moving in the current direction
                while True:
                    new_row = row + direction[0] * step
                    new_col = col + direction[1] * step

                    if 0 <= new_row < 8 and 0 <= new_col < 8:
                        # If the square is empty, the queen can move here
                        if self.grid[new_row][new_col] is None:
                            valid_moves.append((new_row, new_col))
                        # If the square is occupied by a piece of the opposite color, the queen can capture it
                        elif self.grid[new_row][new_col][0] != piece[0]:
                            valid_moves.append((new_row, new_col))
                            break  # The queen captures the piece, so stop in that direction
                        else:
                            break  # The square is blocked by a piece of the same color, stop moving in this direction
                    else:
                        break  # The queen is out of bounds, stop moving in this direction

                    step += 1  # Move to the next square in this direction


        elif piece == "wk" or piece == "bk":
            # King: One square in any direction (horizontal, vertical, or diagonal)
            king_moves = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
            for move in king_moves:
                new_row = row + move[0]
                new_col = col + move[1]
                if 0 <= new_row < 8 and 0 <= new_col < 8:
                    if not self.grid[new_row][new_col] or self.grid[new_row][new_col][0] != piece[0]:
                        valid_moves.append((new_row, new_col))

        if piece == "wk" or piece == "bk":
            # Define castling conditions
            if piece == "wk" and not self.white_king_moved:  # White King
                # Castling with the Queen's Rook
                if not self.white_queen_rook_moved and self.grid[7][0] == "wr":
                    if self.grid[7][1] is None and self.grid[7][2] is None and self.grid[7][3] is None:
                        valid_moves.append((row, col - 2))  # Queen-side castling (move King 2 squares left)

                # Castling with the King's Rook
                if not self.white_king_side_rook_moved and self.grid[7][7] == "wr":
                    if self.grid[7][6] is None and self.grid[7][5] is None:
                        valid_moves.append((row, col + 2))  # King-side castling (move King 2 squares right)
            
            if piece == "bk" and not self.black_king_moved:  # Black King
                # Castling with the Queen's Rook
                if not self.black_queen_rook_moved and self.grid[0][0] == "br":
                    if self.grid[0][1] is None and self.grid[0][2] is None and self.grid[0][3] is None:
                        valid_moves.append((row, col - 2))  # Queen-side castling (move King 2 squares left)

                # Castling with the King's Rook
                if not self.black_king_side_rook_moved and self.grid[0][7] == "br":
                    if self.grid[0][6] is None and self.grid[0][5] is None:
                        valid_moves.append((row, col + 2))  # King-side castling (move King 2 squares right)

        # Pawn Promotion Check
        if piece == "wp" and row == 0:  # White pawn reaches the promotion rank
            valid_moves.append("promote")
        elif piece == "bp" and row == 7:  # Black pawn reaches the promotion rank
            valid_moves.append("promote")

        return valid_moves
    
    def store_opposing_position(self, valid_moves):
        # Clear the opposing piece positions list
        self.opposing_piece_positions.clear()

        # Loop through the valid moves and check if the destination has an opposing piece
        for move in valid_moves:
            move_row, move_col = move
            target_piece = self.grid[move_row][move_col]
            if target_piece and ((self.turn and target_piece[0] == "b") or (not self.turn and target_piece[0] == "w")):
                # If there's an opposing piece, add the move to the global list
                self.opposing_piece_positions.append((move_row, move_col))

        # Store valid moves for further use (can be used to highlight moves, etc.)
        self.valid_moves = valid_moves  # Store all valid moves
        self.opposing_piece_positions = self.opposing_piece_positions  # Store positions with opposing pieces

    def handle_mouse_click(self, pos, square_size):
        """Handle mouse click events for picking up and moving pieces."""
        x, y = pos
        col = x // square_size
        row = y // square_size

        piece = self.grid[row][col]

        if piece and ((self.turn and piece[0] == "w") or (not self.turn and piece[0] == "b")):
            # Ensure the correct side can only select their pieces (White for self.turn == True, Black for False)
            self.dragging_piece = piece
            self.dragging_pos = (row, col)
            self.grid[row][col] = None
            piece_image = self.piece_images.get(piece)
            self.drag_offset = (x - col * square_size, y - row * square_size)

            valid_moves = self.get_valid_moves(piece, row, col)

            self.store_opposing_position(valid_moves)

            if (self.dragging_piece == "wp" and row == 0) or (self.dragging_piece == "bp" and row == 7):
                # Pawn promotion
                self.promotion_position = (row, col)  # Ensure promotion position is set

    def handle_mouse_release(self, pos, square_size, screen):
        """Handle dropping the piece on a valid square."""
        if self.dragging_piece:
            x, y = pos
            col = x // square_size
            row = y // square_size

            valid_moves = self.get_valid_moves(self.dragging_piece, self.dragging_pos[0], self.dragging_pos[1])

            if (row, col) in valid_moves:

                if self.dragging_piece == "wk" and col == self.dragging_pos[1] - 2:  # Queen-side castling for White
                    # Call the perform_castling method for white and queen-side
                    self.perform_castling("w", queen_side=True, king_side=False)

                elif self.dragging_piece == "wk" and col == self.dragging_pos[1] + 2:  # King-side castling for White
                    # Call the perform_castling method for white and king-side
                    self.perform_castling("w", queen_side=False, king_side=True)

                elif self.dragging_piece == "bk" and col == self.dragging_pos[1] - 2:  # Queen-side castling for Black
                    # Call the perform_castling method for black and queen-side
                    self.perform_castling("b", queen_side=True, king_side=False)

                elif self.dragging_piece == "bk" and col == self.dragging_pos[1] + 2:  # King-side castling for Black
                    # Call the perform_castling method for black and king-side
                    self.perform_castling("b", queen_side=False, king_side=True)

                if (self.dragging_piece == "wp" and row == 0) or (self.dragging_piece == "bp" and row == 7):
                    # Pawn promotion to queen
                    self.promotion_position = (row, col)
                    self.promote_pawn()
                else:
                    self.grid[row][col] = self.dragging_piece
                    self.grid[self.dragging_pos[0]][self.dragging_pos[1]] = None

                if (row, col) in self.opposing_piece_positions:
                    self.play_sfx(capture=True)
                    opposing_player = "b" if self.turn else "w"

                    self.check_game_over(self.grid, opposing_player, screen)

                else:
                    self.play_sfx(capture=False)

                if not self.restart:
                    self.toggle_turn()  # Toggle turn after a valid move
                else:
                    self.turn = True
                    self.restart = False
            else:
                original_row, original_col = self.dragging_pos
                self.grid[original_row][original_col] = self.dragging_piece

            self.dragging_piece = None
            self.dragging_pos = None

    
    def perform_castling(self, king_color, queen_side, king_side):
        """
        Handle the castling move for the given color (white or black).
        :param king_color: 'w' or 'b' for white or black pieces.
        :param queen_side: Boolean indicating whether it's a queen-side castling.
        :param king_side: Boolean indicating whether it's a king-side castling.
        """
        # Set starting and ending rows based on king color
        row = 7 if king_color == "w" else 0
        
        # Queen-side castling logic
        if queen_side:
            self.grid[row][2] = f"{king_color}k"  # Move King to the new position
            self.grid[row][0] = None  # Empty the old King position
            
            self.grid[row][3] = f"{king_color}r"  # Move rook to the new position
            self.grid[row][0] = None  # Empty the old rook position
        
        # King-side castling logic
        elif king_side:
            self.grid[row][6] = f"{king_color}k"  # Move King to the new position
            self.grid[row][7] = None  # Empty the old King position
            
            self.grid[row][5] = f"{king_color}r"  # Move rook to the new position
            self.grid[row][7] = None  # Empty the old rook position


    def promote_pawn(self):
        """Automatically promote the pawn to a queen."""
        row, col = self.promotion_position
        if self.turn:  # White's turn
            self.grid[row][col] = "wq"  # Promote to White Queen
        else:  # Black's turn
            self.grid[row][col] = "bq"  # Promote to Black Queen

        # Reset promotion position
        self.promotion_position = None

    def toggle_turn(self):

        """Switch turn between White and Black."""
        if self.turn:
            if self.dragging_piece == "wk":
                self.white_king_moved = True
            elif self.dragging_piece == "wr" and self.dragging_pos == (7, 0):
                self.white_queen_rook_moved = True
            elif self.dragging_piece == "wr" and self.dragging_pos == (7, 7):
                self.white_king_side_rook_moved = True
        else:
            if self.dragging_piece == "bk":
                self.black_king_moved = True
            elif self.dragging_piece == "br" and self.dragging_pos == (0, 0):
                self.black_queen_rook_moved = True
            elif self.dragging_piece == "br" and self.dragging_pos == (0, 7):
                self.black_king_side_rook_moved = True

        self.turn = not self.turn


    def play_sfx(self, capture=False):
        """Play the appropriate sound effect."""
        if capture:
            self.sounds["capture"].play()
        else:
            self.sounds["move"].play()

    def draw(self, screen, square_size):
        """Draw the chessboard and tile labels."""
        if self.font is None:
            self.font = pygame.font.SysFont("Arial", 24, bold=True)

        # Loop to draw squares and labels
        for row in range(self.rows):
            for col in range(self.cols):
                # Alternate tile colors
                is_white_tile = (row + col) % 2 == 0
                tile_color = (240, 217, 181) if is_white_tile else (181, 136, 99)
                label_color = (181, 136, 99) if is_white_tile else (240, 217, 181)

                # Draw the tile
                pygame.draw.rect(screen, tile_color, (col * square_size, row * square_size, square_size, square_size))

                # Draw row numbers (1-8)
                if col == 0:
                    label = self.font.render(str(self.rows - row), True, label_color)
                    label_position = (5, row * square_size + 5)
                    screen.blit(label, label_position)

                # Draw column letters (a-h)
                if row == self.rows - 1:
                    label = self.font.render(chr(ord('a') + col), True, label_color)
                    label_position = (col * square_size + square_size - 20, row * square_size + square_size - 30)
                    screen.blit(label, label_position)

                # Draw pieces if any in this tile
                piece = self.grid[row][col]
                if piece is not None:
                    self.draw_piece(screen, piece, col, row, square_size)

        # Draw the dragging piece if it's being dragged
        if self.dragging_piece:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            piece_image = self.piece_images.get(self.dragging_piece)
            piece_image = pygame.transform.scale(piece_image, (square_size, square_size))
            screen.blit(piece_image, (mouse_x - self.drag_offset[0], mouse_y - self.drag_offset[1]))

        # Draw valid move circles (semi-transparent white)
        if self.dragging_piece:
            valid_moves = self.get_valid_moves(self.dragging_piece, self.dragging_pos[0], self.dragging_pos[1])
            for (row, col) in valid_moves:
                # Create a surface with transparent background
                circle_surface = pygame.Surface((square_size, square_size), pygame.SRCALPHA)  # Add alpha channel

                # Draw a circle on the surface
                pygame.draw.circle(
                    circle_surface, 
                    (255, 255, 255, 156),  # White color with 50% transparency (RGBA)
                    (square_size // 2, square_size // 2),  # Position at the center of the square
                    square_size // 6  # Radius of the circle (adjust size as needed)
                )

                # Blit the circle surface onto the main screen at the appropriate position
                screen.blit(circle_surface, (col * square_size, row * square_size))

    def draw_piece(self, screen, piece, col, row, square_size):
        """Draw a chess piece on the board."""
        piece_image = self.piece_images.get(piece)
        if piece_image:
            piece_image = pygame.transform.scale(piece_image, (square_size, square_size))
            screen.blit(piece_image, (col * square_size, row * square_size))

    def display_game_over(self, screen):
        """Displays a game-over overlay."""

        white = (255, 255, 255)
        black = (0, 0, 0)
        red = (255, 0, 0)
        green = (0, 255, 0)
        font = pygame.font.Font(None, 74)

        screen.fill(black)  # Fill the screen with a solid background

        # Render the text for the overlay

        wins = "WHITE WINS" if self.turn else "BLACK WINS"

        text = font.render("Checkmate", True, red)
        text_rect = text.get_rect(center=(400,  300))
        screen.blit(text, text_rect)

        win_text = font.render(wins, True, white)
        win_text_rect = win_text.get_rect(center=(400,  400))
        screen.blit(win_text, win_text_rect)

        # Render a subtext to continue or exit
        subtext = font.render("Press ESC to Restart", True, green)
        subtext_rect = subtext.get_rect(center=(400, 500))
        screen.blit(subtext, subtext_rect)

        pygame.display.flip()  # Update the screen

        # Wait for user action to exit the game
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:  # Exit on ESC
                        self.initialize_pieces()
                        self.restart = True

                        waiting = False

    # Example integration within the game logic
    def check_game_over(self, grid, opposing_player, screen):
        """Checks if the game is over and triggers the overlay."""
        king_is_exist = False

        for row in grid:
            if opposing_player + "k" in row:
                king_is_exist = True
        print(king_is_exist)
        if not king_is_exist:
            self.display_game_over(screen)