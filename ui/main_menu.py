import pygame

class MainMenu:
    def __init__(self, screen, screen_width, screen_height):
        self.screen = screen
        self.screen_width = screen_width
        self.screen_height = screen_height

        # Fonts with enhanced sizes for readability
        self.font = pygame.font.SysFont("Arial", 50)  # Larger font size for button text
        self.title_font = pygame.font.SysFont("Arial", 80)  # Larger title font for better emphasis

        # Button rectangles for menu options (larger buttons for better interaction)
        self.button_width = self.screen_width // 1.5  # Wider buttons
        self.button_height = 60  # Taller buttons for easier clicking
        self.play_chess_rect = pygame.Rect(self.screen_width // 4 - 60, self.screen_height // 3, self.button_width, self.button_height)
        self.exit_game_rect = pygame.Rect(self.screen_width // 4 - 60, self.screen_height // 2, self.button_width, self.button_height)

        # Colors
        self.button_color = (60, 60, 60)  # Dark button color
        self.button_hover_color = (100, 100, 100)  # Light hover color
        self.text_color = (244, 244, 244)  # White text color for contrast
        self.background_color = (181, 136, 99)  # Solid black background

    def display_menu(self):
        running = True
        while running:
            self.screen.fill(self.background_color)  # Solid black background

            # Render the title with enhanced font size
            title_text = self.title_font.render("Chess Game", True, self.text_color)
            self.screen.blit(title_text, ((self.screen_width - title_text.get_width()) // 2, 100))  # Centered title

            # Render the button texts with the adjusted font
            play_chess_text = self.font.render("Play Game", True, self.text_color)
            exit_game_text = self.font.render("Exit Game", True, self.text_color)

            # Draw buttons with hover effects (larger buttons)
            mouse_pos = pygame.mouse.get_pos()
            if self.play_chess_rect.collidepoint(mouse_pos):
                pygame.draw.rect(self.screen, self.button_hover_color, self.play_chess_rect)
            else:
                pygame.draw.rect(self.screen, self.button_color, self.play_chess_rect)

            if self.exit_game_rect.collidepoint(mouse_pos):
                pygame.draw.rect(self.screen, self.button_hover_color, self.exit_game_rect)
            else:
                pygame.draw.rect(self.screen, self.button_color, self.exit_game_rect)

            # Center the button text within the buttons
            self.screen.blit(play_chess_text, (self.play_chess_rect.centerx - play_chess_text.get_width() // 2,
                                              self.play_chess_rect.centery - play_chess_text.get_height() // 2))
            self.screen.blit(exit_game_text, (self.exit_game_rect.centerx - exit_game_text.get_width() // 2,
                                              self.exit_game_rect.centery - exit_game_text.get_height() // 2))

            pygame.display.flip()

            # Handle events like button clicks
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "exit_game"
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.play_chess_rect.collidepoint(event.pos):
                        return "play_chess"
                    elif self.exit_game_rect.collidepoint(event.pos):
                        return "exit_game"
