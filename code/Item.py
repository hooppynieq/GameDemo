# code/Item.py

import pygame as pg
# Importando PLAYER_ANIMATION_SPEED como substituto
from code.Const import TILE_SIZE, PLAYER_ANIMATION_SPEED


class Item(pg.sprite.Sprite):
    def __init__(self, start_pos, item_type, assets):
        super().__init__()

        self.type = item_type
        self.assets = assets[item_type]
        self.current_frame = 0
        self.animation_timer = 0

        # Posição do tile no mundo (canto superior esquerdo do tile)
        tile_x, tile_y = start_pos

        # Imagem inicial
        self.image = self.assets[0]

        # 1. ANCORAGEM CORRETA: Define o rect inicial e a posição do mundo
        # bottomleft garante que a base do sprite (rect.bottom) esteja no chão (tile_y + TILE_SIZE)
        self.rect = self.image.get_rect(bottomleft=(tile_x, tile_y + TILE_SIZE))

        # 2. POSIÇÃO DO MUNDO: Salva a posição bottomleft absoluta (não se move)
        self.world_pos = list(self.rect.bottomleft)

        # Colisão
        self.collider = self.rect  # Colisão simples
        self.is_collected = False  # Flag para desativar colisão manual

    def _animate(self):
        """Atualiza o frame da animação do item."""
        self.animation_timer += 1

        # Usando PLAYER_ANIMATION_SPEED como substituto temporário
        if self.animation_timer >= PLAYER_ANIMATION_SPEED:
            self.current_frame = (self.current_frame + 1) % len(self.assets)
            self.animation_timer = 0

        # Apenas atualiza a imagem
        self.image = self.assets[self.current_frame]

    def update(self, offset_x):
        """Atualiza o item, aplicando offset da câmera e animação."""
        if not self.is_collected:
            self._animate()

            # Atualiza a posição de desenho (usando self.world_pos para a âncora bottomleft)
            self.rect.bottomleft = (self.world_pos[0] + offset_x, self.world_pos[1])

            # Mantém o collider alinhado ao rect
            self.collider.topleft = self.rect.topleft

        else:
            # Opção mais limpa é usar .kill() no Game.py.
            # Se a lógica de remoção for aqui, você pode usar:
            self.kill()

            # O metodo 'collect' não é necessário se você estiver usando o 'True' no spritecollide do Game.py.