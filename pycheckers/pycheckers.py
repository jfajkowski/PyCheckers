import pygame
import logging

from elements import Board
from strategies import MiniMaxGameStrategy, RandomGameStrategy


class Game:

    def __init__(self, clock, surface: pygame.Surface, max_fps=60):
        self._clock = clock
        self._surface = surface
        self._max_fps = max_fps
        self._board = Board()
        self._player_1 = RandomGameStrategy()
        self._player_2 = RandomGameStrategy()

    def run(self):
        while True:
            clock.tick(self._max_fps)
            self._board.draw(self._surface)
            pygame.display.update()
            self._player_1.move(self._board.light_pieces, self._board)
            self._player_2.move(self._board.dark_pieces, self._board)



if __name__ == '__main__':
    pygame.init()

    clock = pygame.time.Clock()
    resolution = (500, 500)
    screen = pygame.display.set_mode(resolution, pygame.HWSURFACE | pygame.DOUBLEBUF)
    pygame.display.set_caption('PyCheckers')

    game = Game(clock, screen)
    game.run()

    pygame.quit()
