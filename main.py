from tictac import GameTicTacToe


def main():
    board_size = 3
    # 2 - human vs human; 1 - computer vs human
    mode = 1
    GameTicTacToe(board_size, mode)


if __name__ == '__main__':
    main()
