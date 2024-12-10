from tictactoe.tictac import GameTicTacToe


def main():
    board_size = 3
    mode = 1  # 2 - human vs human; 1 - computer vs human
    GameTicTacToe(board_size, mode)


if __name__ == "__main__":
    main()
