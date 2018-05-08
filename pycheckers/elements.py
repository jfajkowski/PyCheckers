from abc import ABC, abstractmethod
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

    @staticmethod
    def name(color: Tuple[int, int, int]):
        if color == Color.LIGHT_PIECE:
            color_name = 'White'
        elif color == Color.DARK_PIECE:
            color_name = 'Black'
        else:
            color_name = 'Undefined'
        return color_name


class Board:

    COLS = 10
    ROWS = 10
    FILLED_ROWS = 3

    def __init__(self):
        self._state = np.empty((Board.ROWS, Board.COLS), dtype=Piece)
        self._square_colors = np.empty((Board.ROWS, Board.COLS), dtype=Tuple[int, int, int])
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
        for y in range(Board.COLS):
            for x in range(Board.ROWS):
                if (y % 2 == 0 and x % 2 == 0) or (y % 2 == 1 and x % 2 == 1):
                    self._square_colors[y][x] = Color.LIGHT_SQUARE
                else:
                    self._square_colors[y][x] = Color.DARK_SQUARE

    def prepare_pieces(self):
        for y in range(Board.COLS):
            for x in range(Board.ROWS):
                if self._square_colors[y][x] is not Color.LIGHT_SQUARE:
                    if y < Board.FILLED_ROWS:
                        piece = Pawn(x, y, Color.DARK_PIECE)
                        self._state[y][x] = piece
                        self.dark_pieces.append(piece)
                    if y > Board.ROWS - Board.FILLED_ROWS - 1:
                        piece = Pawn(x, y, Color.LIGHT_PIECE)
                        self._state[y][x] = piece
                        self.light_pieces.append(piece)

    def draw(self, surface):
        for y in range(Board.COLS):
            for x in range(Board.ROWS):
                self.draw_square(surface, x, y)
                if self.is_occupied(x, y):
                    self._state[y][x].draw(surface)

    def draw_square(self, surface, x, y):
        square_w, square_h = self.square_size(surface)
        square_rect = pygame.Rect(x * square_w,
                                  y * square_h,
                                  square_w, square_h)

        pygame.draw.rect(surface, self._square_colors[x][y], square_rect)

    @staticmethod
    def square_size(surface):
        return int(surface.get_width() / Board.COLS), int(surface.get_height() / Board.ROWS)

    def is_in_bounds(self, x, y):
        return 0 < x < Board.COLS - 1 and 0 < y < Board.ROWS - 1

    def is_occupied(self, x, y):
        return self._state[y][x] is not None


class Piece(ABC):

    def __init__(self, x, y, color: Tuple[int, int, int]):
        self.x = x
        self.y = y
        self._color = color
        self.marked = False

    @abstractmethod
    def moves(self):
        pass

    def draw(self, surface: pygame.Surface):
        square_w, square_h = Board.square_size(surface)
        square_coordinates = (
            self.x * square_w,
            self.y * square_h
        )
        piece_coordinates = (
            int(square_coordinates[0] + square_w / 2),
            int(square_coordinates[1] + square_h / 2)
        )
        piece_size = int(min(square_w, square_h) / 2) - 8

        if self.marked:
            self.draw_marked(surface, piece_coordinates, piece_size)
        else:
            self.draw_unmarked(surface, piece_coordinates, piece_size)

    @abstractmethod
    def draw_marked(self, surface, piece_coordinates, piece_size):
        pass

    @abstractmethod
    def draw_unmarked(self, surface, piece_coordinates, piece_size):
        pass

    def __str__(self):
        return '{} {}'.format(Color.name(self._color), self.__class__.__name__)


class Pawn(Piece):

    def moves(self):
        return [(self.x - 1, self.y - 1), (self.x + 1, self.y - 1),
                (self.x - 1, self.y + 1), (self.x + 1, self.y + 1)]

    def draw_marked(self, surface, piece_coordinates, piece_size):
        pygame.draw.circle(surface, self._color, piece_coordinates, piece_size)
        pygame.draw.circle(surface, Color.MARKED_PIECE, piece_coordinates, int(piece_size / 2), 1)

    def draw_unmarked(self, surface, piece_coordinates, piece_size):
        pygame.draw.circle(surface, self._color, piece_coordinates, piece_size)

        if self._color is Color.DARK_PIECE:
            pygame.draw.circle(surface, Color.LIGHT_PIECE, piece_coordinates, int(piece_size / 2), 1)
        elif self._color is Color.LIGHT_PIECE:
            pygame.draw.circle(surface, Color.DARK_PIECE, piece_coordinates, int(piece_size / 2), 1)


class King(Pawn):

    crown_img = pygame.image.load(pkg_resources.resource_filename(__name__, 'sprites/crown.png'))

    def moves(self):
        super().moves()

    def draw_marked(self, surface, piece_coordinates, piece_size):
        super().draw_marked(surface, piece_coordinates, piece_size)
        surface.blit(King.crown_img, piece_coordinates)

    def draw_unmarked(self, surface, piece_coordinates, piece_size):
        super().draw_unmarked(surface, piece_coordinates, piece_size)
        surface.blit(King.crown_img, piece_coordinates)

