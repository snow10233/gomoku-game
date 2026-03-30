from PySide6.QtWidgets import QMessageBox


class WipDialog(QMessageBox):
    """實作文件要求的「彈出提示框 "暫未開放"」，並強制撐大與美化"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("系統提示")
        self.setText("此模式暫未開放！")

        # 🌟利用 min-width 和 min-height 強制撐大視窗
        self.setStyleSheet(
            """
            QMessageBox { background-color: #2b2b2b; }
            QLabel { color: white; min-width: 300px; min-height: 80px; font-size: 18px; font-weight: bold; }
            QPushButton { background-color: #4CAF50; color: white; border-radius: 5px; padding: 8px 20px; font-size: 16px; }
            QPushButton:hover { background-color: #45a049; }
        """
        )
