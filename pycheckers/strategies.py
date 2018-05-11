import random
from abc import ABC, abstractmethod
from time import sleep

from elements import Board, Piece
from heuristics import light_pieces_dark_pieces_difference_heuristic
from move import Move, Forward, Beat


class GameStrategy(ABC):

    @abstractmethod
    def move(self, pieces, board: Board):
        pass

    def _calculate_valid_moves(self, piece: Piece, board: Board):
        moves = []
        piece_moves = piece.moves()
        if piece_moves:
            for x, y in piece_moves:
                if board.is_in_bounds(x, y) and not board.is_occupied(x, y):
                    moves.append(Forward((piece.x, piece.y), (x, y), board))
                elif board.is_in_bounds(x, y) and board.is_occupied(x, y):
                    moves.append(Beat((piece.x, piece.y), (x, y), board))
        return moves


class AlphaBetaGameStrategy(GameStrategy):

    def __init__(self, heuristic=light_pieces_dark_pieces_difference_heuristic, depth=3):
        self.heuristic = heuristic
        self.depth = depth

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

        if not moves:
            return

        current_move = random.choice(moves)
        current_move.execute()
        sleep(0.05)
