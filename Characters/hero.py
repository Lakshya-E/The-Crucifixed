from settings import *
from Helpers.constants import *

class Hero(pygame.sprite.Sprite):
    def __init__(self, pos, groups, collision_groups):
        super().__init__(groups)
        self.collision_sprites = collision_groups
        print(f"collision sprites: {self.collision_sprites}")
        # Scale the surface from TMX (8x8 -> 24x24)
        # if surf:
        #     self.image = pygame.transform.scale(surf, (TILE_SIZE * SCALE, TILE_SIZE * SCALE))
        # else:

        # Fallback if no surface provided
        self.image = pygame.Surface((TILE_SIZE * SCALE, TILE_SIZE * SCALE))
        self.image.fill('red')

        # Position also needs to be scaled
        scaled_pos = (pos[0] * SCALE, pos[1] * SCALE)
        self.rect = self.image.get_frect(topleft=scaled_pos)
        self.old_rect = self.rect.copy()

        # Player-specific attributes
        self.direction = vector()
        self.speed = PLAYER_ATTRIBUTES["speed"]
        self.gravity = PLAYER_ATTRIBUTES["gravity"]
        self.jump = False
        self.touch_surface = False

    def handle_input(self):
        # Get pressed keys for movement
        keys = pygame.key.get_pressed()
        input_vector = vector(0,0)

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            input_vector.x -= 1
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            input_vector.x += 1
        if keys[pygame.K_SPACE]: # Jump
            if self.touch_surface == True:
                self.direction.y -= 1
                self.jump = True
        self.direction.x = input_vector.normalize().x if input_vector else 0

    def move(self):
        # horizontal
        self.rect.x += self.direction.x * self.speed
        self._check_collision('horizontal')

        # vertical
        if self.jump:
            self.touch_surface = False
            self.direction.y -= self.gravity * 8
            self.rect.y += self.direction.y
            self.jump = False
        
        # going down with gravity
        self.direction.y += self.gravity / 2
        self.rect.y += self.direction.y
        self._check_collision('vertical')

    def _check_collision(self, axis):
        for sprite in self.collision_sprites:
            if sprite.rect.colliderect(self.rect):
                if axis == 'horizontal':
                    # player going left
                    if self.rect.left <= sprite.rect.right and self.old_rect.left >= sprite.old_rect.right: 
                        self.rect.left = sprite.rect.right
                    # player going right
                    elif self.rect.right >= sprite.rect.left and self.old_rect.right <= sprite.old_rect.left: 
                        self.rect.right = sprite.rect.left
                elif axis == 'vertical':
                    # player going bottom
                    if self.rect.bottom >= sprite.rect.top and self.old_rect.bottom <= sprite.old_rect.top: 
                        self.rect.bottom = sprite.rect.top
                        self.touch_surface = True
                    # player going up
                    elif self.rect.top <= sprite.rect.bottom and self.old_rect.top >= sprite.old_rect.bottom: 
                        self.rect.top = sprite.rect.bottom
                    self.direction.y = 0

    def update(self):
        self.old_rect = self.rect.copy()
        self.handle_input()
        self.move()