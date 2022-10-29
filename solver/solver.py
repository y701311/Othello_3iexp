from board.board import Board
from move.location import Location


class Solver:
    """ソルバーの抽象クラス
    """

    def selectLocation(self, board: Board) -> Location:
        """置く場所を選ぶ

        Args:
            board (Board): 置く場所を考える盤

        Returns:
            Location: 石を置く場所
        """
        pass
