from typing import Tuple

import numpy as np

class Color:
    DARK = (0, 0, 0)
    LIGHT = (255, 255, 255)


class Piece:
    def __init__(self, color: Tuple[int, int, int]):
        self._color = color
        self._king = False

    @property
    def is_king(self):
        return self._king

class Square:
    def __init__(self, color: Tuple[int, int, int]):
        self._color = color
        self._piece = None

    def is_occupied(self):
        return self._piece is not None

    def is_available(self):
        return self._color is not Color.LIGHT


class Board:
    SIZE = 10

    def __init__(self):
        self._state = np.empty((Board.SIZE, Board.SIZE), dtype=Square)

    def setUp(self):
        for i in range(Board.SIZE):
            for j in range(Board.SIZE):
                if (i % 2 == 0 and j % 2 == 0) or (i % 2 == 1 and j % 2 == 1):
                    self._state[i][j] = Square(Color.DARK)
                else:
                    self._state[i][j] = Square(Color.LIGHT)
