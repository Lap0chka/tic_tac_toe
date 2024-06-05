from tictac import GameTicTacToe, ComputerVSHumanTicTacToe


def main():
    # board_size = 3
    # mode = 2  # 2 - human vs human; 1 - computer vs human
    # game = GameTicTacToe(3, 2)
    res = ComputerVSHumanTicTacToe()
    res.computer_step()

if __name__ == '__main__':
    main()
