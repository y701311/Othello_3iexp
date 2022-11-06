import numpy as np

from solver.solver import Solver
from board.board import Board
from move.location import Location


class OpponentMoveMinimizer(Solver):
    """1手先の相手の選べる手の数が最小となるように選ぶソルバー
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
        
        moveNums = []
        for loc in placeableLocation:
            board.put(loc)
            board.updateBoardStatus()
            moveNums.append(len(board.getPlaceableLocation()))
            board.undo()
        
        putLocation = placeableLocation[np.argmin(moveNums)]
        return putLocation
