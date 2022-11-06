from board.board import Board
from move.location import Location
from solver.solver import Solver
from solver.eval_function.location_weight import LocationWeight
from solver.search_algorithm.alphabeta import Alphabeta


class LocationWeight_Alphabeta(Solver):
    """
    石の位置の重みによって盤面を評価する関数を評価関数としたアルファベータ探索を行うソルバー
    """

    def __init__(self, depth: int) -> None:
        self.search = Alphabeta(LocationWeight(), depth=depth)

    def selectLocation(self, board: Board) -> Location:
        """置く場所を選ぶ

        Args:
            board (Board): 置く場所を考える盤

        Returns:
            Location: 石を置く場所
        """
        return self.search.selectLocation(board)
