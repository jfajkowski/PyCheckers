from elements import Board


def light_pieces_dark_pieces_difference_heuristic(board: Board):
    return len(board.light_pieces) - len(board.dark_pieces)


def dark_pieces_light_pieces_difference_heuristic(board: Board):
    return len(board.dark_pieces) - len(board.light_pieces)
