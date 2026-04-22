from ..game_page import GamePage
from ui.components import AlertDialog


class MultiGamePage(GamePage):
    def __init__(self):
        super().__init__()
        self.timer_enabled = True

    def handle_undo(self):
        """本地雙人：悔棋只退一顆，需要把回合切換回上一位玩家。"""
        success, undo_positions = self.engine.undo()
        if not success:
            AlertDialog("無法悔棋！(已經退回原點)", self).exec()
            return

        for x, y in undo_positions:
            if 0 <= x < 15 and 0 <= y < 15:
                self.board_widget.board[y][x] = 0

        self.switch_player()
        self.board_widget.update()
        self.timer_label.reset()

    def handle_user_move(self, col, row):
        """本地雙人：每次點擊只落目前玩家的一顆棋。"""
        if self.board_widget.board[row][col] != 0:
            return

        success, board_state = self.engine.put_chess(col, row)
        self.show_battle_result(board_state)  # 檢查遊戲是否結束並暫停計時器

        if not success:
            print("本地雙人落子失敗")
            return

        if board_state == "CONTINUE":
            self.place_signal.emit()
        self.board_widget.board[row][col] = self.now_player

        # 只有遊戲繼續進行才切換玩家重置計時器
        if board_state == "CONTINUE":
            self.switch_player()
            self.board_widget.update()
            self.timer_label.reset()
        else:
            self.board_widget.update()

    def handle_time_out(self):
        """本地雙人：超時直接換手，不做 AI 落子。"""
        if not self.timer_enabled:
            return

        print("本地雙人超時，發送 {OVER_TIME} 並切換回合")
        put_result, board_state = self.engine.over_time()
        self.show_battle_result(board_state)  # 檢查遊戲是否結束並暫停計時器

        if not put_result:
            print("C++ 拒絕 OVER_TIME，前端不切換")
            return

        # 只有遊戲未結束才切換玩家重置計時器
        if board_state == "CONTINUE":
            self.switch_player()
            self.board_widget.update()
            self.timer_label.reset()

    def start_game(self, undo_enable, timer_enable, reset_enable):
        """切到本地雙人頁時，切換後端模式並重置 UI。"""
        self.overlay.hide()
        self._game_ended = False
        success = self.engine.two_player_mode()
        if not success:
            print("C++ 切換 TWO_PLAYER_MODE 失敗")
            return

        self.board_widget.board = [[0 for _ in range(15)] for _ in range(15)]
        self.now_player = 1
        self.player_title.setText("黑棋回合")
        self.board_widget.set_preview_player(1)
        self.board_widget.update()
        self.timer_enabled = timer_enable
        self._apply_switches(undo_enable, timer_enable, reset_enable)
