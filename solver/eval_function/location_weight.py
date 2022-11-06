from board.board import Board
from board.disc import Disc
from move.location import Location
from solver.eval_function.eval_function import EvalFunction


class LocationWeight(EvalFunction):
    """石の位置の重みによって盤面を評価する関数
    """

    def __init__(self) -> None:
        self.weight = [
            [1000,  5, 100,  10,  10, 100,  5, 1000],
            [   5,  1,  15,  20,  20,  15,  1,    5],
            [ 100, 15,  25,  50,  50,  25, 15,  100],
            [  10, 20,  50, 200, 200,  50, 20,   10],
            [  10, 20,  50, 200, 200,  50, 20,   10],
            [ 100, 15,  25,  50,  50,  25, 15,  100],
            [   5,  1,  15,  20,  20,  15,  1,    5],
            [1000,  5, 100,  10,  10, 100,  5, 1000],
        ]

    def eval(self, board: Board, player: Disc) -> float:
        """盤面の評価関数

        Args:
            board (Board): 評価する盤面
            player (Disc): 根ノードのプレイヤー

        Returns:
            float: 盤面の評価値
        """
        evalValue = 0
        loc = Location(0, 0)

        for i in range(1, 9):
            for j in range(1, 9):
                loc.row = i
                loc.column = j
                disc = board.getLocationDisc(loc)
                if disc == Disc.empty:
                    pass
                elif disc == player:
                    evalValue += self.weight[i-1][j-1]
                else:
                    evalValue -= self.weight[i-1][j-1]

        return evalValue
