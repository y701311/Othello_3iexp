from solver.solver import Solver
from board.board import Board
from move.location import Location
from game_io.user_interface import UserInterface


class Human(Solver):
    """人間が手を選ぶソルバー
    """

    def __init__(self, ui: UserInterface) -> None:
        self.ui = ui

    def selectLocation(self, board: Board) -> Location:
        """置く場所を選ぶ

        Args:
            board (Board): 置く場所を考える盤

        Returns:
            Location: 石を置く場所
        """
        putLocation = self.ui.selectLocation(board)
        return putLocation
