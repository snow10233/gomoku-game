from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
)
from PySide6.QtCore import Qt, Signal
from core.engine import GomokuEngine
from ui.components import GameTimerLabel, GomokuBoard, GameButton, AlertDialog


class GamePage(QWidget):
    # 發射信號給 Main Window，告訴它「我要回首頁」
    request_home = Signal()

    def __init__(self):
        super().__init__()

        self.engine = GomokuEngine()

        main_layout = QVBoxLayout(self)
        main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        # --- 頂部時間 & 玩家棋子 ---
        top_layout = QHBoxLayout()
        top_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        top_layout.setSpacing(20)

        self.timer_label = GameTimerLabel()
        top_layout.addWidget(self.timer_label)

        main_layout.addLayout(top_layout)

        # --- 下方功能區塊 ---
        bottom_layout = QHBoxLayout()
        bottom_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        bottom_layout.setSpacing(20)

        # --- 棋盤區塊 ---
        self.board_widget = GomokuBoard()
        bottom_layout.addWidget(self.board_widget)

        # --- 右側功能欄位 ---

        bottom_right_layout = QVBoxLayout()
        bottom_right_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        bottom_right_layout.setSpacing(20)

        self.btn_undo = GameButton("悔棋", self)
        self.btn_reset = GameButton("重置棋盤", self)
        self.btn_back = GameButton("回到主選單", self)

        bottom_right_layout.addWidget(self.btn_undo)
        bottom_right_layout.addWidget(self.btn_reset)
        bottom_right_layout.addWidget(self.btn_back)

        bottom_layout.addLayout(bottom_right_layout)

        main_layout.addLayout(bottom_layout)

        self.board_widget.clicked_pos.connect(
            self.handle_user_move
        )  # 綁定到真正的引擎溝通函式
        self.btn_reset.clicked.connect(self.handle_reset)  # 點擊時發射回首頁信號
        self.btn_undo.clicked.connect(self.handle_undo)  # 點擊時發射回首頁信號
        self.btn_back.clicked.connect(self.request_home.emit)  # 點擊時發射回首頁信號

    def handle_user_move(self, col, row):
        """玩家點擊棋盤時觸發的真正邏輯"""
        # 如果那個格子已經有棋子了，直接忽略，不用吵 C++
        if self.board_widget.board[row][col] != 0:
            return

        print(f"玩家嘗試下棋：({col}, {row})")
        # 透過引擎呼叫 C++
        put_result, board_state, ai_x, ai_y = self.engine.put_chess(col, row)

        if put_result == "SUCCESS" or put_result == "PUT_RESULT":
            # 1. 玩家落子成功，更新本機陣列
            self.board_widget.board[row][col] = 1  # 黑子

            # 2. 如果 AI 有回傳座標，幫 AI 落子
            if ai_x != -1 and ai_y != -1:
                self.board_widget.board[ai_y][ai_x] = 2  # 白子

            # 3. 觸發畫面重繪 & 重置計時器
            self.board_widget.update()
            self.timer_label.reset()

            # TODO: 這裡之後可以根據 board_state 判斷有沒有人贏了
            print(f"當前狀態: {board_state}")
        else:
            print("C++ 引擎拒絕了這步棋！")

    def handle_undo(self):
        """處理玩家按下悔棋按鈕的邏輯"""
        print("玩家要求悔棋，發送 {TAKE_BACK}")

        # 呼叫我們剛剛在 Engine 寫好的函式
        success, undo_positions = self.engine.take_back()

        if success:
            print(f"悔棋成功，C++ 指示移除座標：{undo_positions}")
            # 🌟 根據 C++ 傳回來的座標，精準拔除棋盤上的棋子
            for x, y in undo_positions:
                if 0 <= x < 15 and 0 <= y < 15:  # 座標防呆
                    self.board_widget.board[y][x] = 0  # 將該格設為 0 (空)

            # 畫面重繪
            self.board_widget.update()

            # 悔棋後，輪到玩家重新思考，所以計時器要重置
            self.timer_label.reset()
        else:
            print("無法悔棋")
            alert = AlertDialog("無法悔棋！(已經退回原點)", self)
            alert.exec()

    def handle_reset(self):
        """處理玩家按下RESET按鈕的邏輯"""
        print("玩家要求悔棋，發送 {RESET}")

        response = self.engine.send_command("RESET")
        if response == "SUCCESS":
            print("成功重置")

        self.board_widget.board = [[0 for _ in range(15)] for _ in range(15)]
        self.board_widget.update()
        self.timer_label.start_timer()

    def start_game(self):
        """當從首頁切換過來時，呼叫這個來初始化"""
        # 🌟 告訴 C++ 我們要進入 AI 模式了
        response = self.engine.send_command("AI_MODE")
        if response == "SUCCESS":
            print("C++ 已切換至 AI_MODE")

        self.board_widget.board = [[0 for _ in range(15)] for _ in range(15)]
        self.board_widget.update()
        self.timer_label.start_timer()

    def end_game(self):
        """當切換回首頁時，呼叫這個來清空棋盤"""
        response = self.engine.send_command("HOME_PAGE")
        if response == "SUCCESS":
            print("C++ 已切換至 HOME_PAGE")
