import unittest

from elements import State, Pawn, Color, King
from moves import PawnMove, PawnBeat, KingMove, KingBeat


class PawnMovesTestCase(unittest.TestCase):
    def test_light_pawn_execute_move(self):
        for piece_position, target_position in [((2, 2), (1, 1)),
                                                ((2, 2), (3, 1))]:
            # given
            state = State(5, 5)
            state.add(piece_position[0], piece_position[1], Pawn(Color.LIGHT_PIECE))
            move = PawnMove(state, piece_position, target_position)

            # when
            next_state = move.execute()

            # then
            self.assertTrue(state.get_piece(*piece_position))
            self.assertFalse(state.get_piece(*target_position))
            self.assertFalse(next_state.get_piece(*piece_position))
            self.assertTrue(next_state.get_piece(*target_position))

    def test_light_pawn_invalid_move(self):
        for piece_position, target_position in [((2, 2), (1, 3)),
                                                ((2, 2), (3, 3))]:
            # given
            state = State(5, 5)
            state.add(piece_position[0], piece_position[1], Pawn(Color.LIGHT_PIECE))
            move = PawnMove(state, piece_position, target_position)

            # when

            # then
            self.assertFalse(move.is_valid())

    def test_dark_pawn_execute_move(self):
        for piece_position, target_position in [((2, 2), (1, 3)),
                                                ((2, 2), (3, 3))]:
            # given
            state = State(5, 5)
            state.add(piece_position[0], piece_position[1], Pawn(Color.DARK_PIECE))
            move = PawnMove(state, piece_position, target_position)

            # when
            next_state = move.execute()

            # then
            self.assertTrue(state.get_piece(*piece_position))
            self.assertFalse(state.get_piece(*target_position))
            self.assertFalse(next_state.get_piece(*piece_position))
            self.assertTrue(next_state.get_piece(*target_position))

    def test_dark_pawn_invalid_move(self):
        for piece_position, target_position in [((2, 2), (1, 1)),
                                                ((2, 2), (3, 1))]:
            # given
            state = State(4, 4)
            state.add(piece_position[0], piece_position[1], Pawn(Color.DARK_PIECE))
            move = PawnMove(state, piece_position, target_position)

            # when

            # then
            self.assertFalse(move.is_valid())

    def test_pawn_beat(self):
        for piece_position, target_position in [((1, 1), (2, 2)),
                                                ((1, 3), (2, 2)),
                                                ((3, 1), (2, 2)),
                                                ((3, 3), (2, 2))]:
            for piece_color, target_color in [(Color.LIGHT_PIECE, Color.DARK_PIECE),
                                              (Color.DARK_PIECE, Color.LIGHT_PIECE)]:
                # given
                state = State(5, 5)
                state.add(piece_position[0], piece_position[1], Pawn(piece_color))
                state.add(target_position[0], target_position[1], Pawn(target_color))
                beat = PawnBeat(state, piece_position, target_position)

                # when
                next_state = beat.execute()

                # then
                self.assertTrue(state.get_piece(*piece_position))
                self.assertTrue(state.get_piece(*target_position))
                self.assertFalse(next_state.get_piece(*piece_position))
                self.assertFalse(next_state.get_piece(*target_position))

    def test_pawn_block(self):
        for piece_position, target_position, block_position in [((1, 1), (2, 2), (3, 3)),
                                                                ((1, 3), (2, 2), (3, 1)),
                                                                ((3, 1), (2, 2), (1, 3)),
                                                                ((3, 3), (2, 2), (1, 1))]:
            for piece_color, target_color, block_color in [(Color.LIGHT_PIECE, Color.DARK_PIECE, Color.DARK_PIECE),
                                                           (Color.LIGHT_PIECE, Color.DARK_PIECE, Color.LIGHT_PIECE),
                                                           (Color.DARK_PIECE, Color.LIGHT_PIECE, Color.LIGHT_PIECE),
                                                           (Color.DARK_PIECE, Color.LIGHT_PIECE, Color.DARK_PIECE)]:
                # given
                state = State(5, 5)
                state.add(piece_position[0], piece_position[1], Pawn(piece_color))
                state.add(target_position[0], target_position[1], Pawn(target_color))
                state.add(block_position[0], block_position[1], Pawn(block_color))
                beat = PawnBeat(state, piece_position, target_position)

                # when

                # then
                self.assertFalse(beat.is_valid())

    def test_pawn_multiple_beat(self):
        # given
        piece_color = Color.LIGHT_PIECE
        target_color = Color.DARK_PIECE
        ignored_color = Color.DARK_PIECE

        piece_position = (1, 1)
        target_position_1 = (2, 2)
        target_position_2 = (4, 4)
        ignored_position_1 = (2, 4)
        ignored_position_2 = (4, 2)
        final_position_1 = (3, 3)
        final_position_2 = (5, 5)

        state = State(7, 7)
        state.add(piece_position[0], piece_position[1], Pawn(piece_color))
        state.add(target_position_1[0], target_position_1[1], Pawn(target_color))
        state.add(target_position_2[0], target_position_2[1], Pawn(target_color))
        state.add(ignored_position_1[0], ignored_position_1[1], Pawn(ignored_color))
        state.add(ignored_position_2[0], ignored_position_2[1], Pawn(ignored_color))

        beat = PawnBeat(state, piece_position, target_position_1)
        beat.next_beats.append(PawnBeat(beat.execute(), final_position_1, target_position_2))
        beat.next_beats.append(PawnBeat(beat.execute(), final_position_1, ignored_position_1))
        beat.next_beats.append(PawnBeat(beat.execute(), final_position_1, ignored_position_2))
        beats_list = beat.to_list()

        # when
        next_state_1 = beats_list[0][0].execute()
        next_state_2 = beats_list[0][1].execute()

        # then
        self.assertFalse(next_state_1.get_piece(*piece_position))
        self.assertFalse(next_state_1.get_piece(*target_position_1))
        self.assertTrue(next_state_1.get_piece(*final_position_1))
        self.assertTrue(next_state_1.get_piece(*ignored_position_1))
        self.assertTrue(next_state_1.get_piece(*ignored_position_2))
        self.assertFalse(next_state_2.get_piece(*final_position_1))
        self.assertFalse(next_state_2.get_piece(*target_position_2))
        self.assertTrue(next_state_2.get_piece(*ignored_position_1))
        self.assertTrue(next_state_2.get_piece(*ignored_position_2))
        self.assertTrue(next_state_2.get_piece(*final_position_2))

    def test_pawn_move_and_transform(self):
        for piece_position, target_position in [((1, 1), (0, 0)),
                                                ((1, 1), (2, 0))]:
            # given
            state = State(3, 3)
            state.add(piece_position[0], piece_position[1], Pawn(Color.LIGHT_PIECE))
            move = PawnMove(state, piece_position, target_position)

            # when
            next_state = move.execute()

            # then
            self.assertTrue(state.get_piece(*piece_position))
            self.assertFalse(state.get_piece(*target_position))
            self.assertFalse(next_state.get_piece(*piece_position))
            self.assertTrue(next_state.get_piece(*target_position))

    def test_pawn_beat_and_transform(self):
        for piece_position, target_position in [((0, 2), (1, 1)),
                                                ((2, 2), (1, 1))]:
            # given
            state = State(3, 3)
            state.add(piece_position[0], piece_position[1], Pawn(Color.LIGHT_PIECE))
            state.add(target_position[0], target_position[1], Pawn(Color.DARK_PIECE))
            beat = PawnBeat(state, piece_position, target_position)

            # when
            next_state = beat.execute()

            # then
            self.assertTrue(state.get_piece(*piece_position))
            self.assertTrue(state.get_piece(*target_position))
            self.assertFalse(next_state.get_piece(*piece_position))
            self.assertFalse(next_state.get_piece(*target_position))

    def test_pawn_multiple_beat_and_transform(self):
        # given
        piece_color = Color.DARK_PIECE
        target_color = Color.LIGHT_PIECE
        ignored_color = Color.LIGHT_PIECE

        piece_position = (0, 0)
        target_position_1 = (1, 1)
        target_position_2 = (3, 3)
        ignored_position_1 = (1, 3)
        ignored_position_2 = (3, 1)
        final_position_1 = (2, 2)
        final_position_2 = (4, 4)

        state = State(5, 5)
        state.add(piece_position[0], piece_position[1], Pawn(piece_color))
        state.add(target_position_1[0], target_position_1[1], Pawn(target_color))
        state.add(target_position_2[0], target_position_2[1], Pawn(target_color))
        state.add(ignored_position_1[0], ignored_position_1[1], Pawn(ignored_color))
        state.add(ignored_position_2[0], ignored_position_2[1], Pawn(ignored_color))

        beat = PawnBeat(state, piece_position, target_position_1)
        beat.next_beats.append(PawnBeat(beat.execute(), final_position_1, target_position_2))
        beat.next_beats.append(PawnBeat(beat.execute(), final_position_1, ignored_position_1))
        beat.next_beats.append(PawnBeat(beat.execute(), final_position_1, ignored_position_2))
        beats_list = beat.to_list()

        # when
        next_state_1 = beats_list[0][0].execute()
        next_state_2 = beats_list[0][1].execute()

        # then
        self.assertFalse(next_state_1.get_piece(*piece_position))
        self.assertFalse(next_state_1.get_piece(*target_position_1))
        self.assertTrue(next_state_1.get_piece(*final_position_1))
        self.assertTrue(next_state_1.get_piece(*ignored_position_1))
        self.assertTrue(next_state_1.get_piece(*ignored_position_2))
        self.assertFalse(next_state_2.get_piece(*final_position_1))
        self.assertFalse(next_state_2.get_piece(*target_position_2))
        self.assertTrue(next_state_2.get_piece(*ignored_position_1))
        self.assertTrue(next_state_2.get_piece(*ignored_position_2))
        self.assertTrue(next_state_2.get_piece(*final_position_2))


    def test_pawn_multiple_beat_and_not_transform(self):
        # given
        piece_color = Color.LIGHT_PIECE
        target_color = Color.DARK_PIECE

        piece_position = (0, 2)
        target_position_1 = (1, 1)
        target_position_2 = (3, 1)
        final_position_1 = (2, 0)
        final_position_2 = (4, 2)

        state = State(3, 5)
        state.add(piece_position[0], piece_position[1], Pawn(piece_color))
        state.add(target_position_1[0], target_position_1[1], Pawn(target_color))
        state.add(target_position_2[0], target_position_2[1], Pawn(target_color))

        beat = PawnBeat(state, piece_position, target_position_1)
        beat.next_beats.append(PawnBeat(beat.execute(), final_position_1, target_position_2))
        beats_list = beat.to_list()

        # when
        next_state_1 = beats_list[0][0].execute()
        next_state_2 = beats_list[0][1].execute()

        # then
        self.assertFalse(next_state_1.get_piece(*piece_position))
        self.assertFalse(next_state_1.get_piece(*target_position_1))
        self.assertTrue(next_state_1.get_piece(*final_position_1))
        self.assertFalse(next_state_2.get_piece(*final_position_1))
        self.assertFalse(next_state_2.get_piece(*target_position_2))
        self.assertTrue(next_state_2.get_piece(*final_position_2))

