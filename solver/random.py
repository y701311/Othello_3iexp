import random

from solver.solver import Solver
from board.board import Board
from move.location import Location


class Random(Solver):
    """ランダムに手を選ぶソルバー
    """

    def selectLocation(self, board: Board) -> Location:
        """置く場所を選ぶ

        Args:
            board (Board): 置く場所を考える盤

        Returns:
            Location: 石を置く場所
        """
        placeableLocation = board.getPlaceableLocation()
        if len(placeableLocation) == 0:
            return "pass"
        
        putLocation = random.choice(placeableLocation)
        return putLocation
