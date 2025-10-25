# Enemy.py

import pygame as pg
from code.Const import ENEMY_SPEED, GRAVITY, TILE_SIZE, ENEMY_ANIMATION_SPEED, AGGRO_RANGE


class Enemy(pg.sprite.Sprite):
    def __init__(self, start_pos, enemy_type, assets, game_map):
        super().__init__()

        self.game_map = game_map
        self.type = enemy_type

        # Animação e estados
        # 'assets[enemy_type]' deve conter {'idle': [frames], 'run': [frames]}
        self.animations = assets[enemy_type]
        self.state = 'idle' # Começo ocioso
        self.current_frame = 0
        self.animation_timer = 0

        # Posição e Físicas
        self.pos = list(start_pos)  # [x, y]
        self.vertical_speed = 0
        self.speed = ENEMY_SPEED
        self.direction = 1  # 1: direita, -1: esquerda (usado para movimento e flip)
        self.aggro_range = AGGRO_RANGE # Raio para detectar o jogador

        # Imagem e Rect (Usa o primeiro frame para o rect inicial)
        self.image = self.animations[self.state][0] # Usa o primeiro frame do estado 'idle'
        self.rect = self.image.get_rect(topleft=self.pos)

        # Collider
        self.collider = pg.Rect(self.pos[0], self.pos[1], TILE_SIZE, TILE_SIZE)
        self.on_ground = False

    def _check_aggro(self, player_pos):
        """Verifica a proximidade do jogador e define o estado do inimigo."""

        # Distância horizontal do jogador
        dx = player_pos[0] - self.pos[0]
        distance = abs(dx)
        new_state = self.state

        if distance < self.aggro_range:
            # Jogador está próximo -> Entra no estado de CAÇA
            new_state = 'run'

            # Define a direção para correr EM DIREÇÃO ao jogador
            # Se dx > 0, o jogador está à direita (direction = 1)
            self.direction = 1 if dx > 0 else -1

        else:
            new_state = 'idle' # Entra em idle

        if new_state != self.state:
            print(f"Inimigo mudando de estado: {self.state} -> {new_state}. Distância: {distance}")  # <-- VERIFICAÇÃO
            # Reseta a animação ao mudar para 'idle'
            self.current_frame = 0
            self.animation_timer = 0

            self.state = new_state # Aplica o novo estado

    def _apply_gravity(self):
        """Aplica a gravidade."""
        self.vertical_speed += GRAVITY
        self.vertical_speed = min(self.vertical_speed, 15)  # Limita a velocidade de queda
        self.pos[1] += self.vertical_speed
        self.collider.top = self.pos[1]

    def _check_collision_y(self):
        """Verifica e resolve colisões verticais (chão/teto)."""

        start_col = max(0, self.collider.left // TILE_SIZE)
        end_col = min(len(self.game_map[0]), (self.collider.right + TILE_SIZE - 1) // TILE_SIZE)
        start_row = max(0, self.collider.top // TILE_SIZE)
        end_row = min(len(self.game_map), (self.collider.bottom + TILE_SIZE - 1) // TILE_SIZE)

        for y in range(start_row, end_row):
            for x in range(start_col, end_col):
                # Verifica se é um tile sólido
                if self.game_map[y][x] != ' ':
                    tile_rect = pg.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)

                    if self.collider.colliderect(tile_rect):
                        if self.vertical_speed > 0:  # Caindo (colisão com o chão)
                            # Reposiciona acima do tile
                            self.pos[1] = tile_rect.top - TILE_SIZE
                            self.vertical_speed = 0
                            self.on_ground = True
                        elif self.vertical_speed < 0:  # Batendo a cabeça
                            # Reposiciona abaixo do tile
                            self.pos[1] = tile_rect.bottom
                            self.vertical_speed = 0

                        self.collider.top = self.pos[1]
                        return  # Colidiu e resolveu, pode sair

        self.on_ground = False

    def _move_and_check_collision_x(self):
        """Movimento horizontal e inversão de direção ao bater em paredes."""

        # 1. Aplica o movimento
        self.pos[0] += self.speed * self.direction
        self.collider.left = self.pos[0]

        # 2. Verifica a Colisão X
        start_col = max(0, self.collider.left // TILE_SIZE)
        end_col = min(len(self.game_map[0]), (self.collider.right + TILE_SIZE - 1) // TILE_SIZE)
        start_row = max(0, self.collider.top // TILE_SIZE)
        end_row = min(len(self.game_map), (self.collider.bottom + TILE_SIZE - 1) // TILE_SIZE)

        for y in range(start_row, end_row):
            for x in range(start_col, end_col):
                # Verifica se é um tile sólido
                if self.game_map[y][x] != ' ':
                    tile_rect = pg.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                    if self.collider.colliderect(tile_rect):
                        # Bateu, inverte a direção
                        self.direction *= -1
                        # Pequeno ajuste na posição para sair da colisão imediatamente
                        self.pos[0] += self.speed * self.direction * 2
                        self.collider.left = self.pos[0]
                        return

    def _animate(self):
        """Atualiza o frame da animação do inimigo e aplica o flip."""

        # Seleciona o conjunto de frames baseado no estado atual

        animation_set = self.animations[self.state]
        if not animation_set:
            return
        if self.current_frame >= len(animation_set):
            self.current_frame = 0

        # Lógica de controle de frame
        self.animation_timer += 1
        if self.animation_timer >= ENEMY_ANIMATION_SPEED:
            self.current_frame = (self.current_frame + 1) % len(animation_set)
            self.animation_timer = 0

        # Pega a imagem do frame atual
        img = animation_set[self.current_frame]

        # Aplica o flip de acordo com a direção (mesmo em idle para manter a face)
        if self.direction == -1:
            # Inverte horizontalmente (True), não verticalmente (False)
            self.image = pg.transform.flip(img, True, False)
        else:
            self.image = img

    def update(self, offset_x, player_pos):
        """Atualiza o inimigo, aplicando offset da câmera e executando a lógica."""

        # 1. Verifica Aggro e define o estado/direção
        self._check_aggro(player_pos)

        # 2. Física e Colisão
        self._apply_gravity()
        self._check_collision_y()

        # 3. Movimento (SÓ SE ESTIVER NO ESTADO 'RUN')
        if self.state == 'run':
            self._move_and_check_collision_x()

        # 4. Animação
        self._animate()

        # 5. Atualiza a posição de desenho
        self.rect.topleft = (self.pos[0] + offset_x, self.pos[1])