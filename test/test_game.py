import unittest

from tic_tac_toe.game import Game


class TestGame(unittest.TestCase):

    def setUp(self) -> None:
        """
        Set up a new game instance before each test.
        """
        self.game: Game = Game(3)

    def test_make_move(self) -> None:
        """
        Test that a move is correctly applied to the board.
        """
        self.game.make_move(1, "X")
        board_index = self.game.board[0]
        self.assertEqual("X", board_index[0], "The move was not applied correctly.")

    def test_switch_player(self) -> None:
        """
        Test that the current player is switched correctly.
        """
        self.game.current_player = "X"
        self.game.switch_player()
        self.assertEqual(self.game.current_player, "O", "Player should switch to 'O'.")
        self.game.switch_player()
        self.assertEqual(self.game.current_player, "X", "Player should switch to 'X'.")

    def test_play_game_wins(self) -> None:
        """
        Simulate a winning game and verify the winner.
        """
        self.game.make_move(1, "X")
        self.game.make_move(2, "X")
        self.game.make_move(3, "X")  # Player X wins
        self.assertTrue(self.game.check_winner("X"), "Player X should win the game.")
        self.assertFalse(self.game.check_winner("O"), "Player O should not win.")

    def test_draw_game(self) -> None:
        """
        Simulate a draw game and verify the board state.
        """
        moves = [
            (1, "X"),
            (2, "O"),
            (3, "X"),
            (4, "X"),
            (5, "O"),
            (6, "X"),
            (7, "O"),
            (8, "X"),
            (9, "O"),
        ]
        for field, symbol in moves:
            self.game.make_move(field, symbol)

        self.assertFalse(self.game.check_winner("X"), "There should be no winner in a draw.")
        self.assertFalse(self.game.check_winner("O"), "There should be no winner in a draw.")
        self.assertEqual(
            len(self.game.available_fields()), 0, "No fields should be available in a draw."
        )


if __name__ == "__main__":
    unittest.main()
