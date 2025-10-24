# Enemy.py

import pygame as pg
from code.Const import ENEMY_SPEED, GRAVITY, TILE_SIZE, ENEMY_COLLIDER_SIZE, ENEMY_ANIMATION_SPEED


class Enemy(pg.sprite.Sprite):
    def __init__(self, start_pos, enemy_type, assets, game_map):
        super().__init__()

        # ... (código de inicialização inalterado) ...
        self.game_map = game_map
        self.type = enemy_type

        # Animação
        self.animations = assets[enemy_type]
        self.current_frame = 0
        self.animation_timer = 0

        # Posição e Físicas
        self.pos = list(start_pos)
        self.vertical_speed = 0
        self.speed = ENEMY_SPEED
        self.direction = 1

        # Imagem e Rect
        self.image = self.animations[0]
        self.rect = self.image.get_rect(topleft=self.pos)

        # Collider (Usamos o tamanho do tile para o inimigo)
        self.collider = pg.Rect(self.pos[0], self.pos[1], TILE_SIZE, TILE_SIZE)
        self.on_ground = False  # Novo para controle de queda
        # ... (resto do init) ...

    def _apply_gravity(self):
        """Aplica a gravidade."""
        self.vertical_speed += GRAVITY
        self.vertical_speed = min(self.vertical_speed, 15)
        self.pos[1] += self.vertical_speed
        self.collider.top = self.pos[1]

    def _check_collision_y(self):
        """Verifica e resolve colisões verticais (chão)."""

        start_col = max(0, self.collider.left // TILE_SIZE)
        end_col = min(len(self.game_map[0]), (self.collider.right + TILE_SIZE - 1) // TILE_SIZE)
        start_row = max(0, self.collider.top // TILE_SIZE)
        end_row = min(len(self.game_map), (self.collider.bottom + TILE_SIZE - 1) // TILE_SIZE)

        for y in range(start_row, end_row):
            for x in range(start_col, end_col):
                if self.game_map[y][x] != ' ':
                    tile_rect = pg.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)

                    if self.collider.colliderect(tile_rect):
                        if self.vertical_speed > 0:  # Caindo
                            self.pos[1] = tile_rect.top - TILE_SIZE
                            self.vertical_speed = 0
                            self.on_ground = True
                        elif self.vertical_speed < 0:  # Batendo a cabeça
                            self.pos[1] = tile_rect.bottom
                            self.vertical_speed = 0

                        self.collider.top = self.pos[1]
                        return

        self.on_ground = False

    def _move_and_check_collision_x(self):
        """Movimento horizontal simples e colisão."""

        # ... (código inalterado) ...
        # Move
        self.pos[0] += self.speed * self.direction
        self.collider.left = self.pos[0]

        # Inverte direção se atingir parede (lógica simplificada)
        start_col = max(0, self.collider.left // TILE_SIZE)
        end_col = min(len(self.game_map[0]), (self.collider.right + TILE_SIZE - 1) // TILE_SIZE)
        start_row = max(0, self.collider.top // TILE_SIZE)
        end_row = min(len(self.game_map), (self.collider.bottom + TILE_SIZE - 1) // TILE_SIZE)

        for y in range(start_row, end_row):
            for x in range(start_col, end_col):
                if self.game_map[y][x] != ' ':
                    tile_rect = pg.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                    if self.collider.colliderect(tile_rect):
                        self.direction *= -1
                        self.pos[0] += self.speed * self.direction * 2
                        self.collider.left = self.pos[0]
                        return

    def _animate(self):
        """Atualiza o frame da animação do inimigo."""
        # ... (código inalterado) ...
        self.animation_timer += 1

        if self.animation_timer >= ENEMY_ANIMATION_SPEED:
            self.current_frame = (self.current_frame + 1) % len(self.animations)
            self.animation_timer = 0

        img = self.animations[self.current_frame]
        if self.direction == -1:
            self.image = pg.transform.flip(img, True, False)
        else:
            self.image = img

    def update(self, offset_x):
        """Atualiza o inimigo, aplicando offset da câmera."""
        self._apply_gravity()
        self._check_collision_y()  # NOVO: Colisão vertical
        self._move_and_check_collision_x()
        self._animate()

        # Atualiza a posição de desenho com o offset
        self.rect.topleft = (self.pos[0] + offset_x, self.pos[1])
        # O collider permanece na posição do mundo (pos[0], pos[1])