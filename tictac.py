from random import choice


class TicTacToe:
    """Game TicTacToe"""

    def __init__(self, board_size=3):
        self.board_size = board_size
        self.board = self.create_board(board_size)
        self.step = self.board_size ** 2
        self.current_player = 'X'

    @staticmethod
    def create_board(board_size):
        board = [[cell for cell in range(row, row + board_size)]
                 for row in range(1, board_size ** 2, board_size)]
        return board

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
        """Human or computer step"""
        self.step -= 1
        for row in range(self.board_size):
            for col in range(self.board_size):
                if self.board[row][col] == field:
                    self.board[row][col] = current_player

        self.check_win(current_player)

    def check_win(self, current_player):
        """Check player win or not"""
        won = False
        main_diagonal, additional_diagonal = [], []

        for row in range(self.board_size):

            # check cols
            col_is_win = self.check_win_line(self.board[row])

            # check rows
            line = [self.board[col][row] for col in range(self.board_size)]
            row_is_win = self.check_win_line(line)

            # check line col or row wins
            if row_is_win or col_is_win:
                won = True
                break

            main_diagonal.append(self.board[row][row])
            additional_diagonal.append(self.board[row][self.board_size - 1 - row])

        main_diagonal_is_win = self.check_win_line(main_diagonal)
        additional_diagonal_is_win = self.check_win_line(additional_diagonal)

        if main_diagonal_is_win or additional_diagonal_is_win:
            won = True

        if won:
            print(f'My congratulations. {current_player.upper()} WON !!!')
            self.draw_board()
            self.play_again()

        if self.step == 0:
            print(f"It's draw!")
            return True
        return False

    @staticmethod
    def check_win_line(line):
        """Check line if all elements equal"""
        won = len(set(line)) == 1
        return won

    @staticmethod
    def quit_the_game():
        print('Bye Bye Bye\nSee you latter!!!')
        quit()

    def move(self):
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

    def next_player(self, current_payer: str) -> str:
        if current_payer.lower() == 'x':
            return 'Y'
        return 'X'


class GameSessionTicTacToe(TicTacToe):
    """Class Computer VS Human or Human vs Human"""

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
        available_move = self.available_moves()
        field = choice(available_move)
        return field

    def computer_step(self):
        field = self.best_move()
        self.game_step(field, self.current_player)
        self.current_player = self.next_player(self.current_player)

    def computer_game(self):
        self.computer_step()


class GameTicTacToe(GameSessionTicTacToe):
    def __init__(self, board_size, mode=2):
        super().__init__(board_size)
        self.mode = mode
        self.game()

    def current_game(self):
        if self.mode == 1:
            self.computer_game()
        self.humans_move()

    def game(self):
        while True:
            self.current_game()

    def play_again(self):
        """Start game again or not"""
        play_again = input('Play again? (y-yes): ').lower()
        if play_again == 'y':
            self.__init__(self.board_size, self.mode)
        else:
            self.quit_the_game()
