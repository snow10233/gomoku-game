from PySide6.QtWidgets import (
    QLabel,
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QLineEdit,
    QPushButton,
)


class InputDialog(QDialog):
    """通用的輸入對話框元件"""

    def __init__(self, parent=None, title="輸入", prompt="請輸入內容："):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setFixedSize(300, 150)
        self.setStyleSheet("QDialog { background-color: #2b2b2b; }")

        layout = QVBoxLayout(self)

        self.label = QLabel(prompt)
        self.label.setStyleSheet("color: white; font-size: 16px; font-weight: bold;")
        layout.addWidget(self.label)

        self.input_box = QLineEdit()
        self.input_box.setStyleSheet(
            """
            QLineEdit {
                background-color: #1e1e1e; color: white; 
                border: 2px solid #555; border-radius: 5px; padding: 5px; font-size: 16px;
            }
            QLineEdit:focus { border: 2px solid #4CAF50; }
        """
        )
        layout.addWidget(self.input_box)

        btn_layout = QHBoxLayout()
        self.btn_confirm = QPushButton("確認")
        self.btn_cancel = QPushButton("取消")

        btn_style = """
            QPushButton { background-color: #4CAF50; color: white; border-radius: 5px; padding: 8px; font-size: 14px; font-weight: bold; }
            QPushButton:hover { background-color: #45a049; }
        """
        self.btn_confirm.setStyleSheet(btn_style)
        self.btn_cancel.setStyleSheet(
            btn_style.replace("#4CAF50", "#f44336").replace("#45a049", "#da190b")
        )

        self.btn_confirm.clicked.connect(self.accept)
        self.btn_cancel.clicked.connect(self.reject)

        btn_layout.addWidget(self.btn_confirm)
        btn_layout.addWidget(self.btn_cancel)
        layout.addLayout(btn_layout)

    def get_text(self):
        return self.input_box.text()
