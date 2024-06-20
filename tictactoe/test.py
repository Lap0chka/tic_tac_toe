import unittest
from tictac import TicTacToe


class TestTicTacToe(unittest.TestCase):

    def setUp(self):
        self.game = TicTacToe(board_size=3)

    def test_create_board(self):
        expected_board = [
            [1, 2, 3],
            [4, 5, 6],
            [7, 8, 9]
        ]
        self.assertEqual(self.game.board, expected_board)

    def test_invalid_board_size(self):
        with self.assertRaises(ValueError):
            TicTacToe(board_size=4)

    def test_game_step(self):
        self.game.game_step(1, 'X')
        self.assertEqual(self.game.board[0][0], 'X')

    def test_check_win(self):
        self.game.board = [
            ['X', 'X', 'X'],
            [4, 5, 6],
            [7, 8, 9]
        ]
        self.assertTrue(self.game.check_lines())

    def test_check_draw(self):
        self.game.board = [
            ['X', 'O', 'X'],
            ['X', 'X', 'O'],
            ['O', 'X', 'O']
        ]
        self.assertFalse(self.game.available_moves())

    def test_next_player(self):
        self.assertEqual(self.game.next_player('X'), 'Y')
        self.assertEqual(self.game.next_player('Y'), 'X')

    def test_find_dangerous_move(self):
        line = ['X', 2, 'X']
        self.assertEqual(self.game.find_dangerous_move(line), 2)

    def test_available_moves(self):
        self.game.board = [
            ['X', 'O', 'X'],
            ['X', 5, 'O'],
            ['O', 'X', 9]
        ]
        self.assertEqual(self.game.available_moves(), [5, 9])


if __name__ == '__main__':
    unittest.main()