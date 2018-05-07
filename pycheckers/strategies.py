from abc import ABC, abstractmethod

import random
from time import sleep

from elements import Board, Piece, Color
from heuristics import light_pieces_dark_pieces_difference_heuristic


class GameStrategy(ABC):
    @abstractmethod
    def move(self, board: Board):
        pass

    def _calculate_valid_moves(self, piece: Piece, board: Board):
        if piece._color == Color.LIGHT_PIECE:
            moves = []
            if piece.is_king:
                # TODO Implement king moves logic
                pass
            else:
                piece_x, piece_y = board.position(piece)
                forward_positions = [(piece_x - 1, piece_y - 1), (piece_x + 1, piece_y - 1)]
                backward_positions = [(piece_x - 1, piece_y + 1), (piece_x + 1, piece_y + 1)]

                for x, y in forward_positions:
                    if board.is_in_bounds(x, y) and not board.is_occupied(x, y):
                        next_state = board.state
                        next_state[piece_y][piece_x] = None
                        next_state[y][x] = piece
                        moves.append(next_state)

            return moves



class AlphaBetaGameStrategy(GameStrategy):
    def move(self, board: Board):
        pass


class ManualGameStrategy(GameStrategy):
    def move(self, board: Board):
        pass


class MiniMaxGameStrategy(GameStrategy):
    def __init__(self, heuristic=light_pieces_dark_pieces_difference_heuristic, depth=3):
        self.heuristic = heuristic
        self.depth = depth

    def move(self, board: Board):
        pass

class RandomGameStrategy(GameStrategy):
    def move(self, board: Board):
        moves = []
        for piece in board.light_pieces:
            moves += self._calculate_valid_moves(piece, board)
        board.state = random.choice(moves)
        sleep(1)