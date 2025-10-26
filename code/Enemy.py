#Enemy.py
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

        # Variável para ignorar colisões de tiles não-sólidos (Decorações e Itens)
        self._non_solid_chars = set(DECORATION_MAP_CODES.keys()).union(set(ITEM_MAP_CODES.keys()))

        # Animação e estados
        self.animations = assets[enemy_type]
        self.state = 'idle'
        self.current_frame = 0
        self.animation_timer = 0

        # --- Variáveis de Combate e Estado de Vida ---
        self.health = 25
        self.is_dead = False
        self.is_hit = False
        self.is_attacking = False
        self.kill_flag = False  # Sinaliza que a animação de morte terminou e deve ser removido.

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

        # Collider: REDEFINIÇÃO DO HITBOX PARA EVITAR COLISÃO FANTASMA
        # Criamos um novo Rect que representa apenas o corpo do inimigo.
        # Exemplo: Reduzir a altura em 25% (0.75) e centralizar no X.

        # Estas proporções (0.8 e 0.9) são estimativas. Ajuste com base no tamanho real do seu sprite.
        COLLIDER_WIDTH_FACTOR = 0.8
        COLLIDER_HEIGHT_FACTOR = 0.9

        collider_width = int(self.rect.width * COLLIDER_WIDTH_FACTOR)
        collider_height = int(self.rect.height * COLLIDER_HEIGHT_FACTOR)

        # Criamos o novo collider, alinhando sua base (bottom) com a base do rect da imagem.
        self.collider = pg.Rect(
            self.pos[0] + (self.rect.width - collider_width) / 2,  # Centraliza no X
            self.pos[1] + (self.rect.height - collider_height),  # Alinha a base
            collider_width,
            collider_height
        )

        self.on_ground = False

        # Correção no ajuste inicial de posição: Use o collider.top
        self.pos[1] -= 1
        self.rect.top = self.pos[1]
        self.collider.top = self.pos[1]  # <--- O collider é o que define o Y para a física

    # ----------------------------------------------------------------------
    # MÉTODOS DE FÍSICA E COLISÃO (MANTIDOS)
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
    # MÉTODOS DE COMBATE E LÓGICA (MODIFICADO receive_damage)
    # ----------------------------------------------------------------------

    def receive_damage(self, amount):
        """
        Processa o recebimento de dano.
        Retorna True se o inimigo for morto AGORA.
        """
        if not self.is_dead and not self.is_hit:
            self.health -= amount
            self.health = max(0, self.health)

            is_newly_dead = False  # NOVO: Flag para sinalizar a morte

            if self.health <= 0:
                self.is_dead = True
                self.state = 'death'
                self.is_attacking = False  # Garante que o ataque pare
                is_newly_dead = True  # Sinaliza a morte
            else:
                self.is_hit = True
                self.state = 'hit'

            self.current_frame = 0
            self.animation_timer = 0

            return is_newly_dead  # RETORNA TRUE se o inimigo foi morto

        return False  # Retorna False se o dano foi ignorado ou se o inimigo já estava morto/atingido

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

            if distance < self.attack_range and self.attack_cooldown <= 0:
                new_state = 'attack'
                self.is_attacking = True
                self.attack_cooldown = self.attack_delay
                pass
            else:
                new_state = 'run'
                # CORREÇÃO AQUI: Inverte a lógica de direção.
                # Se dx > 0 (Player à direita), o inimigo deve ir para a direita (1).
                # No seu caso, se o inimigo está de costas, a direção 1 ou -1 está ligada ao flip errado.

                # Vamos tentar INVERTER a direção:
                self.direction = 1 if dx > 0 else -1

                # Se ainda estiver de costas, INVERTA NOVAMENTE:
                # self.direction = 1 if dx < 0 else -1 # (Alternativa)
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
                elif self.is_dead:
                    # Trava no último frame e sinaliza para remoção.
                    self.current_frame = num_frames - 1
                    self.kill_flag = True
                    return  # Sai para evitar redefinição de imagem
                else:
                    self.current_frame = 0

        # 4. Define a imagem e aplica o flip
        img = animation_set[self.current_frame]

        if self.direction == 1:
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

        # 2. Lógica de estado e movimento
        if not self.is_dead:
            if not self.is_hit and not self.is_attacking:
                self._check_aggro(player_pos)

            # Aplica a física (gravidade e colisão)
            self._apply_gravity()
            self._check_collision_y()

            if self.state == 'run':
                self._move_and_check_collision_x()

        else:
            # Mesmo morto, aplica a gravidade para ele cair no chão se estiver no ar
            self._apply_gravity()
            self._check_collision_y()

        # 3. Animação
        self._animate()

        # 4. Atualiza a posição de desenho
        self.rect.topleft = (self.pos[0] + offset_x, self.pos[1])