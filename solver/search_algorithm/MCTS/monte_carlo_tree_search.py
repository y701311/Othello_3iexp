import numpy as np
from copy import deepcopy

from board.board import Board
from move.location import Location
from solver.solver import Solver
from solver.search_algorithm.MCTS.node import Node


class MonteCarloTreeSearch(Solver):
    """モンテカルロ木探索
    """

    def __init__(self, samplingNum: int = 50, expandBase: int = 5, selectChildNodeAlgorithm: str = "UTC") -> None:
        self.samplingNum = samplingNum
        self.expandBase = expandBase
        self.selectChildNodeAlgorithm = selectChildNodeAlgorithm

    def selectLocation(self, board: Board) -> Location:
        """石を置く場所を選択する

        Args:
            board (Board): 置くことを考える盤面

        Returns:
            Location: 石を置く場所
        """
        placeableLocation = board.getPlaceableLocation()
        if len(placeableLocation) == 0:
            # 置ける場所が無いならパス
            return "pass"

        return self.monteCarloTreeSearch(board)

    def monteCarloTreeSearch(self, board: Board) -> Location:
        """モンテカルロ木探索

        Args:
            board (Board): 探索する盤面

        Returns:
            Location: 探索結果
        """
        root = Node(deepcopy(board), None, None)

        for _ in range(self.samplingNum):
            node = root

            # Selection
            while len(node.untriedLocations) == 0 and len(node.childNodes) != 0:
                node = node.selectChildNode(self.selectChildNodeAlgorithm)

            # Expansion
            if (len(node.untriedLocations) != 0 and node.visitNum == self.expandBase) or (node == root):
                node = node.expandChild()

            # Simulation
            winner = node.playout()

            # Backpropagation
            node.backpropagation(winner)

        # 相手番の試行回数が最小の手を選ぶ
        visitNums = []
        for child in root.childNodes:
            visitNums.append(child.visitNum)
        index = np.argmin(visitNums)
        return root.childNodes[index].location
