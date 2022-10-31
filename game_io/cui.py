import os

from board.disc import Disc
from board.board import Board
from move.location import Location


class CUI:
    """コンソール用のUI
    """

    def display(self, board: Board) -> None:
        """ゲームの状況を表示する

        Args:
            board (Board): 状況を表示する盤
        """
        self._displayBoard(board)
        print(f"turn : {board.turn}")
        if board.player == Disc.black:
            print("black`s turn")
        elif board.player == Disc.white:
            print("white`s turn")

    def _displayBoard(self, board: Board) -> None:
        """盤の状況を表示する

        Args:
            board (Board): 状況を表示する盤
        """
        os.system("cls")

        print(" ", end="")
        for i in range(1, 9):
            print(i, end="")
        print()
        for i in range(1, 9):
            print(i, end="")
            for j in range(1, 9):
                location = Location(i, j)
                disc = board.getLocationDisc(location)
                if disc == Disc.black:
                    print("b", end="")
                elif disc == Disc.white:
                    print("w", end="")
                else:
                    print(" ", end="")
            print()
        print()

    def displayResult(self, board: Board) -> None:
        """ゲームの結果を表示する

        Args:
            board (Board): 結果を表示する盤
        """
        self.display(board)
        winner = board.getWinner()
        blackDiscNum, whiteDiscNum = board.getDiscNum()

        print(f"black : {blackDiscNum}  white : {whiteDiscNum}")
        if winner == Disc.black:
            print("winner : black")
        elif winner == Disc.white:
            print("winner : white")
        else:
            print("draw")

    def selectLocation(self, board: Board) -> Location:
        """プレイヤーによる石を置く場所の選択

        Args:
            board (Board): 石を置くことを考える盤
        """
        print("Please enter row and column. For example, 53 means row=5, column=3.")
        print("If you will pass, input \"pass\".")
        print("If you want to return to the previous board, input \"undo\".")

        location = Location(-1, -1)
        while (not location.checkRange()) or (not board.canPut(location)):
            inputStr = input()
            if inputStr == "pass":
                return "pass"
            elif inputStr == "undo":
                return "undo"
            else:
                try:
                    locationInput = int(inputStr)
                    location.row = (locationInput // 10) % 10
                    location.column = locationInput % 10
                    if (not location.checkRange()) or (not board.canPut(location)):
                        print("Invalid input. Please retry.")
                except ValueError:
                    print("Invalid input. Please retry.")

        return location
