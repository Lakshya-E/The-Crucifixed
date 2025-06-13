from os.path import join
from settings import *
from enum import Enum
from Characters.player import Player
from GameEnvironment.in_game_included import environment_objects
from GlobalColours.colour_config import G_COLOURS
from Helpers.helper import *
from GameLevels.level import Level
from pytmx.util_pygame import load_pygame

class GameState(Enum):
    MAIN_MENU = "main_menu"
    PLAYING = "playing"
    PAUSED = "paused"
    GAME_OVER = "game_over"
    SETTINGS = "settings"

class Game:
    def __init__(self):
        # Initialize Pygame
        pygame.init()
        
        # Set up the display using global dimensions
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(GAME_NAME)
        
        # Store screen dimensions for easy access
        self.screen_width = SCREEN_WIDTH
        self.screen_height = SCREEN_HEIGHT
        self.screen_center_x = SCREEN_WIDTH // 2
        self.screen_center_y = SCREEN_HEIGHT // 2
        
        # Clock for controlling frame rate
        self.clock = pygame.time.Clock()
        
        # Game state
        self.current_state = GameState.MAIN_MENU
        self.running = True
        
        # Game objects (initialized when game starts)
        self.player = None
        self.environment_objects = []
        
        # Menu properties (dynamic font sizes based on screen height)
        # Load custom fonts or fall back to default
        self.title_font_size = int(self.screen_height * 0.12)  # 12% of screen height
        self.menu_font_size = int(self.screen_height * 0.06)   # 6% of screen height
        self.small_font_size = int(self.screen_height * 0.04)  # 4% of screen height
        
        self.font = load_font(PRIMARY_FONT, self.title_font_size)
        self.menu_font = load_font(PRIMARY_FONT, self.menu_font_size)
        self.small_font = load_font(PRIMARY_FONT, self.small_font_size)

        # Menu properties
        self.selected_menu_item = 0
        self.menu_items = ["Play", "Settings", "Quit"]
        
        # Menu layout (percentages of screen dimensions)
        self.title_y_percent = 0.25  # Title at 25% from top
        self.menu_start_y_percent = 0.42  # Menu starts at 42% from top
        self.menu_item_spacing_percent = 0.08  # 8% spacing between items
        self.hint_y_percent = 0.83  # Hints at 83% from top

        # Background image
        self.background_image_main_menu = load_background_image(IMAGES_PATH["main_menu_background"])
        self.background_image_game = load_background_image(IMAGES_PATH["game_background"])

        # Levels
        self.tmx_maps = {0: load_pygame(join('Assets', 'TiledMaps', 'level1.tmx'))}
        self.current_level = Level(self.tmx_maps[0])
        
    def run(self):
        """Main game loop - single loop for all states"""
        while self.running:
            # Control frame rate
            self.clock.tick(60)

            # Handle events based on current state
            self.handle_events()
            
            # Update game state
            self.update()
            
            # Draw everything
            self.draw()
        
        # Clean up
        pygame.quit()
        sys.exit()
    
    def handle_events(self):
        """Handle events based on current game state"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif self.current_state == GameState.MAIN_MENU:
                self.handle_main_menu_events(event)
            elif self.current_state == GameState.PLAYING:
                self.handle_gameplay_events(event)
            elif self.current_state == GameState.PAUSED:
                self.handle_pause_events(event)
            elif self.current_state == GameState.GAME_OVER:
                self.handle_game_over_events(event)
    
    def update(self):
        """Update game logic based on current state"""
        if self.current_state == GameState.PLAYING:
            self.update_gameplay()
        # Other states don't need continuous updates
    
    def draw(self):
        """Draw everything based on current state"""
        self.screen.fill(G_COLOURS.background)
        
        if self.current_state == GameState.MAIN_MENU:
            self.draw_main_menu()
        elif self.current_state == GameState.PLAYING:
            self.draw_gameplay()
        elif self.current_state == GameState.PAUSED:
            self.draw_pause_menu()
        elif self.current_state == GameState.GAME_OVER:
            self.draw_game_over()
        
        pygame.display.flip()
    
    # ==================== MAIN MENU ====================
    def handle_main_menu_events(self, event):
        """Handle main menu input"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected_menu_item = (self.selected_menu_item - 1) % len(self.menu_items)
            elif event.key == pygame.K_DOWN:
                self.selected_menu_item = (self.selected_menu_item + 1) % len(self.menu_items)
            elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                self.select_menu_item()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Handle mouse clicks on menu items
            mouse_pos = pygame.mouse.get_pos()
            self.handle_menu_click(mouse_pos)
    
    def select_menu_item(self):
        """Handle menu item selection"""
        if self.selected_menu_item == 0:  # Play
            self.start_game()
        elif self.selected_menu_item == 1:  # Settings
            self.current_state = GameState.SETTINGS
        elif self.selected_menu_item == 2:  # Quit
            self.running = False
    
    def handle_menu_click(self, mouse_pos):
        """Handle mouse clicks on menu"""
        # Calculate menu item positions dynamically
        menu_start_y = int(self.screen_height * self.menu_start_y_percent)
        item_spacing = int(self.screen_height * self.menu_item_spacing_percent)
        
        for i, item in enumerate(self.menu_items):
            item_y = menu_start_y + (i * item_spacing)
            # Create a clickable area around each menu item
            item_height = self.menu_font.get_height()
            
            if item_y <= mouse_pos[1] <= item_y + item_height:
                self.selected_menu_item = i
                self.select_menu_item()
                break
    
    def draw_main_menu(self):
        """Draw the main menu"""
        # Draw background image or solid color
        if self.background_image_main_menu:
            self.screen.blit(self.background_image_main_menu, (0, 0))
        else:
            # Fallback to solid color if no image
            self.screen.fill(G_COLOURS.background)

        # Semi-transparent overlay for better text readability
        self.screen.blit(load_semi_transparent_overlay(110), (0, 0))

        # Draw title (dynamic positioning) - with outline for better visibility
        title_text = self.font.render(GAME_NAME, True, (255, 255, 255))
        title_outline = self.font.render(GAME_NAME, True, (0, 0, 0))
        title_y = int(self.screen_height * self.title_y_percent)
        
        # Draw outline (offset by 2 pixels in each direction)
        for dx in [-2, 0, 2]:
            for dy in [-2, 0, 2]:
                if dx != 0 or dy != 0:  # Don't draw at center position yet
                    outline_rect = title_outline.get_rect(center=(self.screen_center_x + dx, title_y + dy))
                    self.screen.blit(title_outline, outline_rect)
        
        # Draw main title text
        title_rect = title_text.get_rect(center=(self.screen_center_x, title_y))
        self.screen.blit(title_text, title_rect)
        
        # Draw menu items (with outline for better visibility)
        menu_start_y = int(self.screen_height * self.menu_start_y_percent)
        item_spacing = int(self.screen_height * self.menu_item_spacing_percent)
        
        for i, item in enumerate(self.menu_items):
            color = (255, 255, 0) if i == self.selected_menu_item else (255, 255, 255)
            text = self.menu_font.render(item, True, color)
            text_outline = self.menu_font.render(item, True, (0, 0, 0))
            
            item_y = menu_start_y + (i * item_spacing)
            
            # Draw outline
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    if dx != 0 or dy != 0:
                        outline_rect = text_outline.get_rect(center=(self.screen_center_x + dx, item_y + dy))
                        self.screen.blit(text_outline, outline_rect)
            
            # Draw main text
            text_rect = text.get_rect(center=(self.screen_center_x, item_y))
            self.screen.blit(text, text_rect)
        
        # Draw controls hint (with outline)
        hint_text = self.small_font.render("Use arrow keys and Enter, or click to select", True, (128, 128, 128))
        hint_outline = self.small_font.render("Use arrow keys and Enter, or click to select", True, (0, 0, 0))
        hint_y = int(self.screen_height * self.hint_y_percent)
        
        # Draw outline
        outline_rect = hint_outline.get_rect(center=(self.screen_center_x + 1, hint_y + 1))
        self.screen.blit(hint_outline, outline_rect)
        
        # Draw main hint text
        hint_rect = hint_text.get_rect(center=(self.screen_center_x, hint_y))
        self.screen.blit(hint_text, hint_rect)
    
    # ==================== GAMEPLAY ====================
    def start_game(self):
        """Initialize game objects and start playing"""
        # Initialize player at screen center
        self.player = Player()
        
        # Initialize environment
        self.environment_objects = environment_objects
        
        # Change to playing state
        self.current_state = GameState.PLAYING

    def handle_gameplay_events(self, event):
        """Handle gameplay events"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.current_state = GameState.PAUSED
        
        # Let level events
        self.current_level.handle_level_events(event)
    
    def update_gameplay(self):
        """Update gameplay logic"""
        if not self.player:
            return
        
        # Get pressed keys for movement
        keys = pygame.key.get_pressed()
        
        # Handle player input with collision detection
        attack_info = self.player.handle_input(keys, self.environment_objects)
        
        # Process attacks if any
        if attack_info:
            enemies = []  # You'll populate this with actual enemies later
            hits = self.player.attack_handler.process_attack_hits(attack_info, enemies)
            for hit in hits:
                print(f"Hit {hit['target']} for {hit['damage']} damage!")
        
        # Update all objects
        for obj in self.environment_objects:
            obj.update(self.clock.get_time())
        
        # Check for game over conditions
        # if self.player.health <= 0:
        #     self.current_state = GameState.GAME_OVER
    
    def draw_gameplay(self):
        """Draw the gameplay"""
        # Draw background image or solid color
        # if self.background_image_game:
        #     self.screen.blit(self.background_image_game, (0, 0))
        # else:
        #     # Fallback to solid color if no image
        #     self.screen.fill(G_COLOURS.background)

        # # Semi-transparent overlay for better text readability
        # self.screen.blit(load_semi_transparent_overlay(90), (0, 0))

        # Draw the player
        # if self.player:
        #     self.player.draw(self.screen)

        #     if pygame.key.get_pressed()[pygame.K_SPACE]:
        #         self.player.attack_handler.draw_attack_preview(self.screen)
        
        # Draw all environment objects
        # for obj in self.environment_objects:
        #     obj.draw(self.screen)

        self.current_level.run()
    
    # ==================== PAUSE MENU ====================
    def handle_pause_events(self, event):
        """Handle pause menu events"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.current_state = GameState.PLAYING
            elif event.key == pygame.K_q:
                self.current_state = GameState.MAIN_MENU
    
    def draw_pause_menu(self):
        """Draw pause menu over gameplay"""
        # Draw the game in background (dimmed)
        self.draw_gameplay()
        
        # Draw semi-transparent overlay
        self.screen.blit(load_semi_transparent_overlay(160), (0, 0))
        
        # Draw pause text (centered)
        pause_text = self.font.render("PAUSED", True, (255, 255, 255))
        pause_y = int(self.screen_height * 0.42)  # 42% from top
        pause_rect = pause_text.get_rect(center=(self.screen_center_x, pause_y))
        self.screen.blit(pause_text, pause_rect)
        
        # Draw instructions (centered, spaced below pause text)
        resume_text = self.menu_font.render("Press ESC to resume", True, (255, 255, 255))
        resume_y = pause_y + int(self.screen_height * 0.12)  # 12% below pause text
        resume_rect = resume_text.get_rect(center=(self.screen_center_x, resume_y))
        self.screen.blit(resume_text, resume_rect)
        
        quit_text = self.menu_font.render("Press Q to quit to main menu", True, (255, 255, 255))
        quit_y = resume_y + int(self.screen_height * 0.07)  # 7% below resume text
        quit_rect = quit_text.get_rect(center=(self.screen_center_x, quit_y))
        self.screen.blit(quit_text, quit_rect)
    
    # ==================== GAME OVER ====================
    def handle_game_over_events(self, event):
        """Handle game over events"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self.start_game()  # Restart game
            elif event.key == pygame.K_q:
                self.current_state = GameState.MAIN_MENU
    
    def draw_game_over(self):
        """Draw game over screen"""
        # Draw game over text (centered)
        game_over_text = self.font.render("GAME OVER", True, (255, 0, 0))
        game_over_y = int(self.screen_height * 0.42)  # 42% from top
        game_over_rect = game_over_text.get_rect(center=(self.screen_center_x, game_over_y))
        self.screen.blit(game_over_text, game_over_rect)
        
        # Draw restart instructions (centered, spaced below game over text)
        restart_text = self.menu_font.render("Press SPACE to restart", True, (255, 255, 255))
        restart_y = game_over_y + int(self.screen_height * 0.12)  # 12% below game over text
        restart_rect = restart_text.get_rect(center=(self.screen_center_x, restart_y))
        self.screen.blit(restart_text, restart_rect)
        
        quit_text = self.menu_font.render("Press Q to quit to main menu", True, (255, 255, 255))
        quit_y = restart_y + int(self.screen_height * 0.07)  # 7% below restart text
        quit_rect = quit_text.get_rect(center=(self.screen_center_x, quit_y))
        self.screen.blit(quit_text, quit_rect)

# Run the game
if __name__ == "__main__":
    game = Game()
    game.run()
