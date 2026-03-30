from PySide6.QtWidgets import QLabel
from PySide6.QtCore import QTimer
from settings import TIME_LIMIT


class GameTimerLabel(QLabel):
    def __init__(self):
        super().__init__()
        self.setStyleSheet(
            "background-color: green;"
            "color: black;"
            "min-wdith: 250px"
            "font-size: 50px;"
            "font-weight: bold;"
        )
        self.remaining_time = TIME_LIMIT
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.count_down)
        self.update_display()

    def start_timer(self):
        self.remaining_time = TIME_LIMIT
        self.update_display()
        self.timer.start(1000)

    def count_down(self):
        if self.remaining_time > 0:
            self.remaining_time -= 1
            self.update_display()
        else:
            self.timer.stop()
            self.setText("時間到！")
            # 這裡之後可以發送 OVER_TIME 信號

    def update_display(self):
        self.setText(f"剩餘時間: {self.remaining_time} s")

    def reset(self):
        self.timer.stop()
        self.start_timer()
