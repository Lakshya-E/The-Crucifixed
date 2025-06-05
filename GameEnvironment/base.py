# game_objects/base.py
import pygame

class GameObject:
    """Base class for all game objects"""
    def __init__(self, x, y, width, height, color):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.solid = True  # Can other objects pass through this?
        self.visible = True  # Should this be drawn?
    
    def draw(self, screen):
        """Draw the object on screen"""
        if self.visible:
            pygame.draw.rect(screen, self.color, self.rect)
    
    def update(self, dt):
        """Update object state (override in subclasses if needed)"""
        pass
    
    def get_position(self):
        """Get current position as tuple"""
        return (self.rect.x, self.rect.y)
    
    def set_position(self, x, y):
        """Set new position"""
        self.rect.x = x
        self.rect.y = y
    
    def collides_with(self, other):
        """Check collision with another GameObject"""
        return self.rect.colliderect(other.rect)
