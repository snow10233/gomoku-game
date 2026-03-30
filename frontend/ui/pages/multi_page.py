from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QPushButton,
    QLabel,
    QMessageBox,
    QDialog,
)
from PySide6.QtCore import Qt, Signal
from ui.components import InputDialog, MenuButton, WipDialog


class MultiplayerPage(QWidget):
    # 發射信號告訴 main.py "我要回首頁了"
    request_home = Signal()

    def __init__(self):
        super().__init__()

        main_layout = QVBoxLayout(self)
        main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.setSpacing(30)

        # 設定排版
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setSpacing(20)

        title = QLabel("雙人連線模式 (P2P)")
        title.setStyleSheet(
            "background-color: #4f4f4f;"
            " color: white;"
            " font-size: 40px;"
            " font-weight: bold;"
            " min-height: 70px;"
            " min-width: 500px;"
            " border-radius: 10px;"
        )
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(title)

        # 建立三個選項按鈕
        self.btn_create = MenuButton("建立房間", self)
        self.btn_join = MenuButton("加入房間", self)
        self.btn_back = MenuButton("主選單", self)

        layout.addWidget(self.btn_create)
        layout.addWidget(self.btn_join)
        layout.addWidget(self.btn_back)

        main_layout.addLayout(layout)

        # 綁定按鈕邏輯
        self.btn_back.clicked.connect(self.request_home.emit)
        self.btn_create.clicked.connect(self.handle_create_room)
        self.btn_join.clicked.connect(self.handle_join_room)

    def show_wip(self):
        dialog = WipDialog(self)
        dialog.exec()

    def handle_create_room(self):
        print("選擇：建立房間")
        # 根據文件，彈出未開放
        self.show_wip()

    def handle_join_room(self):
        print("選擇：加入房間")
        # 1. 召喚輸入框
        dialog = InputDialog(self, title="加入房間", prompt="請輸入房號:")
        # 2. 等待玩家按確認
        if dialog.exec() == QDialog.DialogCode.Accepted:
            user_input = dialog.get_text()
            print(f"嘗試連線至房號：{user_input}")
            # 3. 彈出未開放提示
            self.show_wip()
