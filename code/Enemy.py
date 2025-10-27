import pygame as pg
from code.Const import (
    ENEMY_SPEED, GRAVITY, TILE_SIZE, ENEMY_ANIMATION_SPEED, AGGRO_RANGE,
    DECORATION_MAP_CODES, ENEMY_COLLIDER_SIZE, ITEM_MAP_CODES
)


class Enemy(pg.sprite.Sprite):
    def __init__(self, start_pos, enemy_type, assets, game_map):
        super().__init__()

        self.game_map = game_map
        self.type = enemy_type

        # Caracteres que não são sólidos no mapa (Decorações e Itens)
        self._non_solid_chars = set(DECORATION_MAP_CODES.keys()).union(set(ITEM_MAP_CODES.keys()))

        # Animação e estados
        self.animations = assets[enemy_type]
        self.state = 'idle'
        self.current_frame = 0
        self.animation_timer = 0

        # Variáveis de Combate e Estado de Vida
        self.health = 25
        self.is_dead = False
        self.is_hit = False
        self.is_attacking = False
        self.kill_flag = False

        # Configurações Específicas (Seashell vs. Tooth)
        self.is_fixed = (self.type == 'seashell')
        self.can_move = not self.is_fixed

        if self.type == 'seashell':
            self.attack_range = TILE_SIZE * 1.0
            self.attack_delay = 120
            self.aggro_range = TILE_SIZE * 3
            self.health = 50
        else:
            self.attack_range = TILE_SIZE * 1.5
            self.attack_delay = 60
            self.aggro_range = AGGRO_RANGE

        self.attack_cooldown = 0

        # Posição e Físicas
        self.pos = list(start_pos)
        self.vertical_speed = 0
        self.speed = ENEMY_SPEED
        # Direção inicial (Seashell fixo, outros móveis)
        self.direction = 1 if self.type != 'seashell' else -1
        self.aggro_range = AGGRO_RANGE

        # Imagem e Rect
        self.image = self.animations[self.state][0]
        self.rect = self.image.get_rect(topleft=self.pos)

        # DEFINIÇÃO DE COLLIDER E POSICIONAMENTO INICIAL NO CHÃO

        # 1. Configurações de Collider (usando fatores de escala)
        COLLIDER_WIDTH_FACTOR = 0.8
        COLLIDER_HEIGHT_FACTOR = 0.9

        collider_width = int(self.rect.width * COLLIDER_WIDTH_FACTOR)
        collider_height = int(self.rect.height * COLLIDER_HEIGHT_FACTOR)

        self.collider = pg.Rect(
            self.pos[0] + (self.rect.width - collider_width) / 2,
            self.pos[1] + (self.rect.height - collider_height),
            collider_width,
            collider_height
        )

        self.on_ground = False

        # 2. Ajusta a base do collider ao chão do tile (ancoragem vertical)
        target_bottom = start_pos[1] + TILE_SIZE
        self.collider.bottom = target_bottom

        # 3. Atualiza a posição 'top' do sprite com base no collider
        self.pos[1] = self.collider.top
        self.rect.top = self.pos[1]

        self.on_ground = False

        # 4. Reajuste final de 1 pixel e estado inicial para inimigos fixos
        target_bottom = start_pos[1] + TILE_SIZE
        self.collider.bottom = target_bottom
        self.pos[1] = self.collider.top
        self.rect.top = self.pos[1]

        if self.is_fixed:
            self.on_ground = True
            # Ajuste de 1 pixel para fixar no chão
            self.pos[1] += 1
            self.collider.top = self.pos[1]
            self.rect.top = self.pos[1]

    def draw_debug(self, screen, offset_x):
        """Desenha o collider do Enemy na tela para depuração (VERMELHO)."""
        debug_rect = self.collider.copy()
        debug_rect.x += offset_x
        pg.draw.rect(screen, (255, 0, 0), debug_rect, 2)

    # MÉTODOS DE FÍSICA E COLISÃO
    def _apply_gravity(self):
        # Inimigos fixos param a gravidade quando tocam o chão
        if self.is_fixed and self.on_ground and self.vertical_speed >= 0:
            self.vertical_speed = 0
            return

        self.vertical_speed += GRAVITY
        self.vertical_speed = min(self.vertical_speed, 15)
        self.pos[1] += self.vertical_speed
        self.collider.top = self.pos[1]
        self.rect.top = self.pos[1]

    def get_top_surface(self):
        """Retorna a coordenada Y do topo da superfície de colisão do inimigo."""
        return self.collider.top

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
        if self.is_fixed:
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
                        # Colisão com parede inverte a direção
                        self.direction *= -1
                        return True
        return False

    # MÉTODOS DE COMBATE E LÓGICA

    def receive_damage(self, amount):
        if not self.is_dead and not self.is_hit:
            self.health -= amount
            self.health = max(0, self.health)

            is_newly_dead = False

            if self.health <= 0:
                self.is_dead = True
                self.state = 'death'
                self.is_attacking = False
                is_newly_dead = True
            else:
                self.is_hit = True
                self.state = 'hit'

            self.current_frame = 0
            self.animation_timer = 0

            return is_newly_dead

        return False

    def can_deal_damage(self):
        # Retorna True se o frame de ataque ativo estiver rodando
        attack_frames = self.animations.get('attack', [])
        if not attack_frames:
            return False

        # Define os frames ativos de hit
        hit_frames = {1, 2, 3}
        return self.is_attacking and int(self.current_frame) in hit_frames

    def _check_aggro(self, player_pos):
        if self.is_dead or self.is_hit or self.is_attacking:
            return

        dx = player_pos[0] - self.pos[0]
        distance = abs(dx)
        new_state = self.state

        if distance < self.aggro_range:
            # Lógica de Ataque
            if distance < self.attack_range and self.attack_cooldown <= 0:
                new_state = 'attack'
                self.is_attacking = True
                self.attack_cooldown = self.attack_delay

            # Lógica de Movimento/Perseguição
            else:
                if not self.is_fixed:
                    new_state = 'run'
                    # Persegue o jogador
                    self.direction = 1 if dx > 0 else -1
                else:
                    new_state = 'idle'

        # Inimigo fora do aggro
        else:
            if not self.is_fixed:
                new_state = 'idle'
            # Inimigos fixos mantêm 'idle'

        if new_state != self.state:
            self.current_frame = 0
            self.animation_timer = 0
            self.state = new_state

    def _move_and_check_collision_x(self):
        # Inimigos fixos e em estado de combate não se movem
        if self.is_fixed or self.is_dead or self.is_hit or self.is_attacking:
            return

        future_x = self.pos[0] + self.speed * self.direction

        # Verifica se há chão ou parede na frente
        step_col = (future_x + self.direction * self.collider.width // 2) // TILE_SIZE
        foot_row = (self.collider.bottom + 1) // TILE_SIZE

        map_width = len(self.game_map[0])
        map_height = len(self.game_map)

        is_at_edge = step_col < 0 or step_col >= map_width
        tile_below = ' '
        if not is_at_edge and foot_row < map_height:
            tile_below = self.game_map[foot_row][step_col]

        # Lógica de Virar ao Chegar na Borda do Chão
        if is_at_edge or tile_below == ' ' or tile_below in self._non_solid_chars:
            if self.on_ground:
                self.direction *= -1
                return

        self.pos[0] = future_x
        self.collider.left = self.pos[0]
        self.rect.left = self.pos[0]

        # Verifica colisão com parede
        if self._check_collision_x():
            self.collider.left = self.pos[0]
            self.rect.left = self.pos[0]

    def _animate(self):
        """Atualiza o frame da animação e aplica o flip."""

        # 1. Prioridade do Estado
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

        # 2. Lógica de Animação
        if self.is_fixed and current_state == 'idle':
            # Seashell em IDLE trava no frame 0
            self.current_frame = 0
            self.animation_timer = 0
        else:
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
                    self.current_frame = num_frames - 1
                    self.kill_flag = True
                    return
                else:
                    self.current_frame = 0

        # 4. Define a imagem e aplica o flip
        img = animation_set[int(self.current_frame)]

        if self.direction == 1:
            self.image = pg.transform.flip(img, True, False)
        else:
            self.image = img

        self.state = current_state

    # LOOP PRINCIPAL

    def update(self, offset_x, player_pos):
        """Atualiza o inimigo."""

        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1

        if not self.is_dead:
            if not self.is_hit and not self.is_attacking:
                self._check_aggro(player_pos)

            # Aplica a física
            self._apply_gravity()
            self._check_collision_y()

            if self.state == 'run':
                self._move_and_check_collision_x()

        else:
            # Gravidade mesmo morto para cair fora do mapa
            self._apply_gravity()
            self._check_collision_y()

        self._animate()

        # Atualiza a posição de desenho
        self.rect.topleft = (self.pos[0] + offset_x, self.pos[1])