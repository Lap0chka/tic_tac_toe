import unittest
from typing import List

from tic_tac_toe.ai import TicTacToeAI
from tic_tac_toe.board import Board


class TestTicTacToeAI(unittest.TestCase):
    def setUp(self) -> None:
        """
        Set up the board and AI instance for testing.
        """
        self.board: Board = Board(3)
        self.ai: TicTacToeAI = TicTacToeAI("X")

    def test_ai_blocks_opponent_win(self) -> None:
        """
        Test that the AI blocks the opponent's winning move.
        """
        self.board.make_move(1, "O")
        self.board.make_move(2, "O")
        move: int = self.ai.ai_move(self.board)
        self.assertEqual(move, 3, "AI should block opponent's win on field 3.")

    def test_ai_chooses_center(self) -> None:
        """
        Test that the AI chooses the center field if available.
        """
        move: int = self.ai.ai_move(self.board)
        self.assertEqual(move, 5, "AI should choose center field if available.")

    def test_ai_chooses_corner(self) -> None:
        """
        Test that the AI prefers corners if the center is occupied.
        """
        self.board.make_move(5, "X")  # Occupy center
        move: int = self.ai.ai_move(self.board)
        self.assertIn(move, [1, 3, 7, 9], "AI should choose a corner if center is occupied.")

    def test_ai_random_move(self) -> None:
        """
        Test that the AI makes the only available move if one field remains.
        """
        moves: List[int] = [1, 2, 3, 4, 5, 6, 7, 8]
        symbols: List[str] = ["X", "O"] * 4
        for move, symbol in zip(moves, symbols):
            self.board.make_move(move, symbol)

        get_move: int = self.ai.ai_move(self.board)
        self.assertEqual(get_move, 9, "AI should choose the only remaining field.")

    def test_ai_win_if_possible(self) -> None:
        """
        Test that the AI makes a winning move if possible.
        """
        self.board.make_move(1, "X")
        self.board.make_move(2, "X")
        move: int = self.ai.ai_move(self.board)
        self.assertEqual(move, 3, "AI should win by placing on field 3.")

    def test_ai_blocks_diagonal_win(self) -> None:
        """
        Test that the AI blocks a diagonal winning move by the opponent.
        """
        self.board.make_move(1, "O")
        self.board.make_move(5, "O")
        move: int = self.ai.ai_move(self.board)
        self.assertEqual(move, 9, "AI should block opponent's diagonal win by placing on field 9.")

    def test_ai_blocks_opponent_in_columns(self) -> None:
        """
        Test that the AI blocks a winning move in a column by the opponent.
        """
        self.board.make_move(1, "O")
        self.board.make_move(4, "O")
        move: int = self.ai.ai_move(self.board)
        self.assertEqual(move, 7, "AI should block opponent's column win by placing on field 7.")


if __name__ == "__main__":
    unittest.main()
