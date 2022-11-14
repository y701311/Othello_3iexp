from board.board import Board
from move.location import Location
from solver.solver import Solver
from solver.eval_function.empty import Empty
from solver.search_algorithm.minimax import Minimax


class Empty_Minimax(Solver):
    """
    空の評価関数でミニマックス探索を行うソルバー
    """

    def __init__(self, depth: int) -> None:
        self.search = Minimax(Empty(), depth=depth)

    def selectLocation(self, board: Board) -> Location:
        """置く場所を選ぶ

        Args:
            board (Board): 置く場所を考える盤

        Returns:
            Location: 石を置く場所
        """
        return self.search.selectLocation(board)
