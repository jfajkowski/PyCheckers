import pygame

class Game:
    def __init__(self, clock, screen, max_fps=60):
        self._clock = clock
        self._screen = screen
        self._max_fps = max_fps

    def run(self):
        while True:
            clock.tick(self._max_fps)


if __name__ == '__main__':
    pygame.init()

    clock = pygame.time.Clock()
    resolution = (640, 480)
    screen = pygame.display.set_mode(resolution, pygame.HWSURFACE | pygame.DOUBLEBUF)
    pygame.display.set_caption('PyCheckers')

    game = Game(clock, screen)
    game.run()

    pygame.quit()
