from PySide6.QtWidgets import QPushButton


class GameButton(QPushButton):
    def __init__(self, text="請輸入文本", parent=None):
        super().__init__(text, parent)
        self.setFixedSize(150, 40)
        self.setStyleSheet(
            """
            QPushButton { 
                background-color: #363636;
                color: white;
                border-radius: 5px;
                font-size: 18px;
            }
            QPushButton:hover { background-color: #535353; }
        """
        )
