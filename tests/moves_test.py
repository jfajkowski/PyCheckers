import unittest

from elements import State, Pawn, Color
from moves import Move, Beat


class PawnMovesTestCase(unittest.TestCase):
    def test_light_pawn_execute_move(self):
        for piece_position, target_position in [((1, 1), (0, 0)),
                                                ((1, 1), (2, 0))]:
            # given
            state = State(3, 3)
            state.add(piece_position[0], piece_position[1], Pawn(Color.LIGHT_PIECE))
            move = Move(state, piece_position, target_position)

            # when
            next_state = move.execute()

            # then
            self.assertTrue(state.get_piece(*piece_position))
            self.assertFalse(state.get_piece(*target_position))
            self.assertFalse(next_state.get_piece(*piece_position))
            self.assertTrue(next_state.get_piece(*target_position))

    def test_light_pawn_invalid_move(self):
        for piece_position, target_position in [((1, 1), (0, 2)),
                                                ((1, 1), (2, 2))]:
            # given
            state = State(3, 3)
            state.add(piece_position[0], piece_position[1], Pawn(Color.LIGHT_PIECE))
            move = Move(state, piece_position, target_position)

            # when

            # then
            self.assertFalse(move.is_valid())

    def test_dark_pawn_execute_move(self):
        for piece_position, target_position in [((1, 1), (0, 2)),
                                                ((1, 1), (2, 2))]:
            # given
            state = State(3, 3)
            state.add(piece_position[0], piece_position[1], Pawn(Color.DARK_PIECE))
            move = Move(state, piece_position, target_position)

            # when
            next_state = move.execute()

            # then
            self.assertTrue(state.get_piece(*piece_position))
            self.assertFalse(state.get_piece(*target_position))
            self.assertFalse(next_state.get_piece(*piece_position))
            self.assertTrue(next_state.get_piece(*target_position))

    def test_dark_pawn_invalid_move(self):
        for piece_position, target_position in [((1, 1), (0, 0)),
                                                ((1, 1), (2, 0))]:
            # given
            state = State(3, 3)
            state.add(piece_position[0], piece_position[1], Pawn(Color.DARK_PIECE))
            move = Move(state, piece_position, target_position)

            # when

            # then
            self.assertFalse(move.is_valid())

    def test_pawn_beat(self):
        for piece_position, target_position in [((0, 0), (1, 1)),
                                                ((0, 2), (1, 1)),
                                                ((2, 0), (1, 1)),
                                                ((2, 2), (1, 1))]:
            for piece_color, target_color in [(Color.LIGHT_PIECE, Color.DARK_PIECE),
                                              (Color.DARK_PIECE, Color.LIGHT_PIECE)]:
                # given
                state = State(3, 3)
                state.add(piece_position[0], piece_position[1], Pawn(piece_color))
                state.add(target_position[0], target_position[1], Pawn(target_color))
                move = Beat(state, piece_position, target_position)

                # when
                next_state = move.execute()

                # then
                self.assertTrue(state.get_piece(*piece_position))
                self.assertTrue(state.get_piece(*target_position))
                self.assertFalse(next_state.get_piece(*piece_position))
                self.assertFalse(next_state.get_piece(*target_position))

    def test_pawn_block(self):
        for piece_position, target_position, block_position in [((0, 0), (1, 1), (2, 2)),
                                                                ((0, 2), (1, 1), (2, 0)),
                                                                ((2, 0), (1, 1), (0, 2)),
                                                                ((2, 2), (1, 1), (0, 0))]:
            for piece_color, target_color, block_color in [(Color.LIGHT_PIECE, Color.DARK_PIECE, Color.DARK_PIECE),
                                                           (Color.LIGHT_PIECE, Color.DARK_PIECE, Color.LIGHT_PIECE),
                                                           (Color.DARK_PIECE, Color.LIGHT_PIECE, Color.LIGHT_PIECE),
                                                           (Color.DARK_PIECE, Color.LIGHT_PIECE, Color.DARK_PIECE)]:
                # given
                state = State(3, 3)
                state.add(piece_position[0], piece_position[1], Pawn(piece_color))
                state.add(target_position[0], target_position[1], Pawn(target_color))
                state.add(block_position[0], block_position[1], Pawn(block_color))
                move = Beat(state, piece_position, target_position)

                # when

                # then
                self.assertFalse(move.is_valid())


if __name__ == '__main__':
    unittest.main()
