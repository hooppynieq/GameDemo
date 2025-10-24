# game.py

import pygame as pg

from code.Const import SCREEN_SIZE, TITLE, TILE_SIZE, GAME_MAP, FPS, CAMERA_X_LIMIT, SCREEN_WIDTH, BLACK
from code.Enemy import Enemy
from code.Item import Item
from code.Player import Player
from code.Trap import Trap
from code.utils import load_background_assets, load_terrain_assets, load_entity_assets, load_audio


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

        # --- Configuração de Áudio ---
        pg.mixer.music.load(self.audio['bg'])
        pg.mixer.music.play(-1)

        # --- Variáveis do Mundo e Câmera ---
        self.score = 0
        self.camera_offset_x = 0
        self.map_width_pixels = len(GAME_MAP[0]) * TILE_SIZE

        # --- Componentes do Jogo ---
        self.player = Player(start_pos=[300, 600], game_map=GAME_MAP, map_width_pixels=self.map_width_pixels)
        self.enemies = pg.sprite.Group()
        self.items = pg.sprite.Group()
        self.traps = pg.sprite.Group()

        self._initialize_entities()

        # ... (Variáveis de Animação do Fundo) ...
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

    def _initialize_entities(self):
        """Cria Inimigos, Itens e Armadilhas com base no GAME_MAP."""
        for y, row in enumerate(GAME_MAP):
            for x, char in enumerate(row):
                pos = (x * TILE_SIZE, y * TILE_SIZE)

                if char == 'E':
                    # Usa 'tooth', a chave do asset animado
                    self.enemies.add(Enemy(pos, 'tooth', self.entity_assets, GAME_MAP))
                elif char == 'I':
                    # Usa 'coin', a chave do asset animado
                    self.items.add(Item(pos, 'coin', self.entity_assets))
                elif char == 'T':
                    # Usa 'spike_ball', a chave do asset estático
                    self.traps.add(Trap(pos, 'spike_ball', self.entity_assets))

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

    def _update_background_and_clouds(self):
        """Atualiza a posição das nuvens e desenha o fundo."""
        # ... (código do background e nuvens inalterado) ...
        self.screen.blit(self.background_assets['background'], (0, 0))

        pos = self.cloud_pos['big_clouds_pos']
        pos -= 0.05
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

    def update(self):
        """Atualiza a lógica do jogo (físicas, animações, entidades, etc.)."""

        self._scroll_camera()

        # Atualização de Entidades (todas recebem o offset para desenho)
        self.player.update(self.camera_offset_x)
        self.enemies.update(self.camera_offset_x)
        self.items.update(self.camera_offset_x)
        self.traps.update(self.camera_offset_x)

        self._check_collisions()

    def draw(self):
        """Desenha todos os elementos na tela."""
        self._update_background_and_clouds()
        self._draw_tiles()

        self._animate_water('big_water', [(300, 550)])
        self._animate_water('medium_water', [(250, 600), (500, 625)])
        self._animate_water('small_water', [(1000, 600), (900, 625)])

        # Desenha Entidades (já estão com offset)
        self.enemies.draw(self.screen)
        self.items.draw(self.screen)
        self.traps.draw(self.screen)
        self.screen.blit(self.player.image, self.player.rect)

        # Desenha Placar
        score_surface = pg.font.SysFont('Arial', 30).render(f"Score: {self.score}", True, BLACK)
        self.screen.blit(score_surface, (10, 10))

        pg.display.update()

    def run(self, keys_pressed, key_event_key=None):
        """Executa um frame do jogo. Retorna o estado do jogo (GAME ou QUIT)."""

        game_state = self._handle_input(keys_pressed, key_event_key)
        if game_state == 'QUIT':
            return 'QUIT'

        self.update()
        self.draw()

        self.clock.tick(FPS)

        return 'GAME'