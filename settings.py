import pygame
import sys
from pygame.math import Vector2 as vector
from Helpers.constants import *

# Game settings
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
FPS = 60

TILE_SIZE = 8
SCALE = 3        # Scale factor (8 * 4 = 32 pixel tiles on screen)
SCALED_TILE_SIZE = TILE_SIZE * SCALE  # 32 - for easy reference
