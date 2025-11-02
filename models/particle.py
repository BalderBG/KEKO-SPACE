import pygame
import random

class Particle(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.x, self.y = pos 
        self.radius = random.randint(3, 7)
        self.color= random.choice([
            (255, 180, 50), #Naranja brillante
            (255, 100, 0),  # Fuego intenso maomeno
            (255, 220, 120) # amarillo suave modo jeep
        ])
        self.alpha = 255
        self.speed_y = random.uniform(1,3)
        self.lifetime = random.randint(20, 40)


    def update(self):
        self.y += self.speed_y
        self.radius *= 0.95
        self.alpha -= 10
        self.lifetime -= 1
        if self.alpha <= 0 or self.radius < 1 or self.lifetime <= 0:
            self.kill()

    def draw(self, surface):
        if self.alpha > 9:
            surface.set_alpha(self.alpha)
            pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), int(self.radius))
            surface.set_alpha(255)