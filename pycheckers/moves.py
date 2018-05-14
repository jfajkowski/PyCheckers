import logging
from copy import copy

from elements import State, Color, Pawn


class Move:
    '''Move from one position to another without beating'''
    def __init__(self, state: State, piece_position, target_position):
        self.state = copy(state)
        self.piece_position = piece_position
        self.target_position = target_position
        self.piece = state.get_piece(*self.piece_position)

    def is_valid(self):
        if isinstance(self.piece, Pawn) and self.is_forward():
            return True

    def is_forward(self):
        delta_y = self.target_position[1] - self.piece_position[1]
        if self.piece.color == Color.DARK_PIECE and delta_y > 0:
            return True
        elif self.piece.color == Color.LIGHT_PIECE and delta_y < 0:
            return True
        return False

    def execute(self):
        logging.debug('Normal move')
        self.state.remove(*self.piece_position)
        final_position = self.target_position
        self.state.add(final_position[0], final_position[1], self.piece)
        return self.state


class Beat(Move):
    def __init__(self, state: State, piece_position, target_position):
        super().__init__(state, piece_position, target_position)
        self.beat_piece = self.state.get_piece(*target_position)

    def is_valid(self):
        final_position = self.calculate_final_position()
        return self.state.is_in_bounds(*final_position) \
               and not self.state.is_occupied(*final_position) \
               and self.piece.color != self.beat_piece.color
    
    def execute(self):
        logging.debug('Beat move')
        piece = self.state.get_piece(*self.piece_position)
        self.state.remove(*self.piece_position)
        self.state.remove(*self.target_position)
        final_position = self.calculate_final_position()
        self.state.add(final_position[0], final_position[1], piece)
        return self.state

    def calculate_final_position(self):
        return (2 * self.target_position[0] - self.piece_position[0],
                2 * self.target_position[1] - self.piece_position[1])
