from board.disc import Disc
from board.bit_board import BitBoard
from solver.solver import Solver
from solver.human import Human
from solver.random import Random
from game_io.cui import CUI


class Game:
    """ゲームの進行や描画を管理するクラス
    """

    def __init__(self, firstSolverName: str = "Human", secondSolverName: str = "Human") -> None:
        """使用できるソルバー名: "Human", "Random"

        Args:
            firstSolverName (str, optional): 黒石（先攻）の手番のソルバー名. Defaults to "Human".
            secondSolverName (str, optional): 白石（後攻）の手番のソルバー名. Defaults to "Human".
        """
        self.board = BitBoard()
        self.ui = CUI()
        # 先手、後手のソルバーのオブジェクト生成
        self.firstSolver = self.generateSolver(firstSolverName)
        self.secondSolver = self.generateSolver(secondSolverName)

    def play(self) -> None:
        """オセロをプレイする
        """
        self.ui.display(self.board)
        while True:
            if self.board.player == Disc.black:
                selection = self.firstSolver.selectLocation(self.board)
            elif self.board.player == Disc.white:
                selection = self.secondSolver.selectLocation(self.board)
            
            if selection == "pass":
                self.board.passPut()
            else:
                self.board.put(selection)

            if self.board.gameIsFinished():
                break
            self.board.updateBoardStatus()
            self.ui.display(self.board)

        self.ui.displayResult(self.board)

    # ソルバーのオブジェクトを生成
    def generateSolver(self, name: str) -> Solver:
        if name == "Random":
            solver = Random()
        else:
            # デフォルトでは人間が打つ
            solver = Human(self.ui)

        return solver
