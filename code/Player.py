# player.py

import pygame as pg

from code.Const import (
    PLAYER_COLLIDER_SIZE, GRAVITY, TILE_SIZE, PLAYER_JUMP_FORCE, PLAYER_SPEED,
    PLAYER_ANIMATION_SPEED, DECORATION_MAP_CODES, ITEM_MAP_CODES
)
# Assumindo que você tem uma função load_player_assets em code.utils
from code.utils import load_player_assets


class Player(pg.sprite.Sprite):
    def __init__(self, start_pos, game_map, map_width_pixels):
        super().__init__()

        # Variável para ignorar colisões de tiles não-sólidos (Decorações e Itens)
        self._non_solid_chars = set(DECORATION_MAP_CODES.keys()).union(set(ITEM_MAP_CODES.keys()))

        # Mapa para Colisão
        self.game_map = game_map

        # Assets
        self.animations = load_player_assets()

        # --- Variáveis de Combate e Estado de Vida ---
        self.health = 100
        self.is_dead = False # CRÍTICO: Estado de Morte
        self.is_hit = False
        self.is_attacking = False
        self.current_direction = 'right'

        # Estado de Movimento e Animação
        self.state = 'idle_right'
        self.current_frame = 0
        self.animation_timer = 0

        # Posição e Físicas
        self.pos = list(start_pos)  # [x, y]
        self.vertical_speed = 0
        self.on_ground = False

        # Imagem e Retângulo
        self.image = self.animations['idle_right'][0]
        self.rect = self.image.get_rect(topleft=self.pos)

        # Collider
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

    # --- MÉTODOS DE COMBATE E DANO ---

    def attack(self):
        """Inicia a animação de ataque."""
        if not self.is_dead and not self.is_hit and not self.is_attacking:
            self.is_attacking = True
            self.current_frame = 0
            self.animation_timer = 0
            self.state = 'attack_' + self.current_direction

    def receive_damage(self, amount):
        """Processa o recebimento de dano (Atualizado para morte)."""
        if self.is_dead or self.is_hit:
            return

        self.health -= amount
        self.health = max(0, self.health)

        if self.health <= 0:
            self.is_dead = True
            # Define o estado de morte para a animação
            self.state = 'death_' + self.current_direction
        else:
            self.is_hit = True
            self.state = 'hit_' + self.current_direction

        self.current_frame = 0
        self.animation_timer = 0

    # --- LÓGICA DE COLISÃO ---

    def _check_collision_y(self):
        """Verifica e resolve colisões verticais com o mapa."""
        collided = False

        if not self.game_map or not self.game_map[0]:
            return collided

        map_height = len(self.game_map)
        map_width = len(self.game_map[0])

        start_col = max(0, self.collider.left // TILE_SIZE)
        end_col = min(map_width, (self.collider.right + TILE_SIZE - 1) // TILE_SIZE)
        start_row = max(0, self.collider.top // TILE_SIZE)
        end_row = min(map_height, (self.collider.bottom + TILE_SIZE - 1) // TILE_SIZE)

        if start_row >= end_row or start_col >= end_col:
            self.on_ground = False
            return collided

        for y in range(start_row, end_row):
            for x in range(start_col, end_col):
                tile_map_char = self.game_map[y][x]

                if tile_map_char != ' ' and tile_map_char not in self._non_solid_chars:
                    tile_rect = pg.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)

                    if self.collider.colliderect(tile_rect):
                        collided = True

                        if self.vertical_speed > 0:  # Caindo
                            self.collider.bottom = tile_rect.top
                            self.on_ground = True
                            self.vertical_speed = 0
                        elif self.vertical_speed < 0:  # Subindo
                            self.collider.top = tile_rect.bottom
                            self.vertical_speed = 0

                        self.pos[1] = self.collider.top - self.collider_offset_y
                        self.collider.top = self.pos[1] + self.collider_offset_y
                        return collided

        self.on_ground = False
        return collided

    def _check_collision_x(self, move_dir):
        """Verifica e resolve colisões horizontais com o mapa."""

        if not self.game_map or not self.game_map[0]:
            return False

        map_height = len(self.game_map)
        map_width = len(self.game_map[0])

        start_col = max(0, self.collider.left // TILE_SIZE)
        end_col = min(map_width, (self.collider.right + TILE_SIZE - 1) // TILE_SIZE)
        start_row = max(0, self.collider.top // TILE_SIZE)
        end_row = min(map_height, (self.collider.bottom + TILE_SIZE - 1) // TILE_SIZE)

        if start_row >= end_row or start_col >= end_col:
            return False

        for y in range(start_row, end_row):
            for x in range(start_col, end_col):
                tile_map_char = self.game_map[y][x]

                if tile_map_char != ' ' and tile_map_char not in self._non_solid_chars:
                    tile_rect = pg.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)

                    if self.collider.colliderect(tile_rect):
                        if move_dir == 'right':
                            self.collider.right = tile_rect.left
                        elif move_dir == 'left':
                            self.collider.left = tile_rect.right

                        self.pos[0] = self.collider.left - self.collider_offset_x
                        self.collider.left = self.pos[0] + self.collider_offset_x
                        return True
        return False

    def jump(self):
        """Faz o jogador pular, se estiver no chão."""
        # Bloqueia o pulo se estiver em estado de ação ou morto
        if self.is_dead or self.is_hit or self.is_attacking:
            return

        if self.on_ground:
            self.vertical_speed = PLAYER_JUMP_FORCE
            self.on_ground = False

    def move(self, keys_pressed):
        """Atualiza a posição horizontal e o estado de animação."""

        # Bloqueia o movimento se estiver em estado de ação ou morto
        if self.is_dead or self.is_hit or self.is_attacking:
            return

        # 1. Movimento Horizontal e Limites do Mundo
        moved = False
        move_dir = ''
        new_x = self.pos[0]

        if keys_pressed[pg.K_d]:
            new_x += PLAYER_SPEED
            move_dir = 'right'
            moved = True
        elif keys_pressed[pg.K_a]:
            new_x -= PLAYER_SPEED
            move_dir = 'left'
            moved = True

        new_x = max(self.min_x, new_x)
        new_x = min(self.max_x, new_x)

        # 2. Atualiza Posição e Colisão X
        if self.pos[0] != new_x:
            self.pos[0] = new_x
            self.collider.left = self.pos[0] + self.collider_offset_x
            self._check_collision_x(move_dir)

        # 3. Atualização do Estado de Animação
        current_direction: str = self.current_direction
        new_state = self.state

        if moved:
            if move_dir == 'right':
                new_state = 'run_right'
            elif move_dir == 'left':
                new_state = 'run_left'
            current_direction = move_dir
        else:
            if current_direction == 'right':
                new_state = 'idle_right'
            else:
                new_state = 'idle_left'

        if new_state != self.state:
            self.current_frame = 0
            self.animation_timer = 0

        self.state = new_state
        self.current_direction = current_direction

    def _animate(self):
        """Atualiza o frame da animação do jogador com lógica de estados."""

        # 1. Prioridade e Determinação do Estado Atual
        if self.is_dead:
            current_state = 'death_' + self.current_direction
            loop = False
        elif self.is_hit:
            current_state = 'hit_' + self.current_direction
            loop = False
        elif self.is_attacking:
            current_state = 'attack_' + self.current_direction
            loop = False
        else:
            current_state = self.state
            loop = True

        animation_set = self.animations[current_state]
        num_frames = len(animation_set)

        if self.current_frame >= num_frames:
            self.current_frame = 0
            self.animation_timer = 0

        # 2. Atualização do Frame
        self.animation_timer += 1

        if self.animation_timer >= PLAYER_ANIMATION_SPEED:
            self.current_frame += 1
            self.animation_timer = 0

        # 3. Lógica de Fim de Animação
        if self.current_frame >= num_frames:
            if loop:
                self.current_frame = 0
            else:
                # Fim do HIT
                if self.is_hit:
                    self.is_hit = False
                    self.state = 'idle_' + self.current_direction
                # Fim do ATTACK
                elif self.is_attacking:
                    self.is_attacking = False
                    self.state = 'idle_' + self.current_direction

                # Morte: Trava no último frame
                if self.is_dead:
                    self.current_frame = num_frames - 1
                else:
                    self.current_frame = 0

        # 4. Define a imagem
        self.image = animation_set[self.current_frame]
        self.state = current_state

    def update(self, offset_x):
        """Lógica de atualização do jogador: gravidade, colisão e animação."""

        # 1. Gravidade e Colisão Vertical (SEMPRE aplicado, mesmo que morto)
        self._apply_gravity()
        self._check_collision_y()

        # 2. Animação
        self._animate()

        # 3. Atualiza o rect principal para o desenho (APLICA O OFFSET)
        self.rect.topleft = (self.pos[0] + offset_x, self.pos[1])