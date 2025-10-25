# code/Decoration.py (CORRIGIDO com Ancoragem Bottomleft e Flip)

import pygame as pg
from code.Const import TILE_SIZE, ENEMY_ANIMATION_SPEED

# VALOR DE AJUSTE: Experimente este valor. Se o helm ainda flutuar, aumente-o.
# Se for muito baixo, diminua.
HELM_ADJUST_Y = 8


class Decoration(pg.sprite.Sprite):
    def __init__(self, asset_key, images, x, y):
        super().__init__()

        self.asset_key = asset_key
        # A imagem/lista de imagens original, antes do flip.
        self.original_images = images

        # Posições iniciais do tile
        tile_x = x * TILE_SIZE
        tile_y = y * TILE_SIZE

        # === 1. LÓGICA DE FLIP ===
        # Define se o sprite deve ser flipado horizontalmente
        # Você pode usar um asset_key específico (ex: 'shell_flipped')
        self.flip_h = self.asset_key.endswith('_flipped')

        # Lógica de Animação e Imagem Inicial
        if isinstance(self.original_images, list):
            self.animated = True
            self.images = self._apply_flip_to_images(self.original_images)
            self.current_frame = 0
            self.animation_timer = 0
            self.image = self.images[0]  # Usa o primeiro frame (já flipado se necessário)
        else:
            self.animated = False
            self.image = self._apply_flip_to_image(self.original_images)  # Imagem única (já flipada se necessário)

        # === 2. CORREÇÃO DA ANCORAGEM ===
        # Define o rect usando bottomleft. O chão está em (tile_y + TILE_SIZE).
        self.rect = self.image.get_rect(bottomleft=(tile_x, tile_y + TILE_SIZE))

        # === 3. AJUSTE CONDICIONAL PARA O HELM ===
        # Este ajuste é necessário SE o asset do helm tiver transparência extra em cima.
        ajuste = HELM_ADJUST_Y if 'helm' in self.asset_key else 0

        # Salva a posição do mundo (bottomleft) com o ajuste aplicado
        # O self.world_pos[1] agora é a coordenada Y do chão + ajuste.
        self.world_pos = [tile_x, (tile_y + TILE_SIZE) + ajuste]

        # 4. Aplica a posição final ao rect
        self.rect.bottomleft = self.world_pos

    def _apply_flip_to_image(self, image):
        """Aplica o flip horizontal se self.flip_h for True."""
        if self.flip_h:
            return pg.transform.flip(image, True, False)
        return image

    def _apply_flip_to_images(self, image_list):
        """Aplica o flip a uma lista de imagens (para animações)."""
        if self.flip_h:
            return [pg.transform.flip(img, True, False) for img in image_list]
        return image_list

    def _animate(self):
        """Atualiza a animação se for um objeto animado."""
        if not self.animated:
            return

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