import pygame
import os
import math
import random
from core import settings
from models.player import Player
from models.obstacle import Obstacle
from models.score import Score
from models.database import ScoreDataBase
from models.level import Level
from models.particle import Particle
from models.transition import takeoff_sequence
from models.background import StarBackground
from views.ui import (
    level_transition,
    landing_sequence,
    ending_sequence,
    show_highscores,
    show_game_over,
    get_initials,
    intro_story
)


class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        self.screen = pygame.display.set_mode((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))
        pygame.display.set_caption("KEKO SPACE")
        self.clock = pygame.time.Clock()

        # Objetos principales
        self.player = Player()
        self.all_sprites = pygame.sprite.Group(self.player)
        self.obstacles = pygame.sprite.Group()
        self.spawn_timer = 0
        self.running = True
        self.score = Score()
        self.db = ScoreDataBase()
        self.level_duration = 90000
        self.level_start_time = pygame.time.get_ticks()
        self.level_complete = False
        self.level = Level("core/levels.json")
        self.background = StarBackground(settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT)

        # Musica de fondo (loop infinito)
        self.music_path = os.path.join("assets", "music", "cosmicchase.mp3")
        if os.path.exists(self.music_path):
            pygame.mixer.music.load(self.music_path)
            pygame.mixer.music.set_volume(0.3)  # volumen medio
            pygame.mixer.music.play(-1)  # bucle infinito

        # Transición inicial de nivel
        level_transition(self.screen, self.level)

        # Datos del nivel actual
        self.level_data = self.level.get_current()

        bg_image_path = self.level.get_background()
        if bg_image_path and os.path.exists(bg_image_path):
            self.bg_image = pygame.image.load(bg_image_path).convert()
        else:
            self.bg_image = None

        self.spawn_interval = self.level_data["spawn_interval"]
        self.bg_color = self.level_data["bg_color"]

    def run(self):
        while self.running:
            dt = self.clock.tick(settings.FPS)
            self.spawn_timer += dt

            # Eventos
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            # Movimiento del jugador
            keys = pygame.key.get_pressed()
            self.player.update(keys)

            # Generar obstáculos
            if self.spawn_timer >= self.spawn_interval:
                obstacle_type = self.level.get_obstacle_type()
                speed_range = self.level_data["speed_range"]
                obstacle = Obstacle(speed_range=speed_range, type=obstacle_type)

                if obstacle_type == "meteorito":
                    obstacle = Obstacle(speed_range=speed_range)
                elif obstacle_type == "satellite":
                    obstacle = Obstacle(speed_range=speed_range)
                    obstacle.image.fill((200, 200, 255))
                elif obstacle_type == "cometa":
                    obstacle = Obstacle(speed_range=speed_range)
                    obstacle.image.fill((255, 150, 150))
                elif obstacle_type == "fuego_espacial":
                    obstacle = Obstacle(speed_range=speed_range)
                    obstacle.image.fill((255, 80, 0))
                else:
                    obstacle = Obstacle(speed_range=speed_range)

                self.obstacles.add(obstacle)
                self.all_sprites.add(obstacle)
                self.spawn_timer = 0

            self.obstacles.update()

            # Colisiones
            if pygame.sprite.spritecollideany(self.player, self.obstacles):
                for obstacle in self.obstacles:
                    if self.player.rect.colliderect(obstacle.rect):
                        obstacle.play_hit_sound()
                        break
                self.player.hit()

            self.score.update()

            # Dibujado
            self.screen.fill((0, 0, 0))  # Fondo negro
            self.background.update()
            self.background.draw(self.screen)

            # Fondo del nivel (si tiene imagen)
            if self.bg_image:
                self.screen.blit(self.bg_image, (0, 0))

            # Sprites
            self.all_sprites.draw(self.screen)

            # HUD
            font = pygame.font.SysFont(None, 24)
            lives_surf = font.render(f"Vidas: {self.player.lives}", True, (255, 255, 255))
            score_surf = font.render(f"Puntos: {self.score.points}", True, (255, 255, 255))
            self.screen.blit(lives_surf, (520, 20))
            self.screen.blit(score_surf, (620, 20))

            # Mensaje de golpe
            now = pygame.time.get_ticks()
            if self.player.hit_message and now - self.player.hit_message_start < self.player.hit_message_duration:
                msg_font = pygame.font.SysFont(None, 36)
                text_surf = msg_font.render(self.player.hit_message, True, (255, 80, 80))
                text_rect = text_surf.get_rect(center=(settings.SCREEN_WIDTH // 2, 100))
                self.screen.blit(text_surf, text_rect)
            else:
                self.player.hit_message = None

            pygame.display.flip()

            # Comprobar fin de nivel
            if self.level.is_level_complete():
                landing_sequence(self.screen, self.player, self.score, self.level)
                takeoff_sequence(self.screen, self.player, self.level)

                if self.level.next_level():
                    self.level_data = self.level.get_current()
                    self.spawn_interval = self.level_data["spawn_interval"]
                    self.bg_color = self.level_data["bg_color"]
                    self.obstacles.empty()
                    self.all_sprites = pygame.sprite.Group(self.player)
                    level_transition(self.screen, self.level)
                else:
                    # 🎵 Detener música antes del final
                    pygame.mixer.music.fadeout(2000)

                    if self.db.is_top_score(self.score.points):
                        initials = get_initials(self.screen)
                        self.db.insert_score(initials, self.score.points)

                    ending_sequence(self.screen, self.player, self.score)
                    show_highscores(self.screen, self.db)
                    restart = show_game_over(self.screen, self.score)
                    if restart:
                        self.__init__()
                    else:
                        self.running = False
                        break

            # Muerte del jugador
            if not self.player.is_alive:
                # inclinacion suave del sonido
                pygame.mixer.music.fadeout(2000)

                if self.db.is_top_score(self.score.points):
                    initials = get_initials(self.screen)
                    self.db.insert_score(initials, self.score.points)

                ending_sequence(self.screen, self.player, self.score)
                show_highscores(self.screen, self.db)
                restart = show_game_over(self.screen, self.score)

                if restart:
                    self.__init__()
                else:
                    self.running = False
                    break

        pygame.quit()