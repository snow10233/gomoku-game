import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QStackedWidget
from settings import WINDOW_WIDTH, WINDOW_HEIGHT
from ui.navigation import Route, Router
from ui.pages import (
    HomePage,
    MultiRemotePage,
    SingleNewPage,
    SingleGamePage,
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
        self.router = Router(self.stacked_widget)

        self.home_page = HomePage()
        self.single_choose_mode_page = SingleChooseModePage()
        self.single_new_page = SingleNewPage()
        self.single_game_page = SingleGamePage()
        self.multi_remote_page = MultiRemotePage()

        self.router.register(Route.HOME, self.home_page)
        self.router.register(Route.SINGLE_CHOOSE_MODE, self.single_choose_mode_page)
        self.router.register(Route.SINGLE_NEW_GAME, self.single_new_page)
        self.router.register(Route.SINGLE_GAME, self.single_game_page)
        self.router.register(Route.MULTI_REMOTE, self.multi_remote_page)
        self.router.go(Route.HOME)

        # 🌟 綁定所有的頁面跳轉邏輯
        self.home_page.request_single_player.connect(self.go_to_single_choose_mode_page)
        self.home_page.request_multi_player.connect(self.go_to_multi_remote_page)

        self.single_new_page.request_home.connect(self.go_to_home_page)
        self.single_new_page.request_start_game.connect(self.go_to_single_game_page)

        self.single_game_page.request_home.connect(self.go_to_home_page)  # 遊戲 -> 首頁

        self.multi_remote_page.request_home.connect(self.go_to_home_page)  # 雙人 -> 首頁

        self.single_choose_mode_page.request_new_game.connect(
            self.go_to_single_new_page
        )
        # self.single_choose_mode_page.request_load_game.connect(self.go_to_load_game)
        self.single_choose_mode_page.request_home.connect(self.go_to_home_page)

    def go_to_home_page(self):
        print("切換回主選單，發送 {HOME_PAGE}")

        current_route = self.router.current_route()
        if current_route == Route.SINGLE_GAME:
            self.single_game_page.end_game()
        self.router.go(Route.HOME)

    def go_to_single_choose_mode_page(self):
        self.router.go(Route.SINGLE_CHOOSE_MODE)

    def go_to_single_new_page(self):
        self.router.go(Route.SINGLE_NEW_GAME)

    def go_to_single_game_page(self):
        # print("切換至遊戲畫面，發送 {AI_MODE}")
        self.router.go(Route.SINGLE_GAME)
        undo_enable = self.single_new_page.btn_undo_enable
        timer_enable = self.single_new_page.btn_timer_enable
        reset_enable = self.single_new_page.btn_reset_enable
        self.single_game_page.start_game(undo_enable, timer_enable, reset_enable)

    def go_to_multi_remote_page(self):
        self.router.go(Route.MULTI_REMOTE)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
