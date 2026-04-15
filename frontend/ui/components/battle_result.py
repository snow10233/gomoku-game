from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont
from ui.components import GameButton
from settings import WINDOW_WIDTH, WINDOW_HEIGHT


class BattleResult(QWidget):
    request_home = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        # 1. 設置半透明背景 (降低亮度效果)
        self.setStyleSheet("background-color: rgba(0, 0, 0, 180);")
        # 讓背景能夠接受點擊事件，阻止點擊穿透到下方的棋盤
        self.setAttribute(Qt.WA_StyledBackground, True)

        # 讓 Overlay 充滿整個視窗
        self.setGeometry(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT)

        # 2. 佈局設計
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(30)

        # 勝利標籤 (置中)
        self.label = QLabel("請輸入文本", self)
        self.label.setStyleSheet("color: gold; background: transparent;")
        self.label.setFont(QFont("Arial", 48, QFont.Bold))
        self.label.setAlignment(Qt.AlignCenter)

        # 返回按鈕
        self.btn_back = GameButton("返回首頁", self)
        self.btn_back.clicked.connect(self.handle_back_home)

        # 3. 安排位置：標籤在中上，按鈕在中下
        layout.addWidget(self.label, alignment=Qt.AlignCenter)
        layout.addWidget(self.btn_back, alignment=Qt.AlignCenter)

        self.setVisible(False)  # 預設隱藏

    def show_result(self, text):
        self.label.setText(text)
        parent = self.parentWidget()
        if parent is not None:
            # 顯示前同步覆蓋層大小，避免父層尺寸變動後無法完整覆蓋
            self.setGeometry(parent.rect())
        # 強制提到最上層，避免被棋盤或其他元件遮住
        self.raise_()
        self.show()
        self.activateWindow()

    def handle_back_home(self):
        self.hide()
        self.request_home.emit()
