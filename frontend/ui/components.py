from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QLineEdit,
    QPushButton,
)
from PySide6.QtGui import QPainter, QPen, QColor, QBrush
from PySide6.QtCore import Qt, Signal, QTimer
from settings import BOARD_SIZE, GRID_SIZE, MARGIN, TIME_LIMIT


class GameTimerLabel(QLabel):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("color: white; font-size: 20px; font-weight: bold;")
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


class GomokuBoard(QWidget):
    clicked_pos = Signal(int, int)  # 當點擊時，發射 (col, row) 的信號

    def __init__(self):
        super().__init__()
        self.board = [[0 for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
        window_size = (BOARD_SIZE - 1) * GRID_SIZE + MARGIN * 2
        self.setFixedSize(window_size, window_size)
        self.setStyleSheet("background-color: #E6B97A;")  # 經典木板色

        # 🌟 魔法 1：開啟滑鼠追蹤 (預設是關閉的)
        # 這樣就算不按下按鈕，滑鼠移動也會觸發 mouseMoveEvent
        self.setMouseTracking(True)

        # 用來記錄滑鼠目前懸停的座標 (col, row)，None 代表沒懸停在格點上
        self.hover_pos = None

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)  # 抗鋸齒，棋子才會圓

        # 1. 畫網格 (保持不變)
        pen = QPen(Qt.black, 2)
        painter.setPen(pen)
        for i in range(BOARD_SIZE):
            x = MARGIN + i * GRID_SIZE
            painter.drawLine(x, MARGIN, x, self.height() - MARGIN)
            y = MARGIN + i * GRID_SIZE
            painter.drawLine(MARGIN, y, self.width() - MARGIN, y)

        # 2. 🌟 魔法 2：畫落子投影 (Hover Preview)
        # 只有在滑鼠有懸停、且該格子是空的情況下才畫
        if self.hover_pos and self.board[self.hover_pos[1]][self.hover_pos[0]] == 0:
            col, row = self.hover_pos
            x = MARGIN + col * GRID_SIZE
            y = MARGIN + row * GRID_SIZE

            # 畫一個半透明的黑子 (用來預覽)
            # 顏色設定：黑色的 RGBA (0, 0, 0, 100)，100 是透明度 (0~255)
            preview_color = QColor(0, 0, 0, 100)
            painter.setBrush(QBrush(preview_color))
            painter.setPen(Qt.PenStyle.NoPen)  # 不要邊框

            radius = GRID_SIZE // 2 - 2
            painter.drawEllipse(x - radius, y - radius, radius * 2, radius * 2)

        # 3. 畫真正的棋子 (保持不變)
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                if self.board[row][col] != 0:
                    x = MARGIN + col * GRID_SIZE
                    y = MARGIN + row * GRID_SIZE
                    color = Qt.black if self.board[row][col] == 1 else Qt.white
                    painter.setBrush(QBrush(color))
                    painter.setPen(QPen(Qt.black, 1))  # 給白子加一點點黑邊框，比較好看
                    radius = GRID_SIZE // 2 - 2
                    painter.drawEllipse(x - radius, y - radius, radius * 2, radius * 2)

    def mouseMoveEvent(self, event):
        """🌟 魔法 3：計算滑鼠懸停格點"""
        # 計算滑鼠最靠近哪一個交叉點
        col = round((event.x() - MARGIN) / GRID_SIZE)
        row = round((event.y() - MARGIN) / GRID_SIZE)

        # 檢查是否在棋盤邊界內
        if 0 <= col < BOARD_SIZE and 0 <= row < BOARD_SIZE:
            new_hover_pos = (col, row)
            # 如果懸停位置改變了，才需要重繪 (節省算力)
            if new_hover_pos != self.hover_pos:
                self.hover_pos = new_hover_pos
                self.update()  # 觸發 paintEvent 重新繪圖
        else:
            # 滑鼠超出棋盤區域，清除投影
            if self.hover_pos is not None:
                self.hover_pos = None
                self.update()

    def leaveEvent(self, event):
        """🌟 魔法 4：當滑鼠離開整個棋盤元件時，清除投影"""
        self.hover_pos = None
        self.update()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            col = round((event.x() - MARGIN) / GRID_SIZE)
            row = round((event.y() - MARGIN) / GRID_SIZE)
            if 0 <= col < BOARD_SIZE and 0 <= row < BOARD_SIZE:
                self.clicked_pos.emit(col, row)

class InputDialog(QDialog):
    """通用的輸入對話框元件"""
    def __init__(self, parent=None, title="輸入", prompt="請輸入內容："):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setFixedSize(300, 150)
        self.setStyleSheet("QDialog { background-color: #2b2b2b; }")

        layout = QVBoxLayout(self)

        self.label = QLabel(prompt)
        self.label.setStyleSheet("color: white; font-size: 16px; font-weight: bold;")
        layout.addWidget(self.label)

        self.input_box = QLineEdit()
        self.input_box.setStyleSheet("""
            QLineEdit {
                background-color: #1e1e1e; color: white; 
                border: 2px solid #555; border-radius: 5px; padding: 5px; font-size: 16px;
            }
            QLineEdit:focus { border: 2px solid #4CAF50; }
        """)
        layout.addWidget(self.input_box)

        btn_layout = QHBoxLayout()
        self.btn_confirm = QPushButton("確認")
        self.btn_cancel = QPushButton("取消")

        btn_style = """
            QPushButton { background-color: #4CAF50; color: white; border-radius: 5px; padding: 8px; font-size: 14px; font-weight: bold; }
            QPushButton:hover { background-color: #45a049; }
        """
        self.btn_confirm.setStyleSheet(btn_style)
        self.btn_cancel.setStyleSheet(btn_style.replace("#4CAF50", "#f44336").replace("#45a049", "#da190b"))

        self.btn_confirm.clicked.connect(self.accept)
        self.btn_cancel.clicked.connect(self.reject)

        btn_layout.addWidget(self.btn_confirm)
        btn_layout.addWidget(self.btn_cancel)
        layout.addLayout(btn_layout)

    def get_text(self):
        return self.input_box.text()