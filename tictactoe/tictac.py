from random import choice


class TicTacToe:
    """Game TicTacToe """

    def __init__(self, board_size=3, mode=2):
        self.board = self.create_board(board_size)
        self.board_size = board_size
        self.mode = mode
        self.current_player = 'X'

    def draw_board(self):
        """Drawing board"""
        print(('_' * self.board_size) * self.board_size, )
        for row in range(self.board_size):
            for cell in range(self.board_size):
                cell = f'|{self.board[row][cell]}|'
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
        """Check human or CP win or not"""
        won = self.check_lines()
        available_move = self.available_moves()

        if won or not available_move:
            self.draw_board()
            if won:
                print(f'My congratulations. {current_player.upper()} WON !!!')
            else:
                print(f"It's draw!")
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

    def move(self) -> int:
        """Human input"""
        available_move = self.available_moves()
        max_number = self.board_size ** 2
        while True:
            self.draw_board()
            try:
                field = input('Choose your field (q latter to quit): ')
                if field.lower() == 'q':
                    self.quit_the_game()
                field = int(field)
                if field in available_move:
                    return field
                print(f'You can choose only available between [1, {max_number}]\nTry again')
            except ValueError:
                print(f'You can choose only number\nTry again')

    def humans_move(self):
        """Here function for human vs human"""
        field = self.move()
        self.game_step(field, self.current_player)
        self.current_player = self.next_player(self.current_player)

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
        self.game_step(field, self.current_player)
        self.current_player = self.next_player(self.current_player)

    def computer_game(self):
        """Computer actions"""
        self.computer_step()

    def find_available_best_move(self) -> int:
        """Check all best move if they available"""
        best_move = [
            self.board[self.board_size // 2][self.board_size // 2],
            self.board[0][0],
            self.board[self.board_size - 1][0],
            self.board[self.board_size - 1][self.board_size - 1],
            self.board[0][self.board_size - 1],
        ]

        available_move = self.available_moves()
        for move in best_move:
            if move in available_move:
                return move
        field = choice(available_move)
        return field


class GameTicTacToe(GameSessionTicTacToe):
    def __init__(self, board_size, mode=2):
        super().__init__(board_size, mode)
        self.game()

    def current_game(self):
        """Choose mode"""
        if self.mode == 1:
            self.computer_game()
        self.humans_move()

    def game(self):
        while True:
            self.current_game()
