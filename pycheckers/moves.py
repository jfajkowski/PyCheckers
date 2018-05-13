import logging
from abc import abstractmethod
from typing import List

from elements import Piece, Board

class Move:

    def __init__(self, moving_piece: Piece, position_to, board: Board):
        self.moving_piece = moving_piece
        self.position_from = (moving_piece.x, moving_piece.y)
        self.position_to = position_to
        self.board = board
        self.next_state = None

    def set_position_from(self, position_from):
        self.position_from = position_from

    @abstractmethod
    def execute(self):
        pass


class Forward(Move):

    def execute(self):
        # move from one position to another without beating
        logging.debug('Normal move')
        self.next_state = self.board.state
        piece = self.next_state[self.position_from[1]][self.position_from[0]]

        # todo: check why piece is null sometimes
        if piece is None:
            return

        self.next_state[self.position_from[1]][self.position_from[0]] = None
        self.next_state[self.position_to[1]][self.position_to[0]] = piece
        piece.x, piece.y = self.position_to
        return self


class Beat(Move):

    def __init__(self, moving_piece: Piece, position_to, board: Board):
        super().__init__(moving_piece, position_to, board)
        self._beat_coords = None

    def execute(self):
        if self._beat_coords is None:
            raise AttributeError('beat_coords are not set')
        # maybe create Forward object here:
        self.next_state = self.board.state
        piece = self.next_state[self.position_from[1]][self.position_from[0]]

        # todo: check why piece is null sometimes
        if piece is None:
            return

        self.next_state[self.position_from[1]][self.position_from[0]] = None
        self.next_state[self.position_to[1]][self.position_to[0]] = None
        self.next_state[self._beat_coords[1]][self._beat_coords[0]] = piece
        piece.x, piece.y = self._beat_coords
        return self

    def get_beat_coords(self):
        piece_to_beat = self.board.get_piece(self.position_to[0], self.position_to[1])
        if piece_to_beat.color == self.moving_piece.color:
            return None
        # down, right
        if self.moving_piece.x - self.position_to[0] < 0 and self.moving_piece.y - self.position_to[1] < 0:
            coords = self.position_to[0] + 1, self.position_to[1] + 1
            if self.board.is_in_bounds(coords[0], coords[1]) and not self.board.is_occupied(coords[0], coords[1]):
                return coords

        # up, right
        elif self.moving_piece.x - self.position_to[0] < 0 < self.moving_piece.y - self.position_to[1]:
            coords = self.position_to[0] + 1, self.position_to[1] - 1
            if self.board.is_in_bounds(coords[0], coords[1]) and not self.board.is_occupied(coords[0], coords[1]):
                return coords

        # down, left
        elif self.moving_piece.x - self.position_to[0] > 0 > self.moving_piece.y - self.position_to[1]:
            coords = self.position_to[0] - 1, self.position_to[1] + 1
            if self.board.is_in_bounds(coords[0], coords[1]) and not self.board.is_occupied(coords[0], coords[1]):
                return coords

        # up, left
        elif self.moving_piece.x - self.position_to[0] > 0 and self.moving_piece.y - self.position_to[1] > 0:
            coords = self.position_to[0] - 1, self.position_to[1] - 1
            if self.board.is_in_bounds(coords[0], coords[1]) and not self.board.is_occupied(coords[0], coords[1]):
                return coords

        return None

    def set_beat_coords(self, coords):
        self._beat_coords = coords


class MultipleBeat(Beat):

    def __init__(self, moving_piece: Piece, position_to, board: Board):
        super().__init__(moving_piece, position_to, board)
        self._beat_coords = None
        self.beats: List[Beat] = []

    def create_beats_path(self):
        pass

    def execute(self):
        pass
