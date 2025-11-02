class Score:
    def __init__(self):
        self.points = 0
        self.last_update = 0
        self.update_interval = 200


    def update(self):
        import pygame
        now = pygame.time.get_ticks()
        if now - self.last_update >= self.update_interval:
            self.points += 2.5
            self.last_update = now


    def reset(self):
        self.points = 0
        self.last_update = 0