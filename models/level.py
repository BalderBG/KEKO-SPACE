import pygame
import json
import os
from core import settings


class Level:
    def __init__(self, file_patch="levels.json"):
        if not os.path.exists(file_patch):
            raise FileNotFoundError(f"No se encontro el archivo {file_patch}")
        
        with open(file_patch, "r", encoding="utf-8") as f:
            data = json.load(f)

        self.levels = data["levels"]
        self.current_level = 0
        self.level_start_time = pygame.time.get_ticks()


    def get_current(self):
        return self.levels[self.current_level]      #ESTO DEVUELVE LOS PARAMETROS DE CADA NIVEL.  
    
    def is_level_complete(self):
        now = pygame.time.get_ticks()
        duration = self.levels[self.current_level]["duration"]
        return now - self.level_start_time >= duration
    
    def next_level(self):
        if self.current_level < len(self.levels) - 1:
            self.current_level += 1
            self.level_start_time = pygame.time.get_ticks()
            return True
        return False
    
    def is_last_level(self):
        return self.current_level == len(self.levels) - 1
    
    def get_obstacle_type(self):
        return self.levels[self.current_level].get("obstacle_type", "meteorito")
    
    def get_background(self):
        return self.levels[self.current_level].get("background", None)
    
    def get_planet(self):
        return self.levels[self.current_level].get("planet", "tierra")