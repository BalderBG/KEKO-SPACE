import pygame
from core import settings
from core.game import Game
from views.ui import main_menu, intro_story

if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))
    pygame.display.set_caption("KEKO")

    choice = main_menu(screen)
    if choice == "new":
        from views.ui import intro_story
        if intro_story(screen):
            Game().run()
            
    elif choice == "exit":
        pygame.quit()