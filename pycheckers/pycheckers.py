import logging

import pygame

from elements import Board, Color
from config_read import read_players




class Game:
    def __init__(self, clock, surface: pygame.Surface, player1, player2, max_fps=1):
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

        paused = False
        while True:
            self._board.draw(self._surface)
            pygame.display.update()

            if not paused:
                if moves:
                    move = moves.pop()
                    logging.debug('Player: {}, Move: {}'.format(Color.name(current_player.color), move))
                    self._board.state = move.execute()
                    clock.tick(self._max_fps)
                else:
                    current_player = self._player_1 if current_player is not self._player_1 else self._player_2
                    moves = current_player.move(self._board.state)
                    if moves:
                        if len(moves) > 0:
                            moves = list(reversed(moves))
                    else:
                        break

            events = pygame.event.get()
            for event in events:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        paused = not paused
                    elif event.key in [pygame.K_PLUS, pygame.K_KP_PLUS]:
                        self._max_fps += 1
                    elif event.key in [pygame.K_MINUS, pygame.K_KP_MINUS]:
                        self._max_fps -= 1
                elif event.type == pygame.QUIT:
                    return



if __name__ == '__main__':
    logging.basicConfig(format='[%(asctime)s][%(levelname)s] %(name)s: %(message)s', level=logging.DEBUG)

    pygame.init()

    players = read_players()
    clock = pygame.time.Clock()
    resolution = (640, 640)
    screen = pygame.display.set_mode(resolution, pygame.HWSURFACE | pygame.DOUBLEBUF)
    pygame.display.set_caption('PyCheckers')

    game = Game(clock, screen, players[0], players[1])
    game.run()

    pygame.quit()
