import unittest
import pygame
from mem679_snake.food import Food
from mem679_snake.config import BLOCK_SIZE, SCREEN_WIDTH, SCREEN_HEIGHT, RED

class TestFood(unittest.TestCase):

    def setUp(self):
        pygame.init()
        self.food = Food()

    def tearDown(self):
        pygame.quit()

    def test_random_position_within_bounds(self):
        x, y = self.food.random_position()
        self.assertTrue(0 <= x < SCREEN_WIDTH)
        self.assertTrue(0 <= y < SCREEN_HEIGHT)
        self.assertEqual(x % BLOCK_SIZE, 0)
        self.assertEqual(y % BLOCK_SIZE, 0)

    def test_get_rect(self):
        rect = self.food.get_rect()
        self.assertEqual(rect.width, BLOCK_SIZE)
        self.assertEqual(rect.height, BLOCK_SIZE)
        self.assertEqual(rect.topleft, self.food.position)

    def test_respawn_changes_position(self):
        old_position = self.food.position
        self.food.respawn()
        new_position = self.food.position
        self.assertNotEqual(old_position, new_position)

    def test_draw(self):
        screen = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.food.draw(screen)
        food_rect = self.food.get_rect()
        self.assertEqual(screen.get_at(food_rect.topleft), RED)

if __name__ == '__main__':
    unittest.main()