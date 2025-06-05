import pygame
import sys
from Characters.player import Player
from settings import SCREEN_HEIGHT, SCREEN_WIDTH
from GlobalColours.colour_config import G_COLOURS
from GameEnvironment.in_game_included import environment_objects

# Initialize pygame
pygame.init()

# Create the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("My First Game - The Crucifixed")

# Game clock for controlling frame rate
clock = pygame.time.Clock()

# Create player object
player = Player(SCREEN_WIDTH, SCREEN_HEIGHT)

# Main game loop
running = True
while running:
    # Handle events (like closing the window)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        else:
            # Let player handle other events (interactions, etc.)
            player.handle_events(event, environment_objects)
    
    # Get pressed keys for movement
    keys = pygame.key.get_pressed()
    
    # Handle player input with collision detection
    attack_info = player.handle_input(keys, environment_objects)  # Now returns attack info

    # Process attacks if any
    if attack_info:
        enemies = []
        hits = player.attack_handler.process_attack_hits(attack_info, enemies)
        for hit in hits:
            print(f"Hit {hit['target']} for {hit['damage']} damage!")

    # Update all objects (for future animated objects)
    for obj in environment_objects:
        obj.update(clock.get_time())

    # Fill screen with black (clear previous frame)
    screen.fill(G_COLOURS.background)
    
    # Draw the player
    player.draw(screen)

    # Draw all environment objects
    for obj in environment_objects:
        obj.draw(screen)
    
    
    # Update the display
    pygame.display.flip()
    
    # Control frame rate (60 FPS)
    clock.tick(60)

# Quit the game
pygame.quit()
sys.exit()
