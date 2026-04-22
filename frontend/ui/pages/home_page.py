from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QKeySequence, QShortcut
from ui.components import MenuButton


class HomePage(QWidget):
    # 定義自訂信號，用來告訴 main.py "玩家想進入單人遊戲了！"
    request_single_player = Signal()
    request_multi_player = Signal()
    request_replay = Signal()
    request_quit = Signal()

    def __init__(self):
        super().__init__()

        main_layout = QVBoxLayout(self)
        main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.setSpacing(30)

        # 設定排版
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setSpacing(20)

        # 標題
        title = QLabel("五子棋 Gomoku Demo")
        title.setStyleSheet(
            """
            qproperty-alignment: 'AlignCenter';
            background-color: #4f4f4f;
            color: white; 
            font-size: 40px;
            font-weight: bold;
            min-height: 70px;
            min-width: 500px;
            border-radius: 10px;
            """
        )
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(title)

        # 建立按鈕
        self.btn_single = MenuButton("單人模式 (AI)", self)
        self.btn_multi = MenuButton("雙人模式", self)
        self.btn_replay = MenuButton("回放棋局", self)

        # 添加按鈕
        layout.addWidget(self.btn_single)
        layout.addWidget(self.btn_multi)
        layout.addWidget(self.btn_replay)

        main_layout.addLayout(layout)

        # 綁定按鈕事件
        self.btn_single.clicked.connect(self.request_single_player.emit)
        self.btn_multi.clicked.connect(self.request_multi_player.emit)
        self.btn_replay.clicked.connect(self.request_replay.emit)

        # Ctrl+C 從主選單直接關閉整個應用 (避免後端卡住佔用)
        quit_shortcut = QShortcut(QKeySequence("Ctrl+C"), self)
        quit_shortcut.activated.connect(self.request_quit.emit)