class KingMovesTestCase(unittest.TestCase):
    def test_king_move(self):
        # given
        size = 5
        piece_position = (int(size / 2), int(size / 2))
        target_positions_diagonal_1 = [(x, x) for x in range(size)]
        target_positions_diagonal_2 = [(size - 1 - x, x) for x in range(size)]
        target_positions_vertical = [(x, int(size / 2)) for x in range(size)]
        target_positions_horizontal = [(int(size / 2), x) for x in range(size)]
        target_positions = target_positions_diagonal_1 + target_positions_diagonal_2 + \
                           target_positions_horizontal + target_positions_vertical

        for target_position in filter(lambda t: t != piece_position, target_positions):
            state = State(size, size)
            state.add(piece_position[0], piece_position[1], King(Color.DARK_PIECE))
            move = KingMove(state, piece_position, target_position)

            # when
            next_state = move.execute()

            # then
            self.assertFalse(next_state.get_piece(*piece_position))
            self.assertTrue(next_state.get_piece(*target_position))

    def test_king_beat(self):
        # given
        size = 5
        piece_position = (0, 0)
        target_position = (2, 2)
        final_positions = [(x, x) for x in range(3, size)]

        for final_position in final_positions:
            state = State(size, size)
            state.add(piece_position[0], piece_position[1], King(Color.DARK_PIECE))
            state.add(target_position[0], target_position[1], Pawn(Color.LIGHT_PIECE))
            beat = KingBeat(state, piece_position, target_position, final_position)

            # when
            next_state = beat.execute()

            # then
            self.assertFalse(next_state.get_piece(*piece_position))
            self.assertFalse(next_state.get_piece(*target_position))
            self.assertTrue(next_state.get_piece(*final_position))


if __name__ == '__main__':
    unittest.main()
