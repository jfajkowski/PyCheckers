from elements import Board


def light_pieces_dark_pieces_difference_heuristic(board: Board):
    return len(board.state.light_pieces) - len(board.state.dark_pieces)


def dark_pieces_light_pieces_difference_heuristic(board: Board):
    return len(board.state.dark_pieces) - len(board.state.light_pieces)
