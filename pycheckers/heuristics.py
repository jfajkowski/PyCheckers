from elements import State, Color


def light_pieces_dark_pieces_difference_heuristic(state: State):
    return len(state.pieces(Color.LIGHT_PIECE)) - len(state.pieces(Color.DARK_PIECE))


def dark_pieces_light_pieces_difference_heuristic(state: State):
    return len(state.pieces(Color.DARK_PIECE)) - len(state.pieces(Color.LIGHT_PIECE))
