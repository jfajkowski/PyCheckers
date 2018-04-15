from abc import ABC, abstractmethod


class GameStrategy(ABC):
    @abstractmethod
    def move(self, board):
        pass


class AlphaBetaGameStrategy(GameStrategy):
    def move(self, board):
        pass


class ManualGameStrategy(GameStrategy):
    def move(self, board):
        pass


class MiniMaxGameStrategy(GameStrategy):
    def move(self, board):
        pass
