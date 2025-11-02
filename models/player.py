import pygame
import os
from core import settings

class Player(pygame.sprite.Sprite):
    def __init__(self, image=None):
        super().__init__()
        # PNG DE LA NAVESITA
        ship_path = os.path.join("assets", "player", "nave.png")

        if os.path.exists(ship_path):
            self.image = pygame.image.load(ship_path).convert_alpha()
        else:
            # Dibujito por si no sale el sprite
            self.image = pygame.Surface((50, 30), pygame.SRCALPHA)
            self.image.fill((0, 180, 200))

        self.rect = self.image.get_rect()
        self.rect.topleft = settings.PLAYER_START_POS


        #Movimiento

        self.base_speed = settings.PLAYER_SPEED
        self.speed = 0
        self.max_speed = self.base_speed * 2.5
        self.acceleration = 0.5
        self.deceleration = 0.3

        #Vidas
        self.lives = 3
        self.is_alive = True 

        #Invulnerabilidad
        self.last_hit_time = 0
        self.invulnerability_ms = 2000

        #Mensaje de invulnerabilidad
        self.hit_message = None
        self.hit_message_start = 0
        self.hit_message_duration = 1400

        # Sonido del motor
        sound_path = os.path.join("assets", "sounds", "motor.wav")
        if os.path.exists(sound_path):
            self.engine_sound = pygame.mixer.Sound(sound_path)
            self.engine_sound.set_volume(0.1)
        else:
            self.engine_sound = None

        self.engine_playing = False   # flag para controlar si suena o no
        self.engine_volume = 0.1
        self.max_volume = 0.3
        self.volume_step = 0.2


    def update(self, key_pressed=None):
        if key_pressed is None:
            return
        
        #Aceleracion arriba o abajo
        if key_pressed[pygame.K_UP]:
            self.speed -= self.acceleration
        elif key_pressed[pygame.K_DOWN]:
            self.speed += self.acceleration
        else:                               #Con esto hacemos una frenada mas disimulada al no pulsar ningun boton
            if self.speed > 0:
                self.speed = max(0, self.speed - self.deceleration)
            elif self.speed < 0:
                self.speed = min(0, self.speed + self.deceleration)


        #Limito aqui la velocidad maxima
        self.speed = max(-self.max_speed, min(self.speed, self.max_speed))

        #Movimiento vertical
        self.rect.y += int(self.speed)

        if self.rect.top < 0:
            self.rect.top = 0
            self.speed = 0


        elif self.rect.bottom > settings.SCREEN_HEIGHT:
            self.rect.bottom = settings.SCREEN_HEIGHT
            self.speed = 0


        now = pygame.time.get_ticks()
        if now - self.last_hit_time < self.invulnerability_ms:
            if (now // 100) % 2 == 0:
                self.image.set_alpha(100) # semitransparente
            else:
                self.image.set_alpha(255) #Aqui se ve entero
        else:
            self.image.set_alpha(255) 

        self.lives = max(0, min(self.lives, 3))


        # Control dinamico del volumen del motor
        if self.engine_sound:
            if key_pressed[pygame.K_UP] or key_pressed[pygame.K_DOWN]:
                # Si no está sonando, reproducir
                if not self.engine_playing:
                    self.engine_sound.play()
                    self.engine_playing = True

                # Subir volumen progresivamente mientras se mantiene pulsado
                self.engine_volume = min(self.engine_volume + self.volume_step, self.max_volume)
                self.engine_sound.set_volume(self.engine_volume)

            else:
                # Soltar tecla reduce el volumen progesivamente y cuando se detiene se queda en el minimo
                if self.engine_playing:
                    # Bajada más suave del volumen
                    self.engine_volume = max(self.engine_volume - (self.volume_step / 3), 0)
                    self.engine_sound.set_volume(self.engine_volume)

                    # Cuando llega casi a 0, hace un fade de salida y se detiene
                    if self.engine_volume <= 0.05:
                        self.engine_sound.fadeout(300)  # 300 ms de desvanecimiento
                        self.engine_playing = False




    def hit(self):
        now = pygame.time.get_ticks()
        if now - self.last_hit_time > self.invulnerability_ms:
            self.lives -= 1
            self.last_hit_time = now
            self.hit_message = "CUIDADO.."
            self.hit_message_start = now
            
        if self.lives <= 0:
            self.is_alive = False
