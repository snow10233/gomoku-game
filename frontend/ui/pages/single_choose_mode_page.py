from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
)
from PySide6.QtCore import Qt, Signal
from ui.components import MenuButton


class SingleChooseModePage(QWidget):
    request_new_game = Signal()
    request_load_game = Signal()
    request_home = Signal()

    def __init__(self):
        super().__init__()

        main_layout = QVBoxLayout(self)
        main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.setSpacing(30)

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setSpacing(20)

        title = QLabel("單人模式 (AI)")
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

        self.btn_new_game = MenuButton("新對局", self)
        self.btn_load_game = MenuButton("載入對局", self)
        self.btn_back = MenuButton("返回主選單", self)

        layout.addWidget(self.btn_new_game)
        layout.addWidget(self.btn_load_game)
        layout.addWidget(self.btn_back)

        main_layout.addLayout(layout)

        self.btn_new_game.clicked.connect(self.request_new_game.emit)
        self.btn_load_game.clicked.connect(self.request_load_game.emit)
        self.btn_back.clicked.connect(self.request_home.emit)