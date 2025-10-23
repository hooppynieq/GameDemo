# game.py

import pygame as pg

from code.Const import TITLE, GAME_MAP, TILE_SIZE, FPS
from code.Player import Player
from code.utils import load_background_assets, load_terrain_assets


class Game:
    def __init__(self, screen):
        self.screen = screen
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.is_running = True

        # Carregamento de Assets
        self.background_assets = load_background_assets()
        self.terrain_images = load_terrain_assets()

        # Componentes do Jogo
        self.player = Player(start_pos=[300, 600], game_map=GAME_MAP)

        # Variáveis de Animação do Fundo
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

    def _update_background_and_clouds(self):
        """Atualiza a posição das nuvens e desenha o fundo."""

        # Background
        self.screen.blit(self.background_assets['background'], (0, 0))

        # Big Clouds (velocidade 0.05, repete a cada 896)
        pos = self.cloud_pos['big_clouds_pos']
        pos -= 0.05
        if pos < -896:
            pos = 0
        self.cloud_pos['big_clouds_pos'] = pos
        self.screen.blit(self.background_assets['big_clouds'], (pos, 315))
        self.screen.blit(self.background_assets['big_clouds'], (pos + 896, 315))
        self.screen.blit(self.background_assets['big_clouds'], (pos + (896 * 2), 315))

        # Small Clouds (velocidade 0.3 e 0.2, repete a cada 1500)
        # Cloud 1
        pos1 = self.cloud_pos['small_cloud_1_pos']
        pos1 -= 0.3
        if pos1 < -1500:
            pos1 = 0
        self.cloud_pos['small_cloud_1_pos'] = pos1
        self.screen.blit(self.background_assets['small_cloud_1'], (120 + pos1, 100))
        self.screen.blit(self.background_assets['small_cloud_1'], (120 + pos1 + 1500, 100))
        self.screen.blit(self.background_assets['small_cloud_1'], (900 + pos1, 50))
        self.screen.blit(self.background_assets['small_cloud_1'], (900 + pos1 + 1500, 50))

        # Cloud 2 & 3 (usam a mesma velocidade de 0.2 no original)
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

        # Calcula qual imagem usar (4 imagens, 48 frames totais, 12 frames por imagem)
        idx = frame // 12

        # Desenha em todas as posições
        for pos in pos_list:
            self.screen.blit(assets[idx], pos)

        # Atualiza a frame (Ciclo de 0 a 47)
        frame = (frame + 1) % 48
        self.water_animation_frame[water_type] = frame

    def _draw_tiles(self):
        """Desenha o mapa do jogo na tela."""
        for y, row in enumerate(GAME_MAP):
            for x, tile_char in enumerate(row):
                if tile_char != ' ':
                    # Otimização: Usa o dicionário de imagens carregadas
                    image = self.terrain_images.get(tile_char)
                    if image:
                        self.screen.blit(image, (x * TILE_SIZE, y * TILE_SIZE))

    def _handle_input(self, keys_pressed, key_event_key=None):
        """Trata as entradas do teclado e mouse para o jogo (em vez do menu)."""

        # Movimento Horizontal
        self.player.move(keys_pressed)

        # Pulo
        if key_event_key == pg.K_SPACE:
            self.player.jump()

        # Sair
        if key_event_key == pg.K_ESCAPE:
            self.is_running = False
            return 'QUIT'

        return 'GAME'

    def update(self):
        """Atualiza a lógica do jogo (físicas, animações, etc.)."""
        self.player.update()

    def draw(self):
        """Desenha todos os elementos na tela."""
        self._update_background_and_clouds()

        # Desenha os tiles (terreno)
        self._draw_tiles()

        # Animação da Água
        self._animate_water('big_water', [(300, 550)])
        self._animate_water('medium_water', [(250, 600), (500, 625)])
        self._animate_water('small_water', [(1000, 600), (900, 625)])

        # Desenha o jogador
        self.screen.blit(self.player.image, self.player.rect)

        pg.display.update()

    def run(self, keys_pressed, key_event_key=None):
        """Executa um frame do jogo. Retorna o estado do jogo (GAME ou QUIT)."""

        # Entrada
        game_state = self._handle_input(keys_pressed, key_event_key)
        if game_state == 'QUIT':
            return 'QUIT'

        # Lógica
        self.update()

        # Desenho
        self.draw()

        # Controla o FPS
        self.clock.tick(FPS)

        return 'GAME'