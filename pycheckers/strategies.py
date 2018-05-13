import random
from abc import ABC, abstractmethod
from time import sleep

from elements import Board, Piece
from heuristics import light_pieces_dark_pieces_difference_heuristic
from moves import Move, Forward, Beat


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
                    moves.append(Forward(piece, (x, y), board))
                elif board.is_in_bounds(x, y) and board.is_occupied(x, y):
                    beat = Beat(piece, (x, y), board)
                    beat_coord = beat.get_beat_coords()
                    if beat_coord is not None:
                        beat.set_beat_coords(beat_coord)
                        moves.append(beat)
        return moves


    def get_multiple_beat_path(self, piece: Piece, board: Board, destination):
        path = []
        move_on = True
        while move_on:
            next_step = self.single_beat_is_possible(piece, board, destination)
            if next_step is not None:
                path.append(next_step)


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
        after_move = current_move.execute()
        if after_move is not None:
            board.state = after_move.next_state
        sleep(0.1)
