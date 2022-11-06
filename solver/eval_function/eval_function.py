from board.board import Board
from board.disc import Disc


class EvalFunction:
    """盤面を評価する関数の抽象クラス
    """

    def eval(self, board: Board, player: Disc) -> float:
        """盤面の評価関数

        Args:
            board (Board): 評価する盤面
            player (Disc): 根ノードのプレイヤー

        Returns:
            float: 盤面の評価値
        """
        pass
