import random
import pygame as pg
from code.Const import TITLE, TILE_SIZE, GAME_MAP, FPS, CAMERA_X_LIMIT, SCREEN_WIDTH, BLACK, DECORATION_MAP_CODES, WHITE
from code.Decoration import Decoration
from code.Enemy import Enemy
from code.Item import Item
from code.Player import Player
from code.Trap import Trap
from code.utils import load_background_assets, load_terrain_assets, load_entity_assets, load_audio, load_decoration_assets


class Game:
    def __init__(self, screen):
        # Configuração inicial do jogo
        self.screen = screen
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.is_playing = False
        self.is_running = True

        # Carregamento de recursos
        self.background_assets = load_background_assets()
        self.terrain_images = load_terrain_assets()
        self.entity_assets = load_entity_assets()
        self.decoration_assets = load_decoration_assets()
        self.audio = load_audio()

        # Variáveis principais de estado
        self.score = 0
        self.camera_offset_x = 0
        self.map_width_pixels = len(GAME_MAP[0]) * TILE_SIZE
        self.player_damage_dealt = False
        self.death_timer = 0
        self.respawn_delay = 180  # tempo até o respawn do jogador
        self.SCORE_TO_WIN = 100
        self.SPAWN_COOLDOWN = 180
        self.spawn_timer = 0
        self.max_enemies_on_screen = 3

        # Posições fixas de spawn de inimigos
        self.SPAWN_POINTS = [
            (1024, 384),
            (128, 512),
            (1088, 576),
            (1600, 640),
            (2240, 640),
        ]

        # Grupos de sprites
        self.player = None
        self.enemies = pg.sprite.Group()
        self.items = pg.sprite.Group()
        self.traps = pg.sprite.Group()
        self.decorations = pg.sprite.Group()

        # Música de fundo
        pg.mixer.music.load(self.audio['bg'])
        pg.mixer.music.play(-1)

        # Posições e animações de fundo
        self.cloud_pos = {'big_clouds_pos': 0, 'small_cloud_1_pos': 0, 'small_cloud_2_pos': 0, 'small_cloud_3_pos': 0}
        self.water_animation_frame = {'big_water': 0, 'medium_water': 0, 'small_water': 0}

    # Inicia novo nível e reseta estado
    def _start_new_level(self):
        self.score = 0
        self.spawn_timer = 0
        self.camera_offset_x = 0
        self.player_damage_dealt = False
        self.enemies.empty()
        self.items.empty()
        self.traps.empty()
        self.decorations.empty()
        self.player = Player(start_pos=[300, 600], game_map=GAME_MAP, map_width_pixels=self.map_width_pixels)
        self.death_timer = 0
        self._create_level_objects()
        self.is_playing = True

    # Recria o jogador após a morte
    def _player_respawn(self):
        self.player = Player(start_pos=[300, 600], game_map=GAME_MAP, map_width_pixels=self.map_width_pixels)
        self.death_timer = 0
        self.camera_offset_x = 0
        self.player_damage_dealt = False

    # Gera inimigos dinamicamente
    def _spawn_enemy(self):
        if len(self.enemies) < self.max_enemies_on_screen:
            if not self.SPAWN_POINTS:
                print("ERRO: Nenhuma posição de spawn configurada!")
                return False
            random_spawn_pos = random.choice(self.SPAWN_POINTS)
            new_enemy = Enemy(start_pos=random_spawn_pos, enemy_type='tooth', assets=self.entity_assets, game_map=GAME_MAP)
            self.enemies.add(new_enemy)
            self.spawn_timer = 0
            return True
        return False

    # Cria objetos do mapa com base no GAME_MAP
    def _create_level_objects(self):
        for y, row in enumerate(GAME_MAP):
            for x, char in enumerate(row):
                pos = (x * TILE_SIZE, y * TILE_SIZE)

                if char == '$':  # moedas
                    self.items.add(Item(pos, 'coin', self.entity_assets))
                elif char == 'V':  # inimigos fixos
                    self.enemies.add(Enemy(start_pos=pos, enemy_type='seashell', assets=self.entity_assets, game_map=GAME_MAP))

                # Decorações
                if char in DECORATION_MAP_CODES:
                    asset_key = DECORATION_MAP_CODES[char]
                    decoration = Decoration(asset_key, self.decoration_assets[asset_key], x, y)
                    self.decorations.add(decoration)

    # Controla o movimento da câmera
    def _scroll_camera(self):
        if not self.player:
            return
        screen_pos_x = self.player.pos[0] + self.camera_offset_x

        if screen_pos_x > SCREEN_WIDTH - CAMERA_X_LIMIT:
            scroll = screen_pos_x - (SCREEN_WIDTH - CAMERA_X_LIMIT)
            if self.camera_offset_x - scroll > SCREEN_WIDTH - self.map_width_pixels:
                self.camera_offset_x -= scroll

        elif screen_pos_x < CAMERA_X_LIMIT:
            scroll = CAMERA_X_LIMIT - screen_pos_x
            if self.camera_offset_x + scroll < 0:
                self.camera_offset_x += scroll

        # Limites da câmera
        self.camera_offset_x = min(0, self.camera_offset_x)
        self.camera_offset_x = max(SCREEN_WIDTH - self.map_width_pixels, self.camera_offset_x)

    # Detecção de colisões e efeitos
    def _check_collisions(self):
        if not self.player:
            return

        if not self.player.is_attacking:
            self.player_damage_dealt = False

        # Itens coletados
        collected_items = pg.sprite.spritecollide(self.player, self.items, True, pg.sprite.collide_rect)
        for item in collected_items:
            if item.type == 'coin':
                self.score += 5
                self.audio['coin'].play()

        # Colisões com inimigos
        hit_enemies = pg.sprite.spritecollide(self.player, self.enemies, False, pg.sprite.collide_rect)
        for enemy in hit_enemies:
            if enemy.is_attacking and enemy.can_deal_damage():
                self.player.receive_damage(10)
            if self.player.is_attacking and not self.player_damage_dealt:
                if enemy.receive_damage(25):
                    self.score += 10
                self.player_damage_dealt = True

    # Atualiza estado geral do jogo
    def update(self):
        if self.score >= self.SCORE_TO_WIN:
            print(f"Vitória! Score {self.score}/{self.SCORE_TO_WIN}. Fim de Jogo!")
            self.is_playing = False
            return

        if self.player and self.player.is_dead:
            self.death_timer += 1
            if self.death_timer >= self.respawn_delay:
                self._player_respawn()
            return

        self.spawn_timer += 1
        if self.spawn_timer >= self.SPAWN_COOLDOWN:
            self._spawn_enemy()

        self._scroll_camera()

        if not self.player:
            return

        player_pos = self.player.pos
        self.player.update(self.camera_offset_x, self.enemies)
        self.enemies.update(self.camera_offset_x, player_pos)
        self.items.update(self.camera_offset_x)
        self.traps.update(self.camera_offset_x)
        self.decorations.update(self.camera_offset_x)

        # Remove inimigos mortos
        for enemy in self.enemies.copy():
            if enemy.is_dead and hasattr(enemy, 'kill_flag') and enemy.kill_flag:
                enemy.kill()

        if not self.player.is_dead:
            self._check_collisions()

    # Define ordem de desenho com base na profundidade
    def _get_depth_sorted_sprites(self):
        if not self.player:
            return []
        sprites = list(self.decorations.sprites()) + list(self.enemies.sprites()) + [self.player]
        sprites.sort(key=lambda s: s.rect.bottom)
        return sprites

    # Renderização de todos os elementos visuais
    def draw(self):
        self.screen.fill(BLACK)
        self._update_background_and_clouds()
        self._animate_water('big_water', [(300, 550)])
        self._animate_water('medium_water', [(250, 600), (500, 625)])
        self._animate_water('small_water', [(1000, 600), (900, 625)])
        self._draw_tiles()

        self.items.draw(self.screen)
        self.traps.draw(self.screen)

        for sprite in self._get_depth_sorted_sprites():
            self.screen.blit(sprite.image, sprite.rect)

        if self.player:
            self.player.draw_debug(self.screen, self.camera_offset_x)

        for enemy in self.enemies:
            if not enemy.kill_flag:
                enemy.draw_debug(self.screen, self.camera_offset_x)

        # Interface: score e vida
        score_surface = pg.font.SysFont('Arial', 30).render(f"Score: {self.score}", True, BLACK)
        self.screen.blit(score_surface, (10, 10))
        if self.player:
            health_surface = pg.font.SysFont('Arial', 30).render(f"Health: {self.player.health}", True, WHITE)
            self.screen.blit(health_surface, (10, 50))

        pg.display.update()

    # Anima fundo e nuvens
    def _update_background_and_clouds(self):
        self.screen.blit(self.background_assets['background'], (0, 0))

        # Movimento contínuo das nuvens
        for key, speed, reset, y_pos in [
            ('big_clouds_pos', 0.1, 896, 315),
            ('small_cloud_1_pos', 0.3, 1500, 100),
            ('small_cloud_2_pos', 0.2, 1500, 200),
            ('small_cloud_3_pos', 0.2, 1500, 250),
        ]:
            pos = self.cloud_pos[key] - speed
            if pos < -reset:
                pos = 0
            self.cloud_pos[key] = pos
            self.screen.blit(self.background_assets[key.replace('_pos', '')], (pos, y_pos))
            self.screen.blit(self.background_assets[key.replace('_pos', '')], (pos + reset, y_pos))

    # Controla animação da água
    def _animate_water(self, water_type, pos_list):
        assets = self.background_assets[water_type]
        frame = self.water_animation_frame[water_type]
        idx = frame // 12
        for pos in pos_list:
            self.screen.blit(assets[idx], pos)
        self.water_animation_frame[water_type] = (frame + 1) % 48

    # Desenha o terreno do mapa
    def _draw_tiles(self):
        for y, row in enumerate(GAME_MAP):
            for x, tile_char in enumerate(row):
                if tile_char != ' ':
                    image = self.terrain_images.get(tile_char)
                    if image:
                        self.screen.blit(image, (x * TILE_SIZE + self.camera_offset_x, y * TILE_SIZE))

    # Controle de entrada do jogador
    def _handle_input(self, keys_pressed, key_event_key=None):
        if not self.player:
            return 'GAME'
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

    # Loop principal do jogo
    def run(self, keys_pressed, key_event_key=None):
        if not self.is_playing or self.player is None:
            self._start_new_level()

        if not self.is_playing:
            return 'MENU'

        game_state = self._handle_input(keys_pressed, key_event_key)
        if game_state == 'QUIT':
            return 'QUIT'

        self.update()
        self.draw()
        self.clock.tick(FPS)
        return 'GAME'
