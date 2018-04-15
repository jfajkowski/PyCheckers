import numpy as np

class Color:
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)


class Piece:
    def __init__(self, color: Color):
        self._color = color
        self._king = False

    @property
    def is_king(self):
        return self._king


class Board:
    def __init__(self):
        self._state = np.empty((10, 10), dtype=Piece)