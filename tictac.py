class TicTacToe:
    """Game TicTacToe"""
    def __init__(self, board_size=3):
        self.board_size = board_size
        self.board = [[cell for cell in range(row, row + board_size)]
                      for row in range(1, board_size ** 2, board_size)]
        self.game()

    def draw_board(self):
        """Drawing board"""
        print(('_' * self.board_size) * self.board_size, )
        for row in range(self.board_size):
            for cell in range(self.board_size):
                cell = f'|{self.board[row][cell]}|'
                print(cell.center(self.board_size), end="")
            print()
        print(('_' * self.board_size) * self.board_size, )

    def game_step(self, field, current_player):
        """Player step"""
        x_or_y = ['Y', 'X'][current_player]
        for row in range(self.board_size):
            for col in range(self.board_size):
                if self.board[row][col] == field:
                    self.board[row][col] = x_or_y
        return current_player % 2 == 0

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
            x_or_y = ['Y', 'X'][current_player % 2 == 0]
            self.draw_board()
            print(f'My congratulations. {x_or_y} WON !!!')
            return True
        return False

    @staticmethod
    def check_win_line(line):
        """Check line if all elements equal"""
        won = len(set(line)) == 1
        return won

    @staticmethod
    def play_again():
        """Start game again or not"""
        play_again = input('Play again? (y-yes): ').lower()
        if play_again == 'y':
            return True
        else:
            print('Bye Bye Bye. See you later!')
            return False

    def game(self):
        """Start game"""
        current_player = True
        while True:
            self.draw_board()
            field = int(input('Choose your field (q latter to quit): '))
            current_player = self.game_step(field, current_player)
            if self.check_win(current_player):
                if self.play_again():
                    self.__init__()
                else:
                    break