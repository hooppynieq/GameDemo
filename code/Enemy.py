# Enemy.py

import pygame as pg
from code.Const import (
    ENEMY_SPEED, GRAVITY, TILE_SIZE, ENEMY_ANIMATION_SPEED, AGGRO_RANGE,
    DECORATION_MAP_CODES, ITEM_MAP_CODES
)


class Enemy(pg.sprite.Sprite):
    def __init__(self, start_pos, enemy_type, assets, game_map):
        super().__init__()

        self.game_map = game_map
        self.type = enemy_type

        self._non_solid_chars = set(DECORATION_MAP_CODES.keys()).union(set(ITEM_MAP_CODES.keys()))

        self.animations = assets[enemy_type]
        self.state = 'idle'
        self.current_frame = 0
        self.animation_timer = 0

        # --- Variáveis de Combate e Estado de Vida ---
        self.health = 50
        self.is_dead = False
        self.is_hit = False
        self.is_attacking = False
        self.kill_flag = False

        # --- Configurações de Combate ---
        self.attack_range = TILE_SIZE * 1.5
        self.attack_cooldown = 0
        self.attack_delay = 60

        # Posição e Físicas
        self.pos = list(start_pos)  # [x, y]
        self.vertical_speed = 0
        self.speed = ENEMY_SPEED
        self.direction = 1  # 1: direita, -1: esquerda
        self.aggro_range = AGGRO_RANGE

        # Imagem e Rect
        self.image = self.animations[self.state][0]
        self.rect = self.image.get_rect(topleft=self.pos)

        # [CORREÇÃO DE ELEVAÇÃO] Calcula a posição Y correta para alinhar a BASE do inimigo
        # (self.rect.bottom) com a BASE do tile (start_pos[1] + TILE_SIZE).

        # A nova posição Y (top) será: (Y do chão) - (Altura da imagem)
        tile_bottom_y = start_pos[1] + TILE_SIZE
        sprite_height = self.image.get_height()

        # Define a posição inicial com o Y corrigido
        self.pos = [start_pos[0], tile_bottom_y - sprite_height]

        self.rect.topleft = self.pos

        # Collider (Agora alinhado corretamente com o rect)
        self.collider = self.rect.copy()  # Usamos uma cópia para fins de colisão se necessário
        self.on_ground = False

        # Removido: as linhas de ajuste desnecessárias (self.pos[1] -= 1, etc.)

        # # Imagem e Rect
        # self.image = self.animations[self.state][0]
        # self.rect = self.image.get_rect(topleft=self.pos)
        #
        # # Collider
        # self.collider = self.rect
        # self.on_ground = False
        #
        # self.pos[1] -= 1
        # self.rect.top = self.pos[1]
        # self.collider.top = self.pos[1]

    # ----------------------------------------------------------------------
    # MÉTODOS DE FÍSICA E COLISÃO (Inalterados)
    # ----------------------------------------------------------------------

    def _apply_gravity(self):
        self.vertical_speed += GRAVITY
        self.vertical_speed = min(self.vertical_speed, 15)
        self.pos[1] += self.vertical_speed
        self.collider.top = self.pos[1]
        self.rect.top = self.pos[1]

    def _check_collision_y(self):
        map_height = len(self.game_map)
        map_width = len(self.game_map[0])

        start_col = max(0, self.collider.left // TILE_SIZE)
        end_col = min(map_width, (self.collider.right + TILE_SIZE - 1) // TILE_SIZE)
        start_row = max(0, self.collider.top // TILE_SIZE)
        end_row = min(map_height, (self.collider.bottom + TILE_SIZE - 1) // TILE_SIZE)

        collided_this_frame = False

        if start_row >= end_row or start_col >= end_col:
            self.on_ground = False
            return False

        for y in range(start_row, end_row):
            for x in range(start_col, end_col):
                tile_map_char = self.game_map[y][x]

                if tile_map_char != ' ' and tile_map_char not in self._non_solid_chars:
                    tile_rect = pg.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)

                    if self.collider.colliderect(tile_rect):
                        collided_this_frame = True

                        if self.vertical_speed > 0:
                            self.collider.bottom = tile_rect.top
                            self.vertical_speed = 0
                            self.on_ground = True
                        elif self.vertical_speed < 0:
                            self.collider.top = tile_rect.bottom
                            self.vertical_speed = 0
                            self.on_ground = False

                        self.pos[1] = self.collider.top
                        self.rect.top = self.pos[1]
                        return True

        if not collided_this_frame:
            self.on_ground = False

        return collided_this_frame

    def _check_collision_x(self):
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
                        self.direction *= -1
                        return True
        return False

    # ----------------------------------------------------------------------
    # MÉTODOS DE COMBATE E LÓGICA
    # ----------------------------------------------------------------------

    def receive_damage(self, amount):
        if not self.is_dead and not self.is_hit:
            self.health -= amount
            self.health = max(0, self.health)

            print(f"Inimigo '{self.type}' recebeu {amount} de dano! Vida atual: {self.health}")

            if self.health <= 0:
                self.is_dead = True
                self.state = 'death'  # Estado de morte
                self.is_attacking =False # Zera o ataque imediatamente!
            else:
                self.is_hit = True
                self.state = 'hit'

            self.current_frame = 0
            self.animation_timer = 0

    def can_deal_damage(self):
        if self.is_dead:
            return False

        attack_frames = self.animations.get('attack', [])
        if not attack_frames:
            return False

        hit_frames = [1, 2, 3]
        return self.is_attacking and self.current_frame in hit_frames

    def _check_aggro(self, player_pos):
        if self.is_dead or self.is_hit or self.is_attacking:
            return

        dx = player_pos[0] - self.pos[0]
        distance = abs(dx)
        new_state = self.state

        if distance < self.aggro_range:
            self.direction = 1 if dx > 0 else -1

            if distance < self.attack_range and self.attack_cooldown <= 0:
                new_state = 'attack'
                self.is_attacking = True
                self.attack_cooldown = self.attack_delay
            else:
                new_state = 'run'
        else:
            new_state = 'idle'

        if new_state != self.state:
            self.current_frame = 0
            self.animation_timer = 0
            self.state = new_state

    def _move_and_check_collision_x(self):
        if self.is_dead or self.is_hit or self.is_attacking:
            return

        future_x = self.pos[0] + self.speed * self.direction

        step_col = (future_x + self.direction * self.collider.width // 2) // TILE_SIZE
        foot_row = (self.collider.bottom + 1) // TILE_SIZE

        map_width = len(self.game_map[0])
        map_height = len(self.game_map)

        is_at_edge = step_col < 0 or step_col >= map_width
        is_above_map_bottom = foot_row >= map_height

        tile_below = ' '
        if not is_at_edge and not is_above_map_bottom and foot_row < map_height:
            tile_below = self.game_map[foot_row][step_col]

        if is_at_edge or tile_below == ' ' or tile_below in self._non_solid_chars:
            if self.on_ground:
                self.direction *= -1
                return

        self.pos[0] = future_x
        self.collider.left = self.pos[0]
        self.rect.left = self.pos[0]

        if self._check_collision_x():
            self.collider.left = self.pos[0]
            self.rect.left = self.pos[0]

    def _animate(self):
        """Atualiza o frame da animação do inimigo e aplica o flip."""

        # 1. Prioridade
        if self.is_dead:
            current_state = 'death'
            loop = False
        elif self.is_hit:
            current_state = 'hit'
            loop = False
        elif self.is_attacking:
            current_state = 'attack'
            loop = False
        else:
            current_state = self.state
            loop = True

        animation_set = self.animations.get(current_state)
        if not animation_set:
            current_state = 'idle'
            animation_set = self.animations.get(current_state, [self.image])
            loop = True

        num_frames = len(animation_set)

        # 2. Atualização do Frame
        # Garante que ele não tente incrementar se já estiver no último frame de morte
        if not (self.is_dead and self.current_frame == num_frames - 1):
            self.animation_timer += 1

            if self.animation_timer >= ENEMY_ANIMATION_SPEED:
                self.current_frame += 1
                self.animation_timer = 0

        # 3. Lógica de Fim de Animação
        if self.current_frame >= num_frames:
            if loop:
                self.current_frame = 0
            else:
                if self.is_hit:
                    self.is_hit = False
                    self.state = 'idle'
                    self.current_frame = 0
                elif self.is_attacking:
                    self.is_attacking = False
                    self.state = 'idle'
                    self.current_frame = 0

                # CORREÇÃO CRÍTICA: Trava no último frame e sinaliza para remoção.
                if self.is_dead:
                    self.current_frame = num_frames - 1
                    self.kill_flag = True
                    # O return é crucial para evitar que ele tente acessar a próxima imagem
                    # se o frame já foi travado.
                    # Não vamos usar o return aqui, mas sim o if no início para travar.
                else:
                    self.current_frame = 0

        # 4. Define a imagem e aplica o flip
        # Se a animação de morte foi travada, garantimos que o frame correto seja usado
        frame_index = self.current_frame
        if self.is_dead and frame_index >= num_frames:
            frame_index = num_frames - 1

        # Garante que frame_index não exceda o num_frames (mesmo que a lógica acima já resolva)
        frame_index = min(frame_index, num_frames - 1)

        img = animation_set[frame_index]

        if self.direction == -1:
            self.image = pg.transform.flip(img, True, False)
        else:
            self.image = img

        self.state = current_state

    # ----------------------------------------------------------------------
    # LOOP PRINCIPAL
    # ----------------------------------------------------------------------

    def update(self, offset_x, player_pos):
        """Atualiza o inimigo."""

        # 1. Gerencia o Cooldown do ataque
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1

        # 2. FÍSICA E COLISÃO VERTICAL (APLICADO SEMPRE)
        self._apply_gravity()
        self._check_collision_y()

        # 3. Lógica de estado e movimento (SÓ SE ESTIVER VIVO)
        if not self.is_dead:

            # Verifica o estado (run/attack/idle) E DEFINE self.direction
            if not self.is_hit and not self.is_attacking:
                self._check_aggro(player_pos)

            if self.state == 'run':
                self._move_and_check_collision_x()

        # 4. Animação
        self._animate()

        # 5. Atualiza a posição de desenho
        self.rect.topleft = (self.pos[0] + offset_x, self.pos[1])