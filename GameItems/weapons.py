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
