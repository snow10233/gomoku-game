import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QStackedWidget
from settings import WINDOW_WIDTH, WINDOW_HEIGHT
from ui.pages import (
    HomePage,
    MultiplayerPage,
    SingalPage,
    SingalGamePage,
    MulitGamePage,
)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("QWidget { background-color: #ccb897; }")
        self.setWindowTitle("C++ Gomoku Qt Edition")
        self.setFixedSize(WINDOW_WIDTH, WINDOW_HEIGHT)

        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        self.home_page = HomePage()

        self.singal_page = SingalPage()
        self.singal_game_page = SingalGamePage()

        self.multi_page = MultiplayerPage()
        self.multi_game_page = MulitGamePage()

        self.stacked_widget.addWidget(self.home_page)  # Index 0

        self.stacked_widget.addWidget(self.singal_page)  # Index 1
        self.stacked_widget.addWidget(self.singal_game_page)  # Index 2

        self.stacked_widget.addWidget(self.multi_page)  # Index 3
        self.stacked_widget.addWidget(self.multi_game_page)  # Index 4

        # 🌟 綁定所有的頁面跳轉邏輯
        self.home_page.request_single_player.connect(self.go_to_singal_page)
        self.home_page.request_multi_player.connect(self.go_to_multi_page)

        self.singal_page.request_home.connect(self.go_to_home_page)
        self.singal_page.request_start_game.connect(self.go_to_singal_game_page)

        self.singal_game_page.request_home.connect(self.go_to_home_page)  # 遊戲 -> 首頁

        self.multi_page.request_home.connect(self.go_to_home_page)  # 雙人 -> 首頁
        # self.multi_page.request_start_game.connect(self.go_to_multi_game_page)  # 雙人 -> 首頁

        self.multi_game_page.request_home.connect(self.go_to_home_page)  # 遊戲 -> 首頁

    def go_to_home_page(self):
        print("切換回主選單，發送 {HOME_PAGE}")
        self.stacked_widget.setCurrentIndex(0)
        self.singal_game_page.end_game()
        self.multi_game_page.end_game()

    def go_to_singal_page(self):
        self.stacked_widget.setCurrentIndex(1)

    def go_to_singal_game_page(self):
        print("切換至遊戲畫面，發送 {AI_MODE}")
        self.stacked_widget.setCurrentIndex(2)
        self.singal_game_page.start_game()  # 🌟 切換過去時，順便啟動計時器和清空棋盤

    def go_to_multi_page(self):
        self.stacked_widget.setCurrentIndex(3)

    def go_to_multi_game_page(self):
        print("切換至遊戲畫面，發送 {TWO_PLAYER_MODE}")
        self.stacked_widget.setCurrentIndex(4)
        self.multi_game_page.start_game()  # 🌟 切換過去時，順便啟動計時器和清空棋盤


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
