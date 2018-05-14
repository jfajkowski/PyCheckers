import unittest
from copy import copy, deepcopy

from elements import State, Pawn, Color


class StateTestCase(unittest.TestCase):
    def test_copy(self):
        # given
        state_a = State(3, 3)
        state_a.add(0, 0, Pawn(Color.LIGHT_PIECE))
        state_a.add(2, 2, Pawn(Color.DARK_PIECE))

        # when
        state_b = copy(state_a)

        # then
        self.assertTrue(state_a.get_piece(0, 0) is state_b.get_piece(0, 0))
        self.assertTrue(state_a.get_piece(2, 2) is state_b.get_piece(2, 2))

    def test_deep_copy(self):
        # given
        state_a = State(3, 3)
        state_a.add(0, 0, Pawn(Color.LIGHT_PIECE))
        state_a.add(2, 2, Pawn(Color.DARK_PIECE))

        # when
        state_b = deepcopy(state_a)

        # then
        self.assertFalse(state_a.get_piece(0, 0) is state_b.get_piece(0, 0))
        self.assertFalse(state_a.get_piece(2, 2) is state_b.get_piece(2, 2))


if __name__ == '__main__':
    unittest.main()
