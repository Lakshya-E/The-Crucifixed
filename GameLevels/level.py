from settings import *
from GameLevels.sprites import Sprite
from Characters.player import Player
from Characters.hero import Hero

class Level:
    def __init__(self, tmx_map):
        self.display_screen = pygame.display.get_surface()

        # Groups
        self.all_sprites = pygame.sprite.Group()
        self.collision_sprites = pygame.sprite.Group()

        self.setup(tmx_map)

    def setup(self, tmx_map):
        for x, y, surf in tmx_map.get_layer_by_name("Ground").tiles():
            Sprite((x*TILE_SIZE, y*TILE_SIZE), surf, (self.all_sprites, self.collision_sprites))
        
        # Player
        # self.player = Player()
        # self.all_sprites.add(self.player)

        for obj in tmx_map.get_layer_by_name("Objects"):
            if obj.name == 'player':
                Hero((obj.x, obj.y), self.all_sprites, self.collision_sprites)

    def run(self):
        self.display_screen.fill('gray')
        self.all_sprites.draw(self.display_screen)

        self.all_sprites.update()

        # Draw the player
        # if self.player:
        #     self.player.draw()

        #     if pygame.key.get_pressed()[pygame.K_SPACE]:
        #         self.player.attack_handler.draw_attack_preview(self.display_screen)

    def handle_level_events(self, event):
        if event.type == pygame.KEYDOWN:
            # print(f"event key: {event.key}")
            pass
        # if self.player:
        #     self.player.handle_events(event, self.environment_objects)
