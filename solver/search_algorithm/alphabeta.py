import numpy as np

from board.board import Board
from move.location import Location
from solver.solver import Solver
from solver.eval_function.eval_function import EvalFunction


class Alphabeta(Solver):
    """アルファベータ法
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
            evalValue.append(self.alphabeta(board, self.depth, -np.inf, np.inf))
            board.undo()
        maxEvalValueIndex = np.argmax(evalValue)

        # 評価値の最も大きい手を選択
        return placeableLocation[maxEvalValueIndex]

    # アルファベータ法
    def alphabeta(self, board: Board, depth: int, alpha: int, beta: int) -> float:
        if board.gameIsFinished() or depth == 0:
            return self.evalFunction.eval(board, self.player)

        placeableLocation = board.getPlaceableLocation()
        if len(placeableLocation) == 0:
            board.passPut()
            board.updateBoardStatus()
            if board.player == self.player:
                alpha = max(alpha, self.alphabeta(board, depth-1, alpha, beta))
                board.undo()
                return alpha
            else:
                beta = min(beta, self.alphabeta(board, depth-1, alpha, beta))
                board.undo()
                return beta

        if board.player == self.player:
            for loc in placeableLocation:
                board.put(loc)
                board.updateBoardStatus()
                alpha = max(alpha, self.alphabeta(
                    board, depth-1, alpha, beta))
                board.undo()
                if alpha >= beta:
                    break  # betaカット
            return alpha
        else:
            for loc in placeableLocation:
                board.put(loc)
                board.updateBoardStatus()
                beta = min(beta, self.alphabeta(board, depth-1, alpha, beta))
                board.undo()
                if alpha >= beta:
                    break  # alphaカット
            return beta
