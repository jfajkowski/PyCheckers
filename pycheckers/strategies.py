from abc import ABC, abstractmethod

from elements import Board
from heuristics import light_pieces_dark_pieces_difference_heuristic


class GameStrategy(ABC):
    @abstractmethod
    def move(self, board: Board):
        pass


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
