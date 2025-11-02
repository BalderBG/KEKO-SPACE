import pygame
import random
import os
from core import settings


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, speed_range=(3, 7), type="meteorito"):
        super().__init__()
        self.type = type
        self.speed = random.randint(*speed_range)

        # CON ESTO CARGO LOS SPRITES
        if self.type == "meteorito":
            meteor_variants = ["meteorito.png", "trozolunar1.png"]
            chosen_sprite = random.choice(meteor_variants)
            image_path = os.path.join("assets", "obstacles", chosen_sprite)
        else:
            image_path = os.path.join("assets", "obstacles", f"{self.type}.png")

        if os.path.exists(image_path):
            self.image = pygame.image.load(image_path).convert_alpha()
        else:
            # SI NO HAY IMAGEN, SE CREA UN CUADRADO COMO AL PRINCIPIO
            self.image = pygame.Surface((40, 40))
            color = self._get_color_by_type(self.type)
            self.image.fill(color)

        # POSICION DE LOS METEOROS (DERECHA)
        self.rect = self.image.get_rect()
        self.rect.x = settings.SCREEN_WIDTH + random.randint(0, 100)
        self.rect.y = random.randint(0, settings.SCREEN_HEIGHT - self.rect.height)

        #SONIDO DE IMPACTO AL COLISIONAR
        self.hit_sound_path = os.path.join("assets", "sounds", "meteor_hit.ogg")
        if os.path.exists(self.hit_sound_path):
            self.hit_sound = pygame.mixer.Sound(self.hit_sound_path)
            self.hit_sound.set_volume(0.2)
        else:
            self.hit_sound = None
            self.has_played_hit_sound = False

    def _get_color_by_type(self, type_name):
        # DEPENDE DE LO QUE SEA CAMBIA DE COLOR
        colors = {
            "meteorito": (180, 100, 50),
            "cometa": (255, 150, 150),
            "satellite": (200, 200, 255),
            "fuego_espacial": (255, 80, 0),
            "asteroide": (160, 120, 100)
        }
        return colors.get(type_name, (255, 255, 255))

    def update(self):
        self.rect.x -= self.speed

        # Si sale de pantalla se elimina
        if self.rect.right < 0:
            self.kill()

    def play_hit_sound(self):
        if not hasattr(self, "has_played_hit_sound"):
            self.has_played_hit_sound = False 

        if self.hit_sound and not self.has_played_hit_sound:
            self.hit_sound.play()
            self.has_played_hit_sound = True