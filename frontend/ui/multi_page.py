from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QMessageBox, QDialog
from PySide6.QtCore import Qt, Signal
from ui.components import InputDialog # 從零件庫引入輸入框

class MultiplayerPage(QWidget):
    # 發射信號告訴 main.py "我要回首頁了"
    request_home = Signal()

    def __init__(self):
        super().__init__()
        self.setStyleSheet("QWidget { background-color: #2b2b2b; }")
        
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setSpacing(20)

        title = QLabel("雙人連線模式 (P2P)")
        title.setStyleSheet("color: white; font-size: 36px; font-weight: bold;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        # 建立三個選項按鈕
        self.btn_create = self.create_button("建立房間")
        self.btn_join = self.create_button("加入房間")
        self.btn_back = self.create_button("⬅ 回到主選單", bg_color="#f44336", hover_color="#da190b")

        layout.addWidget(self.btn_create)
        layout.addWidget(self.btn_join)
        layout.addWidget(self.btn_back)

        # 綁定按鈕邏輯
        self.btn_back.clicked.connect(self.request_home.emit)
        self.btn_create.clicked.connect(self.handle_create_room)
        self.btn_join.clicked.connect(self.handle_join_room)

    def create_button(self, text, bg_color="#4CAF50", hover_color="#45a049"):
        btn = QPushButton(text)
        btn.setFixedSize(250, 50)
        btn.setStyleSheet(f"""
            QPushButton {{ background-color: {bg_color}; color: white; border-radius: 10px; font-size: 18px; font-weight: bold; }}
            QPushButton:hover {{ background-color: {hover_color}; }}
        """)
        return btn

    def show_wip_dialog(self):
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle("系統提示")
        msg_box.setText("此模式暫未開放！\n(Work In Progress)")
        msg_box.setStyleSheet("QMessageBox { background-color: #2b2b2b; } QLabel { color: white; min-width: 300px; min-height: 80px; font-size: 18px; font-weight: bold; } QPushButton { background-color: #4CAF50; color: white; border-radius: 5px; padding: 8px 20px; font-size: 16px; } QPushButton:hover { background-color: #45a049; }")
        msg_box.exec()

    def handle_create_room(self):
        print("選擇：建立房間")
        # 根據文件，彈出未開放
        self.show_wip_dialog() 

    def handle_join_room(self):
        print("選擇：加入房間")
        # 1. 召喚輸入框
        dialog = InputDialog(self, title="加入房間", prompt="請輸入 P2P 房號 (IP/Port)：")
        # 2. 等待玩家按確認
        if dialog.exec() == QDialog.DialogCode.Accepted:
            user_input = dialog.get_text()
            print(f"嘗試連線至房號：{user_input}")
            # 3. 彈出未開放提示
            self.show_wip_dialog()