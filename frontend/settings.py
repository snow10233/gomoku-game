# === 1. 基本設定與常數 ===
BOARD_SIZE = 15
GRID_WIDTH = 40  # 每一格的寬度 (像素)
MARGIN = 60      # 棋盤距離視窗邊緣的空白距離

# 視窗總大小 = (14個間距 * 40) + 左右兩邊的邊距
WINDOW_SIZE = (BOARD_SIZE - 1) * GRID_WIDTH + MARGIN * 2

# 顏色定義 (RGB)
COLOR_BG = (222, 184, 135)  # 經典原木色
COLOR_LINE = (0, 0, 0)      # 黑線
COLOR_BLACK = (0, 0, 0)     # 黑子
COLOR_WHITE = (255, 255, 255) # 白子

TIME_LIMIT = 60  # 每步限制 60 秒