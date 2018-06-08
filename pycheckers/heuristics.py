from elements import State, Color, Board
from typing import Tuple


def light_pieces_dark_pieces_difference_heuristic(state: State):
    return len(state.piece_positions(Color.LIGHT_PIECE)) - len(state.piece_positions(Color.DARK_PIECE))


def dark_pieces_light_pieces_difference_heuristic(state: State):
    return len(state.piece_positions(Color.DARK_PIECE)) - len(state.piece_positions(Color.LIGHT_PIECE))


def light_pieces_maximizing_heuristic(state: State):
    return 10 * light_pieces_dark_pieces_difference_heuristic(state) + distance_to_last_position(state, Color.LIGHT_PIECE)


def dark_pieces_maximizing_heuristic(state: State):
    return 10 * dark_pieces_light_pieces_difference_heuristic(state) + distance_to_last_position(state, Color.DARK_PIECE)


def distance_to_last_position(state: State, color: Tuple[int, int, int]):
    value = 0
    if color == Color.LIGHT_PIECE:
        for x, y in state.piece_positions(color):
            value += Board.ROWS - 1 - y
    else:
        for x, y in state.piece_positions(color):
                value += y
    return value
