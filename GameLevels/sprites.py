from settings import *

class Sprite(pygame.sprite.Sprite):
    def __init__(self, pos, surf, groups):
        super().__init__(groups)

        # Scale the surface from TMX (8x8 -> 24x24)
        if surf:
            self.image = pygame.transform.scale(surf, (TILE_SIZE * SCALE, TILE_SIZE * SCALE))
        else:
            # Fallback if no surface provided
            self.image = pygame.Surface((TILE_SIZE * SCALE, TILE_SIZE * SCALE))
            self.image.fill('black')

        # Position also needs to be scaled
        scaled_pos = (pos[0] * SCALE, pos[1] * SCALE)
        self.rect = self.image.get_frect(topleft=scaled_pos)
        self.old_rect = self.rect.copy()
