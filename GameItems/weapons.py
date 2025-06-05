import pygame
import math

class Weapon:
    def __init__(self, name, damage, attack_range, area_type, cooldown, weapon_type):
        self.name = name
        self.damage = damage
        self.attack_range = attack_range
        self.area_type = area_type  # 'single', 'line', 'cone', 'circle'
        self.cooldown = cooldown  # frames between attacks
        self.weapon_type = weapon_type  # 'melee', 'ranged', 'magic'
        
    def get_attack_area(self, player_x, player_y, direction):
        """Returns list of (x, y) coordinates that this weapon attacks"""
        if self.area_type == 'single':
            return [(player_x + direction[0], player_y + direction[1])]
        elif self.area_type == 'line':
            return self._get_line_area(player_x, player_y, direction)
        elif self.area_type == 'cone':
            return self._get_cone_area(player_x, player_y, direction)
        elif self.area_type == 'circle':
            return self._get_circle_area(player_x, player_y)
        
    def _get_line_area(self, x, y, direction):
        """Attack in a line (for spears, staffs)"""
        positions = []
        for i in range(1, self.attack_range + 1):
            positions.append((x + direction[0] * i, y + direction[1] * i))
        return positions
    
    def _get_cone_area(self, x, y, direction):
        """Attack in a cone (for swords, magic)"""
        positions = []
        # Main direction
        positions.append((x + direction[0], y + direction[1]))
        
        # Side attacks for wider weapons
        if self.attack_range > 1:
            # Perpendicular directions for cone effect
            if direction[0] == 0:  # Moving vertically
                positions.extend([
                    (x - 1, y + direction[1]),
                    (x + 1, y + direction[1])
                ])
            else:  # Moving horizontally
                positions.extend([
                    (x + direction[0], y - 1),
                    (x + direction[0], y + 1)
                ])
        return positions
    
    def _get_circle_area(self, x, y):
        """Attack all around player (for magic spells)"""
        positions = []
        for dx in range(-self.attack_range, self.attack_range + 1):
            for dy in range(-self.attack_range, self.attack_range + 1):
                if dx == 0 and dy == 0:
                    continue
                if dx*dx + dy*dy <= self.attack_range*self.attack_range:
                    positions.append((x + dx, y + dy))
        return positions

# Weapon definitions
WEAPONS = {
    'fists': Weapon('Fists', 5, 1, 'single', 15, 'melee'),
    'sword': Weapon('Iron Sword', 20, 1, 'cone', 25, 'melee'),
    'bow': Weapon('Wooden Bow', 15, 5, 'line', 35, 'ranged'),
    'staff': Weapon('Magic Staff', 25, 2, 'line', 40, 'magic'),
    'magic_blast': Weapon('Magic Blast', 30, 2, 'circle', 50, 'magic'),
}

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.current_weapon = WEAPONS['fists']  # Start with fists
        self.attack_cooldown = 0
        self.facing_direction = (0, 1)  # Default facing down
        
    def update(self):
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1
    
    def equip_weapon(self, weapon_name):
        """Equip a weapon by name"""
        if weapon_name in WEAPONS:
            self.current_weapon = WEAPONS[weapon_name]
            return True
        return False
    
    def attack(self, direction=None):
        """Perform attack with current weapon"""
        if self.attack_cooldown > 0:
            return None  # Still on cooldown
            
        if direction:
            self.facing_direction = direction
            
        # Get attack area based on weapon
        attack_positions = self.current_weapon.get_attack_area(
            self.x, self.y, self.facing_direction
        )
        
        # Set cooldown
        self.attack_cooldown = self.current_weapon.cooldown
        
        # Return attack info
        return {
            'damage': self.current_weapon.damage,
            'positions': attack_positions,
            'weapon_type': self.current_weapon.weapon_type,
            'weapon_name': self.current_weapon.name
        }
    
    def can_attack(self):
        """Check if player can attack right now"""
        return self.attack_cooldown == 0

# Usage example in your game loop
def handle_attack_input(player, keys, mouse_pos=None):
    """Handle different attack inputs"""
    direction = None
    
    # Keyboard directional attack
    if keys[pygame.K_SPACE]:
        # Use current facing direction or movement direction
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            direction = (0, -1)
        elif keys[pygame.K_s] or keys[pygame.K_DOWN]:
            direction = (0, 1)
        elif keys[pygame.K_a] or keys[pygame.K_LEFT]:
            direction = (-1, 0)
        elif keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            direction = (1, 0)
        else:
            direction = player.facing_direction
    
    # Mouse attack (optional)
    elif pygame.mouse.get_pressed()[0] and mouse_pos:
        # Calculate direction from player to mouse
        dx = mouse_pos[0] - player.x * TILE_SIZE
        dy = mouse_pos[1] - player.y * TILE_SIZE
        
        # Convert to grid direction
        if abs(dx) > abs(dy):
            direction = (1 if dx > 0 else -1, 0)
        else:
            direction = (0, 1 if dy > 0 else -1)
    
    if direction:
        return player.attack(direction)
    return None

# Example of processing attacks in your game loop
def process_attack(attack_info, enemies, destructible_objects):
    """Process an attack against enemies and objects"""
    if not attack_info:
        return
    
    hits = []
    for pos in attack_info['positions']:
        # Check for enemies at this position
        for enemy in enemies:
            if (enemy.x, enemy.y) == pos:
                enemy.take_damage(attack_info['damage'])
                hits.append(('enemy', enemy, pos))
        
        # Check for destructible objects
        for obj in destructible_objects:
            if (obj.x, obj.y) == pos:
                obj.take_damage(attack_info['damage'])
                hits.append(('object', obj, pos))
    
    return hits

# Example weapon progression system
class WeaponInventory:
    def __init__(self):
        self.weapons = ['fists']  # Start with fists
        self.weapon_index = 0
    
    def add_weapon(self, weapon_name):
        if weapon_name not in self.weapons:
            self.weapons.append(weapon_name)
    
    def cycle_weapon(self, player):
        """Cycle through available weapons"""
        self.weapon_index = (self.weapon_index + 1) % len(self.weapons)
        weapon_name = self.weapons[self.weapon_index]
        player.equip_weapon(weapon_name)
        return weapon_name

# Example usage:
if __name__ == '__main__':
    player = Player(5, 5)
    
    # Test different weapons
    print(f"Starting weapon: {player.current_weapon.name}")
    
    # Test fist attack
    attack = player.attack((1, 0))
    print(f"Fist attack: {attack}")
    
    # Equip sword and test
    player.equip_weapon('sword')
    attack = player.attack((1, 0))
    print(f"Sword attack: {attack}")
    
    # Equip bow and test
    player.equip_weapon('bow')
    attack = player.attack((1, 0))
    print(f"Bow attack: {attack}")
