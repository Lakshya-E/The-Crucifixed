# player.py
import pygame
from GlobalColours.colour_config import G_COLOURS
from GameEnvironment.base import GameObject
from GameItems.weapons import WEAPONS
from GameActions.combat import AttackHandler

class Player(GameObject):
    def __init__(self, screen_width, screen_height):
        # Initialize as GameObject
        super().__init__(
            screen_width // 2,  # x
            screen_height // 2,  # y
            50,  # width
            50,  # height
            G_COLOURS.player.main  # red color
        )
        
        # Player-specific attributes
        self.speed = 5
        self.health = 100
        self.max_health = 100
        self.attack_power = 10

        # Create attack handler
        self.attack_handler = AttackHandler(self)
        
        # Store screen dimensions for boundary checking
        self.screen_width = screen_width
        self.screen_height = screen_height
        
        # Player is not solid (other objects can overlap)
        self.solid = False
    
    def move_left(self, obstacles=None):
        """Move left if no collision"""
        if self.rect.x > 0:
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
        if self.rect.x < self.screen_width - self.rect.width:
            original_x = self.rect.x
            self.rect.x += self.speed

            # UPDATE FACING DIRECTION
            self.attack_handler.set_facing_direction((1, 0))
            
            if obstacles and self._check_collision(obstacles):
                self.rect.x = original_x
    
    def move_up(self, obstacles=None):
        """Move up if no collision"""
        if self.rect.y > 0:
            original_y = self.rect.y
            self.rect.y -= self.speed

            # UPDATE FACING DIRECTION
            self.attack_handler.set_facing_direction((0, -1))
            
            if obstacles and self._check_collision(obstacles):
                self.rect.y = original_y
    
    def move_down(self, obstacles=None):
        """Move down if no collision"""
        if self.rect.y < self.screen_height - self.rect.height:
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
        if keys[pygame.K_LEFT]:
            self.move_left(obstacles)
        if keys[pygame.K_RIGHT]:
            self.move_right(obstacles)
        if keys[pygame.K_UP]:
            self.move_up(obstacles)
        if keys[pygame.K_DOWN]:
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
        return self.health > 0
    
    def heal(self, amount):
        """Heal player"""
        self.health = min(self.health + amount, self.max_health)

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

    def draw(self, screen):
        """Draw player and health bar"""
        # Draw player
        super().draw(screen)
        
        # Draw simple health bar above player
        bar_width = 50
        bar_height = 6
        health_ratio = self.health / self.max_health
        
        # Background (red)
        pygame.draw.rect(screen, G_COLOURS.player.main, 
                        (self.rect.x, self.rect.y - 10, bar_width, bar_height))
        # Health (green)
        pygame.draw.rect(screen, G_COLOURS.player.healthbar, 
                        (self.rect.x, self.rect.y - 10, bar_width * health_ratio, bar_height))
