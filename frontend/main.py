import pygame
import sys

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

# === 2. 初始化 Pygame ===
pygame.init()
screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
pygame.display.set_caption("Pygame - gomoku test")

#計時器
font = pygame.font.SysFont("Arial", 30) 
clock = pygame.time.Clock()

# 前端自己暫存的假盤面 (測試畫圖用，0=空, 1=黑, 2=白)
board = [[0 for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
current_player = 1 

TIME_LIMIT = 60  # 每步限制 60 秒
turn_start_time = pygame.time.get_ticks()

def draw_board():
    """負責畫出背景跟 15x15 的網格線"""
    screen.fill(COLOR_BG)
    for i in range(BOARD_SIZE):
        # 畫垂直線
        start_y = MARGIN
        end_y = WINDOW_SIZE - MARGIN
        x = MARGIN + i * GRID_WIDTH
        pygame.draw.line(screen, COLOR_LINE, (x, start_y), (x, end_y), 2)
        
        # 畫水平線
        start_x = MARGIN
        end_x = WINDOW_SIZE - MARGIN
        y = MARGIN + i * GRID_WIDTH
        pygame.draw.line(screen, COLOR_LINE, (start_x, y), (end_x, y), 2)

def draw_chess():
    """掃描陣列，把棋子畫到對應的交叉點上"""
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            if board[row][col] != 0:
                # 把陣列的 row, col 反向推算回螢幕上的像素 x, y
                x = MARGIN + col * GRID_WIDTH
                y = MARGIN + row * GRID_WIDTH
                color = COLOR_BLACK if board[row][col] == 1 else COLOR_WHITE
                # 畫圓形 (畫布, 顏色, 圓心座標, 半徑)
                pygame.draw.circle(screen, color, (x, y), GRID_WIDTH // 2 - 2)

# === 3. 遊戲主迴圈 (Game Loop) ===
running = True
while running:
    draw_board()
    draw_chess()

    current_time = pygame.time.get_ticks()
    elapsed_seconds = (current_time - turn_start_time) // 1000 # 算出這回合已經經過了幾秒
    remaining_time = TIME_LIMIT - elapsed_seconds              # 算出剩下幾秒

    # 檢查是否超時
    if remaining_time <= 0:
        print(f"玩家 {current_player} 超時！自動換對手下棋。")
        current_player = 2 if current_player == 1 else 1
        turn_start_time = pygame.time.get_ticks() # 超時換人，重置計時器
        remaining_time = TIME_LIMIT

    # 🚀 3. 繪製計時器文字 (順便顯示現在是誰的回合)
    player_name = "Black" if current_player == 1 else "White"
    # 為了讓畫面更好看，白子回合時文字用深灰色顯示
    text_color = COLOR_BLACK if current_player == 1 else (80, 80, 80) 
    timer_text = f"{player_name} Turn | Time: {remaining_time}s"
    
    text_surface = font.render(timer_text, True, text_color)
    text_rect = text_surface.get_rect(center=(WINDOW_SIZE // 2, 30))
    screen.blit(text_surface, text_rect)

    pygame.display.flip() # 更新畫面
    clock.tick(60)

    # 監聽玩家的動作
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        # 當玩家點擊滑鼠左鍵
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_x, mouse_y = event.pos
            
            # 【前端最核心的數學】
            # 把滑鼠的像素座標，用「四捨五入」找最近的交叉點，轉回 0~14 的索引
            col = round((mouse_x - MARGIN) / GRID_WIDTH)
            row = round((mouse_y - MARGIN) / GRID_WIDTH)
            
            # 檢查有沒有點在棋盤的合法範圍內
            if 0 <= col < BOARD_SIZE and 0 <= row < BOARD_SIZE:
                if board[row][col] == 0:
                    print(f"前端抓到點擊！ 行(row)={row}, 列(col)={col}")
                    
                    # ==========================================
                    # 🚀 未來跟你的 C++ 結合的地方：
                    # 這裡不要直接改 board，而是把字串傳給你的 C++
                    # 例如透過 subprocess: cpp_engine.stdin.write(f"{col} {row}\n")
                    # 然後等待 C++ 回傳結果，再來決定要畫什麼顏色
                    # ==========================================
                    
                    # (現在先假裝下棋，為了給你看視覺效果)
                    board[row][col] = current_player
                    current_player = 2 if current_player == 1 else 1

                    #重製計時器
                    turn_start_time = pygame.time.get_ticks()

pygame.quit()
sys.exit()