import numpy as np

from board.board import Board
from move.location import Location
from solver.solver import Solver
from solver.eval_function.eval_function import EvalFunction


class Minimax(Solver):
    """ミニマックス法
    """

    def __init__(self, evalFunction: EvalFunction, depth: int) -> None:
        self.evalFunction = evalFunction
        self.depth = depth

    # 石を置く場所を選択する
    def selectLocation(self, board: Board) -> Location:
        self.player = board.player

        placeableLocation = board.getPlaceableLocation()
        if len(placeableLocation) == 0:
            # 置ける場所が無いならパス
            return "pass"

        evalValue = []
        for loc in placeableLocation:
            board.put(loc)
            board.updateBoardStatus()
            evalValue.append(self.minimax(board, self.depth, -np.inf, np.inf))
            board.undo()
        maxEvalValueIndex = np.argmax(evalValue)

        # 評価値の最も大きい手を選択
        return placeableLocation[maxEvalValueIndex]

    # ミニマックス法
    def minimax(self, board: Board, depth: int, maxEvalValue: float, minEvalValue: float) -> float:
        if board.gameIsFinished() or depth == 0:
            return self.evalFunction.eval(board, self.player)

        placeableLocation = board.getPlaceableLocation()
        if len(placeableLocation) == 0:
            board.passPut()
            board.updateBoardStatus()
            if board.player == self.player:
                maxEvalValue = max(maxEvalValue, self.minimax(board, depth-1, maxEvalValue, minEvalValue))
                board.undo()
                return maxEvalValue
            else:
                minEvalValue = min(minEvalValue, self.minimax(board, depth-1, maxEvalValue, minEvalValue))
                board.undo()
                return minEvalValue

        if board.player == self.player:
            for loc in placeableLocation:
                board.put(loc)
                board.updateBoardStatus()
                maxEvalValue = max(maxEvalValue, self.minimax(board, depth-1, maxEvalValue, minEvalValue))
                board.undo()
            return maxEvalValue
        else:
            for loc in placeableLocation:
                board.put(loc)
                board.updateBoardStatus()
                minEvalValue = min(minEvalValue, self.minimax(board, depth-1, maxEvalValue, minEvalValue))
                board.undo()
            return minEvalValue
