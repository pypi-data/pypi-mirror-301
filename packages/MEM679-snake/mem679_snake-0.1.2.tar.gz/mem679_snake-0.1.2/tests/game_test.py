import pytest
import pygame
from unittest import mock
from mem679_snake.game import Game
from mem679_snake.config import SCREEN_WIDTH, SCREEN_HEIGHT, BLACK, FPS


@pytest.fixture
def game():
    pygame.init()
    screen = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    return Game(screen)


@mock.patch("mem679_snake.game.pygame.event.get")
def test_handle_events_quit(mock_get_events, game):
    mock_get_events.return_value = [mock.Mock(type=pygame.QUIT)]
    game.handle_events()
    assert not game.running


@mock.patch("mem679_snake.game.pygame.event.get")
def test_handle_events_direction_change(mock_get_events, game):
    with mock.patch.object(game.snake, "change_direction") as mock_change_direction:
        mock_get_events.return_value = [mock.Mock(type=pygame.KEYDOWN, key=pygame.K_UP)]
        game.handle_events()
        mock_change_direction.assert_called_once_with("UP")


@mock.patch("mem679_snake.game.pygame.display.flip")
@mock.patch("mem679_snake.snake.Snake.draw")
@mock.patch("mem679_snake.food.Food.draw")
def test_draw(mock_food_draw, mock_snake_draw, mock_display_flip, game):
    game.draw()
    mock_snake_draw.assert_called_once_with(game.screen)
    mock_food_draw.assert_called_once_with(game.screen)
    mock_display_flip.assert_called_once()
