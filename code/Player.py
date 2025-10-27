import pygame as pg

from code.Const import (
    PLAYER_COLLIDER_SIZE, GRAVITY, TILE_SIZE, PLAYER_JUMP_FORCE, PLAYER_SPEED,
    PLAYER_ANIMATION_SPEED, DECORATION_MAP_CODES, ITEM_MAP_CODES
)
from code.utils import load_player_assets


class Player(pg.sprite.Sprite):
    def __init__(self, start_pos, game_map, map_width_pixels):
        super().__init__()

        # Ignora colisões com tiles não-sólidos (Decorações e Itens)
        self._non_solid_chars = set(DECORATION_MAP_CODES.keys()).union(set(ITEM_MAP_CODES.keys()))

        self.game_map = game_map
        self.animations = load_player_assets()

        # ESTADO DE COMBATE E VIDA
        self.health = 100
        self.is_dead = False
        self.is_hit = False
        self.is_attacking = False
        self.current_direction = 'right'

        self.state = 'idle_right'
        self.current_frame = 0
        self.animation_timer = 0

        # Posição e Físicas
        self.pos = list(start_pos)
        self.vertical_speed = 0
        self.on_ground = False

        self.image = self.animations['idle_right'][0]
        self.rect = self.image.get_rect(topleft=self.pos)

        # Collider (Retângulo de colisão real)
        self.collider_offset_x = 40
        self.collider_offset_y = 8
        self.collider = pg.Rect(self.pos[0] + self.collider_offset_x, self.pos[1] + self.collider_offset_y,
                                PLAYER_COLLIDER_SIZE[0], PLAYER_COLLIDER_SIZE[1])

        # Limites do mundo
        self.map_width_pixels = map_width_pixels
        self.min_x = 0
        self.max_x = map_width_pixels - PLAYER_COLLIDER_SIZE[0] - self.collider_offset_x

    def draw_debug(self, screen, offset_x):
        """Desenha o collider do Player na tela para depuração (AZUL)."""
        debug_rect = self.collider.copy()
        debug_rect.x += offset_x
        pg.draw.rect(screen, (0, 0, 255), debug_rect, 2)
        if self.on_ground:
            pg.draw.rect(screen, (0, 255, 0), self.collider, 2)

    def _apply_gravity(self):
        """Aplica a gravidade e limita a velocidade vertical."""
        self.vertical_speed += GRAVITY
        self.vertical_speed = min(self.vertical_speed, 15)
        self.pos[1] += self.vertical_speed
        self.collider.top = self.pos[1] + self.collider_offset_y

    # MÉTODOS DE COMBATE E DANO

    def attack(self):
        """Inicia a animação de ataque."""
        if not self.is_dead and not self.is_hit and not self.is_attacking:
            self.is_attacking = True
            self.current_frame = 0
            self.animation_timer = 0
            self.state = 'attack_' + self.current_direction

    def receive_damage(self, amount):
        """Processa o recebimento de dano e transiciona para HIT ou DEATH."""
        if self.is_dead or self.is_hit:
            return

        self.health -= amount
        self.health = max(0, self.health)

        if self.health <= 0:
            self.is_dead = True
            self.state = 'death_' + self.current_direction
        else:
            self.is_hit = True
            self.state = 'hit_' + self.current_direction

        self.current_frame = 0
        self.animation_timer = 0

    # LÓGICA DE COLISÃO

    def _check_collision_y(self):
        """Verifica e resolve colisões verticais com tiles sólidos do mapa."""
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

                        if self.vertical_speed > 0:
                            self.collider.bottom = tile_rect.top
                            self.on_ground = True
                            self.vertical_speed = 0
                        elif self.vertical_speed < 0:
                            self.collider.top = tile_rect.bottom
                            self.vertical_speed = 0

                        self.pos[1] = self.collider.top - self.collider_offset_y
                        self.collider.top = self.pos[1] + self.collider_offset_y
                        return collided

        self.on_ground = False
        return collided

    def _check_collision_x(self, move_dir):
        """Verifica e resolve colisões horizontais com tiles sólidos do mapa."""

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

    def check_enemy_surface_collision(self, enemies):
        """Verifica e resolve a colisão de 'stomp' (pouso no topo do inimigo)."""
        for enemy in enemies:
            if self.collider.colliderect(enemy.collider):
                # Se o Player está caindo ou parado e seu fundo está acima do topo do inimigo
                if self.vertical_speed >= 0:
                    if self.collider.bottom <= enemy.collider.top + 5:
                        new_y_bottom = enemy.get_top_surface()
                        self.collider.bottom = new_y_bottom

                        self.vertical_speed = 0
                        self.on_ground = True

                        self.pos[1] = self.collider.top - self.collider_offset_y
                        self.rect.top = self.pos[1]
                        return True
        return False

    def jump(self):
        """Faz o jogador pular, se estiver no chão."""
        if self.is_dead or self.is_hit or self.is_attacking:
            return

        if self.on_ground:
            self.vertical_speed = PLAYER_JUMP_FORCE
            self.on_ground = False

    def move(self, keys_pressed):
        """Atualiza a posição horizontal e o estado de animação."""

        if self.is_dead or self.is_hit or self.is_attacking:
            return

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

        if self.pos[0] != new_x:
            self.pos[0] = new_x
            self.collider.left = self.pos[0] + self.collider_offset_x
            self._check_collision_x(move_dir)

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
        """Atualiza o frame da animação do jogador."""

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

        self.animation_timer += 1

        if self.animation_timer >= PLAYER_ANIMATION_SPEED:
            self.current_frame += 1
            self.animation_timer = 0

        # Lógica de fim de animações não-looping (HIT, ATTACK, DEATH).
        if self.current_frame >= num_frames:
            if loop:
                self.current_frame = 0
            else:
                if self.is_hit:
                    self.is_hit = False
                    self.state = 'idle_' + self.current_direction
                elif self.is_attacking:
                    self.is_attacking = False
                    self.state = 'idle_' + self.current_direction

                if self.is_dead:
                    self.current_frame = num_frames - 1
                else:
                    self.current_frame = 0

        self.image = animation_set[self.current_frame]
        self.state = current_state

    def update(self, offset_x, enemies):
        """Lógica de atualização do jogador: gravidade, colisão e animação."""

        # Aplica Física e Colisão Vertical (Mesmo se morto).
        self._apply_gravity()
        self._check_collision_y()
        self.check_enemy_surface_collision(enemies)

        self._animate()

        # Atualiza o rect de desenho (aplica offset da câmera).
        self.rect.topleft = (self.collider.left + offset_x - self.collider_offset_x,
                             self.collider.top - self.collider_offset_y)