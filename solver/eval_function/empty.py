from board.board import Board
from board.disc import Disc
from solver.eval_function.eval_function import EvalFunction


class Empty(EvalFunction):
    """石の位置の重みによって盤面を評価する関数
    """

    def __init__(self) -> None:
        pass

    def eval(self, board: Board, player: Disc) -> float:
        """盤面の評価関数

        Args:
            board (Board): 評価する盤面
            player (Disc): 根ノードのプレイヤー

        Returns:
            float: 盤面の評価値
        """
        return 0
