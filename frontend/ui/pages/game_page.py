from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
)
from PySide6.QtCore import Qt, Signal
from core.engine import GomokuEngine
from ui.components import (
    GameTimerLabel,
    GomokuBoard,
    GameButton,
    AlertDialog,
    BattleResult,
)


class GamePage(QWidget):
    # 發射信號給 Main Window，告訴它「我要回首頁」
    request_home = Signal()

    def __init__(self):
        super().__init__()
        self.engine = GomokuEngine()
        self.overlay = BattleResult(self)

        # --- 總功能區塊 ---
        main_layout = QVBoxLayout(self)
        main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # --- 頂部功能區塊 ---
        top_layout = QHBoxLayout()
        top_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        top_layout.setSpacing(20)

        # --- 時間 ---
        self.timer_label = GameTimerLabel()

        # --- 玩家棋子 ---
        self.now_player = 1  # 1 黑 2 白
        self.player_title = QLabel("黑棋回合")
        self.player_title.setStyleSheet(
            """
            qproperty-alignment: 'AlignCenter';
            background-color: #4f4f4f;
            color: white; 
            font-size: 40px;
            font-weight: bold;
            min-height: 70px;
            min-width: 200px;
            border-radius: 10px;
            """
        )
        self.player_title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # --- 下方功能區塊 ---
        bottom_layout = QHBoxLayout()
        bottom_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        bottom_layout.setSpacing(20)

        # --- 棋盤區塊 ---
        self.board_widget = GomokuBoard()
        self.board_widget.set_preview_player(1)

        # --- 右側功能欄位 ---
        bottom_right_layout = QVBoxLayout()
        bottom_right_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        bottom_right_layout.setSpacing(20)

        # --- 按鈕設置 ---
        self.btn_undo = GameButton("悔棋", self)
        self.btn_reset = GameButton("重置棋盤", self)
        self.btn_back = GameButton("返回主選單", self)

        bottom_right_layout.addWidget(self.btn_undo)
        bottom_right_layout.addWidget(self.btn_reset)
        bottom_right_layout.addWidget(self.btn_back)

        # --- 組合 ---
        top_layout.addWidget(self.timer_label)
        top_layout.addWidget(self.player_title)

        bottom_layout.addWidget(self.board_widget)
        bottom_layout.addLayout(bottom_right_layout)

        main_layout.addLayout(top_layout)
        main_layout.addLayout(bottom_layout)

        # --- 功能設定 ---
        self.board_widget.clicked_pos.connect(self.handle_user_move)
        self.timer_label.time_out.connect(self.handle_time_out)
        self.btn_reset.clicked.connect(self.handle_reset)
        self.btn_undo.clicked.connect(self.handle_undo)
        self.btn_back.clicked.connect(self.request_home.emit)
        self.overlay.request_home.connect(self.request_home.emit)

    def switch_player(self):
        """切換玩家並更新標題"""
        if self.now_player == 1:
            self.now_player = 2
            self.player_title.setText("白棋回合")
        else:
            self.now_player = 1
            self.player_title.setText("黑棋回合")
        self.board_widget.set_preview_player(self.now_player)

    def handle_time_out(self):
        print("前端發現超時！準備聯絡 C++ 引擎處理換人...")
        print("發送 {OVER_TIME}")

        # 呼叫我們剛剛在 Engine 寫好的函式
        put_result, board_state, ai_x, ai_y = self.engine.over_time()

        

        if put_result == "SUCCESS":
            # 幫 AI 落子
            self.board_widget.board[ai_y][ai_x] = 2
            # AI 模式固定由玩家(黑棋)操作，超時後仍回到黑棋回合
            self.now_player = 1
            self.player_title.setText("黑棋回合")
            self.board_widget.set_preview_player(1)

            # 畫面重繪
            self.board_widget.update()
            self.timer_label.reset()
        else:
            print("C++ 引擎拒絕了這步棋！")

    def handle_user_move(self, col, row):
        """玩家點擊棋盤時觸發的真正邏輯"""
        # 如果那個格子已經有棋子了，直接忽略，不用吵 C++
        if self.board_widget.board[row][col] != 0:
            return

        put_result, board_state, ai_x, ai_y = self.engine.put_chess(col, row)

        self.show_battle_result(board_state)  # 無論成功與否都要檢查是否有勝負結果需要顯示

        if put_result:
            # str -> intvi
            ai_x = int(ai_x)
            ai_y = int(ai_y)

            # 1. AI 模式固定：玩家為黑棋
            self.board_widget.board[row][col] = 1

            # 2. 幫 AI 落子
            if ai_x != -2 and ai_y != -2:  # -2 -2為悔棋代號
                self.board_widget.board[ai_y][ai_x] = 2

            # 3. 顯示與預覽維持玩家黑棋回合
            self.now_player = 1
            self.player_title.setText("黑棋回合")
            self.board_widget.set_preview_player(1)

            # 4. 觸發畫面重繪 & 重置計時器
            self.board_widget.update()
            self.timer_label.reset()

            print(f"當前棋盤狀態: {board_state}")
        else:
            print(f"落子失敗 原因:{put_result}")

    def handle_undo(self):
        """處理玩家按下悔棋按鈕的邏輯"""
        print("玩家要求悔棋，發送 {TAKE_BACK}")

        # 呼叫我們剛剛在 Engine 寫好的函式
        success, undo_positions = self.engine.undo()

        if success:
            print(f"悔棋成功 C++ 指示移除座標：{undo_positions}")
            for x, y in undo_positions:
                if 0 <= x < 15 and 0 <= y < 15:  # 座標防呆
                    self.board_widget.board[y][x] = 0  # 將該格設為 0 (空)

            # 畫面重繪
            self.board_widget.update()

            # 悔棋後，輪到玩家重新思考，所以計時器要重置
            self.timer_label.reset()
        else:
            print("悔棋失敗")
            alert = AlertDialog("無法悔棋！(已經退回原點)", self)
            alert.exec()

    def handle_reset(self):
        """處理玩家按下RESET按鈕的邏輯"""
        print("玩家要求悔棋，發送 {RESET}")

        success = self.engine.send_command("RESET")
        if success:
            self.board_widget.board = [[0 for _ in range(15)] for _ in range(15)]
            self.now_player = 1
            self.player_title.setText("黑棋回合")
            self.board_widget.set_preview_player(1)
            self.board_widget.update()
            self.timer_label.start_timer()
        else:
            print(f"C++重置失敗")

    def start_game(self, undo_enable, timer_enable, reset_enable):
        """當從首頁切換過來時，呼叫這個來初始化"""
        self.overlay.hide()
        # 告訴 C++ 我們要開始新遊戲了，讓它做好準備
        success = self.engine.send_command("AI_MODE")
        if success:
            # 重置棋盤
            self.board_widget.board = [[0 for _ in range(15)] for _ in range(15)]
            self.now_player = 1
            self.player_title.setText("黑棋回合")
            self.board_widget.set_preview_player(1)
            self.board_widget.update()

            # 悔棋按鈕的顯示與否
            if not undo_enable:
                self.btn_undo.setVisible(False)
            else:
                self.btn_undo.setVisible(True)

            # 計時器的顯示和啟動
            if not timer_enable:
                self.timer_label.setVisible(False)
                self.timer_label.switch(False)
            else:
                self.timer_label.setVisible(True)
                self.timer_label.switch(True)
                self.timer_label.start_timer()

            # 重置按鈕的顯示與否
            if not reset_enable:
                self.btn_reset.setVisible(False)
            else:
                self.btn_reset.setVisible(True)
        else:
            print(f"C++切換失敗")

    def end_game(self):
        """當切換回首頁時，呼叫這個來清空棋盤"""
        success = self.engine.send_command("HOME_PAGE")
        if success:
            print("C++ 已切換至 HOME_PAGE")
            # 暫停計時器
            self.timer_label.timer.stop()
        else:
            print("C++切換失敗")

    def show_battle_result(self, result):
        """顯示勝負結果的覆蓋層"""
        if result == "BLACK_WIN":
            self.timer_label.timer.stop()
            self.overlay.show_result("黑棋獲勝！")
        elif result == "WHITE_WIN":
            self.timer_label.timer.stop()
            self.overlay.show_result("白棋獲勝！")
        elif result == "DRAW":
            self.timer_label.timer.stop()
            self.overlay.show_result("平局！")

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.overlay.setGeometry(self.rect())