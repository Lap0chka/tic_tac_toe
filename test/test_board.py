import unittest
from typing import List

from tic_tac_toe.board import Board


class TestBoard(unittest.TestCase):
    def test_singleton(self) -> None:
        """
        Test that the Board class follows the Singleton pattern.
        """
        board1: Board = Board()
        board2: Board = Board()
        self.assertIs(board1, board2, "Board should follow the Singleton pattern.")

    def test_create_board(self) -> None:
        """
        Test the creation of the game board.
        """
        board: Board = Board(3)
        expected_board: List[List[int]] = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
        self.assertEqual(board.board, expected_board, "Board initialization is incorrect.")

        with self.assertRaises(ValueError):
            Board(4)  # Should raise ValueError for even board size

    def test_get_rows(self) -> None:
        """
        Test that rows are retrieved correctly.
        """
        board: Board = Board(3)
        rows: List[List[int]] = board.get_rows()
        self.assertEqual(rows, [[1, 2, 3], [4, 5, 6], [7, 8, 9]], "Row retrieval is incorrect.")

    def test_get_columns(self) -> None:
        """
        Test that columns are retrieved correctly.
        """
        board: Board = Board(3)
        columns: List[List[int]] = board.get_columns()
        self.assertEqual(
            columns, [[1, 4, 7], [2, 5, 8], [3, 6, 9]], "Column retrieval is incorrect."
        )

    def test_get_diagonals(self) -> None:
        """
        Test that diagonals are retrieved correctly.
        """
        board: Board = Board(3)
        diagonals: List[List[int]] = board.get_diagonals()
        self.assertEqual(diagonals, [[1, 5, 9], [3, 5, 7]], "Diagonal retrieval is incorrect.")

    def test_check_winner(self) -> None:
        """
        Test the winner checking functionality.
        """
        board: Board = Board(3)
        board.board = [["X", "X", "X"], [4, 5, 6], [7, 8, 9]]
        self.assertTrue(board.check_winner("X"), "Winner check is incorrect.")
        self.assertFalse(board.check_winner("O"), "Winner check is incorrect.")

    def test_make_move(self) -> None:
        """
        Test that moves are made correctly and invalid moves raise errors.
        """
        board: Board = Board(3)
        board.make_move(5, "X")
        self.assertEqual(board.board[1][1], "X", "Move was not made correctly.")

        with self.assertRaises(ValueError):
            board.make_move(5, "O")  # Field already occupied

        with self.assertRaises(ValueError):
            board.make_move(10, "X")  # Invalid field

    def test_available_fields(self) -> None:
        """
        Test the calculation of available fields on the board.
        """
        board: Board = Board(3)
        board.make_move(5, "X")
        available: List[int] = board.available_fields()
        self.assertEqual(
            available, [1, 2, 3, 4, 6, 7, 8, 9], "Available fields calculation is incorrect."
        )


if __name__ == "__main__":
    unittest.main()
