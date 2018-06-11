import math
import random
import pygame
from abc import ABC, abstractmethod
from typing import Tuple

from elements import State, Piece, Pawn, King, Color, Board
from heuristics import light_pieces_dark_pieces_difference_heuristic
from moves import PawnMove, PawnBeat, KingMove, KingBeat


class GameStrategy(ABC):
    def __init__(self, color):
        self._color = color

    @property
    def color(self):
        return self._color

    @abstractmethod
    def move(self, state: State):
        pass

    def _calculate_all_moves(self, state: State, color: Tuple[int, int, int]):
        beats = []
        for piece_position in state.piece_positions(color):
            beats += self._calculate_valid_beats(piece_position, state)
        if beats:
            return beats

        moves = []
        for piece_position in state.piece_positions(color):
            moves += self._calculate_valid_moves(piece_position, state)
        if moves:
            return moves

        return []

    def _calculate_valid_moves(self, piece_position, state: State):
        moves = []
        piece = state.get_piece(*piece_position)
        target_positions = piece.target_positions(*piece_position)
        for target_position in target_positions:
            if state.is_in_bounds(*target_position) and not state.is_occupied(*target_position):
                move = KingMove(state, piece_position, target_position) if isinstance(piece, King) \
                       else PawnMove(state, piece_position, target_position)
                if move.is_valid():
                    moves.append([move])
        return moves

    def _calculate_valid_beats(self, piece_position, state: State, previous_beat: PawnBeat = None):
        beats = []
        if piece_position is None:
            return beats

        piece = state.get_piece(*piece_position)
        target_positions = piece.target_positions(*piece_position)
        for target_position in target_positions:
            if state.is_in_bounds(*target_position) and state.is_occupied(*target_position) \
                    and state.get_color(*target_position) != piece.color:
                sub_beats = []
                if isinstance(piece, King):
                    final_positions = KingBeat.calculate_final_positions(piece_position, target_position)
                    for final_position in final_positions:
                        sub_beats.append(KingBeat(state, piece_position, target_position, final_position))
                else:
                    sub_beats.append(PawnBeat(state, piece_position, target_position))

                for sub_beat in sub_beats:
                    if sub_beat.is_valid():
                        next_state = sub_beat.execute()

                        beats += self._calculate_valid_beats(sub_beat.final_position, next_state, sub_beat)
                        if previous_beat:
                            previous_beat.next_beats.append(sub_beat)
                            sub_beat.previous_beat = previous_beat
                        else:
                            beats += sub_beat.to_list()
        return beats


class AlphaBetaGameStrategy(GameStrategy):
    def __init__(self, color, heuristic=light_pieces_dark_pieces_difference_heuristic, depth=10):
        super().__init__(color)
        self._heuristic = heuristic
        self._depth = depth

    def move(self, state: State):
        # alpha for maximizer, beta for minimizer
        alpha, beta = -math.inf, math.inf
        best_move, best_value = None, -math.inf

        for move in self._calculate_all_moves(state, self._color):
            initial_state = move[-1].execute()
            value = self.alpha_beta(initial_state, Color.opposite(self._color), alpha, beta, self._depth - 1)
            if value > best_value:
                best_value, best_move = value, move
        return best_move, False

    def alpha_beta(self, state, color: Tuple[int, int, int], alpha, beta, depth):
        if depth == 0 or state.is_ending():
            heuristic = self._heuristic(state)
            return heuristic

        if color == self._color:
            for move in self._calculate_all_moves(state, color):
                next_state = move[-1].execute()
                alpha = max(alpha, self.alpha_beta(next_state, Color.opposite(color), alpha, beta, depth - 1))
                if beta <= alpha:
                    return beta
            return alpha
        else:
            for move in self._calculate_all_moves(state, color):
                next_state = move[-1].execute()
                beta = min(beta, self.alpha_beta(next_state, Color.opposite(color), alpha, beta, depth - 1))
                if beta <= alpha:
                    return alpha
            return beta


