# player.py
from settings import *
from GlobalColours.colour_config import G_COLOURS
from GameEnvironment.base import GameObject
from GameEnvironment.environment import HealthBar
from GameItems.weapons import WEAPONS
from GameActions.combat import AttackHandler
from Helpers.constants import *

class Player(GameObject):
    def __init__(self):
        # Initialize as GameObject
        super().__init__(
            SCREEN_WIDTH // 2,  # x
            SCREEN_HEIGHT // 2,  # y
            50,  # width
            100,  # height
            G_COLOURS.player.main  # red color
        )

        self.display_screen = pygame.display.get_surface()
        
        # Player-specific attributes
        self.speed = PLAYER_ATTRIBUTES["speed"]
        self.health = HEALTH_BAR_ATTRIBUTES["max_health"]
        self.attack_power = PLAYER_ATTRIBUTES["attack_power"]

        # Create attack handler
        self.attack_handler = AttackHandler(self)
        
        # Store screen dimensions for boundary checking
        self.screen_width = SCREEN_WIDTH
        self.screen_height = SCREEN_HEIGHT
        
        # Player is not solid (other objects can overlap)
        self.solid = False

        # Create health bar
        self.health_bar = HealthBar(G_COLOURS.healthbar.green)
    
    def move_left(self, obstacles=None):
        """Move left if no collision"""
        if self.rect.x > 0 + SURFACE_PADDING["left"]:
            # Try to move
            original_x = self.rect.x
            self.rect.x -= self.speed

            # UPDATE FACING DIRECTION
            self.attack_handler.set_facing_direction((-1, 0))
            
            # Check for collisions
            if obstacles and self._check_collision(obstacles):
                self.rect.x = original_x  # Undo movement
    
    def move_right(self, obstacles=None):
        """Move right if no collision"""
        if self.rect.x < self.screen_width - self.rect.width - SURFACE_PADDING["right"]:
            original_x = self.rect.x
            self.rect.x += self.speed

            # UPDATE FACING DIRECTION
            self.attack_handler.set_facing_direction((1, 0))
            
            if obstacles and self._check_collision(obstacles):
                self.rect.x = original_x
    
    def move_up(self, obstacles=None):
        """Move up if no collision"""
        if self.rect.y > 0 + SURFACE_PADDING["top"]:
            original_y = self.rect.y
            self.rect.y -= self.speed

            # UPDATE FACING DIRECTION
            self.attack_handler.set_facing_direction((0, -1))
            
            if obstacles and self._check_collision(obstacles):
                self.rect.y = original_y
    
    def move_down(self, obstacles=None):
        """Move down if no collision"""
        if self.rect.y < self.screen_height - self.rect.height - SURFACE_PADDING["bottom"]:
            original_y = self.rect.y
            self.rect.y += self.speed

            # UPDATE FACING DIRECTION
            self.attack_handler.set_facing_direction((0, 1))
            
            if obstacles and self._check_collision(obstacles):
                self.rect.y = original_y
    
    def _check_collision(self, obstacles):
        """Check if player collides with any solid obstacles"""
        for obstacle in obstacles:
            if obstacle.solid and self.collides_with(obstacle):
                return True
        return False
    
    def handle_input(self, keys, obstacles=None):
        """Handle all player input"""
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.move_left(obstacles)
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.move_right(obstacles)
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.move_up(obstacles)
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.move_down(obstacles)

        # Handle attack input and return attack info
        attack_info = self.attack_handler.handle_attack_input(keys)
        return attack_info
    
    def interact_with_objects(self, objects):
        """Handle player interactions with nearby objects"""
        for obj in objects:
            if self._is_near(obj, range=80):
                if hasattr(obj, 'interact'):
                    obj.interact()
                    return True  # Successfully interacted
        return False  # No interaction happened
    
    def _is_near(self, other_object, range=60):
        """Check if player is within interaction range of another object"""
        dx = abs(self.rect.centerx - other_object.rect.centerx)
        dy = abs(self.rect.centery - other_object.rect.centery)
        return dx < range and dy < range
    
    def handle_events(self, event, objects=None):
        """Handle single events like key presses"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_e:
                if objects:
                    success = self.interact_with_objects(objects)
                    if not success:
                        print("Nothing to interact with nearby")
            elif event.key == pygame.K_r:
                # Another interaction key - maybe for examining objects
                print("Examine action!")
            elif event.key == pygame.K_i:
                # Open inventory
                print("Opening inventory...")
        
        return False  # Return True if event should stop other processing
    
    def take_damage(self, damage):
        """Take damage and return True if still alive"""
        self.health -= damage
        self.health_bar.update(max(self.health, 0))
        return self.health > 0
    
    def heal(self, amount):
        """Heal player"""
        self.health = min(self.health + amount, self.max_health)
        self.health_bar.update(self.health)

    def update(self):
        """Update player and attack handler"""
        self.attack_handler.update()

    # Delegate weapon methods to attack handler
    def equip_weapon(self, weapon_name):
        """Equip a weapon by name"""
        return self.attack_handler.equip_weapon(weapon_name)
    
    def get_current_weapon(self):
        """Get currently equipped weapon"""
        return self.attack_handler.get_current_weapon()
    
    def can_attack(self):
        """Check if player can attack right now"""
        return self.attack_handler.can_attack()

    def draw(self):
        """Draw player and health bar"""
        # Background (red)
        pygame.draw.rect(self.display_screen, G_COLOURS.player.main, 
                        (self.rect.x, self.rect.y, PLAYER_ATTRIBUTES["width"], PLAYER_ATTRIBUTES["height"]))
        # Health (green)
        self.health_bar.draw(self.display_screen)
        