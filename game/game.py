from board.disc import Disc
from board.bit_board import BitBoard
from solver.solver import Solver
from solver.human import Human
from solver.random import Random
from solver.opponent_move_minimizer import OpponentMoveMinimizer
from solver.location_weight_alphabeta import LocationWeight_Alphabeta
from game_io.cui import CUI


class Game:
    """ゲームの進行や描画を管理するクラス
    """

    def __init__(self, firstSolverName: str = "Human", secondSolverName: str = "Human") -> None:
        """使用できるソルバー名: "Human", "Random", "OpponentMoveMinimizer"

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
        self.board = BitBoard()
        self.ui.display(self.board)
        while True:
            if self.board.player == Disc.black:
                selection = self.firstSolver.selectLocation(self.board)
            elif self.board.player == Disc.white:
                selection = self.secondSolver.selectLocation(self.board)
            
            if selection == "pass":
                self.board.passPut()
            elif selection == "undo":
                self.board.undo()
                self.ui.display(self.board)
                continue
            else:
                self.board.put(selection)

            if self.board.gameIsFinished():
                break
            self.board.updateBoardStatus()
            self.ui.display(self.board)

        self.ui.displayResult(self.board)
    
    def calculatePlayResult(self, playNum: int) -> None:
        """対戦を何度も行い、勝率を計算する

        Args:
            playNum (int): 対戦の試行回数
        """
        blackWin = 0
        whiteWin = 0
        draw = 0

        progress = 0
        for i in range(playNum):
            if ((i + 1) / playNum) >= progress:
                print(f"progress... {float(progress * 100):.4}%")
                progress += 0.05

            winner, (blackDiscNum, WhiteDiscNum) = self.playWithoutDisplay()
            if winner == Disc.black:
                blackWin += 1
            elif winner == Disc.white:
                whiteWin += 1
            else:
                draw += 1
        
        print(f"progress... 100%")
        print(f"play: {playNum} times")
        print(f"black win: {blackWin}, white win: {whiteWin}, draw: {draw}")
        print(f"winning percentage; black: {blackWin / playNum * 100:.3}%, white: {whiteWin / playNum * 100:.3}%")
    
    def playWithoutDisplay(self) -> tuple[Disc, tuple[int, int]]:
        """表示無しで対戦する

        Returns:
            tuple[Disc, tuple[int, int]]: 勝者の石の色、黒石の数、白石の数
        """
        self.board = BitBoard()
        while True:
            if self.board.player == Disc.black:
                selection = self.firstSolver.selectLocation(self.board)
            elif self.board.player == Disc.white:
                selection = self.secondSolver.selectLocation(self.board)
            
            if selection == "pass":
                self.board.passPut()
            elif selection == "undo":
                self.board.undo()
                continue
            else:
                self.board.put(selection)

            if self.board.gameIsFinished():
                break
            self.board.updateBoardStatus()
        
        return (self.board.getWinner(), self.board.getDiscNum())

    # ソルバーのオブジェクトを生成
    def generateSolver(self, name: str) -> Solver:
        if name == "Random":
            solver = Random()
        elif name == "OpponentMoveMinimizer":
            solver = OpponentMoveMinimizer()
        elif name == "LocationWeight_Alphabeta":
            solver = LocationWeight_Alphabeta(depth=5)
        else:
            # デフォルトでは人間が打つ
            solver = Human(self.ui)

        return solver
