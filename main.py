import pygame
from ui.main_menu import MainMenu
from ui.game_mode import GameModeMenu  # Import GameModeMenu
from core.board import ChessBoard  # Import ChessBoard to start the game

pygame.init()

# Screen dimensions
screen_width = 800
screen_height = 800
square_size = screen_width // 8  # Assuming the board is 8x8

# Create the screen object
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Chess Game")

# Initialize and display the main menu
main_menu = MainMenu(screen, screen_width, screen_height)
menu_option = main_menu.display_menu()  # Capture the return value

if menu_option == "exit_game":
    pygame.quit()  # Exit the program if "Exit Game" is selected
elif menu_option == "play_chess":
    # Show the game mode selection menu after "Play Chess" is clicked
    game_mode_menu = GameModeMenu(screen, screen_width, screen_height)
    game_mode_option = game_mode_menu.display_menu()

    if game_mode_option == "exit_game":
        pygame.quit()  # Exit if the user chooses to exit from the game mode menu
    elif game_mode_option == "2_players":
        # Start a 2-player game
        board = ChessBoard()
        running = True
        while running:
            screen.fill((255, 255, 255))  # White background
            board.draw(screen, screen_width // 8)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    board.handle_mouse_click(event.pos, square_size)
                elif event.type == pygame.MOUSEBUTTONUP:
                    board.handle_mouse_release(event.pos, square_size, screen)

            pygame.display.flip()

    elif game_mode_option == "vs_ai":
        # Start a game against AI (implement AI logic here)
        pass

# Quit Pygame
pygame.quit()
