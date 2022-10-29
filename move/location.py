
class Location:
    """盤上の場所を表すクラス
    """

    def __init__(self, row: int, column: int) -> None:
        self.row = row
        self.column = column

    def checkRange(self) -> bool:
        """範囲の検証

        Returns:
            bool: 行と列が共に盤の座標の範囲内にあるならtrueを、そうでないならfalseを返す
        """
        if (1 <= self.row <= 8) and (1 <= self.column <= 8):
            return True
        else:
            return False
