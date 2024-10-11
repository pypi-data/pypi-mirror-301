import pytest
from unittest import mock
from mem679_snake.snake import Snake
from mem679_snake.config import BLOCK_SIZE, SCREEN_WIDTH, SCREEN_HEIGHT, YELLOW
import pygame

@pytest.fixture
def snake():
    return Snake()

def test_initialization(snake):
    # Verify initial body position, direction, and new_block flag
    assert snake.body == [(100, 50), (90, 50), (80, 50)]
    assert snake.direction == "RIGHT"
    assert not snake.new_block

def test_get_head_position(snake):
    # Verify head position is the first element in body
    assert snake.get_head_position() == (100, 50)

@mock.patch("mem679_snake.snake.pygame.Rect")
def test_get_head_rect(mock_rect, snake):
    # Test that get_head_rect creates a pygame.Rect with head coordinates
    head_position = snake.get_head_position()
    snake.get_head_rect()
    mock_rect.assert_called_once_with(head_position[0], head_position[1], BLOCK_SIZE, BLOCK_SIZE)

def test_change_direction(snake):
    # Test changing direction to a non-opposite direction
    snake.change_direction("DOWN")
    assert snake.direction == "DOWN"

    # Test changing direction to an opposite direction (should not change)
    snake.change_direction("UP")
    assert snake.direction == "DOWN"  # Remains unchanged

def test_move(snake):
    # Move the snake and verify new head and tail positions
    snake.move()
    assert snake.body[0] == (120, 50)  # New head position in "RIGHT" direction
    assert len(snake.body) == 3  # Length unchanged

def test_grow(snake):
    # Set the snake to grow and move
    snake.grow()
    assert snake.new_block is True
    snake.move()
    assert len(snake.body) == 4  # Length increased by one
    assert snake.new_block is False  # Flag reset after growing

def test_check_collision_with_self(snake):
    # No self-collision initially
    assert not snake.check_collision_with_self()
    
    # Make a self-collision by adding the head position elsewhere in the body
    snake.body = [(100, 50), (90, 50), (100, 50)]
    assert snake.check_collision_with_self()

def test_check_collision_with_walls(snake):
    # Check collision when snake moves beyond screen boundaries
    snake.body[0] = (-10, 50)  # Left wall collision
    assert snake.check_collision_with_walls()
    
    snake.body[0] = (SCREEN_WIDTH + 10, 50)  # Right wall collision
    assert snake.check_collision_with_walls()
    
    snake.body[0] = (50, -10)  # Top wall collision
    assert snake.check_collision_with_walls()
    
    snake.body[0] = (50, SCREEN_HEIGHT + 10)  # Bottom wall collision
    assert snake.check_collision_with_walls()

@mock.patch("mem679_snake.snake.pygame.draw.rect")
def test_draw(mock_draw_rect, snake):
    # Mock screen surface
    mock_screen = mock.Mock()
    
    # Call draw method and check if pygame.draw.rect is called for each body segment
    snake.draw(mock_screen)
    assert mock_draw_rect.call_count == len(snake.body)
    
    # Verify it was called with expected color and rect parameters for each segment
    for segment in snake.body:
        mock_draw_rect.assert_any_call(
            mock_screen,
            YELLOW,
            pygame.Rect(segment[0], segment[1], BLOCK_SIZE, BLOCK_SIZE),
        )
