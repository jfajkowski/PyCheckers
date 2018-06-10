from abc import ABC, abstractmethod
from copy import deepcopy, copy
from typing import Tuple

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
            return 'White'
        elif color == Color.DARK_PIECE:
            return 'Black'

    @staticmethod
    def opposite(color: Tuple[int, int, int]):
        if color == Color.LIGHT_PIECE:
            return Color.DARK_PIECE
        elif color == Color.DARK_PIECE:
            return Color.LIGHT_PIECE


class Board:
    COLS = 8
    ROWS = 8
    FILLED_ROWS = 3

    def __init__(self):
        self._square_colors = np.empty((Board.ROWS, Board.COLS), dtype=Tuple[int, int, int])
        self._state = State(Board.ROWS, Board.COLS)
        self._build()

    @property
    def state(self):
        return copy(self._state)

    @state.setter
    def state(self, value):
        self._state = copy(value)

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
                        piece = Pawn(Color.DARK_PIECE)
                        self._state.add(x, y, piece)
                    if y > Board.ROWS - Board.FILLED_ROWS - 1:
                        piece = Pawn(Color.LIGHT_PIECE)
                        self._state.add(x, y, piece)

    def draw(self, surface):
        for y in range(Board.COLS):
            for x in range(Board.ROWS):
                self.draw_square(surface, x, y)
                if self.state.is_occupied(x, y):
                    self.state.get_piece(x, y).draw(surface, x, y)

    def draw_square(self, surface, x, y):
        square_w, square_h = self.square_size(surface)
        square_rect = pygame.Rect(x * square_w,
                                  y * square_h,
                                  square_w, square_h)

        pygame.draw.rect(surface, self._square_colors[x][y], square_rect)

    @staticmethod
    def square_size(surface):
        return int(surface.get_width() / Board.COLS), int(surface.get_height() / Board.ROWS)


class State:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.matrix = np.empty((rows, cols), dtype=Piece)
        self.light_pieces = 0
        self.dark_pieces = 0

    def __copy__(self):
        cls = self.__class__
        result = cls.__new__(cls)
        for k, v in self.__dict__.items():
            setattr(result, k, copy(v))
        return result

    def __deepcopy__(self, memo):
        cls = self.__class__
        result = cls.__new__(cls)
        memo[id(self)] = result
        for k, v in self.__dict__.items():
            setattr(result, k, deepcopy(v))
        return result

    def add(self, x, y, piece):
        self.matrix[y][x] = piece
        if piece.color == Color.LIGHT_PIECE:
            self.light_pieces += 1
        elif piece.color == Color.DARK_PIECE:
            self.dark_pieces += 1

    def remove(self, x, y):
        piece = self.get_piece(x, y)
        self.matrix[y][x] = None
        if piece.color == Color.LIGHT_PIECE:
            self.light_pieces -= 1
        elif piece.color == Color.DARK_PIECE:
            self.dark_pieces -= 1

    def get_piece(self, x, y):
        return self.matrix[y][x]

    def get_color(self, x, y):
        return self.matrix[y][x].color

    def get_position(self, piece):
        for y in range(self.rows):
            for x in range(self.cols):
                if self.matrix[y][x] is piece:
                    return x, y

    def is_occupied(self, x, y):
        return self.matrix[y][x] is not None

    def piece_positions(self, color):
        result = []
        for y in range(self.rows):
            for x in range(self.cols):
                if self.is_occupied(x, y) and self.get_color(x, y) == color:
                    result.append((x, y))
        return result

    def is_in_bounds(self, x, y):
        return 0 <= x < self.cols and 0 <= y < self.rows

    def transform_into_king(self, x, y):
        color = self.get_color(x, y)
        self.remove(x, y)
        self.add(x, y, King(color))

    def is_ending(self):
        return self.light_pieces == 0 or self.dark_pieces == 0


class Piece(ABC):
    def __init__(self, color: Tuple[int, int, int]):
        self.color = color
        self.marked = False

    @staticmethod
    @abstractmethod
    def target_positions(x, y):
        pass

    def draw(self, surface, x, y):
        square_w, square_h = Board.square_size(surface)
        square_coordinates = (
            x * square_w,
            y * square_h
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
        return '{} {}'.format(Color.name(self.color), self.__class__.__name__)


class Pawn(Piece):
    @staticmethod
    def target_positions(x, y):
        target_positions = [(x - 1, y + 1), (x + 1, y + 1),
                            (x - 1, y - 1), (x + 1, y - 1)]
        return target_positions

    def draw_marked(self, surface, piece_coordinates, piece_size):
        pygame.draw.circle(surface, self.color, piece_coordinates, piece_size)
        pygame.draw.circle(surface, Color.MARKED_PIECE, piece_coordinates, int(piece_size / 2), 1)

    def draw_unmarked(self, surface, piece_coordinates, piece_size):
        pygame.draw.circle(surface, self.color, piece_coordinates, piece_size)

        if self.color == Color.DARK_PIECE:
            pygame.draw.circle(surface, Color.LIGHT_PIECE, piece_coordinates, int(piece_size / 2), 1)
        elif self.color == Color.LIGHT_PIECE:
            pygame.draw.circle(surface, Color.DARK_PIECE, piece_coordinates, int(piece_size / 2), 1)


class King(Pawn):
    CROWN_IMG = pygame.image.load(pkg_resources.resource_filename(__name__, 'sprites/crown.png'))

    @staticmethod
    def target_positions(x, y):
        target_positions = []
        for j in range(-Board.COLS, Board.COLS):
            for i in range(-Board.COLS, Board.COLS):
                if -1 < (x + 1 * i) < Board.COLS and -1 < (y + 1 * j) < Board.COLS and i != 0 and j != 0 and i*i == j*j:
                    target_positions.append((x + 1 * i, y + 1 * j))

        return target_positions

    def draw_marked(self, surface, piece_coordinates, piece_size):
        super().draw_marked(surface, piece_coordinates, piece_size)
        surface.blit(King.CROWN_IMG, piece_coordinates)

    def draw_unmarked(self, surface, piece_coordinates, piece_size):
        super().draw_unmarked(surface, piece_coordinates, piece_size)
        surface.blit(King.CROWN_IMG, piece_coordinates)
