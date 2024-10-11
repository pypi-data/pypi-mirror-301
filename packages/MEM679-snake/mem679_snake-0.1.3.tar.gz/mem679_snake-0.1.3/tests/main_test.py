import pytest
from unittest import mock
from mem679_snake.game import Game
from mem679_snake.config import SCREEN_WIDTH, SCREEN_HEIGHT
from mem679_snake.main import main

@mock.patch("mem679_snake.main.pygame")  # Mock the entire pygame module in main
@mock.patch("mem679_snake.main.Game")    # Mock the Game class
def test_main(mock_game_class, mock_pygame):
    # Mock screen and game instance
    mock_screen = mock.Mock()
    mock_game_instance = mock.Mock()

    # Set up mocks for pygame components
    mock_pygame.display.set_mode.return_value = mock_screen
    mock_game_class.return_value = mock_game_instance

    # Call main function
    main()

    # Assertions to verify correct behavior
    # Check if pygame.init was called
    mock_pygame.init.assert_called_once()

    # Check if display was set up with correct resolution
    mock_pygame.display.set_mode.assert_called_once_with((SCREEN_WIDTH, SCREEN_HEIGHT))

    # Verify that the window caption was set
    mock_pygame.display.set_caption.assert_called_once_with("Snake Game")

    # Verify that Game class was instantiated with the screen
    mock_game_class.assert_called_once_with(mock_screen)

    # Check if the game instance's run method was called
    mock_game_instance.run.assert_called_once()

    # Ensure pygame.quit was called to clean up
    mock_pygame.quit.assert_called_once()
