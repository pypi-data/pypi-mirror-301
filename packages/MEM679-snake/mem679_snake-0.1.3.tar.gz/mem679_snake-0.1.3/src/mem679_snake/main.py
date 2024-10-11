import pygame
from mem679_snake.game import Game
from mem679_snake.config import SCREEN_WIDTH, SCREEN_HEIGHT

def main():
    """
    Initialize the game and run the main game loop.
    """
    # Initialize all imported pygame modules
    pygame.init()
    
    # Set up the display with the specified width and height
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    
    # Set the caption for the window
    pygame.display.set_caption("Snake Game")

    # Create an instance of the Game class and start the game loop
    game = Game(screen)
    game.run()

    # Quit pygame and clean up resources
    pygame.quit()

if __name__ == "__main__":
    main()
