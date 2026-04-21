from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QFileDialog,
)
from PySide6.QtCore import Qt, Signal
from ui.components import (
    GomokuBoard,
    GameButton,
    AlertDialog,
)


class ReplayPage(QWidget):
    """回放模式：讀 .gmk 檔，用 stack 實現下一步/上一步。

    - `future` 堆疊：尚未回放的步驟 (最上層即為下一個要走的步)
    - `history` 堆疊：已回放的步驟，回退時 pop 回 `future`
    - 遇到 OT 佔位：只換手不落子，並彈提示 (Q11-B)
    """

    request_home = Signal()

    def __init__(self):
        super().__init__()

        main_layout = QVBoxLayout(self)
        main_layout.setAlignment(Qt.AlignCenter)

        top_layout = QHBoxLayout()
        top_layout.setAlignment(Qt.AlignCenter)
        top_layout.setSpacing(20)

        self.info_label = QLabel("尚未載入棋譜")
        self.info_label.setStyleSheet(
            """
            qproperty-alignment: 'AlignCenter';
            background-color: #4f4f4f;
            color: white;
            font-size: 28px;
            font-weight: bold;
            min-height: 70px;
            min-width: 500px;
            border-radius: 10px;
            """
        )
        top_layout.addWidget(self.info_label)

        bottom_layout = QHBoxLayout()
        bottom_layout.setAlignment(Qt.AlignCenter)
        bottom_layout.setSpacing(20)

        self.board_widget = GomokuBoard()
        self.board_widget.setMouseTracking(False)

        bottom_right_layout = QVBoxLayout()
        bottom_right_layout.setAlignment(Qt.AlignCenter)
        bottom_right_layout.setSpacing(20)

        self.btn_load = GameButton("載入棋譜", self)
        self.btn_prev = GameButton("上一步", self)
        self.btn_next = GameButton("下一步", self)
        self.btn_back = GameButton("返回主選單", self)

        bottom_right_layout.addWidget(self.btn_load)
        bottom_right_layout.addWidget(self.btn_prev)
        bottom_right_layout.addWidget(self.btn_next)
        bottom_right_layout.addWidget(self.btn_back)

        bottom_layout.addWidget(self.board_widget)
        bottom_layout.addLayout(bottom_right_layout)

        main_layout.addLayout(top_layout)
        main_layout.addLayout(bottom_layout)

        self.btn_load.clicked.connect(self.handle_load)
        self.btn_prev.clicked.connect(self.handle_prev)
        self.btn_next.clicked.connect(self.handle_next)
        self.btn_back.clicked.connect(self.request_home.emit)

        # 覆寫 GomokuBoard 的預設點擊：回放不允許玩家下棋
        self.board_widget.mousePressEvent = lambda event: None

        self.mode = None
        self.future = []   # stack: 下一步先 pop 最後一個
        self.history = []  # stack: 上一步先 pop 最後一個
        self._update_info()

    def handle_load(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "選擇要回放的棋局檔", "", "Gomoku Files (*.gmk);;All Files (*)"
        )
        if not file_path:
            return

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                sub_mode = f.readline().strip()
                replay = f.readline().strip()
        except OSError as err:
            AlertDialog(f"讀取失敗：{err}", self).exec()
            return

        if sub_mode not in ("AI_MODE", "TWO_PLAYER_MODE"):
            AlertDialog("檔案格式無效", self).exec()
            return

        steps = self._parse_replay(replay)
        # future 以 pop 取最前：所以要反向 push，使頂端為第一步
        self.future = list(reversed(steps))
        self.history = []
        self.mode = sub_mode
        self.board_widget.board = [[0 for _ in range(15)] for _ in range(15)]
        self.board_widget.update()
        self._update_info()

    def handle_next(self):
        if not self.future:
            AlertDialog("已經是最後一步！", self).exec()
            return

        step = self.future.pop()
        self.history.append(step)

        if step == "OT":
            self._update_info()
            AlertDialog("此處發生超時換手 (OT)", self).exec()
            # OT 本身不落子，直接再走一步真正的棋
            self.handle_next()
            return

        col, row = step
        # 依 history 目前黑/白輪替推算顏色
        # AI_MODE 玩家黑、AI 白；雙人交替
        player = self._player_of_step_index(len(self.history) - 1)
        self.board_widget.board[row][col] = player
        self.board_widget.update()
        self._update_info()

    def handle_prev(self):
        if not self.history:
            AlertDialog("已經是第一步！", self).exec()
            return

        step = self.history.pop()
        self.future.append(step)

        if step == "OT":
            # 連退：繼續退到真正的棋
            self._update_info()
            self.handle_prev()
            return

        col, row = step
        self.board_widget.board[row][col] = 0
        self.board_widget.update()
        self._update_info()

    def _player_of_step_index(self, idx):
        """根據 mode 和 history 中有幾個實際落子 (不含 OT) 推算顏色。"""
        non_ot = [s for s in self.history[: idx + 1] if s != "OT"]
        ot_count = sum(1 for s in self.history[: idx + 1] if s == "OT")
        # 每一次實際落子換手；OT 本身也算換一次手
        toggles = (len(non_ot) - 1) + ot_count
        return 1 if toggles % 2 == 0 else 2

    def _update_info(self):
        if self.mode is None:
            self.info_label.setText("尚未載入棋譜")
            return
        played = len([s for s in self.history if s != "OT"])
        total = played + len([s for s in self.future if s != "OT"])
        self.info_label.setText(f"{self.mode}　{played} / {total} 步")

    @staticmethod
    def _parse_replay(replay):
        steps = []
        for token in replay.split():
            if token == "OT":
                steps.append("OT")
                continue
            if len(token) < 2 or not ("A" <= token[0] <= "O"):
                continue
            try:
                steps.append((ord(token[0]) - ord("A"), int(token[1:])))
            except ValueError:
                continue
        return steps
