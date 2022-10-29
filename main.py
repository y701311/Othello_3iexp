from game.game import Game


def main():
    game = Game(firstSolverName="Human", secondSolverName="Human")
    game.play()


if __name__ == "__main__":
    main()
