import pygame
from GameItems.weapons import WEAPONS

class AttackHandler:
    """Handles all attack-related logic and mechanics"""
    
    def __init__(self, player):
        self.player = player
        self.attack_cooldown = 0
        self.current_weapon = WEAPONS['fists']
        self.facing_direction = (0, 1)  # Default facing down
        
    def update(self):
        """Update attack cooldown"""
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1
    
    def can_attack(self):
        """Check if can attack right now"""
        return self.attack_cooldown == 0
    
    def equip_weapon(self, weapon_name):
        """Equip a weapon by name"""
        if weapon_name in WEAPONS:
            self.current_weapon = WEAPONS[weapon_name]
            return True
        return False
    
    def get_current_weapon(self):
        """Get currently equipped weapon"""
        return self.current_weapon
    
    def set_facing_direction(self, direction):
        """Set the direction player is facing"""
        self.facing_direction = direction
    
    def perform_attack(self, direction=None):
        """
        Perform attack with current weapon
        Returns attack info or None if can't attack
        """
        if not self.can_attack():
            return None
            
        if direction:
            self.facing_direction = direction
        
        # Convert player pixel position to grid position for weapon calculations
        grid_x = self.player.rect.centerx // 50  # Assuming 50px grid
        grid_y = self.player.rect.centery // 50
        
        # Get attack area based on weapon
        attack_positions = self.current_weapon.get_attack_area(
            grid_x, grid_y, self.facing_direction
        )
        
        # Convert grid positions back to pixel positions for collision detection
        pixel_positions = [(x * 50, y * 50) for x, y in attack_positions]
        
        # Set cooldown
        self.attack_cooldown = self.current_weapon.cooldown
        
        # Return attack info
        return {
            'damage': self.current_weapon.damage,
            'grid_positions': attack_positions,
            'pixel_positions': pixel_positions,
            'weapon_type': self.current_weapon.weapon_type,
            'weapon_name': self.current_weapon.name,
            'attacker': self.player
        }
    
    def handle_attack_input(self, keys, mouse_pos=None):
        """
        Handle attack input and determine direction
        Returns attack info if attack is performed
        """
        direction = None
        
        # Check for attack key (spacebar)
        if keys[pygame.K_SPACE]:
            # Determine direction based on movement keys
            if keys[pygame.K_UP]:
                direction = (0, -1)
            elif keys[pygame.K_DOWN]:
                direction = (0, 1)
            elif keys[pygame.K_LEFT]:
                direction = (-1, 0)
            elif keys[pygame.K_RIGHT]:
                direction = (1, 0)
            else:
                # Use current facing direction if no movement key pressed
                direction = self.facing_direction
        
        # Optional: Mouse attack
        elif pygame.mouse.get_pressed()[0] and mouse_pos:
            direction = self._calculate_mouse_direction(mouse_pos)
        
        if direction:
            return self.perform_attack(direction)
        return None
    
    def _calculate_mouse_direction(self, mouse_pos):
        """Calculate attack direction from player to mouse position"""
        player_center_x = self.player.rect.centerx
        player_center_y = self.player.rect.centery
        
        dx = mouse_pos[0] - player_center_x
        dy = mouse_pos[1] - player_center_y
        
        # Convert to grid direction (8-directional or 4-directional)
        if abs(dx) > abs(dy):
            return (1 if dx > 0 else -1, 0)
        else:
            return (0, 1 if dy > 0 else -1)
    
    def process_attack_hits(self, attack_info, targets):
        """
        Process attack against list of potential targets
        Returns list of hit targets
        """
        if not attack_info:
            return []
        
        hits = []
        
        for target in targets:
            # Check if target is in any attack position
            target_grid_x = target.rect.centerx // 50
            target_grid_y = target.rect.centery // 50
            
            if (target_grid_x, target_grid_y) in attack_info['grid_positions']:
                # Apply damage if target has take_damage method
                if hasattr(target, 'take_damage'):
                    target.take_damage(attack_info['damage'])
                
                hits.append({
                    'target': target,
                    'damage': attack_info['damage'],
                    'position': (target_grid_x, target_grid_y)
                })
        
        return hits
    
    def draw_attack_preview(self, screen, direction=None):
        """
        Draw preview of attack area (for debugging or UI)
        """
        if not direction:
            direction = self.facing_direction
        
        grid_x = self.player.rect.centerx // 50
        grid_y = self.player.rect.centery // 50
        
        attack_positions = self.current_weapon.get_attack_area(
            grid_x, grid_y, direction
        )
        
        # Draw semi-transparent rectangles for attack area
        for pos_x, pos_y in attack_positions:
            pixel_x = pos_x * 50
            pixel_y = pos_y * 50
            
            # Create semi-transparent surface
            attack_surface = pygame.Surface((50, 50))
            attack_surface.set_alpha(100)  # Semi-transparent
            attack_surface.fill((255, 255, 0))  # Yellow
            
            screen.blit(attack_surface, (pixel_x, pixel_y))
