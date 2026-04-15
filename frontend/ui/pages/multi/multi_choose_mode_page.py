from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
)
from PySide6.QtCore import Qt, Signal
from ui.components import MenuButton


class MultiChooseModePage(QWidget):
    request_local_game = Signal()
    request_remote_game = Signal()
    request_home = Signal()

    def __init__(self):
        super().__init__()

        main_layout = QVBoxLayout(self)
        main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.setSpacing(30)

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setSpacing(20)

        title = QLabel("雙人模式")
        title.setStyleSheet(
            """
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

        self.btn_local_game = MenuButton("本地對戰", self)
        self.btn_remote_game = MenuButton("遠端對戰", self)
        self.btn_back = MenuButton("返回主選單", self)

        layout.addWidget(self.btn_local_game)
        layout.addWidget(self.btn_remote_game)
        layout.addWidget(self.btn_back)

        main_layout.addLayout(layout)

        self.btn_local_game.clicked.connect(self.request_local_game.emit)
        self.btn_remote_game.clicked.connect(self.request_remote_game.emit)
        self.btn_back.clicked.connect(self.request_home.emit)
