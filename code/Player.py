# player.py

import pygame as pg

from code.Const import PLAYER_COLLIDER_SIZE, GRAVITY, TILE_SIZE, PLAYER_JUMP_FORCE, PLAYER_SPEED, PLAYER_ANIMATION_SPEED
from code.utils import load_player_assets

class Player(pg.sprite.Sprite):
    def __init__(self, start_pos, game_map, map_width_pixels):
        super().__init__()

        # Mapa para Colisão
        self.game_map = game_map



        # Assets
        self.animations = load_player_assets()

        # Estado de Movimento e Animação
        self.state = 'idle_right'  # Posições possíveis: 'idle_right', 'idle_left', 'run_right', 'run_left'
        self.current_frame = 0
        self.animation_timer = 0

        # Posição e Físicas
        self.pos = list(start_pos)  # [x, y]
        self.vertical_speed = 0
        self.on_ground = False

        # Imagem e Retângulo (Para desenho e colisão visual)
        self.image = self.animations['idle_right'][0]
        self.rect = self.image.get_rect(topleft=self.pos)

        # Collider (Retângulo menor e centralizado para colisão precisa)
        self.collider_offset_x = 40
        self.collider_offset_y = 8
        self.collider = pg.Rect(self.pos[0] + self.collider_offset_x, self.pos[1] + self.collider_offset_y,
                                PLAYER_COLLIDER_SIZE[0], PLAYER_COLLIDER_SIZE[1])

        # Limite do mundo
        self.map_width_pixels = map_width_pixels
        self.min_x = 0
        self.max_x = map_width_pixels - PLAYER_COLLIDER_SIZE[0] - self.collider_offset_x

    def _apply_gravity(self):
        """Aplica a gravidade e a velocidade vertical."""
        self.vertical_speed += GRAVITY
        self.vertical_speed = min(self.vertical_speed, 15)
        self.pos[1] += self.vertical_speed
        self.collider.top = self.pos[1] + self.collider_offset_y

    def _check_collision_y(self):
        """Verifica e resolve colisões verticais com o mapa."""
        collided = False

        # Calcula a área de tiles para verificar
        start_col = max(0, self.collider.left // TILE_SIZE)
        end_col = min(len(self.game_map[0]), (self.collider.right + TILE_SIZE - 1) // TILE_SIZE)
        start_row = max(0, self.collider.top // TILE_SIZE)
        end_row = min(len(self.game_map), (self.collider.bottom + TILE_SIZE - 1) // TILE_SIZE)

        for y in range(start_row, end_row):
            for x in range(start_col, end_col):
                if self.game_map[y][x] != ' ':
                    tile_rect = pg.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)

                    if self.collider.colliderect(tile_rect):
                        collided = True
                        if self.vertical_speed > 0:  # Caindo (colisão por baixo)
                            self.pos[1] = tile_rect.top - self.collider_offset_y - PLAYER_COLLIDER_SIZE[1]
                            self.vertical_speed = 0
                            self.on_ground = True
                        elif self.vertical_speed < 0:  # Pulando (colisão por cima)
                            self.pos[1] = tile_rect.bottom - self.collider_offset_y
                            self.vertical_speed = 0

                        self.collider.top = self.pos[1] + self.collider_offset_y
                        return collided

        self.on_ground = False
        return collided

    def _check_collision_x(self, move_dir):
        """Verifica e resolve colisões horizontais com o mapa."""

        # Calcula a área de tiles para verificar
        start_col = max(0, self.collider.left // TILE_SIZE)
        end_col = min(len(self.game_map[0]), (self.collider.right + TILE_SIZE - 1) // TILE_SIZE)
        start_row = max(0, self.collider.top // TILE_SIZE)
        end_row = min(len(self.game_map), (self.collider.bottom + TILE_SIZE - 1) // TILE_SIZE)

        for y in range(start_row, end_row):
            for x in range(start_col, end_col):
                if self.game_map[y][x] != ' ':
                    tile_rect = pg.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)

                    if self.collider.colliderect(tile_rect):
                        if move_dir == 'left':
                            self.pos[0] = tile_rect.right - self.collider_offset_x
                        elif move_dir == 'right':
                            self.pos[0] = tile_rect.left - self.collider_offset_x - PLAYER_COLLIDER_SIZE[0]

                        self.collider.left = self.pos[0] + self.collider_offset_x
                        return True
        return False

    def jump(self):
        """Faz o jogador pular, se estiver no chão."""
        if self.on_ground:
            self.vertical_speed = PLAYER_JUMP_FORCE
            self.on_ground = False

    def move(self, keys_pressed):
        """
        Atualiza a posição horizontal e o estado de animação baseado nas teclas pressionadas.
        CORRIGIDO: Lógica para manter a direção IDLE.
        """
        # 1. Movimento Horizontal e Limites do Mundo
        moved = False
        move_dir = ''
        new_x = self.pos[0]  # Posição inicial para o cálculo

        # Left (A)
        if keys_pressed[pg.K_a]:
            new_x -= PLAYER_SPEED
            move_dir = 'left'
            moved = True

        # Right (D)
        if keys_pressed[pg.K_d]:
            new_x += PLAYER_SPEED
            move_dir = 'right'
            moved = True

        # APLICAÇÃO DO LIMITE HORIZONTAL (Mantendo sua lógica correta)
        new_x = max(self.min_x, new_x)
        new_x = min(self.max_x, new_x)

        # 2. Atualiza Posição e Colisão X
        if self.pos[0] != new_x:
            self.pos[0] = new_x
            self.collider.left = self.pos[0] + self.collider_offset_x

            # Colisão X pode reajustar self.pos[0] se bater em uma parede
            self._check_collision_x(move_dir)

        # 3. Atualização do Estado de Animação (CORRIGIDA)

        # Obtém a direção atual (esquerda/direita) do estado.
        current_direction: str = 'right' if 'right' in self.state else 'left'
        new_state = self.state

        if moved:
            # CORREÇÃO: Usamos 'new_state' de forma consistente para RUN
            if move_dir == 'right':
                new_state = 'run_right'
            elif move_dir == 'left':
                new_state = 'run_left'
            current_direction = move_dir
        else:
            # Lógica para IDLE
            if current_direction == 'right':
                new_state = 'idle_right'
            else:
                new_state = 'idle_left'

        # Transição de Estado e Reset (Se o estado MUDOU, reinicia o frame)
        if new_state != self.state:
            self.current_frame = 0
            self.animation_timer = 0

        self.state = new_state  # Aplica o novo estado final

    def _animate(self):
        """
        Atualiza o frame da animação do jogador.
        CORRIGIDO: Garante que o índice não saia do limite da lista.
        """

        current_animation = self.animations[self.state]
        num_frames = len(current_animation)

        # Garante que o índice atual é válido para a animação atual
        if self.current_frame >= num_frames:
            self.current_frame = 0
            self.animation_timer = 0

        # Incrementa o timer
        self.animation_timer += 1

        if self.animation_timer >= PLAYER_ANIMATION_SPEED:
            # Cicla o frame
            self.current_frame = (self.current_frame + 1) % num_frames
            self.animation_timer = 0

        # Define a imagem
        self.image = current_animation[self.current_frame]

    def update(self, offset_x):
        """Lógica de atualização do jogador: gravidade, colisão e animação.
        Recebe o offset para atualizar a posição de desenho.
        """

        # 1. Gravidade e Colisão Vertical
        self._apply_gravity()
        self._check_collision_y()

        # 2. Animação
        self._animate()

        # 3. Atualiza o rect principal para o desenho (APLICA O OFFSET)
        self.rect.topleft = (self.pos[0] + offset_x, self.pos[1])
