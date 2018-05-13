from abc import ABC, abstractmethod
from copy import deepcopy
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
    COLS = 8
    ROWS = 8
    FILLED_ROWS = 3

    def __init__(self):
        self._square_colors = np.empty((Board.ROWS, Board.COLS), dtype=Tuple[int, int, int])
        self._state = State(Board.ROWS, Board.COLS)
        self._build()

    @property
    def state(self):
        return deepcopy(self._state)

    @state.setter
    def state(self, value):
        self._state = deepcopy(value)

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
                    self.state.get_piece(x, y).draw(surface)

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
        self.light_pieces: List[Piece] = []
        self.dark_pieces: List[Piece] = []
        self.state_matrix = np.empty((rows, cols), dtype=Piece)

    def __deepcopy__(self, memo):
        cls = self.__class__
        result = cls.__new__(cls)
        memo[id(self)] = result
        light_pieces = []
        dark_pieces = []
        state_matrix = deepcopy(self.__dict__['state_matrix'])
        for piece in filter(lambda x: x is not None, state_matrix.flatten()):
            if piece.color is Color.DARK_PIECE:
                dark_pieces.append(piece)
            elif piece.color is Color.LIGHT_PIECE:
                light_pieces.append(piece)
            else:
                raise RuntimeError("Undefined color")
        setattr(result, 'light_pieces', light_pieces)
        setattr(result, 'dark_pieces', dark_pieces)
        setattr(result, 'state_matrix', state_matrix)
        return result

    def add(self, x, y, piece):
        self.state_matrix[y][x] = piece
        if piece.color is Color.DARK_PIECE:
            self.dark_pieces.append(piece)
        elif piece.color is Color.LIGHT_PIECE:
            self.light_pieces.append(piece)
        else:
            raise RuntimeError("Undefined color")
        piece.x, piece.y = x, y

    def remove(self, x, y):
        piece = self.state_matrix[y][x]
        piece.x, piece.y = None, None
        self.state_matrix[y][x] = None
        if piece.color is Color.DARK_PIECE:
            self.dark_pieces.remove(piece)
        elif piece.color is Color.LIGHT_PIECE:
            self.light_pieces.remove(piece)
        else:
            raise RuntimeError("Undefined color")

    def get_piece(self, x, y):
        return self.state_matrix[y][x]

    def is_occupied(self, x, y):
        return self.state_matrix[y][x] is not None

    def pieces(self, color):
        if color is Color.DARK_PIECE:
            return self.dark_pieces
        elif color is Color.LIGHT_PIECE:
            return self.light_pieces
        else:
            raise RuntimeError("Undefined color")

    def is_in_bounds(self, x, y):
        return 0 <= x < Board.COLS and 0 <= y < Board.ROWS



class Piece(ABC):
    def __init__(self, color: Tuple[int, int, int]):
        self.x = None
        self.y = None
        self.color = color
        self.marked = False

    def __deepcopy__(self, memo):
        cls = self.__class__
        result = cls.__new__(cls)
        memo[id(self)] = result
        for k, v in self.__dict__.items():
            setattr(result, k, deepcopy(v))
        return result

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
        return '{} {}'.format(Color.name(self.color), self.__class__.__name__)


class Pawn(Piece):
    def moves(self):
        return [(self.x - 1, self.y + 1), (self.x + 1, self.y + 1),
                (self.x - 1, self.y - 1), (self.x + 1, self.y - 1)]

    def draw_marked(self, surface, piece_coordinates, piece_size):
        pygame.draw.circle(surface, self.color, piece_coordinates, piece_size)
        pygame.draw.circle(surface, Color.MARKED_PIECE, piece_coordinates, int(piece_size / 2), 1)

    def draw_unmarked(self, surface, piece_coordinates, piece_size):
        pygame.draw.circle(surface, self.color, piece_coordinates, piece_size)

        if self.color is Color.DARK_PIECE:
            pygame.draw.circle(surface, Color.LIGHT_PIECE, piece_coordinates, int(piece_size / 2), 1)
        elif self.color is Color.LIGHT_PIECE:
            pygame.draw.circle(surface, Color.DARK_PIECE, piece_coordinates, int(piece_size / 2), 1)


class King(Pawn):
    CROWN_IMG = pygame.image.load(pkg_resources.resource_filename(__name__, 'sprites/crown.png'))

    def moves(self):
        all_moves = []

        for j in range(-Board.COLS, Board.COLS):
            for i in range(-Board.COLS, Board.COLS):
                if -1 < (self.x + 1 * i) < Board.COLS and -1 < (self.y + 1 * j) < Board.COLS and i != 0 and j != 0 and i*i == j*j:
                    all_moves.append((self.x + 1 * i, self.y + 1 * j))

        return all_moves

    def draw_marked(self, surface, piece_coordinates, piece_size):
        super().draw_marked(surface, piece_coordinates, piece_size)
        surface.blit(King.CROWN_IMG, piece_coordinates)

    def draw_unmarked(self, surface, piece_coordinates, piece_size):
        super().draw_unmarked(surface, piece_coordinates, piece_size)
        surface.blit(King.CROWN_IMG, piece_coordinates)
