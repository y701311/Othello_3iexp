from move.location import Location
from board.disc import Disc


class Board:
    """オセロの盤を表すクラス
    """

    def __init__(self) -> None:
        # 打っているプレイヤーの石の色
        self.player = Disc.black
        self.turn = 1

    def put(self, location: Location) -> None:
        """指定された場所に石を置く

        Args:
            location (Location): 石を置く場所
        """
        pass

    def passPut(self) -> None:
        """パスをする
        """
        pass

    def canPut(self, location: Location) -> bool:
        """指定された場所に石を置けるかどうかを返す

        Args:
            location (Location): 石を置けるか調べる場所

        Returns:
            bool: 石を置けるならtrue、置けないならfalse
        """
        pass

    def getPlaceableLocation(self) -> list[Location]:
        """置ける場所をLocationのlistとして返す

        Returns:
            list[Location]: 置ける場所のリスト
        """
        pass

    def _reverse(self, location: Location) -> None:
        """反転処理

        Args:
            location (Location): 石を置く場所
        """
        pass

    def updateBoardStatus(self) -> None:
        """ボードのパラメータを更新
        """
        pass

    def getWinner(self) -> Disc:
        """石の数がより多い色を返す

        Returns:
            Disc: 石の数がより多い石の色 引き分けならDisc.emptyを返す
        """
        pass

    def getDiscNum(self) -> tuple[int, int]:
        """黒石と白石の数を返す

        Returns:
            tuple[int, int]: 黒石の数、白石の数を要素とするタプル
        """
        pass

    def getLocationDisc(self, location: Location) -> Disc:
        """指定された場所の石の色を返す

        Args:
            location (Location): 石の色を知りたい場所

        Returns:
            Disc: 指定された場所の石の色
        """
        pass

    def gameIsFinished(self) -> bool:
        """ゲームの終了判定

        Returns:
            bool: ゲームが終了したならtrue、そうでないならfalseを返す
        """
        pass