class ManualGameStrategy(GameStrategy):
    def __init__(self, color):
        super().__init__(color)
        self._next_beat_piece = None

    def move(self, state: State):

        beats = []
        for piece in state.piece_positions(self._color):
            beats += self._calculate_valid_beats(piece, state)
        moves = []
        for piece in state.piece_positions(self._color):
            moves += self._calculate_valid_moves(piece, state)

        while True:
            click_up = None
            click_down = None
            move_clicked = False

            while not move_clicked:
                ev = pygame.event.get()

                for event in ev:
                    if event.type == pygame.MOUSEBUTTONUP:
                        x, y = pygame.mouse.get_pos()
                        x = int(x / (640 / Board.ROWS))  # board width
                        y = int(y / (640 / Board.COLS))  # board height
                        click_up = (x, y)
                        move_clicked = True

                    if event.type == pygame.MOUSEBUTTONDOWN:
                        x, y = pygame.mouse.get_pos()
                        x = int(x / (640 / Board.ROWS))
                        y = int(y / (640 / Board.COLS))
                        click_down = (x, y)

            if click_up == click_down:
                continue

            if self._next_beat_piece and self._next_beat_piece != click_down:
                continue

            if beats:
                current_beat = None
                for b in beats:
                    if b[0].piece_position == click_down and b[0].final_position == click_up:
                        if current_beat is None or len(current_beat[0].next_beats) < len(b[0].next_beats):
                            current_beat = b

                if current_beat is None:
                    continue

                piece = state.get_piece(*click_down)
                beat_to_return = None
                if isinstance(piece, King):
                    beat_to_return = KingBeat(state, current_beat[0].piece_position, current_beat[0].target_position, current_beat[0].final_position)
                else:
                    beat_to_return = PawnBeat(state, current_beat[0].piece_position, current_beat[0].target_position)

                if len(current_beat[0].next_beats) > 0:
                    self._next_beat_piece = current_beat[0].final_position
                    return [beat_to_return], True
                else:
                    self._next_beat_piece = None
                    return [beat_to_return], False

            if moves and not beats:
                for m in moves:
                    if m[0].piece_position == click_down and m[0].target_position == click_up:
                        return m, False


class MinMaxGameStrategy(GameStrategy):
    def __init__(self, color, heuristic=light_pieces_dark_pieces_difference_heuristic, depth=4):
        super().__init__(color)
        self._heuristic = heuristic
        self._depth = depth

    def move(self, state: State):
        best_move, best_value = None, -math.inf
        for move in self._calculate_all_moves(state, self._color):
            next_state = move[-1].execute()
            value = self.min_max(next_state, Color.opposite(self._color), self._depth - 1)
            if value > best_value:
                best_move, best_value = move, value
        return best_move, False

    def min_max(self, state: State, color: Tuple[int, int, int], depth: int):
        if depth == 0 or state.is_ending():
            return self._heuristic(state)

        if color == self._color:
            best_value = -math.inf
            for move in self._calculate_all_moves(state, color):
                next_state = move[-1].execute()
                value = self.min_max(next_state, Color.opposite(color), depth - 1)
                best_value = max(best_value, value)
            return best_value
        else:
            best_value = math.inf
            for move in self._calculate_all_moves(state, color):
                next_state = move[-1].execute()
                value = self.min_max(next_state, Color.opposite(color), depth - 1)
                best_value = min(best_value, value)
            return best_value


class RandomGameStrategy(GameStrategy):
    def move(self, state: State):
        beats = []
        for piece in state.piece_positions(self._color):
            beats += self._calculate_valid_beats(piece, state)

        if beats:
            return random.choice(beats), False

        moves = []
        for piece in state.piece_positions(self._color):
            moves += self._calculate_valid_moves(piece, state)

        if moves:
            return random.choice(moves), False
