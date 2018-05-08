import random
from abc import ABC, abstractmethod
from time import sleep

from elements import Board, Piece
from heuristics import light_pieces_dark_pieces_difference_heuristic


class GameStrategy(ABC):

    @abstractmethod
    def move(self, pieces, board: Board):
        pass

    def _calculate_valid_moves(self, piece: Piece, board: Board):
        moves = []
        for x, y in piece.moves():
            if board.is_in_bounds(x, y) and not board.is_occupied(x, y):
                moves.append(((piece.x, piece.y), (x, y)))
        return moves



class AlphaBetaGameStrategy(GameStrategy):

    def move(self, pieces, board: Board):
        pass


class ManualGameStrategy(GameStrategy):

    def move(self, pieces, board: Board):
        pass


class MiniMaxGameStrategy(GameStrategy):

    def __init__(self, heuristic=light_pieces_dark_pieces_difference_heuristic, depth=3):
        self.heuristic = heuristic
        self.depth = depth

    def move(self, pieces, board: Board):
        pass


class RandomGameStrategy(GameStrategy):

    def move(self, pieces, board: Board):
        moves = []
        for piece in pieces:
            moves += self._calculate_valid_moves(piece, board)
        position_from, position_to = random.choice(moves)

        next_state = board.state
        piece = next_state[position_from[1]][position_from[0]]
        next_state[position_from[1]][position_from[0]] = None
        next_state[position_to[1]][position_to[0]] = piece
        piece.x, piece.y = position_to
        board.state = next_state
        sleep(1)