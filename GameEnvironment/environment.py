# game_objects/environment.py
import pygame
from .base import GameObject
from GlobalColours.colour_config import G_COLOURS
from Helpers.constants import PLAYER_ATTRIBUTES, HEALTH_BAR_ATTRIBUTES

class Wall(GameObject):
    """Static wall that blocks movement"""
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height, G_COLOURS.wall)  # White
        self.solid = True

class Door(GameObject):
    """Door that can be opened/closed"""
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height, G_COLOURS.door.closed)  # Brown
        self.is_open = False
        self.solid = True
    
    def interact(self):
        """Called when player interacts with this door"""
        if self.is_open:
            self.close()
        else:
            self.open()
    
    def open(self):
        """Open the door"""
        self.is_open = True
        self.solid = False
        self.color = G_COLOURS.door.opened  # Lighter brown when open
        print("Door opened!")
    
    def close(self):
        """Close the door"""
        self.is_open = False
        self.solid = True
        self.color = G_COLOURS.door.closed  # Original brown
        print("Door closed!")

class Chest(GameObject):
    """Treasure chest that can contain items"""
    def __init__(self, x, y):
        super().__init__(x, y, 40, 30, G_COLOURS.chest.closed)  # Dark brown
        self.is_open = False
        self.solid = True
        self.contents = []  # Items inside the chest
    
    def interact(self):
        """Called when player interacts with this chest"""
        if not self.is_open:
            items = self.open()
            print(f"Opened chest! Found {len(items)} items")
        else:
            print("Chest is already open")
    
    def open(self):
        """Open the chest"""
        if not self.is_open:
            self.is_open = True
            self.color = G_COLOURS.chest.opened  # Lighter when open
            return self.contents
        return []

class Obstacle(GameObject):
    """Generic obstacle (rocks, debris, etc.)"""
    def __init__(self, x, y, width, height, color=G_COLOURS.debris):
        super().__init__(x, y, width, height, color)  # Gray by default
        self.solid = True

class HealthBar():
    """Displays the player's health"""
    def __init__(self, colour):
        self.width = HEALTH_BAR_ATTRIBUTES["width"]
        self.height = HEALTH_BAR_ATTRIBUTES["height"]
        self.x = HEALTH_BAR_ATTRIBUTES["x"]
        self.y = HEALTH_BAR_ATTRIBUTES["y"]
        self.max_health = HEALTH_BAR_ATTRIBUTES["max_health"]
        self.current_health = 70 #HEALTH_BAR_ATTRIBUTES["max_health"]

        self.colour = colour
        solid = False

    def draw(self, screen):
        """Draw the health bar on screen"""
        health_ratio = self.current_health / self.max_health
        
        pygame.draw.rect(screen, G_COLOURS.healthbar.outline, 
                (self.x - 2, self.y - 2, self.width + 4, self.height + 4))
        pygame.draw.rect(screen, G_COLOURS.healthbar.empty, 
                (self.x, self.y, self.width, self.height))
        pygame.draw.rect(screen, self.colour, 
                (self.x, self.y, self.width * health_ratio, self.height))

    def update(self, health):
        """Update the health bar to match the player's health"""
        if health > self.max_health:
            health = self.max_health
        elif health < 0:
            health = 0
        self.current_health = health
