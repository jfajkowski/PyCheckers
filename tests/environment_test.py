import unittest


class PyGameTestCase(unittest.TestCase):
    def test_pygame_installation(self):
        try:
            import pygame
            pygame.init()
            pygame.display.set_mode((500, 400), 0, 32)
            pygame.quit()
        except ModuleNotFoundError:
            self.fail("PyGame is not installed properly!")

    def test_numpy_installation(self):
        try:
            import numpy as np
        except ModuleNotFoundError:
            self.fail("Numpy is not installed properly!")


if __name__ == '__main__':
    unittest.main()
