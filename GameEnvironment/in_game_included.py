from settings import SCREEN_HEIGHT, SCREEN_WIDTH
from .environment import Wall, Door, Chest, Obstacle

environment_objects = [
    # Walls around the border
    Wall(0, 0, SCREEN_WIDTH, 20),           # Top wall
    Wall(0, SCREEN_HEIGHT - 20, SCREEN_WIDTH, 20),  # Bottom wall
    Wall(0, 0, 20, SCREEN_HEIGHT),          # Left wall
    Wall(SCREEN_WIDTH - 20, 0, 20, SCREEN_HEIGHT),  # Right wall
    
    # Some obstacles in the middle
    Obstacle(300, 300, 50, 50),             # Rock
    Chest(100, 400),                        # Treasure chest
    Door(350, 100, 20, 50),                 # Door
]
