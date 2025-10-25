# game.py
import pygame as pg

from code.Const import TITLE, TILE_SIZE, GAME_MAP, FPS, CAMERA_X_LIMIT, SCREEN_WIDTH, BLACK, DECORATION_MAP_CODES

from code.Decoration import Decoration
from code.Enemy import Enemy
from code.Item import Item
from code.Player import Player
from code.Trap import Trap
from code.utils import load_background_assets, load_terrain_assets, load_entity_assets, load_audio, \
    load_decoration_assets


class Game:
    def __init__(self, screen):
        self.screen = screen
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.is_running = True

        # --- Carregamento de Assets ---
        self.background_assets = load_background_assets()
        self.terrain_images = load_terrain_assets()
        self.entity_assets = load_entity_assets()
        self.audio = load_audio()

        # Carregamento de Assets de Decoração (Necessário antes de criar objetos)
        self.decoration_assets = load_decoration_assets()

        # --- Variáveis do Mundo e Câmera ---
        self.score = 0
        self.camera_offset_x = 0
        self.map_width_pixels = len(GAME_MAP[0]) * TILE_SIZE

        # --- Componentes do Jogo ---
        self.player = Player(start_pos=[300, 600], game_map=GAME_MAP, map_width_pixels=self.map_width_pixels)
        self.enemies = pg.sprite.Group()
        self.items = pg.sprite.Group()
        self.traps = pg.sprite.Group()
        self.decorations = pg.sprite.Group()  # Novo Grupo para Decorações

        # Criação de objetos do mapa (Inimigos, Itens, Decorações, etc.)
        self._create_level_objects()

        # --- Configuração de Áudio ---
        pg.mixer.music.load(self.audio['bg'])
        pg.mixer.music.play(-1)

        # --- Variáveis de Animação do Fundo ---
        self.cloud_pos = {
            'big_clouds_pos': 0,
            'small_cloud_1_pos': 0,
            'small_cloud_2_pos': 0,
            'small_cloud_3_pos': 0,
        }
        self.water_animation_frame = {
            'big_water': 0,
            'medium_water': 0,
            'small_water': 0,
        }

    # ----------------------------------------------------------------------
    ## Criação de Nível
    # ----------------------------------------------------------------------

    def _create_level_objects(self):
        """Cria Inimigos, Itens, Armadilhas e Decorações com base no GAME_MAP."""
        for y, row in enumerate(GAME_MAP):
            for x, char in enumerate(row):  # A variável de iteração é 'char'
                pos = (x * TILE_SIZE, y * TILE_SIZE)

                # Lógica de Inimigos, Itens, Armadilhas
                if char == 'E':
                    self.enemies.add(Enemy(pos, 'tooth', self.entity_assets, GAME_MAP))
                elif char == '$':
                    self.items.add(Item(pos, 'coin', self.entity_assets))
                elif char == 'T':
                    self.traps.add(Trap(pos, 'spike_ball', self.entity_assets))

                # === Lógica para criar Decorações ===
                # CORREÇÃO: Usando 'char' em vez de 'tile_char'
                if char in DECORATION_MAP_CODES:
                    asset_key = DECORATION_MAP_CODES[char]

                    # 1. Obtenha os assets (imagem ou lista de frames)
                    images = self.decoration_assets[asset_key]

                    # 2. Instancia a CLASSE Decoration IMPORTADA
                    decoration = Decoration(asset_key, images, x, y)

                    # 3. Adiciona ao grupo
                    self.decorations.add(decoration)

    def _scroll_camera(self):
        """Calcula o offset da câmera baseado na posição do jogador."""
        screen_pos_x = self.player.pos[0] + self.camera_offset_x

        if screen_pos_x > SCREEN_WIDTH - CAMERA_X_LIMIT:
            scroll = screen_pos_x - (SCREEN_WIDTH - CAMERA_X_LIMIT)

            if self.camera_offset_x - scroll > SCREEN_WIDTH - self.map_width_pixels:
                self.camera_offset_x -= scroll

        elif screen_pos_x < CAMERA_X_LIMIT:
            scroll = CAMERA_X_LIMIT - screen_pos_x

            if self.camera_offset_x + scroll < 0:
                self.camera_offset_x += scroll

        self.camera_offset_x = min(0, self.camera_offset_x)
        self.camera_offset_x = max(SCREEN_WIDTH - self.map_width_pixels, self.camera_offset_x)

    def _check_collisions(self):
        """Verifica colisões entre o jogador e as entidades."""

        # Colisão com Itens
        collected_items = pg.sprite.spritecollide(self.player, self.items, True, pg.sprite.collide_rect)
        for item in collected_items:
            if item.type == 'coin':
                self.score += 10
                self.audio['coin'].play()

        # Colisão com Inimigos
        if pg.sprite.spritecollide(self.player, self.enemies, False, pg.sprite.collide_rect):
            # Lógica de dano/game over aqui
            pass

        # Colisão com Armadilhas
        if pg.sprite.spritecollide(self.player, self.traps, False, pg.sprite.collide_rect):
            # Lógica de dano aqui
            pass

    # ----------------------------------------------------------------------
    ## Atualização e Desenho
    # ----------------------------------------------------------------------

    def update(self):
        """Atualiza a lógica do jogo (físicas, animações, entidades, etc.)."""

        self._scroll_camera()

        # Posição do player no mundo (não na tela)
        player_pos = self.player.pos

        # Atualização de Entidades
        self.player.update(self.camera_offset_x)

        # CORREÇÃO/REDUÇÃO: O grupo self.enemies.update já itera sobre os sprites,
        # então não precisa do loop 'for enemy in self.enemies'. Mantenha o grupo.
        self.enemies.update(self.camera_offset_x, player_pos)

        self.items.update(self.camera_offset_x)
        self.traps.update(self.camera_offset_x)

        # NOVO: Atualiza a posição e animação das decorações
        self.decorations.update(self.camera_offset_x)

        self._check_collisions()

    # NOVO MeTODO: Combina o Player e Decorações para Ordenação
    def _get_depth_sorted_sprites(self):
        """Retorna uma lista de sprites (Player e Decorações) ordenada por coordenada Y."""

        # O player precisa ser tratado como um sprite, mas ele é uma instância solta.
        # Precisamos da coordenada Y do *ponto de contato com o chão* (bottom) para a ordenação.
        # Player.rect.bottom é a melhor âncora para a profundidade.

        # 1. Cria uma lista de todos os sprites que precisam de ordenação
        # Note que o 'self.player' é um objeto, mas ele tem 'image' e 'rect'
        sprites_to_sort = list(self.decorations.sprites())
        sprites_to_sort.append(self.player)  # Adiciona o Player

        # 2. Ordena a lista
        # Usamos o rect.bottom (a base do sprite) para determinar qual está mais perto.
        # Sprites com rect.bottom menor (mais acima na tela) devem ser desenhados PRIMEIRO (por baixo).
        # Sprites com rect.bottom maior (mais abaixo na tela) devem ser desenhados POR ÚLTIMO (por cima).

        # O argumento key=lambda s: s.rect.bottom faz a ordenação.
        sprites_to_sort.sort(key=lambda s: s.rect.bottom)

        return sprites_to_sort

    def draw(self):
        """Desenha todos os elementos na tela."""
        self._update_background_and_clouds()

        # Desenha Água Animada
        self._animate_water('big_water', [(300, 550)])
        self._animate_water('medium_water', [(250, 600), (500, 625)])
        self._animate_water('small_water', [(1000, 600), (900, 625)])
        self._draw_tiles()

        # NOVO: Desenha Decorações (antes de itens e inimigos, geralmente)
        # self.decorations.draw(self.screen)

        # Desenha Entidades
        self.items.draw(self.screen)
        self.traps.draw(self.screen)
        self.enemies.draw(self.screen)

        # ==========================================================
        # NOVO: DESENHO ORDENADO POR PROFUNDIDADE (PLAYER E DECORAÇÕES)
        # ==========================================================
        for sprite in self._get_depth_sorted_sprites():
            self.screen.blit(sprite.image, sprite.rect)

        # Desenha Placar (sempre por cima de tudo)
        score_surface = pg.font.SysFont('Arial', 30).render(f"Score: {self.score}", True, BLACK)
        self.screen.blit(score_surface, (10, 10))

        pg.display.update()

    # --- Funções Auxiliares de Desenho (Mantidas) ---

    def _update_background_and_clouds(self):
        """Atualiza a posição das nuvens e desenha o fundo."""
        # ... (código do background e nuvens inalterado) ...
        self.screen.blit(self.background_assets['background'], (0, 0))

        pos = self.cloud_pos['big_clouds_pos']
        pos -= 0.1
        if pos < -896:
            pos = 0
        self.cloud_pos['big_clouds_pos'] = pos
        self.screen.blit(self.background_assets['big_clouds'], (pos, 315))
        self.screen.blit(self.background_assets['big_clouds'], (pos + 896, 315))
        self.screen.blit(self.background_assets['big_clouds'], (pos + (896 * 2), 315))

        pos1 = self.cloud_pos['small_cloud_1_pos']
        pos1 -= 0.3
        if pos1 < -1500:
            pos1 = 0
        self.cloud_pos['small_cloud_1_pos'] = pos1
        self.screen.blit(self.background_assets['small_cloud_1'], (120 + pos1, 100))
        self.screen.blit(self.background_assets['small_cloud_1'], (120 + pos1 + 1500, 100))
        self.screen.blit(self.background_assets['small_cloud_1'], (900 + pos1, 50))
        self.screen.blit(self.background_assets['small_cloud_1'], (900 + pos1 + 1500, 50))

        pos2 = self.cloud_pos['small_cloud_2_pos']
        pos2 -= 0.2
        if pos2 < -1500:
            pos2 = 0
        self.cloud_pos['small_cloud_2_pos'] = pos2
        self.screen.blit(self.background_assets['small_cloud_2'], (250 + pos2, 200))
        self.screen.blit(self.background_assets['small_cloud_2'], (250 + pos2 + 1500, 200))
        self.screen.blit(self.background_assets['small_cloud_2'], (1000 + pos2, 150))
        self.screen.blit(self.background_assets['small_cloud_2'], (1000 + pos2 + 1500, 150))

        pos3 = self.cloud_pos['small_cloud_3_pos']
        pos3 -= 0.2
        if pos3 < -1500:
            pos3 = 0
        self.cloud_pos['small_cloud_3_pos'] = pos3
        self.screen.blit(self.background_assets['small_cloud_3'], (650 + pos3, 250))
        self.screen.blit(self.background_assets['small_cloud_3'], (650 + pos3 + 1500, 250))

    def _animate_water(self, water_type, pos_list):
        """Gerencia a animação e o desenho das reflexões da água."""
        assets = self.background_assets[water_type]
        frame = self.water_animation_frame[water_type]

        idx = frame // 12

        for pos in pos_list:
            self.screen.blit(assets[idx], pos)

        frame = (frame + 1) % 48
        self.water_animation_frame[water_type] = frame

    def _draw_tiles(self):
        """Desenha o mapa do jogo, aplicando o offset da câmera."""
        for y, row in enumerate(GAME_MAP):
            for x, tile_char in enumerate(row):
                if tile_char != ' ':
                    image = self.terrain_images.get(tile_char)
                    if image:
                        self.screen.blit(image, (x * TILE_SIZE + self.camera_offset_x, y * TILE_SIZE))

    def _handle_input(self, keys_pressed, key_event_key=None):
        """Trata as entradas do teclado para o jogo."""

        self.player.move(keys_pressed)

        if key_event_key == pg.K_SPACE:
            self.player.jump()
            self.audio['jump'].play()

        if key_event_key == pg.K_ESCAPE:
            return 'QUIT'

        return 'GAME'

    # ----------------------------------------------------------------------
    ## Loop Principal
    # ----------------------------------------------------------------------

    def run(self, keys_pressed, key_event_key=None):
        """Executa um frame do jogo. Retorna o estado do jogo (GAME ou QUIT)."""

        game_state = self._handle_input(keys_pressed, key_event_key)
        if game_state == 'QUIT':
            return 'QUIT'

        self.update()
        self.draw()

        self.clock.tick(FPS)

        return 'GAME'