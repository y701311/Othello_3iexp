from board.board import Board
from move.location import Location
from board.disc import Disc


class BitBoard(Board):
    """BoardクラスのBitBoardとしての実装
    """

    def __init__(self) -> None:
        # 打っているプレイヤーの色
        self.player = Disc.black
        self.turn = 1
        self.playerBoard = 0x0000000810000000
        self.opponentBoard = 0x0000001008000000

    def _locationToBits(self, location: Location) -> int:
        """指定された場所のみビットが立っているボードに変換

        Args:
            location (Location): 指定する場所

        Returns:
            int: 指定された場所のみビットが立っているボード
        """
        bits = 1
        shift = 63 - (8*(location.row - 1) + (location.column - 1))
        return bits << shift

    def put(self, location: Location) -> None:
        """指定された場所に置く

        Args:
            location (Location): 石を置く場所
        """
        if self.canPut(location):
            self._reverse(location)

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
        if location.checkRange():
            putBoard = self._locationToBits(location)
            legalBoard = self._makeLegalBoard()
            # 指定された場所が合法手に含まれているか
            return (putBoard & legalBoard) == putBoard
        else:
            return False

    def _makeLegalBoard(self) -> int:
        """合法手のビットのみが立っているボードを生成

        Returns:
            int: 合法手のビットのみが立っているボード
        """
        legalBoard = 0
        # 空きマスのみにビットが立っているボード
        blankBoard = ~(self.playerBoard | self.opponentBoard)
        # 左右の端を除く相手ボード
        horizontalMaskedOpponentBoard = self.opponentBoard & 0x7e7e7e7e7e7e7e7e
        # 上下の端を除く相手ボード
        verticalMaskedOpponentBoard = self.opponentBoard & 0x00ffffffffffff00
        # 上下左右の端を除く相手ボード
        allSideMaskedOpponentBoard = self.opponentBoard & 0x007e7e7e7e7e7e00
        # 相手の石がある場所を保存する
        opponentDiscs = 0

        # 8方向をチェック
        # 1度に返せる石は6つまで
        # 左
        opponentDiscs = horizontalMaskedOpponentBoard & (self.playerBoard << 1)
        opponentDiscs |= horizontalMaskedOpponentBoard & (opponentDiscs << 1)
        opponentDiscs |= horizontalMaskedOpponentBoard & (opponentDiscs << 1)
        opponentDiscs |= horizontalMaskedOpponentBoard & (opponentDiscs << 1)
        opponentDiscs |= horizontalMaskedOpponentBoard & (opponentDiscs << 1)
        opponentDiscs |= horizontalMaskedOpponentBoard & (opponentDiscs << 1)
        legalBoard |= blankBoard & (opponentDiscs << 1)

        # 右
        opponentDiscs = horizontalMaskedOpponentBoard & (self.playerBoard >> 1)
        opponentDiscs |= horizontalMaskedOpponentBoard & (opponentDiscs >> 1)
        opponentDiscs |= horizontalMaskedOpponentBoard & (opponentDiscs >> 1)
        opponentDiscs |= horizontalMaskedOpponentBoard & (opponentDiscs >> 1)
        opponentDiscs |= horizontalMaskedOpponentBoard & (opponentDiscs >> 1)
        opponentDiscs |= horizontalMaskedOpponentBoard & (opponentDiscs >> 1)
        legalBoard |= blankBoard & (opponentDiscs >> 1)

        # 上
        opponentDiscs = verticalMaskedOpponentBoard & (self.playerBoard << 8)
        opponentDiscs |= verticalMaskedOpponentBoard & (opponentDiscs << 8)
        opponentDiscs |= verticalMaskedOpponentBoard & (opponentDiscs << 8)
        opponentDiscs |= verticalMaskedOpponentBoard & (opponentDiscs << 8)
        opponentDiscs |= verticalMaskedOpponentBoard & (opponentDiscs << 8)
        opponentDiscs |= verticalMaskedOpponentBoard & (opponentDiscs << 8)
        legalBoard |= blankBoard & (opponentDiscs << 8)

        # 下
        opponentDiscs = verticalMaskedOpponentBoard & (self.playerBoard >> 8)
        opponentDiscs |= verticalMaskedOpponentBoard & (opponentDiscs >> 8)
        opponentDiscs |= verticalMaskedOpponentBoard & (opponentDiscs >> 8)
        opponentDiscs |= verticalMaskedOpponentBoard & (opponentDiscs >> 8)
        opponentDiscs |= verticalMaskedOpponentBoard & (opponentDiscs >> 8)
        opponentDiscs |= verticalMaskedOpponentBoard & (opponentDiscs >> 8)
        legalBoard |= blankBoard & (opponentDiscs >> 8)

        # 左上
        opponentDiscs = allSideMaskedOpponentBoard & (self.playerBoard << 9)
        opponentDiscs |= allSideMaskedOpponentBoard & (opponentDiscs << 9)
        opponentDiscs |= allSideMaskedOpponentBoard & (opponentDiscs << 9)
        opponentDiscs |= allSideMaskedOpponentBoard & (opponentDiscs << 9)
        opponentDiscs |= allSideMaskedOpponentBoard & (opponentDiscs << 9)
        opponentDiscs |= allSideMaskedOpponentBoard & (opponentDiscs << 9)
        legalBoard |= blankBoard & (opponentDiscs << 9)

        # 右上
        opponentDiscs = allSideMaskedOpponentBoard & (self.playerBoard << 7)
        opponentDiscs |= allSideMaskedOpponentBoard & (opponentDiscs << 7)
        opponentDiscs |= allSideMaskedOpponentBoard & (opponentDiscs << 7)
        opponentDiscs |= allSideMaskedOpponentBoard & (opponentDiscs << 7)
        opponentDiscs |= allSideMaskedOpponentBoard & (opponentDiscs << 7)
        opponentDiscs |= allSideMaskedOpponentBoard & (opponentDiscs << 7)
        legalBoard |= blankBoard & (opponentDiscs << 7)

        # 右下
        opponentDiscs = allSideMaskedOpponentBoard & (self.playerBoard >> 9)
        opponentDiscs |= allSideMaskedOpponentBoard & (opponentDiscs >> 9)
        opponentDiscs |= allSideMaskedOpponentBoard & (opponentDiscs >> 9)
        opponentDiscs |= allSideMaskedOpponentBoard & (opponentDiscs >> 9)
        opponentDiscs |= allSideMaskedOpponentBoard & (opponentDiscs >> 9)
        opponentDiscs |= allSideMaskedOpponentBoard & (opponentDiscs >> 9)
        legalBoard |= blankBoard & (opponentDiscs >> 9)

        # 左下
        opponentDiscs = allSideMaskedOpponentBoard & (self.playerBoard >> 7)
        opponentDiscs |= allSideMaskedOpponentBoard & (opponentDiscs >> 7)
        opponentDiscs |= allSideMaskedOpponentBoard & (opponentDiscs >> 7)
        opponentDiscs |= allSideMaskedOpponentBoard & (opponentDiscs >> 7)
        opponentDiscs |= allSideMaskedOpponentBoard & (opponentDiscs >> 7)
        opponentDiscs |= allSideMaskedOpponentBoard & (opponentDiscs >> 7)
        legalBoard |= blankBoard & (opponentDiscs >> 7)

        return legalBoard

    def getPlaceableLocation(self) -> list[Location]:
        """置ける場所をLocationのlistとして返す

        Returns:
            list[Location]: 置ける場所のリスト
        """
        placeableLocation = []
        legalBoard = self._makeLegalBoard()
        mask = 1

        for i in range(1, 9):
            for j in range(1, 9):
                if (legalBoard & (mask << (63 - (8*(i - 1) + (j - 1))))) != 0:
                    placeableLocation.append(Location(i, j))

        return placeableLocation

    def _reverse(self, location: Location) -> None:
        """反転処理

        Args:
            location (Location): 石を置く場所
        """
        put = self._locationToBits(location)
        rev = self._getReverseBoard(put)

        self.playerBoard ^= (put | rev)
        self.opponentBoard ^= rev

    def _getReverseBoard(self, put: int) -> int:
        """反転箇所のビットが立っているボードを返す

        Args:
            put (int): 石を置いた場所のみビットが立っているボード

        Returns:
            int: 反転箇所のビットが立っているボード
        """
        # 反転箇所のビットが立っているボード
        rev = 0

        # 左右の端を除く相手ボード
        horizontalMaskedOpponentBoard = self.opponentBoard & 0x7e7e7e7e7e7e7e7e
        # 上下の端を除く相手ボード
        verticalMaskedOpponentBoard = self.opponentBoard & 0x00ffffffffffff00
        # 上下左右の端を除く相手ボード
        allSideMaskedOpponentBoard = self.opponentBoard & 0x007e7e7e7e7e7e00

        # 8方向をチェック
        # 1度に返せる石は6つまで
        # 左
        opponentDiscs = horizontalMaskedOpponentBoard & (put << 1)
        opponentDiscs |= horizontalMaskedOpponentBoard & (opponentDiscs << 1)
        opponentDiscs |= horizontalMaskedOpponentBoard & (opponentDiscs << 1)
        opponentDiscs |= horizontalMaskedOpponentBoard & (opponentDiscs << 1)
        opponentDiscs |= horizontalMaskedOpponentBoard & (opponentDiscs << 1)
        opponentDiscs |= horizontalMaskedOpponentBoard & (opponentDiscs << 1)
        if (self.playerBoard & (opponentDiscs << 1)) != 0:
            rev |= opponentDiscs

        # 右
        opponentDiscs = horizontalMaskedOpponentBoard & (put >> 1)
        opponentDiscs |= horizontalMaskedOpponentBoard & (opponentDiscs >> 1)
        opponentDiscs |= horizontalMaskedOpponentBoard & (opponentDiscs >> 1)
        opponentDiscs |= horizontalMaskedOpponentBoard & (opponentDiscs >> 1)
        opponentDiscs |= horizontalMaskedOpponentBoard & (opponentDiscs >> 1)
        opponentDiscs |= horizontalMaskedOpponentBoard & (opponentDiscs >> 1)
        if (self.playerBoard & (opponentDiscs >> 1)) != 0:
            rev |= opponentDiscs

        # 上
        opponentDiscs = verticalMaskedOpponentBoard & (put << 8)
        opponentDiscs |= verticalMaskedOpponentBoard & (opponentDiscs << 8)
        opponentDiscs |= verticalMaskedOpponentBoard & (opponentDiscs << 8)
        opponentDiscs |= verticalMaskedOpponentBoard & (opponentDiscs << 8)
        opponentDiscs |= verticalMaskedOpponentBoard & (opponentDiscs << 8)
        opponentDiscs |= verticalMaskedOpponentBoard & (opponentDiscs << 8)
        if (self.playerBoard & (opponentDiscs << 8)) != 0:
            rev |= opponentDiscs

        # 下
        opponentDiscs = verticalMaskedOpponentBoard & (put >> 8)
        opponentDiscs |= verticalMaskedOpponentBoard & (opponentDiscs >> 8)
        opponentDiscs |= verticalMaskedOpponentBoard & (opponentDiscs >> 8)
        opponentDiscs |= verticalMaskedOpponentBoard & (opponentDiscs >> 8)
        opponentDiscs |= verticalMaskedOpponentBoard & (opponentDiscs >> 8)
        opponentDiscs |= verticalMaskedOpponentBoard & (opponentDiscs >> 8)
        if (self.playerBoard & (opponentDiscs >> 8)) != 0:
            rev |= opponentDiscs

        # 左上
        opponentDiscs = allSideMaskedOpponentBoard & (put << 9)
        opponentDiscs |= allSideMaskedOpponentBoard & (opponentDiscs << 9)
        opponentDiscs |= allSideMaskedOpponentBoard & (opponentDiscs << 9)
        opponentDiscs |= allSideMaskedOpponentBoard & (opponentDiscs << 9)
        opponentDiscs |= allSideMaskedOpponentBoard & (opponentDiscs << 9)
        opponentDiscs |= allSideMaskedOpponentBoard & (opponentDiscs << 9)
        if (self.playerBoard & (opponentDiscs << 9)) != 0:
            rev |= opponentDiscs

        # 右上
        opponentDiscs = allSideMaskedOpponentBoard & (put << 7)
        opponentDiscs |= allSideMaskedOpponentBoard & (opponentDiscs << 7)
        opponentDiscs |= allSideMaskedOpponentBoard & (opponentDiscs << 7)
        opponentDiscs |= allSideMaskedOpponentBoard & (opponentDiscs << 7)
        opponentDiscs |= allSideMaskedOpponentBoard & (opponentDiscs << 7)
        opponentDiscs |= allSideMaskedOpponentBoard & (opponentDiscs << 7)
        if (self.playerBoard & (opponentDiscs << 7)) != 0:
            rev |= opponentDiscs

        # 右下
        opponentDiscs = allSideMaskedOpponentBoard & (put >> 9)
        opponentDiscs |= allSideMaskedOpponentBoard & (opponentDiscs >> 9)
        opponentDiscs |= allSideMaskedOpponentBoard & (opponentDiscs >> 9)
        opponentDiscs |= allSideMaskedOpponentBoard & (opponentDiscs >> 9)
        opponentDiscs |= allSideMaskedOpponentBoard & (opponentDiscs >> 9)
        opponentDiscs |= allSideMaskedOpponentBoard & (opponentDiscs >> 9)
        if (self.playerBoard & (opponentDiscs >> 9)) != 0:
            rev |= opponentDiscs

        # 左下
        opponentDiscs = allSideMaskedOpponentBoard & (put >> 7)
        opponentDiscs |= allSideMaskedOpponentBoard & (opponentDiscs >> 7)
        opponentDiscs |= allSideMaskedOpponentBoard & (opponentDiscs >> 7)
        opponentDiscs |= allSideMaskedOpponentBoard & (opponentDiscs >> 7)
        opponentDiscs |= allSideMaskedOpponentBoard & (opponentDiscs >> 7)
        opponentDiscs |= allSideMaskedOpponentBoard & (opponentDiscs >> 7)
        if (self.playerBoard & (opponentDiscs >> 7)) != 0:
            rev |= opponentDiscs

        return rev

    def gameIsFinished(self) -> bool:
        """ゲームの終了判定

        Returns:
            bool: ゲームが終了したならtrue、そうでないならfalseを返す
        """
        # 自分、相手が共に合法手が無いなら終了
        playerLegalBoard = self._makeLegalBoard()
        self._swapBoard()
        opponentLegalBoard = self._makeLegalBoard()
        self._swapBoard()

        return (playerLegalBoard == 0) and (opponentLegalBoard == 0)

    def updateBoardStatus(self) -> None:
        """ボードのパラメータを更新
        """
        self._swapBoard()
        self._changePlayerColor()
        self.turn += 1

    def _swapBoard(self) -> None:
        """自分と相手のボードを入れ替える
        """
        temp = self.playerBoard
        self.playerBoard = self.opponentBoard
        self.opponentBoard = temp

    def _changePlayerColor(self) -> None:
        """打ち手の色を入れ替える
        """
        if self.player == Disc.black:
            self.player = Disc.white
        else:
            self.player = Disc.black

    def getWinner(self) -> Disc:
        """石の数がより多い色を返す

        Returns:
            Disc: 石の数がより多い石の色 引き分けならDisc.emptyを返す
        """
        blackDiscNum, whiteDiscNum = self.getDiscNum()

        if blackDiscNum > whiteDiscNum:
            return Disc.black
        elif blackDiscNum < whiteDiscNum:
            return Disc.white
        else:
            return Disc.empty

    def getDiscNum(self) -> tuple[int, int]:
        """黒石と白石の数を返す

        Returns:
            tuple[int, int]: 黒石の数、白石の数を要素とするタプル
        """
        if self.player == Disc.black:
            blackDiscNum = self._numOfDisc(self.playerBoard)
            whiteDiscNum = self._numOfDisc(self.opponentBoard)
        else:
            whiteDiscNum = self._numOfDisc(self.playerBoard)
            blackDiscNum = self._numOfDisc(self.opponentBoard)

        return blackDiscNum, whiteDiscNum

    def _numOfDisc(self, board: int) -> int:
        """ボードの立っているビット数を数える

        Args:
            board (int): 立っているビット数を数えるボード

        Returns:
            int: 立っているビットの数
        """
        # forで回してもいいが、ビット演算で計算すると
        # O(N)からO(logN)になる
        mask1bit = 0x5555555555555555
        mask2bit = 0x3333333333333333
        mask4bit = 0x0f0f0f0f0f0f0f0f
        mask8bit = 0x00ff00ff00ff00ff
        mask16bit = 0x0000ffff0000ffff
        mask32bit = 0x00000000ffffffff

        board = (board & mask1bit) + ((board >> 1) & mask1bit)
        board = (board & mask2bit) + ((board >> 2) & mask2bit)
        board = (board & mask4bit) + ((board >> 4) & mask4bit)
        board = (board & mask8bit) + ((board >> 8) & mask8bit)
        board = (board & mask16bit) + ((board >> 16) & mask16bit)
        return (board & mask32bit) + ((board >> 32) & mask32bit)

    def getLocationDisc(self, location: Location) -> Disc:
        """指定された場所の石の色を返す

        Args:
            location (Location): 石の色を知りたい場所

        Returns:
            Disc: 指定された場所の石の色
        """
        mask = self._locationToBits(location)
        if self.player == Disc.black:
            if (self.playerBoard & mask) != 0:
                return Disc.black
            elif (self.opponentBoard & mask) != 0:
                return Disc.white
            else:
                return Disc.empty
        elif self.player == Disc.white:
            if (self.playerBoard & mask) != 0:
                return Disc.white
            elif (self.opponentBoard & mask) != 0:
                return Disc.black
            else:
                return Disc.empty
