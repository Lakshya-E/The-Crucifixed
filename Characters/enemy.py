class Enemy:
    def __init__(self, x, y, enemy_type="basic"):
        self.x, self.y = x, y
        self.type = enemy_type
        self.health = 100
        self.speed = 1
        self.detection_range = 5
        self.state = "patrol"  # patrol, chase, search
        
    def update(self, player_pos, walls, obstacles):
        if self.can_see_player(player_pos, walls):
            self.state = "chase"
            self.move_towards_player(player_pos)
        else:
            self.patrol()
    
    def can_see_player(self, player_pos, walls):
        # Line-of-sight check
        pass
    
    def move_towards_player(self, player_pos):
        # Chase logic
        pass
    
    def patrol(self):
        # Patrol behavior
        pass
