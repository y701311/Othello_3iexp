import numpy as np
from copy import deepcopy

from board.board import Board
from board.disc import Disc
from move.location import Location


class Node:
    """モンテカルロ木探索のためのノードを表すクラス
    """

    def __init__(self, board: Board, parentNode: "Node", location: Location) -> None:
        self.board = board
        self.parentNode = parentNode
        self.location = location

        self.win = 0
        self.visitNum = 0
        self.childNodes = []
        self.untriedLocations = board.getPlaceableLocation()

    def expandChild(self) -> "Node":
        """子ノードを展開する

        Returns:
            Node: 展開した子ノード
        """
        board = deepcopy(self.board)
        if len(self.untriedLocations) != 0:
            loc = self.untriedLocations.pop(
                np.random.randint(len(self.untriedLocations)))
            board.put(loc)
            board.updateBoardStatus()
            child = Node(board, self, loc)
        else:
            board.passPut()
            board.updateBoardStatus()
            child = Node(board, self, "pass")

        self.childNodes.append(child)
        return child

    def playout(self) -> Disc:
        """ゲーム終了までランダムに石を置き、勝った石の色を返す

        Returns:
            Disc: プレイアウトで勝った石の色
        """
        board = deepcopy(self.board)

        while not board.gameIsFinished():
            placeableLocation = board.getPlaceableLocation()
            if len(placeableLocation) != 0:
                loc = placeableLocation[np.random.randint(
                    len(placeableLocation))]
                board.put(loc)
            else:
                board.passPut()
            board.updateBoardStatus()

        return board.getWinner()

    def backpropagation(self, winner: Disc) -> None:
        """プレイアウトの結果を木の根まで伝播させる

        Args:
            winner (Disc): _description_
        """
        node = self
        while node is not None:
            node.visitNum += 1
            if winner == node.board.player:
                node.win += 1
            elif winner == Disc.empty:
                node.win += 0.5

            node = node.parentNode

    def selectChildNode(self, selectChildNodeAlgorithm: str) -> "Node":
        """子ノードを選択する

        Args:
            selectChildNodeAlgorithm (str): 子ノードを選択するアルゴリズム

        Returns:
            Node: 選択した子ノード
        """
        if selectChildNodeAlgorithm == "UTC":
            return self.selectChildNodeByUct()

    def selectChildNodeByUct(self) -> "Node":
        """UCB1に基づいて子ノードを選択する

        Returns:
            Node: 選択された子ノード
        """
        selectionPriority = []
        for child in self.childNodes:
            selectionPriority.append(self._calculatePriority(child))

        index = np.argmax(selectionPriority)
        return self.childNodes[index]

    def _calculatePriority(self, node: "Node") -> float:
        """UCB1に基づいたノードの探索優先度を返す

        Args:
            node (Node): 探索優先度を計算するノード

        Returns:
            float: 探索優先度
        """
        c = np.sqrt(2)
        value = node.win / node.visitNum + c * \
            np.sqrt(np.log(self.visitNum) / node.visitNum)
        return value
