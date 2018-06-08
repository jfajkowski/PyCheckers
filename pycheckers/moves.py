import logging
import numpy as np
from copy import copy

from elements import State, Color, Pawn, King, Board


class Move:
    '''Move from one position to another without beating'''

    def __init__(self, state: State, piece_position, target_position):
        self._state = copy(state)
        self.piece_position = piece_position
        self.target_position = target_position
        self.piece = state.get_piece(*self.piece_position)

    @property
    def state(self):
        return copy(self._state)

    def is_valid(self):
        if isinstance(self.piece, Pawn) and self.is_forward():
            return True
        return False

    def is_forward(self):
        delta_y = self.target_position[1] - self.piece_position[1]
        if self.piece.color == Color.DARK_PIECE and delta_y > 0:
            return True
        elif self.piece.color == Color.LIGHT_PIECE and delta_y < 0:
            return True
        return False

    def execute(self):
        next_state = self.state
        next_state.remove(*self.piece_position)
        final_position = self.target_position
        next_state.add(final_position[0], final_position[1], self.piece)
        if self.is_on_last_position(final_position):
            next_state.transform_into_king(*final_position)
        return next_state

    def is_on_last_position(self, piece_position):
        if self.piece.color == Color.DARK_PIECE and piece_position[1] == self._state.rows - 1:
            return True
        elif self.piece.color == Color.LIGHT_PIECE and piece_position[1] == 0:
            return True
        return False

    # get all possible positions where the Piece can be placed after beating piece.
    @staticmethod
    def calculate_final_positions(piece_position, target_position):
        final_positions = []
        y = target_position[1]
        x = target_position[0]
        sign_y = np.sign(y - piece_position[1])
        sign_x = np.sign(x - piece_position[0])
        for j in range(-Board.COLS, Board.COLS):
            for i in range(-Board.COLS, Board.COLS):
                # every field after the beating piece (in the context of attacking piece)
                if -1 < (x + sign_x * i) < Board.COLS and -1 < (y + sign_y * j) < Board.COLS:
                    # fields on diagonal in the right direction
                    if i * i == j * j and j > 0 and i > 0:
                        final_positions.append(((x + sign_x * i), (y + sign_y * j)))
        return final_positions

    # check if any other Piece stay on a path between piece_position and target_position
    def is_path_empty(self, start_position, aim_position, including_aim):
        param = 1 if including_aim else 0
        y = aim_position[1]
        x = aim_position[0]
        sign_y = np.sign(y - start_position[1])
        sign_x = np.sign(x - start_position[0])
        for j in range(-Board.COLS, Board.COLS):
            for i in range(-Board.COLS, Board.COLS):
                # every field after the beating piece (in the context of attacking piece)
                if -1 < (x + sign_x * i) < Board.COLS and -1 < (y + sign_y * j) < Board.COLS:
                    # fields between attacking piece and the aim (including the aim position or not)
                    if i * i == j * j and j < param and i < param:
                        if sign_x * (x + sign_x * i) > sign_x * start_position[0] \
                                and sign_y * (y + sign_y * j) > sign_y * start_position[1]:
                            if self.state.is_occupied((x + sign_x * i), (y + sign_y * j)):
                                return False
        return True


class Beat(Move):
    def __init__(self, state: State, piece_position, target_position):
        super().__init__(state, piece_position, target_position)
        self.beat_piece = self.state.get_piece(*target_position)
        self.next_beats = []
        self.final_position = self.calculate_final_position()

    def is_valid(self):
        final_position = self.calculate_final_position()
        return self.state.is_in_bounds(*final_position) \
               and not self.state.is_occupied(*final_position) \
               and self.piece.color != self.beat_piece.color

    def execute(self):
        next_state = self.state
        next_state.remove(*self.piece_position)
        next_state.remove(*self.target_position)
        next_state.add(self.final_position[0], self.final_position[1], self.piece)
        if self.is_on_last_position(self.final_position):
            next_state.transform_into_king(*self.final_position)
        return next_state

    # can be replaced by calculate_final_positions() method. Then final pos should be set in constructor, or setter method.
    def calculate_final_position(self):
        return (2 * self.target_position[0] - self.piece_position[0],
                2 * self.target_position[1] - self.piece_position[1])

    def to_list(self):
        return self.unfold(self)

    @staticmethod
    def unfold(beat):
        if not beat.next_beats:
            return [[beat]]
        else:
            sequences = []
            for next_beat in beat.next_beats:
                for sequence in Beat.unfold(next_beat):
                    sequences.append([beat] + sequence)
            return sequences


class KingsMove(Move):
    # valid is only when there is no pieces on the path
    def is_valid(self):
        if isinstance(self.piece, King):
            return self.is_path_empty(self.piece_position, self.target_position, True)
        return False

    def execute(self):
        next_state = self.state
        next_state.remove(*self.piece_position)
        final_position = self.target_position
        next_state.add(final_position[0], final_position[1], self.piece)
        return next_state


class KingsBeat(Beat):
    def __init__(self, state: State, piece_position, target_position, final_position):
        super().__init__(state, piece_position, target_position)
        self.beat_piece = self.state.get_piece(*target_position)
        self.next_beats = []
        self.final_position = final_position

    # valid when there is no piece on the path between attacking piece and the aim and between aim and the final position (including it).
    def is_valid(self):
        if self.piece.color != self.beat_piece.color:
            if self.is_path_empty(self.piece_position, self.target_position, False) \
                    and self.is_path_empty(self.target_position, self.final_position, True):
                return True
            return False
        return False

    def execute(self):
        next_state = self.state
        next_state.remove(*self.piece_position)
        next_state.remove(*self.target_position)
        next_state.add(self.final_position[0], self.final_position[1], self.piece)
        return next_state
