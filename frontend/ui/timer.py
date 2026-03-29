import pygame
from settings import TIME_LIMIT

class Timer:
    def __init__(self):
        self.turn_start_time = pygame.time.get_ticks()
        self.remaining_time = TIME_LIMIT

    def get_remain_time(self):
        current_time = pygame.time.get_ticks()
        self.remaining_time = TIME_LIMIT - (current_time - self.turn_start_time) // 1000 # 算出這回合已經經過了幾秒  
        return self.remaining_time

    def reset(self):
        self.turn_start_time = pygame.time.get_ticks() # 超時換人，重置計時器
        self.remaining_time = TIME_LIMIT