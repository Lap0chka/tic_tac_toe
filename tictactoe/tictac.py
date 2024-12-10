from random import choice
from typing import List, Optional, Union

from logger import Logger

logger_instance = Logger(__name__, "log_file.log")
logger = logger_instance.get_logger()


class TicTacToe:
    """
    A class to represent the game of Tic Tac Toe.

    This class implements a singleton pattern to ensure only one instance of the game exists.
    """

    __slots__ = ("board_size", "board", "_mode", "current_player", "hide")
    _instance = None

    def __new__(cls, *args, **kwargs):
        """
        Singleton pattern implementation. Ensures only one instance of TicTacToe can be created.
        """
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, board_size: int = 3, mode: int = 2) -> None:
        """
        Initialize the Tic Tac Toe game.

        Args:
            board_size (int): The size of the game board (default is 3).
            mode (int): The game mode, where 1 represents Player vs AI and 2 represents Player vs Player (default is 2).
        """
        self.board: List[List[Optional[int]]] = self.create_board(board_size)
        self.board_size: int = board_size
        self.mode: int = mode
        self.current_player: str = "X"
        self.hide: bool = False

    @property
    def mode(self) -> int:
        """
        Get the current game mode.

        Returns:
            int: The current mode (1 or 2).
        """
        return self._mode

    @mode.setter
    def mode(self, mode: int) -> None:
        """
        Set the game mode.

        Args:
            mode (int): The new game mode (1 for Player vs AI, 2 for Player vs Player).

        Raises:
            ValueError: If the mode is not 1 or 2.
        """
        if mode not in [1, 2]:
            raise ValueError("Mode must be 1 or 2.")
        self._mode = mode

    def draw_board(self) -> None:
        """
        Draw the current state of the game board.

        """
        border = "_" * (self.board_size * 2 + 1)
        print(border)

        for row in range(self.board_size):
            for col in range(self.board_size):
                value = self.board[row][col]
                # Hide cell if hide flag is True and the cell contains an integer
                if self.hide and isinstance(value, int):
                    value = " "
                cell = f'|{value if value is not None else " "}|'
                print(cell, end="")
            print()
        print(border)

    def game_step(self, field: int, current_player: str) -> None:
        """
        Make a move by placing the current player's marker on the board.

        Args:
            field (int): The number of the cell where the player wants to place their marker.
            current_player (str): The marker of the current player ('X' or 'O').

        Raises:
            ValueError: If the specified field is not found on the board.
        """
        for row in range(self.board_size):
            for col in range(self.board_size):
                if self.board[row][col] == field:
                    self.board[row][col] = current_player
                    break

        self.check_win(current_player)

    def check_lines(self, dangerous: bool = False) -> Union[str, bool]:
        """
        Check rows, columns, and diagonals for a winning line or potential danger.

        Args:
            dangerous (bool): If True, check for potential dangerous lines (threats).
                              If False, check for winning lines.

        Returns:
            Union[str, bool]: Returns 'X' or 'O' if there's a winning or dangerous line, otherwise False.
        """
        main_diagonal: List = []
        additional_diagonal: List = []

        # 1 - check for a winning line, 2 - check for dangerous (threat) lines
        check_win_dangerous: int = 2 if dangerous else 1

        for row in range(self.board_size):
            # Check columns
            column = self.board[row]
            col_result = self.check_line(column, check_win_dangerous)
            if col_result:
                return col_result

            # Check rows
            line = [self.board[col][row] for col in range(self.board_size)]
            row_result = self.check_line(line, check_win_dangerous)
            if row_result:
                return row_result

            # Collect diagonals
            main_diagonal.append(self.board[row][row])
            additional_diagonal.append(self.board[row][self.board_size - 1 - row])

        # Check main diagonal
        main_diag_result = self.check_line(main_diagonal, check_win_dangerous)
        if main_diag_result:
            return main_diag_result

        # Check additional diagonal
        add_diag_result = self.check_line(additional_diagonal, check_win_dangerous)
        if add_diag_result:
            return add_diag_result

        return False

    def check_win(self, current_player: str) -> None:
        """
        Check if the current player has won or if the game is a draw.

        Args:
            current_player (str): The marker of the current player ('X' or 'O').
        """
        # Check for a winning condition
        won = self.check_lines()
        # Get the list of available moves
        available_moves = self.available_moves()

        # If there's a win or no available moves (draw), handle the game end
        if won or not available_moves:
            # Redraw the board with the current state
            self.draw_board()

            if won:
                print(f"Congratulations! {current_player.upper()} WON!!!")
                logger.info(f"Player {current_player.upper()} won.")
            else:
                print("It's a draw!")
                logger.info("It's a draw!")

            # Ask if players want to play again
            self.play_again()

    def play_again(self) -> None:
        """
        Ask the player if they want to start a new game or quit.

        If the player chooses 'y', the game is restarted. Otherwise, the game is exited.
        """
        play_again_input = input("Play again? (y-yes): ").strip().lower()
        if play_again_input == "y":
            self.__init__(self.board_size, self.mode)
        else:
            self.quit_the_game()

    def check_line(
        self, line: List[Union[int, str]], check_win_dangerous: int
    ) -> Optional[Union[str, bool]]:
        """
        Check if a line (row, column, or diagonal) meets the winning or dangerous condition.

        Args:
            line (List[Union[int, str]]): The line to be checked.
            check_win_dangerous (int): 1 for checking a win, 2 for checking a dangerous condition.

        Returns:
            Optional[Union[str, bool]]: Returns True if there's a win, the player's marker if a dangerous condition is met,
                                        or None if no condition is met.
        """
        won = len(set(line)) == check_win_dangerous

        if check_win_dangerous != 1 and won:
            return self.find_dangerous_move(line)

        if won:
            return line[0] if isinstance(line[0], str) else True

        return None

    def available_moves(self) -> List[int]:
        """
        Get a list of available moves on the board.

        Returns:
            List[int]: A list of numbers representing available cells on the board.
        """
        all_numbers_board = range(1, (self.board_size**2) + 1)
        available = [
            self.board[row][col]
            for row in range(self.board_size)
            for col in range(self.board_size)
            if self.board[row][col] in all_numbers_board
        ]
        return available

    @staticmethod
    def find_dangerous_move(line: List[Union[int, str]]) -> Optional[int]:
        """
        Find a potentially dangerous move (an empty cell represented by an integer) in the given line.

        Args:
            line (List[Union[int, str]]): A line (row, column, or diagonal) to check.

        Returns:
            Optional[int]: The first integer found in the line (representing an empty cell) or None if no integer is found.
        """
        return next((x for x in line if isinstance(x, int)), None)

    @staticmethod
    def quit_the_game() -> None:
        """
        Quit the game with a farewell message and log the action.
        """
        print("Bye Bye Bye\nSee you later!!!")
        logger.debug("Game exited by user.")
        quit()

    @staticmethod
    def next_player(current_player: str) -> str:
        """
        Switch the current player between 'X' and 'O'.

        Args:
            current_player (str): The current player's marker ('X' or 'O').

        Returns:
            str: The next player's marker.
        """
        if current_player.upper() == "X":
            return "O"
        return "X"

    @staticmethod
    def create_board(board_size: int) -> List[List[int]]:
        """
        Create an initial game board with sequentially numbered cells.

        Args:
            board_size (int): The size of the board (must be an odd number).

        Returns:
            List[List[int]]: A 2D list representing the game board with numbered cells.

        Raises:
            ValueError: If the board size is not an odd number.
        """
        if board_size % 2 == 0:
            raise ValueError("Board size can only be odd numbers (3, 5, 7, 9, ...).")

        board = [
            [cell for cell in range(row, row + board_size)]
            for row in range(1, board_size**2, board_size)
        ]
        return board


