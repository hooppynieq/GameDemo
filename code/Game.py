# game.py
import pygame as pg

from code.Const import TITLE, TILE_SIZE, GAME_MAP, FPS, CAMERA_X_LIMIT, SCREEN_WIDTH, BLACK, DECORATION_MAP_CODES, WHITE

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

        self.is_playing = False
        self.is_running = True

        # Assets
        self.background_assets = load_background_assets()
        self.terrain_images = load_terrain_assets()
        self.entity_assets = load_entity_assets()
        self.decoration_assets = load_decoration_assets()
        self.audio = load_audio()

        # Variáveis do Mundo e Câmera
        self.score = 0
        self.camera_offset_x = 0
        self.map_width_pixels = len(GAME_MAP[0]) * TILE_SIZE

        # Variável de controle para garantir que o Player só cause dano uma vez por ataque
        self.player_damage_dealt = False
        self.death_timer = 0  # NOVO: Timer para o respawn
        self.respawn_delay = 180  # 3 segundos (180 frames a 60 FPS)

        # Inicialização VAZIA dos Componentes do Jogo
        self.player = None
        self.enemies = pg.sprite.Group()
        self.items = pg.sprite.Group()
        self.traps = pg.sprite.Group()
        self.decorations = pg.sprite.Group()

        # Configuração de Áudio
        pg.mixer.music.load(self.audio['bg'])
        pg.mixer.music.play(-1)

        # Variáveis de Animação do Fundo (Mantidas)
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

    def setup_level(self):
        """Inicializa o player e todos os objetos do nível. Chamado na transição de MENU para GAME e no Respawn."""

        # Reseta o score e a câmera (Opcional: Depende se você quer manter o score no respawn)
        # self.score = 0
        self.camera_offset_x = 0
        self.player_damage_dealt = False

        # Limpa os grupos antigos
        self.enemies.empty()
        self.items.empty()
        self.traps.empty()
        self.decorations.empty()

        # 1. Cria o Player
        self.player = Player(start_pos=[300, 600], game_map=GAME_MAP, map_width_pixels=self.map_width_pixels)
        self.death_timer = 0  # Reseta o timer de morte

        # 2. Cria os objetos do nível (Recria todos, incluindo inimigos)
        self._create_level_objects()

        # 3. Define o estado como ativo
        self.is_playing = True

    # ----------------------------------------------------------------------
    ## Criação de Nível e Câmera (Mantidas)
    # ----------------------------------------------------------------------

    def _create_level_objects(self):
        """Cria Inimigos, Itens, Armadilhas e Decorações com base no GAME_MAP."""
        for y, row in enumerate(GAME_MAP):
            for x, char in enumerate(row):
                pos = (x * TILE_SIZE, y * TILE_SIZE)

                if char == 'E':
                    self.enemies.add(Enemy(pos, 'tooth', self.entity_assets, GAME_MAP))
                elif char == '$':
                    self.items.add(Item(pos, 'coin', self.entity_assets))
                elif char == 'T':
                    self.traps.add(Trap(pos, 'spike_ball', self.entity_assets))

                if char in DECORATION_MAP_CODES:
                    asset_key = DECORATION_MAP_CODES[char]
                    images = self.decoration_assets[asset_key]
                    decoration = Decoration(asset_key, images, x, y)
                    self.decorations.add(decoration)

    def _scroll_camera(self):
        """Calcula o offset da câmera baseado na posição do jogador."""
        if not self.player: return

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

    # ----------------------------------------------------------------------
    ## Colisões (Mantidas)
    # ----------------------------------------------------------------------

    def _check_collisions(self):
        """Verifica colisões entre o jogador e as entidades."""
        if not self.player: return

        # Checa se o ataque do player terminou para resetar o controle de dano
        if not self.player.is_attacking:
            self.player_damage_dealt = False

        # Colisão com Itens
        collected_items = pg.sprite.spritecollide(self.player, self.items, True, pg.sprite.collide_rect)
        for item in collected_items:
            if item.type == 'coin':
                self.score += 10
                self.audio['coin'].play()

        # Colisão e Lógica de Dano com Inimigos
        hit_enemies = pg.sprite.spritecollide(self.player, self.enemies, False, pg.sprite.collide_rect)
        for enemy in hit_enemies:
            # 1. Dano do Inimigo ao Player
            if enemy.is_attacking and enemy.can_deal_damage():
                self.player.receive_damage(10)

                # 2. Dano do Player ao Inimigo
            if self.player.is_attacking and not self.player_damage_dealt:
                enemy.receive_damage(25)
                self.player_damage_dealt = True

                # Colisão com Armadilhas
        # (Adicione aqui a lógica de dano por armadilha se necessário)

    # ----------------------------------------------------------------------
    ## Atualização e Desenho
    # ----------------------------------------------------------------------

    def update(self):
        """Atualiza a lógica do jogo (físicas, animações, entidades, etc.)."""

        # NOVO: LÓGICA DE MORTE E RESPAWN
        if self.player and self.player.is_dead:
            self.death_timer += 1
            if self.death_timer >= self.respawn_delay:
                self.setup_level()  # Respawn / Recarrega o nível
                return  # Pula o resto da atualização neste frame
        # FIM: LÓGICA DE MORTE E RESPAWN

        self._scroll_camera()

        if not self.player: return

        player_pos = self.player.pos

        # Atualização de Entidades
        self.player.update(self.camera_offset_x)
        self.enemies.update(self.camera_offset_x, player_pos)
        self.items.update(self.camera_offset_x)
        self.traps.update(self.camera_offset_x)
        self.decorations.update(self.camera_offset_x)

        # CORREÇÃO: Remoção de Inimigos Mortos (Usando .copy() para iteração segura)
        for enemy in self.enemies.copy():
            # Se o inimigo sinalizou que terminou sua animação de morte
            if enemy.kill_flag:
                enemy.kill()  # <--- ISSO VAI REMOVER O SPRITE DO GRUPO (self.enemies)

        # Colisões são verificadas APENAS se o player estiver vivo
        if not self.player.is_dead:
            self._check_collisions()

    def _get_depth_sorted_sprites(self):
        """Retorna uma lista de sprites (Player, Inimigos e Decorações) ordenada por coordenada Y."""
        if not self.player: return []

        sprites_to_sort = list(self.decorations.sprites())
        sprites_to_sort.extend(self.enemies.sprites())
        sprites_to_sort.append(self.player)
        sprites_to_sort.sort(key=lambda s: s.rect.bottom)
        return sprites_to_sort

    def draw(self):
        """Desenha todos os elementos na tela."""

        self.screen.fill(BLACK)
        self._update_background_and_clouds()

        # Desenha Água Animada e Tiles
        self._animate_water('big_water', [(300, 550)])
        self._animate_water('medium_water', [(250, 600), (500, 625)])
        self._animate_water('small_water', [(1000, 600), (900, 625)])
        self._draw_tiles()

        # Desenha Entidades (Itens e Armadilhas)
        self.items.draw(self.screen)
        self.traps.draw(self.screen)

        # Desenho Ordenado (Player, Inimigos e Decorações)
        for sprite in self._get_depth_sorted_sprites():
            self.screen.blit(sprite.image, sprite.rect)

        # Desenha Placar e VIDA
        score_surface = pg.font.SysFont('Arial', 30).render(f"Score: {self.score}", True, BLACK)
        self.screen.blit(score_surface, (10, 10))

        if self.player:
            health_text = f"Health: {self.player.health}"
            # Usa a cor WHITE para ser visível sobre o fundo
            health_surface = pg.font.SysFont('Arial', 30).render(health_text, True, WHITE)
            self.screen.blit(health_surface, (10, 50))

        pg.display.update()

    # --- Funções Auxiliares de Desenho (Inalteradas) ---
    def _update_background_and_clouds(self):
        """Atualiza a posição das nuvens e desenha o fundo."""
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
        """Trata as entradas do teclado para o jogo ATIVO."""

        if not self.player: return 'GAME'

        # NOVO: Não permite input de movimento se o player estiver morto
        if self.player.is_dead:
            if key_event_key == pg.K_ESCAPE:
                return 'QUIT'
            return 'GAME'

        self.player.move(keys_pressed)

        if key_event_key == pg.K_SPACE:
            self.player.jump()
            self.audio['jump'].play()

        if key_event_key == pg.K_z:
            self.player.attack()

        if key_event_key == pg.K_ESCAPE:
            return 'QUIT'

        return 'GAME'

    # ----------------------------------------------------------------------
    ## Loop Principal
    # ----------------------------------------------------------------------

    def run(self, keys_pressed, key_event_key=None):
        """Executa um frame do jogo. Retorna o estado do jogo (GAME ou QUIT)."""

        if not self.is_playing:
            self.setup_level()

        game_state = self._handle_input(keys_pressed, key_event_key)
        if game_state == 'QUIT':
            return 'QUIT'

        self.update()
        self.draw()

        self.clock.tick(FPS)

        return 'GAME'