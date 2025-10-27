import pygame as pg
from code.Const import TILE_SIZE, GENERIC_ANIMATION_SPEED


class Item(pg.sprite.Sprite):
    def __init__(self, start_pos, item_type, assets):
        super().__init__()

        self.type = item_type
        self.assets = assets[item_type]
        self.current_frame = 0
        self.animation_timer = 0

        tile_x, tile_y = start_pos

        self.image = self.assets[0]

        # ANCORAGEM: bottomleft garante que o item seja desenhado no chão do tile.
        self.rect = self.image.get_rect(bottomleft=(tile_x, tile_y + TILE_SIZE))
        self.world_pos = list(self.rect.bottomleft)
        self.collider = self.rect
        self.is_collected = False

    def _animate(self):
        self.animation_timer += 1

        if self.animation_timer >= GENERIC_ANIMATION_SPEED:
            self.current_frame = (self.current_frame + 1) % len(self.assets)
            self.animation_timer = 0

        self.image = self.assets[self.current_frame]

    def update(self, offset_x):
        if not self.is_collected:
            self._animate()
            self.rect.bottomleft = (self.world_pos[0] + offset_x, self.world_pos[1])
            self.collider.topleft = self.rect.topleft
        else:
            # Remove o sprite do grupo após a coleta (is_collected = True)
            self.kill()