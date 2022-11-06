import numpy as np
from copy import deepcopy

from board.board import Board
from move.location import Location
from solver.solver import Solver
from solver.eval_function.eval_function import EvalFunction


class Alphabeta_copy(Solver):
    """アルファベータ法
    """

    def __init__(self, evalFunction: EvalFunction, depth: int) -> None:
        self.evalFunction = evalFunction
        self.depth = depth

    # 石を置く場所を選択する
    def selectLocation(self, board: Board) -> Location:
        self.visited = 0 ##### DEBUG #####
        self.player = board.player

        placeableLocation = board.getPlaceableLocation()
        if len(placeableLocation) == 0:
            # 置ける場所が無いならパス
            return "pass"

        evalValue = []
        for loc in placeableLocation:
            # 1手先の盤面
            oneMoveAheadBoard = deepcopy(board)
            oneMoveAheadBoard.put(loc)
            oneMoveAheadBoard.updateBoardStatus()
            evalValue.append(self.alphabeta(oneMoveAheadBoard, self.depth, -np.inf, np.inf))
        maxEvalValueIndex = np.argmax(evalValue)

        print(f"copy visited: {self.visited}") ##### DEBUG #####
        # 評価値の最も大きい手を選択
        return placeableLocation[maxEvalValueIndex]

    # アルファベータ法
    def alphabeta(self, board: Board, depth: int, alpha: int, beta: int) -> float:
        self.visited += 1 ##### DEBUG #####
        if board.gameIsFinished() or depth == 0:
            return self.evalFunction.eval(board, self.player)

        placeableLocation = board.getPlaceableLocation()
        if len(placeableLocation) == 0:
            board.passPut()
            board.updateBoardStatus()
            if board.player == self.player:
                alpha = max(alpha, self.alphabeta(board, depth-1, alpha, beta))
                return alpha
            else:
                beta = min(beta, self.alphabeta(board, depth-1, alpha, beta))
                return beta

        if board.player == self.player:
            for loc in placeableLocation:
                oneMoveAheadBoard = deepcopy(board)
                oneMoveAheadBoard.put(loc)
                oneMoveAheadBoard.updateBoardStatus()
                alpha = max(alpha, self.alphabeta(oneMoveAheadBoard, depth-1, alpha, beta))
                if alpha >= beta:
                    break  # betaカット
            return alpha
        else:
            for loc in placeableLocation:
                oneMoveAheadBoard = deepcopy(board)
                oneMoveAheadBoard.put(loc)
                oneMoveAheadBoard.updateBoardStatus()
                beta = min(beta, self.alphabeta(oneMoveAheadBoard, depth-1, alpha, beta))
                if alpha >= beta:
                    break  # alphaカット
            return beta
