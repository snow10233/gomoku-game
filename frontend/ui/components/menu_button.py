from PySide6.QtWidgets import QPushButton


class MenuButton(QPushButton):
    def __init__(self, text="請輸入文本", parent=None):
        super().__init__(text, parent)
        self.setFixedSize(250, 50)
        self.setStyleSheet(
            """
            QPushButton { 
                background-color: #4CAF50;
                color: white;
                border-radius: 10px;
                font-size: 18px;
            }
            QPushButton:hover { background-color: #45a049; }
        """
        )
