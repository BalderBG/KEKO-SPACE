import pygame
import random
import os
import math
from models.particle import Particle
from core import settings

def takeoff_sequence(screen, player, level):
    clock = pygame.time.Clock()
    font_big = pygame.font.SysFont(None, 60)

    # Sonido del fuego del motor
    fire_sound_path = os.path.join("assets", "sounds", "engine_fire.ogg")
    fire_channel = None
    if os.path.exists(fire_sound_path):
        fire_sound = pygame.mixer.Sound(fire_sound_path)
        fire_sound.set_volume(0.4)
        fire_channel = fire_sound.play(loops=-1)

    # Recuperar planeta actual
    planet_name = level.get_planet()
    planet_path = os.path.join("assets", "planets", f"{planet_name}.png")

    if os.path.exists(planet_path):
        planet_image = pygame.image.load(planet_path).convert_alpha()
        planet_rect = planet_image.get_rect(center=(settings.SCREEN_WIDTH // 2, settings.SCREEN_HEIGHT - 150))
    else:
        planet_image = None
        planet_rect = pygame.Rect(0, 0, 400, 400)
        planet_rect.center = (settings.SCREEN_WIDTH // 2, settings.SCREEN_HEIGHT - 150)

    # Nave
    ship_path = os.path.join("assets", "player", "nave.png")
    if os.path.exists(ship_path):
        ship_image = pygame.image.load(ship_path).convert_alpha()
    else:
        ship_image = pygame.Surface((60, 40), pygame.SRCALPHA)
        pygame.draw.polygon(ship_image, (255, 255, 255), [(0, 40), (30, 0), (60, 40)])

    ship_rect = ship_image.get_rect(center=(settings.SCREEN_WIDTH // 2, settings.SCREEN_HEIGHT - 230))
    particles = pygame.sprite.Group()

    ship_speed = 0.5
    acceleration = 0.05
    angle = 25  # empieza inclinado del aterrizaje

    taking_off = True
    phase = "up"  # Fase de subida vertical

    while taking_off:
        dt = clock.tick(60)
        screen.fill((5, 5, 20))

        # Movimiento del planeta (desciende lentamente)
        if planet_rect.centery < settings.SCREEN_HEIGHT + 200:
            planet_rect.centery += 1

        # Fase 1 subida vertical
        if phase == "up":
            ship_speed += acceleration
            ship_rect.centery -= ship_speed

            if ship_rect.centery <= settings.SCREEN_HEIGHT // 2:
                phase = "right"
                ship_speed = 3

        # Fase 2 moverse hacia la derecha
        elif phase == "right":
            if angle > 0:
                angle -= 2  # gira suavemente hacia la derecha
            ship_rect.centerx += ship_speed
            ship_speed *= 1.02  # acelera un poco

        rotated_ship = pygame.transform.rotate(ship_image, -angle)
        rotated_rect = rotated_ship.get_rect(center=ship_rect.center)

        # Partículas a la izquierda del motor
        for _ in range(5):
            rad = math.radians(angle)
            offset_x = -math.cos(rad) * 25 + math.sin(rad) * 10
            offset_y = math.sin(rad) * 25 + math.cos(rad) * 10
            fx = ship_rect.centerx + offset_x
            fy = ship_rect.centery + offset_y
            p = Particle((fx, fy))
            p.speed_y = -math.sin(rad) * 4 + random.uniform(-0.5, 0.5)
            p.x -= math.cos(rad) * 1.5
            p.color = random.choice([(255, 220, 100), (255, 160, 50), (255, 240, 180)])
            particles.add(p)

        # Actualizar y dibujar partículas
        for p in list(particles):
            p.update()
            p.draw(screen)

        # Dibujar planeta
        if planet_image:
            screen.blit(planet_image, planet_rect)
        else:
            pygame.draw.circle(screen, (80, 100, 120), planet_rect.center, 200)

        # Dibujar nave
        screen.blit(rotated_ship, rotated_rect)

        pygame.display.flip()

        # Cuando sale de pantalla, fin de animación
        if ship_rect.left > settings.SCREEN_WIDTH or ship_rect.bottom < -50:
            taking_off = False

    # Detener el sonido al finalizar el despegue
    if fire_channel:
        fire_channel.stop()

    # Transición de texto
    screen.fill((0, 0, 0))

    if level.is_last_level():
        text_message = "Has probado la DEMO de KEKO SPACE"
    else:
        text_message = "Despegando hacia el siguiente destino..."

    text = font_big.render(text_message, True, (255, 255, 255))
    text_rect = text.get_rect(center=(settings.SCREEN_WIDTH // 2, settings.SCREEN_HEIGHT // 2))
    screen.blit(text, text_rect)
    pygame.display.flip()
    pygame.time.delay(3000)

    # Si no es el ultimo nivel saldrá un "Pulsa cualquier tecla para continuar" Es una funcion de continuidad
    if not level.is_last_level():
        font_small = pygame.font.SysFont(None, 36)
        blink_timer = 0
        show_text = True
        waiting = True

        while waiting:
            dt = clock.tick(60)
            blink_timer += dt

            # Efecto parpadeante
            if blink_timer > 600:
                show_text = not show_text
                blink_timer = 0

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    waiting = False
                    pygame.quit()
                    return
                elif event.type == pygame.KEYDOWN:
                    waiting = False

            screen.fill((0, 0, 0))
            screen.blit(text, text_rect)
            if show_text:
                continue_text = font_small.render("Pulsa cualquier tecla para continuar...", True, (200, 200, 200))
                continue_rect = continue_text.get_rect(center=(settings.SCREEN_WIDTH // 2, settings.SCREEN_HEIGHT // 2 + 80))
                screen.blit(continue_text, continue_rect)

            pygame.display.flip()