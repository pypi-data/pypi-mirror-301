import pygame
from mem679_snake.config import BLOCK_SIZE, SCREEN_WIDTH, SCREEN_HEIGHT, GREEN

class Snake:
    """
    A class representing the player's snake in the game.

    Attributes:
        body (list of tuples): The coordinates of each segment of the snake.
        direction (str): The current direction the snake is moving.
        new_block (bool): Flag to indicate if a new block needs to be added to the snake.
    """
    
    def __init__(self):
        """
        Initializes the Snake with a default position and direction.
        """
        self.body = [(100, 50), (90, 50), (80, 50)]
        self.direction = "RIGHT"
        self.new_block = False  # Flag to indicate when to grow the snake

    def get_head_position(self):
        """
        Returns the position of the snake's head.
        
        Returns:
            tuple: The (x, y) coordinates of the head segment.
        """
        return self.body[0]

    def get_head_rect(self):
        """
        Returns a Pygame Rect object representing the snake's head, 
        used for collision detection.
        
        Returns:
            pygame.Rect: Rectangle for the snake's head segment.
        """
        x, y = self.get_head_position()
        return pygame.Rect(x, y, BLOCK_SIZE, BLOCK_SIZE)

    def change_direction(self, new_direction):
        """
        Changes the direction of the snake if the new direction is 
        not directly opposite to the current one.
        
        Args:
            new_direction (str): The new direction for the snake ("UP", "DOWN", "LEFT", "RIGHT").
        """
        opposite_directions = {
            "UP": "DOWN",
            "DOWN": "UP",
            "LEFT": "RIGHT",
            "RIGHT": "LEFT",
        }
        if new_direction != opposite_directions.get(self.direction):
            self.direction = new_direction

    def move(self):
        """
        Moves the snake by adding a new head position in the current direction and 
        removing the tail segment unless the snake has just eaten.
        """
        x, y = self.get_head_position()

        # Update head position based on direction
        if self.direction == "UP":
            y -= BLOCK_SIZE
        elif self.direction == "DOWN":
            y += BLOCK_SIZE
        elif self.direction == "LEFT":
            x -= BLOCK_SIZE
        elif self.direction == "RIGHT":
            x += BLOCK_SIZE

        new_head = (x, y)
        self.body.insert(0, new_head)  # Insert new head position

        if not self.new_block:
            self.body.pop()  # Remove the last block if no growth needed
        else:
            self.new_block = False  # Reset flag after growing

    def grow(self):
        """
        Sets the flag to grow the snake by adding a new block 
        after the next move.
        """
        self.new_block = True

    def check_collision_with_self(self):
        """
        Checks if the snake's head has collided with any part of its body.

        Returns:
            bool: True if collision occurs, False otherwise.
        """
        return self.get_head_position() in self.body[1:]

    def check_collision_with_walls(self):
        """
        Checks if the snake's head has collided with the screen boundaries.

        Returns:
            bool: True if collision occurs, False otherwise.
        """
        x, y = self.get_head_position()
        return x < 0 or x >= SCREEN_WIDTH or y < 0 or y >= SCREEN_HEIGHT

    def draw(self, screen):
        """
        Draws each segment of the snake onto the game screen.

        Args:
            screen (pygame.Surface): The screen to draw the snake on.
        """
        for segment in self.body:
            pygame.draw.rect(
                screen,
                GREEN,
                pygame.Rect(segment[0], segment[1], BLOCK_SIZE, BLOCK_SIZE),
            )
