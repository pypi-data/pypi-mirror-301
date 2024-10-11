import unittest

import mem679_snake.config as config


class TestConfig(unittest.TestCase):
    def test_screen_settings(self):
        self.assertEqual(config.SCREEN_WIDTH, 800)
        self.assertEqual(config.SCREEN_HEIGHT, 600)
        self.assertEqual(config.BLOCK_SIZE, 20)

    def test_colors(self):
        self.assertEqual(config.WHITE, (255, 255, 255))
        self.assertEqual(config.BLACK, (0, 0, 0))
        self.assertEqual(config.YELLOW, (255, 198, 0))
        self.assertEqual(config.RED, (255, 0, 0))

    def test_game_settings(self):
        self.assertEqual(config.FPS, 10)


if __name__ == "__main__":
    unittest.main()
