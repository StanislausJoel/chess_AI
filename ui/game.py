import pygame
from ui.main_menu import MainMenu  # Import MainMenu to display the initial menu
from ui.game_mode import GameModeMenu  # Import GameModeMenu for 2 players vs AI
from core.board import ChessBoard  # Import ChessBoard to start the game

class Game():
    def __init__(self):
        pygame.init()

        # Screen dimensions
        self.screen_width = 800
        self.screen_height = 800
        self.square_size = self.screen_width // 8  # Assuming the board is 8x8

        # Create the screen object
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Chess Game")

    def run(self):
        # Create the main menu and handle what happens after it is displayed
        main_menu = MainMenu(self.screen, self.screen_width, self.screen_height)
        menu_option = main_menu.display_menu()

        if menu_option == "exit_game":
            pygame.quit()  # Exit the game if the user chooses to exit
            return

        if menu_option == "play_chess":
            # Show the game mode selection menu after "Play Chess" is clicked
            game_mode_menu = GameModeMenu(self.screen, self.screen_width, self.screen_height)
            game_mode_option = game_mode_menu.display_menu()

            if game_mode_option == "exit_game":
                pygame.quit()  # Exit if the user chooses to exit from the game mode menu
                return
            elif game_mode_option == "2_players":
                self.start_game(two_players=True)
            elif game_mode_option == "vs_ai":
                self.start_game(two_players=False)

    def start_game(self, two_players):
        # Initialize the ChessBoard
        board = ChessBoard()

        running = True
        while running:
            self.screen.fill((255, 255, 255))  # White background
            board.draw(self.screen, self.square_size)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    board.handle_mouse_click(event.pos, self.square_size)
                elif event.type == pygame.MOUSEBUTTONUP:
                    board.handle_mouse_release(event.pos, self.square_size, self.screen)

            pygame.display.flip()

        pygame.quit()

# Run the game
if __name__ == "__main__":
    game = Game()
    game.run()
