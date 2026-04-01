from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
)
from PySide6.QtCore import Qt, Signal
from ui.components import MenuButton


class newORload(QWidget):
    request_New = Signal()
    request_Load = Signal()
    request_Back = Signal()

    def __init__(self):
        super().__init__()

        main_layout = QVBoxLayout(self)
        main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.setSpacing(30)

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setSpacing(20)

        title = QLabel("單人模式 (Single Mode)")
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

        self.btn_New = MenuButton("新對局 (New Game)", self)
        self.btn_Load = MenuButton("載入對局 (Load Game)", self)
        self.btn_Back = MenuButton("返回主選單 (Back)", self)

        layout.addWidget(self.btn_New)
        layout.addWidget(self.btn_Load)
        layout.addWidget(self.btn_Back)

        main_layout.addLayout(layout)

        self.btn_New.clicked.connect(self.request_New.emit)
        self.btn_Load.clicked.connect(self.request_Load.emit)
        self.btn_Back.clicked.connect(self.request_Back.emit)