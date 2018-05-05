from typing import Tuple, List

import numpy as np
import pygame


class Color:
    LIGHT_PIECE = (0, 0, 0)
    DARK_PIECE = (255, 255, 255)
    LIGHT_SQUARE = (121, 85, 72)
    DARK_SQUARE = (62, 39, 35)


class Board:
    SIZE = 10
    FILLED_ROWS = 3

    def __init__(self):
        self.state = np.empty((Board.SIZE, Board.SIZE), dtype=Square)
        self.light_pieces: List[Piece] = []
        self.dark_pieces: List[Piece] = []
        self._build()
        self.prepare_pieces()

    def _build(self):
        for i in range(Board.SIZE):
            for j in range(Board.SIZE):
                if (i % 2 == 0 and j % 2 == 0) or (i % 2 == 1 and j % 2 == 1):
                    self.state[j][i] = Square(Color.LIGHT_SQUARE)
                else:
                    self.state[j][i] = Square(Color.DARK_SQUARE)

    def clear(self):
        for row in self.state[Board.FILLED_ROWS:-Board.FILLED_ROWS]:
            for square in row:
                if square.is_available():
                    square.piece = None

        self.light_pieces = []
        self.dark_pieces = []

    def prepare_pieces(self):
        for row in self.state[:Board.FILLED_ROWS]:
            for square in row:
                if square.is_available():
                    piece = Piece(Color.LIGHT_PIECE)
                    square.piece = piece
                    self.light_pieces.append(piece)

        for row in self.state[-Board.FILLED_ROWS:]:
            for square in row:
                if square.is_available():
                    piece = Piece(Color.DARK_PIECE)
                    square.piece = piece
                    self.dark_pieces.append(piece)

    def draw(self, surface):
        for i in range(Board.SIZE):
            for j in range(Board.SIZE):
                self.state[i][j].draw(surface, j, i)


class Square:
    def __init__(self, color: Tuple[int, int, int]):
        self._color = color
        self.piece = None

    def is_occupied(self):
        return self.piece is not None

    def is_available(self):
        return self._color is not Color.LIGHT_SQUARE

    def draw(self, surface: pygame.Surface, x, y):
        self._draw_square(surface, x, y)
        if self.piece:
            self.piece.draw(surface, x, y)

    def _draw_square(self, surface: pygame.Surface, x, y):
        w = surface.get_width()
        h = surface. get_height()
        board_size = min(w, h)
        square_size = int(board_size / Board.SIZE)
        square_rect = pygame.Rect((w - board_size) / 2 + x * square_size,
                                  (h - board_size) / 2 + y * square_size,
                                  square_size, square_size)
        pygame.draw.rect(surface, self._color, square_rect)

    def __str__(self):
        return '{}'.format(self.piece)


class Piece:
    def __init__(self, color: Tuple[int, int, int]):
        self._color = color
        self._king = False

    @property
    def is_king(self):
        return self._king

    def draw(self, surface: pygame.Surface, x, y):
        w = surface.get_width()
        h = surface.get_height()
        board_size = min(w, h)
        piece_radius = int((board_size / Board.SIZE) / 2)
        piece_pos = (
            int((w - board_size) / 2 + (x + 0.5) * (piece_radius * 2)),
            int((h - board_size) / 2 + (y + 0.5) * (piece_radius * 2))
        )
        pygame.draw.circle(surface, self._color, piece_pos, piece_radius)

    def __str__(self):
        if self._color is Color.DARK_PIECE:
            return 'White'
        elif self._color is Color.LIGHT_PIECE:
            return 'Black'
