# code/Decoration.py (CORRIGIDO com Ancoragem Bottomleft e Ajuste de Helm)

import pygame as pg
from code.Const import TILE_SIZE, ENEMY_ANIMATION_SPEED

# VALOR DE AJUSTE: Experimente este valor. Se o helm ainda flutuar, aumente-o.
# Se for muito baixo, diminua.
HELM_ADJUST_Y = 8


class Decoration(pg.sprite.Sprite):
    def __init__(self, asset_key, images, x, y):
        super().__init__()

        self.asset_key = asset_key
        self.images = images

        # Posições iniciais do tile
        tile_x = x * TILE_SIZE
        tile_y = y * TILE_SIZE

        # Lógica de Animação e Imagem Inicial
        if isinstance(self.images, list):
            self.animated = True
            self.current_frame = 0
            self.animation_timer = 0
            self.image = self.images[0]  # Usa o primeiro frame
        else:
            self.animated = False
            self.image = self.images

        # === 1. CORREÇÃO DA ANCORAGEM ===
        # Define o rect usando bottomleft. O chão está em (tile_y + TILE_SIZE).
        self.rect = self.image.get_rect(bottomleft=(tile_x, tile_y + TILE_SIZE))

        # === 2. AJUSTE CONDICIONAL PARA O HELM ===
        # Este ajuste é necessário SE o asset do helm tiver transparência extra em cima.
        ajuste = HELM_ADJUST_Y if self.asset_key == 'helm' else 0

        # Salva a posição do mundo (bottomleft) com o ajuste aplicado
        # O self.world_pos[1] agora é a coordenada Y do chão + ajuste.
        self.world_pos = [tile_x, (tile_y + TILE_SIZE) + ajuste]

        # 3. Aplica a posição final ao rect
        self.rect.bottomleft = self.world_pos

    def _animate(self):
        """Atualiza a animação se for um objeto animado (helm)."""
        if not self.animated:
            return

        # Use ENEMY_ANIMATION_SPEED (ou sua constante ITEM/DECORATION_ANIMATION_SPEED)
        self.animation_timer += 1
        if self.animation_timer >= ENEMY_ANIMATION_SPEED:
            self.current_frame = (self.current_frame + 1) % len(self.images)
            self.animation_timer = 0

        # Apenas atualiza a imagem, o rect não muda de tamanho aqui.
        self.image = self.images[self.current_frame]

    def update(self, offset_x):
        """Aplica o offset da câmera e atualiza a animação."""
        self._animate()

        # === 4. CORREÇÃO DA ATUALIZAÇÃO ===
        # Usa a âncora bottomleft da posição do mundo para desenhar.
        self.rect.bottomleft = (self.world_pos[0] + offset_x, self.world_pos[1])