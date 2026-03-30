from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QPainter, QPen, QColor, QBrush
from PySide6.QtCore import Qt, Signal
from settings import BOARD_SIZE, GRID_SIZE, MARGIN


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
