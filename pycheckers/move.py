import logging
from abc import abstractmethod

from elements import Piece, Board


# move from one position to another without beating
def forward(board: Board, position_from, position_to):
    logging.info('Normal move')
    next_state = board.state
    piece = next_state[position_from[1]][position_from[0]]
    next_state[position_from[1]][position_from[0]] = None
    next_state[position_to[1]][position_to[0]] = piece
    piece.x, piece.y = position_to
    board.state = next_state
    return board


def beat(board: Board, position_from, position_to):
    logging.info('Beat move')
    return board


class Move:

    def __init__(self, position_from, position_to, board: Board):
        self.position_from = position_from
        self.position_to = position_to
        self.board = board

    def set_position_from(self, position_from):
        self.position_from = position_from

    @abstractmethod
    def execute(self):
        pass


class Beat(Move):

    def execute(self):
        beat(self.board, self.position_from, self.position_to)


class Forward(Move):

    def execute(self):
        forward(self.board, self.position_from, self.position_to)