class GameTicTacToe(TicTacToe):
    """
    A class representing the Tic Tac Toe game with additional functionalities
    for handling user interactions and game flow.
    """

    def __init__(self, board_size: int, mode: int = 2) -> None:
        """
        Initialize the GameTicTacToe instance.

        Args:
            board_size (int): The size of the game board.
            mode (int): The game mode (default is 2: Player vs Player).
        """
        super().__init__(board_size, mode)
        self.choose_tic_or_toe()
        self.game()

    def move(self) -> int:
        """
        Handle the human player's move input.

        Returns:
            int: The chosen field number for the player's move.

        Raises:
            SystemExit: If the user chooses to quit the game by entering 'q'.
        """
        available_moves = self.available_moves()
        max_number = self.board_size**2

        while True:
            self.draw_board()  # Draw the board with the current state
            try:
                user_input = (
                    input("Choose your field ('q' to quit, 'o' to hide/show numbers): ")
                    .strip()
                    .lower()
                )

                if user_input == "q":
                    self.quit_the_game()  # Quit the game if 'q' is pressed
                elif user_input == "o":
                    self.hide = not self.hide  # Toggle hide/show numbers
                    continue  # Redisplay the board and continue the loop

                field = int(user_input)  # Convert input to integer

                if field in available_moves:
                    logger.info(f"Human chose field {field}")
                    return field  # Return the valid chosen field
                else:
                    print(
                        f"Invalid choice. Please choose from available fields between [1, {max_number}]. Try again."
                    )
            except ValueError:
                print("Invalid input. Please enter a number corresponding to an available field.")
                logger.critical("Invalid input value")

    def humans_move(self) -> None:
        """
        Execute the human player's move in a human vs. human game.

        - Prompts the player to select a field.
        - Updates the board and switches to the next player.
        """
        field = self.move()
        self.game_step(field, self.current_player)
        logger.info(f"Player {self.current_player} moved to field {field}")
        self.current_player = self.next_player(self.current_player)
        logger.info(f"Next move: {self.current_player}")

    def best_move(self) -> int:
        """
        Determine the best move for the computer.

        - First, check for dangerous situations (potential loss).
        - If no danger is detected, find the best available move.

        Returns:
            int: The field number representing the best move for the computer.
        """
        dangerous_num = self.check_danger()
        if dangerous_num:
            logger.info(
                f"Computer detected a dangerous situation and will move to field {dangerous_num}"
            )
            return dangerous_num

        field = self.find_available_best_move()
        logger.info(f"Computer selected the best available move: field {field}")
        return field

    def check_danger(self) -> int:
        """
        Check if there is a dangerous situation for the computer (potential immediate loss).

        Returns:
            int: The field number to block the opponent's winning move.
        """
        dangerous_num = self.check_lines(dangerous=True)
        if dangerous_num:
            logger.info(f"Dangerous move detected: field {dangerous_num}")
        return dangerous_num

    def computer_step(self) -> None:
        """
        Execute the computer's move.

        - Determines the best move and updates the board.
        - Switches to the next player.
        """
        field = self.best_move()
        self.game_step(field, self.current_player)
        logger.info(f"Computer moved to field {field}")
        self.current_player = self.next_player(self.current_player)
        logger.info(f"Next move: {self.current_player}")

    def find_available_best_move(self) -> int:
        """
        Find the best available move for the computer, prioritizing the center and then the corners.

        Returns:
            int: The chosen field number for the best move.
        """
        # Define the best moves in order: center, then corners
        best_moves = [
            self.board[self.board_size // 2][self.board_size // 2],  # Center
            self.board[0][0],  # Top-left corner
            self.board[self.board_size - 1][0],  # Bottom-left corner
            self.board[self.board_size - 1][self.board_size - 1],  # Bottom-right corner
            self.board[0][self.board_size - 1],  # Top-right corner
        ]

        # Get the list of available moves
        available_moves: List[int] = self.available_moves()

        # Check for the best move that is available
        for move in best_moves:
            if move in available_moves:
                logger.info(f"Best available move selected: {move}")
                return move

        # If no best move is available, choose a random available move
        random_move = choice(available_moves)
        logger.info(f"No optimal move found, selecting random move: {random_move}")
        return random_move

    def choose_tic_or_toe(self) -> None:
        """
        Prompt the user to choose their symbol ('X' or 'O') for the Tic Tac Toe game.

        - If the user chooses 'X', they make the first move.
        - If the user chooses 'O', the computer makes the first move.
        """
        while True:
            current_player = input("What symbol do you want to play (x or o): ").strip().lower()

            if current_player not in ["x", "o"]:
                print('You can choose only "x" or "o". Try again.')
                continue

            logger.info(f"User will play as {current_player.upper()}")

            self.current_player = current_player.upper()

            if current_player == "o":
                self.current_player = "X"
                self.computer_step()

            break

    def game(self) -> None:
        """
        Start and manage the main game loop.

        The loop continues until the game ends via a win, draw, or user quitting.
        - If the mode is 1 (Player vs AI), the computer makes its move.
        - Otherwise, it's the human's turn.
        """
        logger.debug("Game started")
        while True:
            self.humans_move()
            self.computer_step()
