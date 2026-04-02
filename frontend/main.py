import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QStackedWidget
from settings import WINDOW_WIDTH, WINDOW_HEIGHT
from ui.pages import (
    HomePage,
    MultiplayerPage,
    SingleNewPage,
    SingleGamePage,
    MulitGamePage,
    SingleChooseModePage,
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
        self.single_choose_mode_page = SingleChooseModePage()
        self.single_new_page = SingleNewPage()
        self.single_game_page = SingleGamePage()
        self.multi_page = MultiplayerPage()
        # self.multi_game_page = MulitGamePage()

        self.stacked_widget.addWidget(self.home_page)  # Index 0
        self.stacked_widget.addWidget(self.single_choose_mode_page)  # Index 1
        self.stacked_widget.addWidget(self.single_new_page)  # Index 2
        self.stacked_widget.addWidget(self.single_game_page)  # Index 3
        self.stacked_widget.addWidget(self.multi_page)  # Index 4
        # self.stacked_widget.addWidget(self.multi_game_page)  # Index 5

        self.stacked_widget.setCurrentIndex(0)

        # 🌟 綁定所有的頁面跳轉邏輯
        self.home_page.request_single_player.connect(self.go_to_new_or_load_page)
        self.home_page.request_multi_player.connect(self.go_to_multi_page)

        self.single_new_page.request_home.connect(self.go_to_home_page)
        self.single_new_page.request_start_game.connect(self.go_to_single_game_page)

        self.single_game_page.request_home.connect(self.go_to_home_page)  # 遊戲 -> 首頁

        self.multi_page.request_home.connect(self.go_to_home_page)  # 雙人 -> 首頁
        # self.multi_page.request_start_game.connect(self.go_to_multi_game_page)  # 雙人 -> 首頁

        # self.multi_game_page.request_home.connect(self.go_to_home_page)  # 遊戲 -> 首頁

        self.single_choose_mode_page.request_new_game.connect(
            self.go_to_single_new_page
        )
        # self.single_choose_mode_page.request_load_game.connect(self.go_to_load_game)
        self.single_choose_mode_page.request_home.connect(self.go_to_home_page)

    def go_to_home_page(self):
        print("切換回主選單，發送 {HOME_PAGE}")

        if self.stacked_widget.currentIndex() == 3:
            self.single_game_page.end_game()
        # elif self.stacked_widget.currentIndex() == 5:
        #     self.multi_game_page.end_game()
        self.stacked_widget.setCurrentIndex(0)

    def go_to_new_or_load_page(self):
        self.stacked_widget.setCurrentIndex(1)

    def go_to_single_new_page(self):
        self.stacked_widget.setCurrentIndex(2)

    def go_to_single_game_page(self):
        # print("切換至遊戲畫面，發送 {AI_MODE}")
        self.stacked_widget.setCurrentIndex(3)
        undo_enable = self.single_new_page.btn_undo_enable
        timer_enable = self.single_new_page.btn_timer_enable
        # print(f"undo:{undo_enable}, timer:{timer_enable}")
        self.single_game_page.start_game(undo_enable, timer_enable)

    def go_to_multi_page(self):
        self.stacked_widget.setCurrentIndex(4)

    # def go_to_multi_game_page(self):
    #     # print("切換至遊戲畫面，發送 {TWO_PLAYER_MODE}")
    #     self.stacked_widget.setCurrentIndex(5)
    #     self.multi_game_page.start_game()  # 🌟 切換過去時，順便啟動計時器和清空棋盤


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
