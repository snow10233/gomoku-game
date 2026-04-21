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
    ReplayPage,
    SingleNewPage,
    SingleGamePage,
    SingleChooseModePage,
)
from assets.audio.audio_manager import AudioManager

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
        self.replay_page = ReplayPage()

        # 初始化音效管理器
        self.audio = AudioManager()

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

        #2. 啟動首頁音樂
        self.audio.play_bgm("menu")

        # 🌟 綁定所有的頁面跳轉邏輯
        self.home_page.request_single_player.connect(self.go_to_single_choose_mode_page)
        self.home_page.request_multi_player.connect(self.go_to_multi_choose_mode_page)

        self.single_new_page.request_home.connect(self.go_to_home_page)
        self.single_new_page.request_start_game.connect(self.go_to_single_game_page)

        self.single_game_page.request_home.connect(self.go_to_home_page)  # 遊戲 -> 首頁

        # 🌟 綁定勝負音效信號
        self.single_game_page.win_signal.connect(lambda: self.audio.play_sfx("victory"))
        self.single_game_page.lose_signal.connect(lambda: self.audio.play_sfx("defeat"))

        # 綁定落子音效信號
        self.single_game_page.place_signal.connect(lambda: self.audio.play_sfx("place"))

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

        self.audio.play_bgm("menu", fade_ms=1500)

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

        self.audio.play_bgm("play", fade_ms=1000)
        
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
        self._load_game_file(expected_mode="AI_MODE")

    def load_multi_game(self):
        self._load_game_file(expected_mode="TWO_PLAYER_MODE")

    def _load_game_file(self, expected_mode):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "選擇要載入的棋局檔", "", "Gomoku Files (*.gmk);;All Files (*)"
        )
        if not file_path:
            return

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                sub_mode = f.readline().strip()
                replay = f.readline().strip()
        except OSError as err:
            print(f"讀取棋局檔失敗: {err}")
            return

        if sub_mode != expected_mode:
            print(f"棋局檔模式不符，檔案為 {sub_mode}，此入口為 {expected_mode}")
            return

        target_page = (
            self.single_game_page
            if sub_mode == "AI_MODE"
            else self.multi_game_page
        )

        if sub_mode == "AI_MODE":
            self.router.go(Route.SINGLE_GAME)
            self.audio.play_bgm("play", fade_ms=1000)
        else:
            self.router.go(Route.MULTI_GAME)

        target_page.resume_from_replay(sub_mode, replay)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
