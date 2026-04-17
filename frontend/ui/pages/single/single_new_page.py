from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
)
from PySide6.QtCore import Qt, Signal
from ui.components import MenuButton, WipDialog


class SingleNewPage(QWidget):
    request_home = Signal()
    request_start_game = Signal()

    def __init__(self, title_text="單人模式 (AI)"):
        super().__init__()

        main_layout = QVBoxLayout(self)
        main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.setSpacing(30)

        # 設定排版
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setSpacing(20)

        title = QLabel(title_text)
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

        # 建立三個選項按鈕
        self.btn_start = MenuButton("開始遊戲", self)
        self.btn_back = MenuButton("返回主選單", self)

        self.btn_undo_enable = True
        self.btn_timer_enable = True
        self.btn_reset_enable = True
        self.btn_can_undo = MenuButton("開啟悔棋功能", self)
        self.btn_can_timer = MenuButton("開啟落子限時", self)
        self.btn_can_reset = MenuButton("開啟重置棋盤", self)

        layout.addWidget(self.btn_start)
        layout.addWidget(self.btn_can_undo)
        layout.addWidget(self.btn_can_timer)
        layout.addWidget(self.btn_can_reset)
        layout.addWidget(self.btn_back)

        main_layout.addLayout(layout)

        # 綁定按鈕邏輯
        self.btn_start.clicked.connect(self.request_start_game.emit)
        self.btn_can_undo.clicked.connect(self.can_undo_onclick)
        self.btn_can_timer.clicked.connect(self.can_timer_onclick)
        self.btn_can_reset.clicked.connect(self.can_reset_onclick)
        self.btn_back.clicked.connect(self.request_home.emit)

    def show_wip(self):
        dialog = WipDialog(self)
        dialog.exec()

    def can_undo_onclick(self):
        self.btn_undo_enable = not self.btn_undo_enable

        if self.btn_undo_enable:
            self.btn_can_undo.setStyleSheet(
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
            self.btn_can_undo.setText("開啟悔棋功能")
        else:
            self.btn_can_undo.setStyleSheet(
                """
              QPushButton { 
                  background-color: #FF0000;
                  color: white;
                  border-radius: 10px;
                  font-size: 18px;
              }
              QPushButton:hover { background-color: #C70000; }
              """
            )
            self.btn_can_undo.setText("關閉悔棋功能")

    def can_timer_onclick(self):
        self.btn_timer_enable = not self.btn_timer_enable

        if self.btn_timer_enable:
            self.btn_can_timer.setStyleSheet(
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
            self.btn_can_timer.setText("開啟落子限時")
        else:
            self.btn_can_timer.setStyleSheet(
                """
              QPushButton { 
                  background-color: #FF0000;
                  color: white;
                  border-radius: 10px;
                  font-size: 18px;
              }
              QPushButton:hover { background-color: #C70000; }
              """
            )
            self.btn_can_timer.setText("關閉落子限時")

    def can_reset_onclick(self):
        self.btn_reset_enable = not self.btn_reset_enable

        if self.btn_reset_enable:
            self.btn_can_reset.setStyleSheet(
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
            self.btn_can_reset.setText("開啟重置棋盤")
        else:
            self.btn_can_reset.setStyleSheet(
                """
              QPushButton { 
                  background-color: #FF0000;
                  color: white;
                  border-radius: 10px;
                  font-size: 18px;
              }
              QPushButton:hover { background-color: #C70000; }
              """
            )
            self.btn_can_reset.setText("關閉重置棋盤")