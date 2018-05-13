import pygame

from elements import Board, Color
from strategies import RandomGameStrategy


class Game:
    def __init__(self, clock, surface: pygame.Surface, max_fps=60):
        self._clock = clock
        self._surface = surface
        self._max_fps = max_fps
        self._board = Board()
        self._player_1 = RandomGameStrategy(Color.LIGHT_PIECE)
        self._player_2 = RandomGameStrategy(Color.DARK_PIECE)

    def run(self):
        current_player = None
        self._board.prepare_pieces()

        while True:
            clock.tick(self._max_fps)
            self._board.draw(self._surface)
            pygame.display.update()
            current_player = self._player_1 if current_player is not self._player_1 else self._player_2
            move = current_player.move(self._board.state)
            if move:
                self._board.state = move.execute()
            else:
                break


if __name__ == '__main__':
    pygame.init()

    clock = pygame.time.Clock()
    resolution = (500, 500)
    screen = pygame.display.set_mode(resolution, pygame.HWSURFACE | pygame.DOUBLEBUF)
    pygame.display.set_caption('PyCheckers')

    game = Game(clock, screen)
    game.run()

    pygame.quit()
