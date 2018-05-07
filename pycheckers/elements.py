from typing import Tuple, List

import numpy as np
import pkg_resources
import pygame


class Color:
    LIGHT_PIECE = (255, 255, 255)
    DARK_PIECE = (0, 0, 0)
    MARKED_PIECE = (255, 0, 0)
    LIGHT_SQUARE = (121, 85, 72)
    DARK_SQUARE = (62, 39, 35)


class Board:
    SIZE = 10
    FILLED_ROWS = 3

    def __init__(self):
        self._state = np.empty((Board.SIZE, Board.SIZE), dtype=Piece)
        self._square_colors = np.empty((Board.SIZE, Board.SIZE), dtype=Tuple[int, int, int])
        self.light_pieces: List[Piece] = []
        self.dark_pieces: List[Piece] = []
        self._build()
        self.prepare_pieces()

    @property
    def state(self):
        return np.array(self._state, copy=True)

    @state.setter
    def state(self, value):
        self._state = value

    def _build(self):
        for y in range(Board.SIZE):
            for x in range(Board.SIZE):
                if (y % 2 == 0 and x % 2 == 0) or (y % 2 == 1 and x % 2 == 1):
                    self._square_colors[y][x] = Color.LIGHT_SQUARE
                else:
                    self._square_colors[y][x] = Color.DARK_SQUARE

    def prepare_pieces(self):
        for y in range(Board.SIZE):
            for x in range(Board.SIZE):
                if self.is_available(x, y):
                    if y < Board.FILLED_ROWS:
                        piece = Piece(Color.DARK_PIECE)
                        self._state[y][x] = piece
                        self.dark_pieces.append(piece)
                    if y > Board.SIZE - Board.FILLED_ROWS - 1:
                        piece = Piece(Color.LIGHT_PIECE)
                        self._state[y][x] = piece
                        self.light_pieces.append(piece)

    def draw(self, surface):
        for y in range(Board.SIZE):
            for x in range(Board.SIZE):
                self.draw_square(surface, x, y)
                if self.is_occupied(x, y):
                    self._state[y][x].draw(surface, x, y)

    def draw_square(self, surface, x, y):
        w = surface.get_width()
        h = surface.get_height()
        board_size = min(w, h)
        square_size = int(board_size / Board.SIZE)
        square_rect = pygame.Rect((w - board_size) / 2 + x * square_size,
                                  (h - board_size) / 2 + y * square_size,
                                  square_size, square_size)

        pygame.draw.rect(surface, self._square_colors[x][y], square_rect)

    def position(self, piece):
        for y in range(Board.SIZE):
            for x in range(Board.SIZE):
                if self.is_occupied(x, y) and self._state[y][x] is piece:
                    return x, y

    def is_in_bounds(self, x, y):
        return 0 < x < Board.SIZE - 1 and 0 < y < Board.SIZE - 1

    def is_occupied(self, x, y):
        return self._state[y][x] is not None

    def is_available(self, x, y):
        return self._square_colors[y][x] is not Color.LIGHT_SQUARE


class Piece:
    crown_img = pygame.image.load(pkg_resources.resource_filename(__name__, 'sprites/crown.png'))

    def __init__(self, color: Tuple[int, int, int]):
        self._color = color
        self._king = False
        self._marked = False

    @property
    def is_king(self):
        return self._king

    @property
    def is_marked(self):
        return self._marked

    def draw(self, surface: pygame.Surface, x, y):
        w = surface.get_width()
        h = surface.get_height()
        board_size = min(w, h)
        square_size = int(board_size / Board.SIZE)
        piece_radius = int((board_size / Board.SIZE) / 2) - 8
        square_pos = (
            int((w - board_size) / 2 + x * square_size),
            int((h - board_size) / 2 + y * square_size)
        )
        piece_pos = (
            int(square_pos[0] + square_size / 2),
            int(square_pos[1] + square_size / 2)
        )
        pygame.draw.circle(surface, self._color, piece_pos, piece_radius)


        if self.is_marked:
            pygame.draw.circle(surface, Color.MARKED_PIECE, piece_pos, int(piece_radius / 2), 1)
        elif self._color is Color.DARK_PIECE:
            pygame.draw.circle(surface, Color.LIGHT_PIECE, piece_pos, int(piece_radius / 2), 1)
        elif self._color is Color.LIGHT_PIECE:
            pygame.draw.circle(surface, Color.DARK_PIECE, piece_pos, int(piece_radius / 2), 1)

        if self.is_king:
            surface.blit(Piece.crown_img, square_pos)


    def __str__(self):
        if self._color is Color.DARK_PIECE:
            return 'Dark'
        elif self._color is Color.LIGHT_PIECE:
            return 'Light'
