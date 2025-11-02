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



def main_menu(screen):
    #Inicio el fondo de estrellas
    background = StarBackground(settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT)
    clock = pygame.time.Clock()

    #Fuente y texto
    font_title = pygame.font.SysFont(None, 100)
    font_menu = pygame.font.SysFont(None, 50)

    title = font_title.render("K.E.K.O SPACE", True, (255, 255, 255))
    options = ["Nueva partida", "Salir"]
    selected = 0

    #Musica del menú
    try:
        pygame.mixer.music.load("assets/music/16bit.mp3")
        pygame.mixer.music.play(-1)
    except:
        pass   #Si no existe la musica, se queda en silencio

    while True:
        #Dibuja el fondo
        screen.fill((0, 0, 0))
        background.update()
        background.draw(screen)

        #Dibujo de titulo
        screen.blit(title, title.get_rect(center=(settings.SCREEN_WIDTH // 2, 180)))

        #Dibujo de opciones de parpadeo
        for i, option in enumerate(options):
            if i == selected:
                #efecto de parpadeo
                blink = (pygame.time.get_ticks() // 400) % 2
                color = (255, 255, 255) if blink == 0 else (180, 180, 180)
            else:
                color = (180, 180, 180)

            text = font_menu.render(option, True, color)
            screen.blit(text, text.get_rect(center=(settings.SCREEN_WIDTH // 2, 320 + i * 80)))

        # actualizados de
        pygame.display.flip()
        clock.tick(60)

        #Manejo de eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return "exit"
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected = (selected - 1) % len(options)
                elif event.key == pygame.K_DOWN:
                    selected = (selected + 1) % len(options)  
                elif event.key == pygame.K_RETURN:
                    if options[selected] == "Nueva partida":
                        pygame.mixer.music.stop()
                        return "new"
                    elif options[selected] == "Salir":
                        pygame.quit()
                        return "exit"

def intro_story(screen):
    clock = pygame.time.Clock()
    pygame.mixer.stop()

    bg_color = (0, 0, 0)
    screen.fill(bg_color)

    # Tipografía tipo "máquina de escribir"
    font = pygame.font.SysFont("couriernew", 26, bold=False)
    story_lines = [
        "Hace mucho tiempo, en una galaxia perdida...",
        "",
        "K.E.K.O, un navegante cibermercenario,",
        "busca a través del espacio recursos,",
        "tesoros olvidados y tecnología prohibida.",
        "",
        "Su nave, impulsada por energía cuántica,",
        "viaja de planeta en planeta enfrentando peligros.",
        "",
        "Pero esta vez, algo ha cambiado...",
        "Una señal antigua resuena desde un mundo perdido...",
        "y K.E.K.O se prepara para su mayor desafío..."
    ]

    current_line = 0
    current_text = ""
    writing = True
    delay_between_chars = 40  # milisegundos entre letras
    delay_between_lines = 800  # pausa entre líneas completas
    last_char_time = pygame.time.get_ticks()

    running = True
    skip_intro = False

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                return False
            if event.type == pygame.KEYDOWN:
                skip_intro = True
                running = False

        screen.fill(bg_color)

        # Texto tipo máquina de escribir
        now = pygame.time.get_ticks()
        if writing and current_line < len(story_lines):
            line = story_lines[current_line]
            if now - last_char_time > delay_between_chars:
                if len(current_text) < len(line):
                    current_text += line[len(current_text)]
                    last_char_time = now
                else:
                    writing = False
                    last_char_time = now
        else:
            if now - last_char_time > delay_between_lines:
                current_line += 1
                current_text = ""
                writing = True

        # Dibujar texto guapardo
        y_start = settings.SCREEN_HEIGHT // 2 - 200  # Posicion del texto
        for i in range(current_line):
            text_surface = font.render(story_lines[i], True, (230, 230, 230))
            text_rect = text_surface.get_rect(center=(settings.SCREEN_WIDTH // 2, y_start + i * 35))
            screen.blit(text_surface, text_rect)

        if current_line < len(story_lines):
            text_surface = font.render(current_text, True, (230, 230, 230))
            text_rect = text_surface.get_rect(center=(settings.SCREEN_WIDTH // 2, y_start + current_line * 35))
            screen.blit(text_surface, text_rect)

        pygame.display.flip()
        clock.tick(60)

        if current_line >= len(story_lines):
            pygame.time.delay(1500)
            running = False

    return True

def show_game_over(screen, score):
    font_big = pygame.font.SysFont(None, 72)
    font_small = pygame.font.SysFont(None, 36)

    text_gameover = font_big.render("FIN DEL JUEGO", True, (255, 255, 255))
    text_score = font_small.render(f"Tu puntuación: {score.points}", True, (255, 255, 255))
    text_restart = font_small.render("Pulsa R para reiniciar o ESC para salir del juego", True, (180, 180, 180))

    screen.fill((10, 10, 30))
    screen.blit(text_gameover, text_gameover.get_rect(center=(630, 80)))
    screen.blit(text_score, text_score.get_rect(center=(630, 150)))
    screen.blit(text_restart, text_restart.get_rect(center=(630, 480)))
    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                waiting = False
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    return True
                if event.key == pygame.K_ESCAPE:
                    return False

def get_initials(screen):       #Iniciales final del juego
    initials = ""
    font = pygame.font.SysFont(None, 60)
    prompt_font = pygame.font.SysFont(None, 36)
    prompt_text = prompt_font.render("¡Nuevo récord! Escribe tus iniciales:", True, (255, 255, 255))

    entering = True
    while entering:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                entering = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and len(initials) > 0:
                    entering = False
                elif event.key == pygame.K_BACKSPACE:
                    initials = initials[:-1]
                elif len(initials) < 3 and event.unicode.isalpha():
                    initials += event.unicode.upper()

        # Fondo oscuro 
        screen.fill((10, 10, 30))

        # Centro de texto
        center_x = screen.get_width() // 2
        center_y = screen.get_height() // 2

        # Texto superior 
        prompt_rect = prompt_text.get_rect(center=(center_x, center_y - 80))
        screen.blit(prompt_text, prompt_rect)

        # Texto de iniciales 
        text_surface = font.render(initials or "_ _ _", True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(center_x, center_y + 20))
        screen.blit(text_surface, text_rect)

        pygame.display.flip()

    return initials or "XXX"


def show_highscores(screen, db):        #Puntuaciones
    font_big = pygame.font.SysFont(None, 60)
    font_small = pygame.font.SysFont(None, 36)

    # Puntuaciones
    scores = db.get_top_scores()
    screen.fill((10, 10, 30))

    # Título 
    title_surface = font_big.render("MEJORES PUNTUACIONES", True, (255, 255, 255))
    title_rect = title_surface.get_rect(center=(screen.get_width() // 2, 100))
    screen.blit(title_surface, title_rect)

    # Renderizado 
    y = 180
    for i, (name, points) in enumerate(scores, start=1):
        line_surface = font_small.render(f"{i}. {name} — {points}", True, (255, 255, 255))
        line_rect = line_surface.get_rect(center=(screen.get_width() // 2, y))
        screen.blit(line_surface, line_rect)
        y += 45

    # Mensaje inferior 
    info_surface = font_small.render("Pulsa cualquier tecla para continuar", True, (200, 200, 200))
    info_rect = info_surface.get_rect(center=(screen.get_width() // 2, y + 60))
    screen.blit(info_surface, info_rect)

    pygame.display.flip()

    # Funcion de espera hasta que la tecla se presione
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN:
                waiting = False

def landing_sequence(screen, player, score, level):  # Animación de aterrizaje
    font_big = pygame.font.SysFont(None, 60)
    clock = pygame.time.Clock()

    # Sonido de fuego del motor
    fire_sound_path = os.path.join("assets", "sounds", "engine_fire.ogg")
    fire_channel = None
    if os.path.exists(fire_sound_path):
        fire_sound = pygame.mixer.Sound(fire_sound_path)
        fire_sound.set_volume(0.4)
        fire_channel = fire_sound.play(loops=-1)

    # Obtener planeta actual
    planet_name = level.get_planet()
    planet_image_path = os.path.join("assets", "planets", f"{planet_name}.png")

    if os.path.exists(planet_image_path):
        planet_image = pygame.image.load(planet_image_path).convert_alpha()
        planet_rect = planet_image.get_rect(center=(settings.SCREEN_WIDTH // 2, settings.SCREEN_HEIGHT + 300))
    else:
        planet_image = None
        planet_rect = pygame.Rect(0, 0, 300, 300)
        planet_rect.center = (settings.SCREEN_WIDTH // 2, settings.SCREEN_HEIGHT + 300)

    # Colores alternativos si no hay sprite
    colors = {
        "planeta1": (70, 150, 255),
        "planeta2": (200, 80, 60),
        "planeta3": (180, 120, 90),
        "planeta4": (210, 180, 120),
        "planeta5": (80, 100, 255)
    }
    planet_color = colors.get(planet_name, (120, 120, 120))

    # Carga sprite de la nave
    ship_path = os.path.join("assets", "player", "nave.png")
    if os.path.exists(ship_path):
        ship_image = pygame.image.load(ship_path).convert_alpha()
    else:
        ship_image = pygame.Surface((60, 40), pygame.SRCALPHA)
        pygame.draw.polygon(ship_image, (255, 255, 255), [(0, 40), (30, 0), (60, 40)])

    ship_rect = ship_image.get_rect(center=(settings.SCREEN_WIDTH // 2, 100))
    rotation_angle = 0
    target_angle = 90  
    ship_speed = 5.0
    landed = False

    # Parámetros del planeta
    planet_radius = 120  # porque el planeta mide 300x300
    visual_margin = 10   # para que la nave no se hunda
    target_y = planet_rect.centery - planet_radius - visual_margin

    # Control de seguridad (por si algo se cuelga)
    start_time = pygame.time.get_ticks()
    max_duration = 10_000  # 10 segundos máximo

    particles = pygame.sprite.Group()  #Esto es para generar particulas

    # Animación principal de descenso
    while not landed:
        dt = clock.tick(60)
        screen.fill((5, 5, 20))

        # Mover planeta hacia arriba
        if planet_rect.centery > settings.SCREEN_HEIGHT - planet_radius:
            planet_rect.centery -= 1

        # Recalcular punto de aterrizaje dinámicamente
        target_y = planet_rect.centery - planet_radius - visual_margin

        # Distancia entre nave y planeta
        distance = target_y - ship_rect.centery

        # Desaceleración
        if distance > 250:
            ship_speed = max(ship_speed - 0.05, 1.5)
        else:
            ship_speed = max(ship_speed - 0.08, 0.2)

        ship_rect.centery += ship_speed

        # Rotación progresiva
        progress = max(0, min(1, 1 - (distance / 400)))  # 0 al inicio, 1 al llegar cerca del planeta
        rotation_angle = 90 * progress  # va girando poco a poco hasta ponerse vertical
        rotated_ship = pygame.transform.rotate(ship_image, rotation_angle)
        rotated_rect = rotated_ship.get_rect(center=ship_rect.center)

        # Dibujar planeta
        if planet_image:
            screen.blit(planet_image, planet_rect)
        else:
            pygame.draw.circle(screen, planet_color, planet_rect.center, planet_radius)

        # Dibujar nave
        screen.blit(rotated_ship, rotated_rect)

        #Generar particulas
        if ship_speed > 0.3:
            for _ in range(1):  
                angle_offset = random.uniform(0, 2 * math.pi)
                radius = random.randint(15, 30)
                fx = ship_rect.centerx + math.cos(angle_offset) * radius
                fy = ship_rect.centery + math.sin(angle_offset) * radius + 10  # un poco más abajo
                p = Particle((fx, fy))
                particles.add(p)

        for p in list(particles):
            p.update()
            p.draw(screen)

        pygame.display.flip()

        # Condición de aterrizaje con tolerancia
        if ship_rect.centery >= target_y - 5:
            ship_rect.centery = target_y
            landed = True

        # Seguridad para salir del bucle si tarda demasiado
        if pygame.time.get_ticks() - start_time > max_duration:
            landed = True

    # Detener sonido al aterrizar
    if fire_channel:
        fire_channel.stop()

    # Pequeña animación de reposo
    for i in range(30):
        clock.tick(60)
        screen.fill((5, 5, 20))
        if planet_image:
            screen.blit(planet_image, planet_rect)
        else:
            pygame.draw.circle(screen, planet_color, planet_rect.center, planet_radius)

        rotated_ship = pygame.transform.rotate(ship_image, target_angle)
        rotated_rect = rotated_ship.get_rect(center=(ship_rect.centerx, target_y))
        screen.blit(rotated_ship, rotated_rect)
        pygame.display.flip()

    # Mensaje de completado
    text = font_big.render(f"Nivel {level.current_level + 1} completado en {planet_name.title()}!", True, (255, 255, 255))
    screen.fill((5, 5, 20))
    if planet_image:
        screen.blit(planet_image, planet_rect)
    else:
        pygame.draw.circle(screen, planet_color, planet_rect.center, planet_radius)
    screen.blit(text, text.get_rect(center=(settings.SCREEN_WIDTH // 2, 200)))

    pygame.display.flip()
    pygame.time.delay(6000)

def ending_sequence(screen, player, score):
    import pygame
    from core import settings

    clock = pygame.time.Clock()
    font_big = pygame.font.SysFont(None, 72)
    font_med = pygame.font.SysFont(None, 48)
    font_small = pygame.font.SysFont(None, 32)

    # Fondo inicial
    bg_color = (5, 5, 20)
    screen.fill(bg_color)
    pygame.display.flip()

    # transicion
    fade_surface = pygame.Surface((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))
    fade_surface.fill((0, 0, 0))

    for alpha in range(255, -1, -5):  # Esto hace que se desvanezca
        screen.fill(bg_color)
        fade_surface.set_alpha(alpha)
        screen.blit(fade_surface, (0, 0))
        pygame.display.flip()
        clock.tick(60)

    # Textos
    text1 = font_big.render("Misión Completada!", True, (255, 255, 255))
    text2 = font_med.render(f"Puntuación total: {score.points}", True, (255, 255, 199))
    text3 = font_small.render("Pulsa cualquier tecla para ver los récords", True, (180, 180, 180))

    # Aparecen con un leve efecto de entrada
    y_positions = [200, 280, 380]
    texts = [text1, text2, text3]

    for i, text in enumerate(texts):
        for alpha in range(0, 256, 15):  # aparición progresiva
            temp_surface = text.copy()
            temp_surface.set_alpha(alpha)
            screen.fill(bg_color)
            for j in range(i + 1):
                # dibujar los anteriores completos
                screen.blit(texts[j], texts[j].get_rect(center=(settings.SCREEN_WIDTH // 2, y_positions[j])))
            screen.blit(temp_surface, temp_surface.get_rect(center=(settings.SCREEN_WIDTH // 2, y_positions[i])))
            pygame.display.flip()
            clock.tick(30)

    # Esto espera a que hagas una accion
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN:
                waiting = False
        clock.tick(30)

def level_transition(screen, level):
    font_big = pygame.font.SysFont(None, 80)
    font_small = pygame.font.SysFont(None, 40)
    clock = pygame.time.Clock()
    colors = [
    (10, 10, 30),
    (15, 15, 50),
    (30, 15, 40),
    (40, 25, 15),
    (50, 10, 10)
]
    bg_color = colors[(level.current_level - 1) % len(colors)]
    screen.fill(bg_color)


    text_level = font_big.render(f"NIVEL {level.current_level + 1}", True, (255, 255, 255))
    text_ready = font_small.render("Saltando al hiperespacio", True, (200, 200, 200))

    fade_surface = pygame.Surface((screen.get_width(), screen.get_height()))
    fade_surface.fill((0, 0, 0))

    for alpha in range(255, -1, -5):
        fade_surface.set_alpha(alpha)
        screen.fill((10, 10, 30))
        screen.blit(text_level, text_level.get_rect(center=(screen.get_width() // 2, 250)))
        screen.blit(text_ready, text_ready.get_rect(center=(screen.get_width() // 2, 350)))
        screen.blit(fade_surface, (0, 0))
        pygame.display.flip()
        clock.tick(30)

    pygame.time.delay(1500) # esto es una pausa.