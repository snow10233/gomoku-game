from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QLabel,
    QMessageBox,
    QDialog,
    QLineEdit,
)
from PySide6.QtCore import Qt, Signal


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
        self.btn_single = self.create_button("單人模式 (AI)")
        self.btn_load = self.create_button("載入棋局")
        self.btn_multi = self.create_button("雙人模式 (P2P)")
        self.btn_replay = self.create_button("回放棋局")

        layout.addWidget(self.btn_single)
        layout.addWidget(self.btn_load)
        layout.addWidget(self.btn_multi)
        layout.addWidget(self.btn_replay)

        # 綁定按鈕事件
        self.btn_single.clicked.connect(self.on_single_player_clicked)
        self.btn_load.clicked.connect(self.show_wip_dialog)  # 暫未開放
        self.btn_multi.clicked.connect(self.request_multiplayer.emit)  # 暫未開放
        self.btn_replay.clicked.connect(self.show_wip_dialog)  # 暫未開放

    def create_button(self, text):
        btn = QPushButton(text)
        btn.setFixedSize(250, 50)
        btn.setStyleSheet(
            """
            QPushButton { background-color: #4CAF50; color: white; border-radius: 10px; font-size: 18px; }
            QPushButton:hover { background-color: #45a049; }
        """
        )
        return btn

    def show_wip_dialog(self):
        """實作文件要求的「彈出提示框 "暫未開放"」，並強制撐大與美化"""
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle("系統提示")
        msg_box.setText("此模式暫未開放！\n(Work In Progress)")

        # 🌟 魔法在這裡：利用 min-width 和 min-height 強制撐大視窗
        msg_box.setStyleSheet(
            """
            QMessageBox { background-color: #2b2b2b; }
            QLabel { color: white; min-width: 300px; min-height: 80px; font-size: 18px; font-weight: bold; }
            QPushButton { background-color: #4CAF50; color: white; border-radius: 5px; padding: 8px 20px; font-size: 16px; }
            QPushButton:hover { background-color: #45a049; }
        """
        )
        msg_box.exec()

    def on_single_player_clicked(self):
        # 發射信號給 Main Window，要求切換頁面
        self.request_single_player.emit()
