import pygame

from elements import Board, Color
from config_read import read_players


class Game:
    def __init__(self, clock, surface: pygame.Surface, player1, player2, max_fps=5):
        self._clock = clock
        self._surface = surface
        self._max_fps = max_fps
        self._board = Board()
        self._player_1 = player1
        self._player_2 = player2

    def run(self):
        current_player = None
        moves = []
        self._board.prepare_pieces()

        while True:
            self._board.draw(self._surface)
            pygame.display.update()
            if moves:
                self._board.state = moves.pop().execute()
                clock.tick(self._max_fps)
            else:
                current_player = self._player_1 if current_player is not self._player_1 else self._player_2
                moves = current_player.move(self._board.state)
                if moves:
                    if len(moves) > 0:
                        moves = list(reversed(moves))
                else:
                    break


if __name__ == '__main__':
    pygame.init()

    players = read_players()
    clock = pygame.time.Clock()
    resolution = (500, 500)
    screen = pygame.display.set_mode(resolution, pygame.HWSURFACE | pygame.DOUBLEBUF)
    pygame.display.set_caption('PyCheckers')

    game = Game(clock, screen, players[0], players[1])
    game.run()

    pygame.quit()
