from random import choice
from logger import Logger

logger_instance = Logger(__name__, 'log_file.log')
logger = logger_instance.get_logger()


class TicTacToe:
    """Game TicTacToe """

    def __init__(self, board_size=3, mode=2):
        self.board = self.create_board(board_size)
        self.board_size = board_size
        self.mode = mode
        self.current_player = 'X'
        self.hide = False

    def draw_board(self, hide=False):
        """Drawing board"""
        print(('_' * self.board_size) * self.board_size, )
        for row in range(self.board_size):
            for cell in range(self.board_size):
                value = self.board[row][cell]
                if hide and type(self.board[row][cell]) == int:
                    value = ' '
                cell = f'|{value}|'
                print(cell.center(self.board_size), end="")
            print()
        print(('_' * self.board_size) * self.board_size, )

    def game_step(self, field: int, current_player: str):
        """Human or computer step (Put value in board)"""
        for row in range(self.board_size):
            for col in range(self.board_size):
                if self.board[row][col] == field:
                    self.board[row][col] = current_player
        self.check_win(current_player)

    def check_lines(self, dangerous=False):
        """Function checks rows cols and diagonals"""

        main_diagonal, additional_diagonal = [], []

        check_win_dangerous = 1  # 1 - check win line 2 - check dangerous
        if dangerous:
            check_win_dangerous = 2

        for row in range(self.board_size):

            # check cols
            col_is_win = self.check_line(self.board[row], check_win_dangerous)
            if col_is_win:
                return col_is_win

            # check rows
            line = [self.board[col][row] for col in range(self.board_size)]
            row_is_win = self.check_line(line, check_win_dangerous)

            # check line col or row wins
            if row_is_win:
                return row_is_win

            main_diagonal.append(self.board[row][row])
            additional_diagonal.append(self.board[row][self.board_size - 1 - row])

        main_diagonal_is_win = self.check_line(main_diagonal, check_win_dangerous)
        if main_diagonal_is_win:
            return main_diagonal_is_win

        additional_diagonal_is_win = self.check_line(additional_diagonal, check_win_dangerous)
        if additional_diagonal_is_win:
            return additional_diagonal_is_win

        return False

    def check_win(self, current_player: str):
        """Check if the current player (human or CP) has won or if the game is a draw."""
        # Check if there's a winning condition
        won = self.check_lines()
        # Get the list of available moves
        available_moves = self.available_moves()

        if won or not available_moves:
            # Redraw the board with the current state
            self.draw_board(self.hide)

            if won:
                print(f'My congratulations. {current_player.upper()} WON!!!')
                logger.info(f'Player {current_player.upper()} won')
            else:
                print("It's a draw!")
                logger.info("It's a draw!")

            # Ask if players want to play again
            self.play_again()

    def play_again(self):
        """Start game again or not"""
        play_again = input('Play again? (y-yes): ').lower()
        if play_again == 'y':
            self.__init__(self.board_size, self.mode)
        else:
            self.quit_the_game()

    def check_line(self, line: list[int], check_win_dangerous: int) -> int | None | bool:
        won = len(set(line)) == check_win_dangerous
        if check_win_dangerous != 1 and won:
            return self.find_dangerous_move(line)
        return won

    def available_moves(self) -> list:
        """Search available field for move"""
        all_numbers_board = range(1, (self.board_size ** 2) + 1)
        available = [self.board[row][col] for row in range(self.board_size)
                     for col in range(self.board_size)
                     if self.board[row][col] in all_numbers_board
                     ]
        return available

    @staticmethod
    def find_dangerous_move(line):
        num = next((x for x in line if isinstance(x, int)), None)
        return num

    @staticmethod
    def quit_the_game():
        """QUIT"""
        print('Bye Bye Bye\nSee you latter!!!')
        logger.debug('Bye Bye')
        quit()

    @staticmethod
    def next_player(current_payer: str) -> str:
        """Function change TicTac"""
        if current_payer.lower() == 'x':
            return 'Y'
        return 'X'

    @staticmethod
    def create_board(board_size: int) -> list[list]:
        """CREATE BOARD"""
        if board_size % 2 == 0:
            raise ValueError('Board size can be only odd numbers (3, 5, 7, 9...)')
        board = [[cell for cell in range(row, row + board_size)]
                 for row in range(1, board_size ** 2, board_size)]
        return board


class GameSessionTicTacToe(TicTacToe):
    """Class Computer VS Human or Human vs Human"""

    def choose_tic_or_toe(self):
        """Prompt the user to choose their symbol (X or O) for the tic-tac-toe game."""
        while True:
            current_player = input("What tic tac do you want to play (x or o): ").strip().lower()

            if current_player not in ['x', 'o']:
                print('You can choose only x or o')
                continue

            logger.info(f'User will play {current_player.upper()}')

            if current_player == 'o':
                break

            self.humans_move()
            break

    def move(self) -> int:
        """Handles human player's move input."""
        available_moves = self.available_moves()
        max_number = self.board_size ** 2

        while True:
            self.draw_board(self.hide)  # Draw the board with or without hidden numbers
            try:
                choice = input("Choose your field ('q' to quit, 'o' to hide/show numbers): ").strip().lower()

                if choice == 'q':
                    self.quit_the_game()  # Quit the game if 'q' is pressed
                elif choice == 'o':
                    self.hide = not self.hide  # Toggle hide/show numbers
                    continue  # Redisplay the board and continue loop

                field = int(choice)  # Convert input to integer
                if field in available_moves:
                    logger.info(f'Human chose field {field}')
                    return field  # Return the valid chosen field
                else:
                    print(f'You can choose only from available fields between [1, {max_number}]. Try again.')
            except ValueError:
                print('You can choose only numbers. Try again.')
                logger.critical("Invalid input value")

    def humans_move(self):
        """Here function for human vs human"""
        field = self.move()
        self.game_step(field, self.current_player)
        logger.info(f'Moved player {self.current_player}')
        self.current_player = self.next_player(self.current_player)
        logger.info(f'Next move - {self.current_player}')

    def best_move(self) -> int:
        """Search best move for Computer"""
        dangerous_num = self.check_danger()
        if dangerous_num:
            return dangerous_num
        field = self.find_available_best_move()
        return field

    def check_danger(self) -> int:
        dangerous_num = self.check_lines(dangerous=True)
        return dangerous_num

    def computer_step(self):
        """Computer step"""
        field = self.best_move()
        logger.info(f'Computer moved field {field}')
        self.game_step(field, self.current_player)
        self.current_player = self.next_player(self.current_player)

    def find_available_best_move(self) -> int:
        """Find the best available move starting from the center and then corners."""
        # Define the best moves in order: center, then corners
        best_moves = [
            self.board[self.board_size // 2][self.board_size // 2],  # Center
            self.board[0][0],  # Top-left corner
            self.board[self.board_size - 1][0],  # Bottom-left corner
            self.board[self.board_size - 1][self.board_size - 1],  # Bottom-right corner
            self.board[0][self.board_size - 1],  # Top-right corner
        ]

        # Get the list of available moves
        available_moves = self.available_moves()

        # Check for the best move that is available
        for move in best_moves:
            if move in available_moves:
                return move

        # If no best move is available, choose a random available move
        return choice(available_moves)


class GameTicTacToe(GameSessionTicTacToe):
    def __init__(self, board_size, mode=2):
        super().__init__(board_size, mode)
        self.choose_tic_or_toe()
        self.game()

    def current_game(self):
        """Choose mode"""
        if self.mode == 1:
            self.computer_step()
        self.humans_move()

    def game(self):
        logger.debug("Start Game")

        while True:
            self.current_game()
