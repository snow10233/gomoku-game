import pygame
import sys
from core.engine_bridge import GomokuEngine
from ui.gomoku_window import Window
from settings import BOARD_SIZE
from ui.timer import Timer

def main():
    # === 初始化 Pygame ===
    pygame.init()
    engine = GomokuEngine()
    window = Window()
    timer = Timer()
    clock = pygame.time.Clock()
    current_player = 1 # 0=空, 1=黑, 2=白

    # 測試用 先不加進主迴圈
    engine.send_game_mode("AI_MODE")

    # === 遊戲主迴圈 ===
    running = True
    while running:
        window.draw_board()
        window.draw_chess()

        remaining_time = timer.get_remain_time()# 算出剩下幾秒

        # 檢查是否超時
        if remaining_time <= 0:
            print(f"玩家 {current_player} 超時！自動換對手下棋。")
            current_player = 2 if current_player == 1 else 1
            timer.reset()

        window.draw_timer(remaining_time, current_player)

        pygame.display.flip() # 更新畫面
        clock.tick(60)

        # 監聽玩家的動作
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            # 當玩家點擊滑鼠左鍵
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                x, y = event.pos
                col, row = window.get_chess_pos(x, y)
                
                # 檢查有沒有點在棋盤的合法範圍內
                if window.is_pos_valid(col, row):
                    print(f"前端抓到點擊！ 行(row)={row}, 列(col)={col}")
                    engine.send_action("PUT_CHESS")
                    res, state, ai_x, ai_y = engine.put_chess(row, col)
                    print(f"後端說：落子{res}, 目前狀態{state}, AI下({ai_x}, {ai_y})")
                    window.put_chess_in_screen(col, row, current_player)
                    current_player = 2 if current_player == 1 else 1
                    timer.reset()

if __name__ == "__main__":
    main()
    sys.exit()