# Item.py

import pygame as pg
from code.Const import TILE_SIZE, PLAYER_ANIMATION_SPEED


class Item(pg.sprite.Sprite):
    def __init__(self, start_pos, item_type, assets):
        super().__init__()

        self.type = item_type

        # ... (código de animação e posição inalterado) ...
        self.animations = assets[item_type]
        self.current_frame = 0
        self.animation_timer = 0

        self.pos = list(start_pos)
        self.image = self.animations[0]
        self.rect = self.image.get_rect(topleft=self.pos)

        # Colisão
        self.collider = self.rect  # Colisão simples
        self.is_collected = False  # NOVO: Flag para desativar colisão manual

    def _animate(self):
        # ... (código inalterado) ...
        self.animation_timer += 1
        if self.animation_timer >= PLAYER_ANIMATION_SPEED:
            self.current_frame = (self.current_frame + 1) % len(self.animations)
            self.animation_timer = 0

        self.image = self.animations[self.current_frame]

    def update(self, offset_x):
        """Atualiza o item, aplicando offset da câmera."""
        if not self.is_collected:
            self._animate()
            # Atualiza a posição de desenho e colisão com o offset
            self.rect.topleft = (self.pos[0] + offset_x, self.pos[1])
            self.collider.topleft = (self.pos[0] + offset_x, self.pos[1])
        else:
            # Se for coletado, move o rect/collider para fora da tela
            self.rect.topleft = (-100, -100)
            self.collider.topleft = (-100, -100)

    # Metodo para lidar com coleta
    def collect(self):
        """Chamado quando o item é coletado."""
        self.is_collected = True
        # Como o Pygame já remove o item do grupo de sprites,
        # a próxima chamada a update vai mover o rect/collider para fora da tela.