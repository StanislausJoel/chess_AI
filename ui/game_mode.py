import pygame

class GameModeMenu:
    def __init__(self, screen, screen_width, screen_height):
        self.screen = screen
        self.screen_width = screen_width
        self.screen_height = screen_height

        # Fonts with enhanced sizes for a more readable UI
        self.font = pygame.font.SysFont("Arial", 50)  # Larger font size for button text
        self.title_font = pygame.font.SysFont("Arial", 80)  # Larger title font for better emphasis

        # Button rectangles for game mode options (larger buttons for better interaction)
        self.button_width = self.screen_width // 1.5  # Wider buttons
        self.button_height = 60  # Taller buttons for easier clicking
        self.two_players_rect = pygame.Rect(self.screen_width // 4 - 60, self.screen_height // 3, self.button_width, self.button_height)
        self.vs_ai_rect = pygame.Rect(self.screen_width // 4 - 60, self.screen_height // 2, self.button_width, self.button_height)

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
            game_mode_title = self.title_font.render("Choose Game Mode", True, self.text_color)
            self.screen.blit(game_mode_title, ((self.screen_width - game_mode_title.get_width()) // 2, 100))  # Centered title

            # Render the button texts with the adjusted font
            two_players_text = self.font.render("2 Players", True, self.text_color)
            vs_ai_text = self.font.render("VS AI", True, self.text_color)

            # Draw buttons with hover effects (larger buttons)
            mouse_pos = pygame.mouse.get_pos()
            if self.two_players_rect.collidepoint(mouse_pos):
                pygame.draw.rect(self.screen, self.button_hover_color, self.two_players_rect)
            else:
                pygame.draw.rect(self.screen, self.button_color, self.two_players_rect)

            if self.vs_ai_rect.collidepoint(mouse_pos):
                pygame.draw.rect(self.screen, self.button_hover_color, self.vs_ai_rect)
            else:
                pygame.draw.rect(self.screen, self.button_color, self.vs_ai_rect)

            # Center the button text within the buttons
            self.screen.blit(two_players_text, (self.two_players_rect.centerx - two_players_text.get_width() // 2,
                                                self.two_players_rect.centery - two_players_text.get_height() // 2))
            self.screen.blit(vs_ai_text, (self.vs_ai_rect.centerx - vs_ai_text.get_width() // 2,
                                          self.vs_ai_rect.centery - vs_ai_text.get_height() // 2))

            pygame.display.flip()

            # Handle events like button clicks
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "exit_game"
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.two_players_rect.collidepoint(event.pos):
                        return "2_players"
                    elif self.vs_ai_rect.collidepoint(event.pos):
                        return "vs_ai"
