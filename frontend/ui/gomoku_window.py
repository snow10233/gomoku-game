import pygame
from settings import WINDOW_SIZE, COLOR_BG, BOARD_SIZE, MARGIN, GRID_WIDTH, COLOR_LINE, COLOR_WHITE, COLOR_BLACK

class Window:
    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
        self.font = pygame.font.SysFont("Arial", 30) 
        pygame.display.set_caption("Gomoku")
        self.board = [[0 for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]

    def draw_board(self):
        """負責畫出背景跟 15x15 的網格線"""
        self.screen.fill(COLOR_BG)
        for i in range(BOARD_SIZE):
            # 畫垂直線
            start_y = MARGIN
            end_y = WINDOW_SIZE - MARGIN
            x = MARGIN + i * GRID_WIDTH
            pygame.draw.line(self.screen, COLOR_LINE, (x, start_y), (x, end_y), 2)
            
            # 畫水平線
            start_x = MARGIN
            end_x = WINDOW_SIZE - MARGIN
            y = MARGIN + i * GRID_WIDTH
            pygame.draw.line(self.screen, COLOR_LINE, (start_x, y), (end_x, y), 2)

    def draw_chess(self):
        """掃描陣列，把棋子畫到對應的交叉點上"""
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                if self.board[row][col] != 0:
                    # 把陣列的 row, col 反向推算回螢幕上的像素 x, y
                    x = MARGIN + col * GRID_WIDTH
                    y = MARGIN + row * GRID_WIDTH
                    color = COLOR_BLACK if self.board[row][col] == 1 else COLOR_WHITE
                    # 畫圓形 (畫布, 顏色, 圓心座標, 半徑)
                    pygame.draw.circle(self.screen, color, (x, y), GRID_WIDTH // 2 - 2)

    def get_chess_pos(self, x, y):
        col = round((x - MARGIN) / GRID_WIDTH)
        row = round((y - MARGIN) / GRID_WIDTH)
        return col, row
    
    def is_pos_valid(self, col, row):
        return self.board[row][col] == 0 and 0 <= col < BOARD_SIZE and 0 <= row < BOARD_SIZE
    
    def put_chess_in_screen(self, col, row, current_player):
        self.board[row][col] = current_player

    def draw_timer(self, remaining_time, current_player):
        player_name = "Black" if current_player == 1 else "White"
        # 為了讓畫面更好看，白子回合時文字用深灰色顯示
        text_color = (200, 200, 200) if current_player == 1 else (80, 80, 80) 
        timer_text = f"{player_name} Turn | Time: {remaining_time}s"
        text_surface = self.font.render(timer_text, True, text_color)
        text_rect = text_surface.get_rect(center=(WINDOW_SIZE // 2, 30))
        self.screen.blit(text_surface, text_rect)

    def close(self):
        pygame.quit()