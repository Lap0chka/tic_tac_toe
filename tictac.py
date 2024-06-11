from random import choice


class TicTacToe:
    """Game TicTacToe"""

    def __init__(self, board_size=3, mode=2):
        self.board_size = board_size
        self.mode = mode
        self.board = self.create_board(board_size)
        self.step = self.board_size ** 2
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
        self.step -= 1
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
                return True

            # check rows
            line = [self.board[col][row] for col in range(self.board_size)]
            row_is_win = self.check_line(line, check_win_dangerous)

            # check line col or row wins
            if row_is_win:
                return True

            main_diagonal.append(self.board[row][row])
            additional_diagonal.append(self.board[row][self.board_size - 1 - row])

        main_diagonal_is_win = self.check_line(main_diagonal, check_win_dangerous)
        if main_diagonal_is_win:
            return True

        additional_diagonal_is_win = self.check_line(additional_diagonal, check_win_dangerous)
        if additional_diagonal_is_win:
            return True

        return False

    def check_win(self, current_player: str):
        """Check human or CP win or not"""
        won = self.check_lines()

        if won or self.step == 0:
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

    @staticmethod
    def check_line(line: list[int], check_win_dangerous: int) -> bool:
        won = len(set(line)) == check_win_dangerous
        return won

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
        board = [[cell for cell in range(row, row + board_size)]
                 for row in range(1, board_size ** 2, board_size)]
        return board


class GameSessionTicTacToe(TicTacToe):
    """Class Computer VS Human or Human vs Human"""

    def move(self) -> int:
        """Human input"""
        max_number = self.board_size ** 2
        while True:
            self.draw_board()
            try:
                field = input('Choose your field (q latter to quit): ')
                if field.lower() == 'q':
                    self.quit_the_game()
                field = int(field)
                if field > max_number or field < 1:
                    print(f'You can choose only number between [1, {max_number}]\nTry again')
                return field
            except ValueError:
                print(f'You can choose only number\nTry again')

    def humans_move(self):
        """Here function for human vs human"""
        field = self.move()
        self.game_step(field, self.current_player)
        self.current_player = self.next_player(self.current_player)

    def available_moves(self) -> list:
        """Search available field for move"""
        all_numbers_board = range(1, self.board_size ** 2)
        available = [self.board[row][col] for row in range(self.board_size)
                     for col in range(self.board_size)
                     if self.board[row][col] in all_numbers_board
                     ]
        return available

    def best_move(self):
        """Search best move for Computer"""
        available_move = self.available_moves()
        field = choice(available_move)
        return field

    def check_danger(self):
        res = self.check_lines(dangerous=True)
        print(res)

    def computer_step(self):
        """Computer step"""
        field = self.best_move()
        self.game_step(field, self.current_player)
        self.current_player = self.next_player(self.current_player)
        self.check_danger()

    def computer_game(self):
        """Computer actions"""
        self.computer_step()


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
