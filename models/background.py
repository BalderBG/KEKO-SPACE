import pygame
import random

class Star:
    def __init__(self, x, y, speed, size, color):
        self.x = x
        self.y = y
        self.speed = speed
        self.size = size
        self.color = color

    def update(self, width, height):
        self.x -= self.speed
        if self.x < 0:
            self.x = width
            self.y = random.randint(0, height)

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), self.size)


class StarBackground:
    def __init__(self, width, height, num_stars=150):
        self.width = width
        self.height = height
        self.stars = []

        for _ in range(num_stars):
            x = random.randint(0, width)
            y = random.randint(0, height)
            layer = random.choice([1, 2, 3])

            if layer == 1:
                speed = 0.3
                size = 1
                color = (120, 120, 120)
            elif layer == 2:
                speed = 0.6
                size = 2
                color = (180, 180, 180)
            else:
                speed = 1.0
                size = 3
                color = (255, 255, 255)

            self.stars.append(Star(x, y, speed, size, color))

    def update(self):
        for star in self.stars:
            star.update(self.width, self.height)

    def draw(self, surface):
        for star in self.stars:
            star.draw(surface)
