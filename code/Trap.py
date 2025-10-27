import pygame as pg
from code.Const import TILE_SIZE


class Trap(pg.sprite.Sprite):
    def __init__(self, start_pos, trap_type, assets):
        super().__init__()

        self.type = trap_type
        self.pos = list(start_pos)
        self.image = assets[trap_type]
        self.rect = self.image.get_rect(topleft=self.pos)
        collider_height = int(TILE_SIZE * 0.75)
        self.collider = pg.Rect(self.pos[0], self.pos[1] + (TILE_SIZE - collider_height), TILE_SIZE, collider_height)

    def update(self, offset_x):
        self.rect.topleft = (self.pos[0] + offset_x, self.pos[1])

        self.collider.topleft = (self.pos[0] + offset_x, self.pos[1] + (self.rect.height - self.collider.height))