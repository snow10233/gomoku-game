import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QStackedWidget, QFileDialog
from settings import WINDOW_WIDTH, WINDOW_HEIGHT
from ui.navigation import Route, Router
from ui.pages import (
    HomePage,
    MultiChooseModePage,
    MultiGamePage,
    MultiLocalChooseModePage,
    MultiLocalNewPage,
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
        self.multi_choose_mode_page = MultiChooseModePage()
        self.multi_local_choose_mode_page = MultiLocalChooseModePage()
        self.multi_local_new_page = MultiLocalNewPage()
        self.multi_game_page = MultiGamePage()
        self.multi_remote_page = MultiRemotePage()

        self.router.register(Route.HOME, self.home_page)
        self.router.register(Route.SINGLE_CHOOSE_MODE, self.single_choose_mode_page)
        self.router.register(Route.SINGLE_NEW_GAME, self.single_new_page)
        self.router.register(Route.SINGLE_GAME, self.single_game_page)
        self.router.register(Route.MULTI_CHOOSE_MODE, self.multi_choose_mode_page)
        self.router.register(
            Route.MULTI_LOCAL_CHOOSE_MODE, self.multi_local_choose_mode_page
        )
        self.router.register(Route.MULTI_NEW_GAME, self.multi_local_new_page)
        self.router.register(Route.MULTI_GAME, self.multi_game_page)
        self.router.register(Route.MULTI_REMOTE, self.multi_remote_page)
        self.router.go(Route.HOME)

        # 🌟 綁定所有的頁面跳轉邏輯
        self.home_page.request_single_player.connect(self.go_to_single_choose_mode_page)
        self.home_page.request_multi_player.connect(self.go_to_multi_choose_mode_page)

        self.single_new_page.request_home.connect(self.go_to_home_page)
        self.single_new_page.request_start_game.connect(self.go_to_single_game_page)

        self.single_game_page.request_home.connect(self.go_to_home_page)  # 遊戲 -> 首頁

        self.multi_choose_mode_page.request_local_game.connect(
            self.go_to_multi_local_choose_mode_page
        )
        self.multi_choose_mode_page.request_remote_game.connect(
            self.go_to_multi_remote_page
        )
        self.multi_choose_mode_page.request_home.connect(self.go_to_home_page)

        self.multi_local_choose_mode_page.request_new_game.connect(
            self.go_to_multi_new_page
        )
        self.multi_local_choose_mode_page.request_load_game.connect(
            self.load_multi_game
        )
        self.multi_local_choose_mode_page.request_home.connect(self.go_to_home_page)

        self.multi_local_new_page.request_home.connect(self.go_to_home_page)
        self.multi_local_new_page.request_start_game.connect(self.go_to_multi_game_page)

        self.multi_game_page.request_home.connect(self.go_to_home_page)
        self.multi_remote_page.request_home.connect(
            self.go_to_home_page
        )  # 雙人 -> 首頁

        self.single_choose_mode_page.request_new_game.connect(
            self.go_to_single_new_page
        )
        self.single_choose_mode_page.request_load_game.connect(self.load_single_game)
        self.single_choose_mode_page.request_home.connect(self.go_to_home_page)

    def go_to_home_page(self):
        print("切換回主選單，發送 {HOME_PAGE}")

        current_route = self.router.current_route()
        if current_route == Route.SINGLE_GAME:
            self.single_game_page.end_game()
        elif current_route == Route.MULTI_GAME:
            self.multi_game_page.end_game()
        self.router.go(Route.HOME)

    def go_to_single_choose_mode_page(self):
        self.router.go(Route.SINGLE_CHOOSE_MODE)

    def go_to_multi_choose_mode_page(self):
        self.router.go(Route.MULTI_CHOOSE_MODE)

    def go_to_multi_local_choose_mode_page(self):
        self.router.go(Route.MULTI_LOCAL_CHOOSE_MODE)

    def go_to_single_new_page(self):
        self.router.go(Route.SINGLE_NEW_GAME)

    def go_to_multi_new_page(self):
        self.router.go(Route.MULTI_NEW_GAME)

    def go_to_single_game_page(self):
        # print("切換至遊戲畫面，發送 {AI_MODE}")
        self.router.go(Route.SINGLE_GAME)
        undo_enable = self.single_new_page.btn_undo_enable
        timer_enable = self.single_new_page.btn_timer_enable
        reset_enable = self.single_new_page.btn_reset_enable
        self.single_game_page.start_game(undo_enable, timer_enable, reset_enable)

    def go_to_multi_remote_page(self):
        self.router.go(Route.MULTI_REMOTE)

    def go_to_multi_game_page(self):
        self.router.go(Route.MULTI_GAME)
        undo_enable = self.multi_local_new_page.btn_undo_enable
        timer_enable = self.multi_local_new_page.btn_timer_enable
        reset_enable = self.multi_local_new_page.btn_reset_enable
        self.multi_game_page.start_game(undo_enable, timer_enable, reset_enable)

    def load_single_game(self):
        """打开文件选择对话框来加载单人游戏"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "选择要加载的游戏文件", "", "Gomoku Files (*.pgn);;All Files (*)"
        )
        if file_path:
            print(f"加载单人游戏文件: {file_path}")
            # TODO: 实现游戏加载逻辑
            self.go_to_single_game_page()

    def load_multi_game(self):
        """打开文件选择对话框来加载本地双人游戏"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "选择要加载的游戏文件", "", "Gomoku Files (*.pgn);;All Files (*)"
        )
        if file_path:
            print(f"加载双人游戏文件: {file_path}")
            # TODO: 实现游戏加载逻辑
            self.go_to_multi_game_page()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
