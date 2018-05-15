import random
from abc import ABC, abstractmethod

from elements import State, Piece
from heuristics import light_pieces_dark_pieces_difference_heuristic
from moves import Move, Beat


class GameStrategy(ABC):
    def __init__(self, color):
        self._color = color

    @abstractmethod
    def move(self, state: State):
        pass

    def _calculate_valid_moves(self, piece: Piece, state: State):
        moves = []
        piece_position, target_positions = piece.positions(state)
        for target_position in target_positions:
            if state.is_in_bounds(*target_position) and not state.is_occupied(*target_position):
                move = Move(state, piece_position, target_position)
                if move.is_valid():
                    moves.append([move])
        return moves

    def _calculate_valid_beats(self, piece: Piece, state: State, previous_beat: Beat = None):
        beats = []
        piece_position, target_positions = piece.positions(state)
        for target_position in target_positions:
            if state.is_in_bounds(*target_position) and state.is_occupied(*target_position) \
                    and state.get_piece(*target_position).color != self._color:
                beat = Beat(state, piece_position, target_position)
                if beat.is_valid():
                    next_state = beat.execute()
                    self._calculate_valid_beats(piece, next_state, beat)
                    if previous_beat:
                        previous_beat.next_beats.append(beat)
                    else:
                        beats += beat.to_list()
        return beats



class AlphaBetaGameStrategy(GameStrategy):

    def __init__(self, color, heuristic=light_pieces_dark_pieces_difference_heuristic, depth=3):
        super().__init__(color)
        self.heuristic = heuristic
        self.depth = depth

    def move(self, state: State):
        pass


class ManualGameStrategy(GameStrategy):
    def move(self, state: State):
        pass


class MiniMaxGameStrategy(GameStrategy):
    def __init__(self, color, heuristic=light_pieces_dark_pieces_difference_heuristic, depth=3):
        super().__init__(color)
        self.heuristic = heuristic
        self.depth = depth

    def move(self, state: State):
        pass


class RandomGameStrategy(GameStrategy):
    def move(self, state: State):
        beats = []
        for piece in state.pieces(self._color):
            beats += self._calculate_valid_beats(piece, state)

        if beats:
            return random.choice(beats)

        moves = []
        for piece in state.pieces(self._color):
            moves += self._calculate_valid_moves(piece, state)

        if moves:
            return random.choice(moves)
