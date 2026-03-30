from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
)
from PySide6.QtCore import Qt, Signal
from ui.components import MenuButton, WipDialog


class HomePage(QWidget):
    # 定義自訂信號，用來告訴 main.py "玩家想進入單人遊戲了！"
    request_single_player = Signal()
    request_multiplayer = Signal()

    def __init__(self):
        super().__init__()
        self.setStyleSheet("QWidget { background-color: #2b2b2b; }")

        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setSpacing(20)

        # 標題
        title = QLabel("五子棋 Gomoku Pro")
        title.setStyleSheet("color: white; font-size: 36px; font-weight: bold;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        # 建立按鈕
        self.btn_single = MenuButton("單人模式 (AI)", self)
        self.btn_multi = MenuButton("雙人模式 (P2P)", self)
        self.btn_load = MenuButton("載入棋局", self)
        self.btn_replay = MenuButton("回放棋局", self)

        layout.addWidget(self.btn_single)
        layout.addWidget(self.btn_multi)
        layout.addWidget(self.btn_load)
        layout.addWidget(self.btn_replay)

        # 綁定按鈕事件
        self.btn_single.clicked.connect(self.request_single_player.emit)
        self.btn_multi.clicked.connect(self.request_multiplayer.emit)  # 暫未開放
        self.btn_load.clicked.connect(self.show_wip)  # 暫未開放
        self.btn_replay.clicked.connect(self.show_wip)  # 暫未開放

    def show_wip(self):
        dialog = WipDialog(self)
        dialog.exec()
