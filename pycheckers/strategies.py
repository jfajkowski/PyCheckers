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
        piece_moves = piece.moves()
        if piece_moves:
            for x, y in piece_moves:
                move = None
                if state.is_in_bounds(x, y) and not state.is_occupied(x, y):
                    move = Move(state, (piece.x, piece.y), (x, y))
                elif state.is_in_bounds(x, y) and state.is_occupied(x, y):
                    move = Beat(state, (piece.x, piece.y), (x, y))
                if move and move.is_valid():
                    moves.append(move)
        return moves


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
        moves = []
        for piece in state.pieces(self._color):
            moves += self._calculate_valid_moves(piece, state)

        if not moves:
            return

        return random.choice(moves)
