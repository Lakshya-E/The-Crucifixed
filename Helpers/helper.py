import pygame
from settings import SCREEN_HEIGHT, SCREEN_WIDTH

def load_background_image(image_path):
        """Load and scale background image to fit screen"""
        try:
            # Load the image
            original_image = pygame.image.load(image_path)
            print(f"Background image '{image_path}' loaded successfully!")

            # Scale the image to fit the screen while maintaining aspect ratio
            return pygame.transform.scale(original_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

        except pygame.error as e:
            print(f"Could not load background image '{image_path}': {e}")
            print("Main menu will use solid color background instead.")
            return None
        except FileNotFoundError:
            print(f"Background image file '{image_path}' not found.")
            print("Main menu will use solid color background instead.")
            return None

def load_font(font_path, size):
        """Load custom font or fall back to default font"""
        try:
            # Try to load custom font
            custom_font = pygame.font.Font(font_path, size)
            print(f"Custom font '{font_path}' loaded successfully!")
            return custom_font
            
        except pygame.error as e:
            print(f"Could not load font '{font_path}': {e}")
            print(f"Using default font at size {size} instead.")
            return pygame.font.Font(None, size)
        except FileNotFoundError:
            print(f"Font file '{font_path}' not found.")
            print(f"Using default font at size {size} instead.")
            return pygame.font.Font(None, size)
        except FileNotFoundError:
            print(f"Background image file '{image_path}' not found.")
            print("Main menu will use solid color background instead.")
            self.background_image = None

def load_semi_transparent_overlay(alpha):
    # Semi-transparent overlay for better text readability
    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    overlay.set_alpha(alpha)  # Adjust transparency (0-255, lower = more transparent)
    overlay.fill((0, 0, 0))  # Black overlay
    return overlay
    self.screen.blit(overlay, (0, 0))
