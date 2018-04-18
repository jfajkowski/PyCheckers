from typing import Tuple

import numpy as np


class Color:
    DARK = (0, 0, 0)
    LIGHT = (255, 255, 255)


class Board:
    SIZE = 10
    FILLED_ROWS = 3

    def __init__(self):
        self.squares = np.empty((Board.SIZE, Board.SIZE), dtype=Square)
        self.light_pieces = []
        self.dark_pieces = []

    def build(self):
        for i in range(Board.SIZE):
            for j in range(Board.SIZE):
                if (i % 2 == 0 and j % 2 == 0) or (i % 2 == 1 and j % 2 == 1):
                    self.squares[i][j] = Square(Color.DARK)
                else:
                    self.squares[i][j] = Square(Color.LIGHT)

    def clear(self):
        for row in self.squares[Board.FILLED_ROWS:-Board.FILLED_ROWS]:
            for square in row:
                if square.is_available():
                    square.piece = None

        self.light_pieces = []
        self.dark_pieces = []

    def prepare_pieces(self):
        for row in self.squares[:Board.FILLED_ROWS]:
            for square in row:
                if square.is_available():
                    piece = Piece(Color.LIGHT)
                    square.piece = piece
                    self.light_pieces.append(piece)

        for row in self.squares[-Board.FILLED_ROWS:]:
            for square in row:
                if square.is_available():
                    piece = Piece(Color.DARK)
                    square.piece = piece
                    self.dark_pieces.append(piece)


class Square:
    def __init__(self, color: Tuple[int, int, int]):
        self._color = color
        self.piece = None

    def is_occupied(self):
        return self.piece is not None

    def is_available(self):
        return self._color is not Color.LIGHT


class Piece:
    def __init__(self, color: Tuple[int, int, int]):
        self._color = color
        self._king = False

    @property
    def is_king(self):
        return self._king
