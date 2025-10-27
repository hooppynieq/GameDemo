import pygame as pg
from code.Const import TILE_SIZE, GENERIC_ANIMATION_SPEED


class Decoration(pg.sprite.Sprite):
    def __init__(self, asset_key, images, x, y):
        super().__init__()

        self.asset_key = asset_key
        self.original_images = images

        tile_x = x * TILE_SIZE
        tile_y = y * TILE_SIZE

        self.flip_h = self.asset_key.endswith('_flipped')

        if isinstance(self.original_images, list):
            self.animated = True
            self.images = self._apply_flip_to_images(self.original_images)
            self.current_frame = 0
            self.animation_timer = 0
            self.image = self.images[0]
        else:
            self.animated = False
            self.image = self._apply_flip_to_image(self.original_images)

        self.rect = self.image.get_rect(bottomleft=(tile_x, tile_y + TILE_SIZE))
        self.world_pos = [tile_x, (tile_y + TILE_SIZE) ]

        self.rect.bottomleft = self.world_pos

    def _apply_flip_to_image(self, image):
        if self.flip_h:
            return pg.transform.flip(image, True, False)
        return image

    def _apply_flip_to_images(self, image_list):
        if self.flip_h:
            return [pg.transform.flip(img, True, False) for img in image_list]
        return image_list

    def _animate(self):
        if not self.animated:
            return

        self.animation_timer += 1

        if self.animation_timer >= GENERIC_ANIMATION_SPEED:
            self.current_frame = (self.current_frame + 1) % len(self.images)
            self.animation_timer = 0

        self.image = self.images[self.current_frame]

    def update(self, offset_x):
        self._animate()
        self.rect.bottomleft = (self.world_pos[0] + offset_x, self.world_pos[1])