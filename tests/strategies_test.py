import unittest

from elements import Color, State, Pawn
from heuristics import light_pieces_dark_pieces_difference_heuristic
from strategies import MinMaxGameStrategy


class MinMaxTestCase(unittest.TestCase):
    def test_simple_state(self):
        # given
        strategy = MinMaxGameStrategy(color=Color.LIGHT_PIECE,
                                      heuristic=light_pieces_dark_pieces_difference_heuristic,
                                      depth=1)

        state = State(5, 5)
        state.add(2, 4, Pawn(Color.LIGHT_PIECE))
        state.add(1, 1, Pawn(Color.DARK_PIECE))
        state.add(1, 3, Pawn(Color.DARK_PIECE))
        state.add(3, 3, Pawn(Color.DARK_PIECE))

        # when
        move = strategy.move(state)
        next_state = move[-1].execute()

        # then
        self.assertFalse(next_state.get_piece(2, 4))
        self.assertFalse(next_state.get_piece(1, 1))
        self.assertFalse(next_state.get_piece(1, 3))
        self.assertTrue(next_state.get_piece(3, 3))
        self.assertTrue(next_state.get_piece(2, 0))

    def test_complex_state(self):
        # given
        strategy = MinMaxGameStrategy(color=Color.LIGHT_PIECE,
                                      heuristic=light_pieces_dark_pieces_difference_heuristic,
                                      depth=3)

        state = State(5, 5)
        state.add(0, 4, Pawn(Color.LIGHT_PIECE))
        state.add(2, 4, Pawn(Color.LIGHT_PIECE))
        state.add(3, 3, Pawn(Color.LIGHT_PIECE))
        state.add(1, 1, Pawn(Color.DARK_PIECE))
        state.add(3, 1, Pawn(Color.DARK_PIECE))
        state.add(0, 2, Pawn(Color.DARK_PIECE))

        # when
        move = strategy.move(state)
        next_state = move[-1].execute()

        # then
        self.assertFalse(next_state.get_piece(3, 3))
        self.assertTrue(next_state.get_piece(2, 2))

    def test_avoid(self):
        # given
        strategy = MinMaxGameStrategy(color=Color.LIGHT_PIECE,
                                      heuristic=light_pieces_dark_pieces_difference_heuristic,
                                      depth=2)

        state = State(5, 5)
        state.add(3, 3, Pawn(Color.LIGHT_PIECE))
        state.add(2, 2, Pawn(Color.LIGHT_PIECE))
        state.add(0, 0, Pawn(Color.DARK_PIECE))

        # when
        move = strategy.move(state)
        next_state = move[-1].execute()

        # then
        self.assertFalse(next_state.get_piece(1, 1))


if __name__ == '__main__':
    unittest.main()
