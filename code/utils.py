# utils.py

import pygame as pg
from code.Const import TILE_SIZE, TILE_ASSET_PATHS, SCREEN_WIDTH, SCREEN_HEIGHT, AUDIO_PATHS


def load_and_scale_image(path, size, flip=False):
    """Carrega uma imagem, inverte (se necessário) e redimensiona."""
    try:
        image = pg.image.load(path).convert_alpha()
        if flip:
            image = pg.transform.flip(image, True, False)
        return pg.transform.scale(image, size)
    except pg.error as e:
        print(f"Erro ao carregar imagem: {path}. Erro: {e}")
        # Retorna uma superfície vazia para evitar quebra total
        return pg.Surface(size, pg.SRCALPHA)


def load_player_assets():
    """Carrega e organiza todos os assets do jogador (idle e run, direita e esquerda)."""
    base_path = './asset/Captain Clown Nose/Captain Clown Nose/without Sword/'
    player_size = (128, 80)

    animations = {
        'idle_right': [],
        'idle_left': [],
        'run_right': [],
        'run_left': []
    }

    # IDLE
    for i in range(1, 6):  # Idle 01 a Idle 05
        path = f'{base_path}Idle/Idle {i:02d}.png'
        img_right = load_and_scale_image(path, player_size)
        img_left = load_and_scale_image(path, player_size, flip=True)
        animations['idle_right'].append(img_right)
        animations['idle_left'].append(img_left)

    # RUN
    for i in range(1, 7):  # Run 01 a Run 06
        path = f'{base_path}Run/Run {i:02d}.png'
        img_right = load_and_scale_image(path, player_size)
        img_left = load_and_scale_image(path, player_size, flip=True)
        animations['run_right'].append(img_right)
        animations['run_left'].append(img_left)

    return animations


def load_terrain_assets():
    """Carrega os assets do terreno."""
    terrain_images = {}
    for key, path in TILE_ASSET_PATHS.items():
        terrain_images[key] = load_and_scale_image(path, (TILE_SIZE, TILE_SIZE))
    return terrain_images


def load_background_assets():
    """Carrega os assets de fundo (BG, nuvens, água)."""
    assets = {'background': load_and_scale_image('./asset/Palm Tree Island/Background/BG Image.png',(SCREEN_WIDTH, SCREEN_HEIGHT)),
              'big_clouds': load_and_scale_image('./asset/Palm Tree Island/Background/Big Clouds.png', (896, 202)),
              'small_cloud_1': load_and_scale_image('./asset/Palm Tree Island/Background/Small Cloud 1.png', (148, 48)),
              'small_cloud_2': load_and_scale_image('./asset/Palm Tree Island/Background/Small Cloud 2.png', (266, 70)),
              'small_cloud_3': load_and_scale_image('./asset/Palm Tree Island/Background/Small Cloud 3.png', (280, 78))}

    # Background e Nuvens

    # Animações da Água
    # utils.py

    # ... (código anterior da função load_background_assets)

    # Animações da Água - Corrigido o mapeamento dos nomes de arquivo
    water_map = {
        'big_water': 'Water Reflect Big',
        'medium_water': 'Water Reflect Medium',
        'small_water': 'Water Reflect Small'
    }

    water_sizes = {
        'big_water': (340, 20),
        'medium_water': (106, 6),
        'small_water': (70, 6)
    }

    for w_key, base_name in water_map.items():
        assets[w_key] = []
        size = water_sizes[w_key]
        base_path = './asset/Palm Tree Island/Background/'

        for i in range(1, 5):  # De 01 a 04
            # O nome do arquivo é AGORA construído corretamente:
            # Ex: './asset/Palm Tree Island/Background/Water Reflect Big 01.png'
            path = f'{base_path}{base_name} {i:02d}.png'
            assets[w_key].append(load_and_scale_image(path, size))

    return assets


def load_entity_assets(assets=None):
    if assets is None:
        assets = {}
    """Carrega assets de inimigos, itens e armadilhas."""
    tooth_size = (64, 64)
    assets['tooth'] = []
    tooth_base_path = './asset/enemies/Fierce Tooth/idle/'
    for i in range(1, 6):  # Tooth 1 a 6
        assets['tooth'].append(load_and_scale_image(f'{tooth_base_path}{i}.png', tooth_size))

    # Exemplo: Moeda
    coin_size = (32, 32)
    assets['coin'] = []
    coin_base_path = './asset/items/coin/Gold Coin/'
    for i in range(1, 4):  # Coin 1 a 4
        assets['coin'].append(load_and_scale_image(f'{coin_base_path}{i}.png', coin_size))

    # Exemplo: Espeto (Trap)
    assets['spike_ball'] = load_and_scale_image('./asset/trap/spike_ball/Spiked Ball.png', (TILE_SIZE, TILE_SIZE))

    return assets


def load_audio():
    """Carrega os arquivos de áudio."""
    pg.mixer.init()
    audio = {}
    try:
        audio['bg'] = AUDIO_PATHS['bg']
        audio['jump'] = pg.mixer.Sound(AUDIO_PATHS['jump'])
        audio['coin'] = pg.mixer.Sound(AUDIO_PATHS['coin'])

        # Define o volume para SFX (opcional)
        audio['jump'].set_volume(0.5)
        audio['coin'].set_volume(0.8)

    except pg.error as e:
        print(f"Erro ao carregar áudio. Verifique os caminhos no Const.py. Erro: {e}")
        # Cria objetos Sound vazios para evitar quebra
        audio['jump'] = pg.mixer.Sound(pg.sndarray.make_sound([[0]]))
        audio['coin'] = pg.mixer.Sound(pg.sndarray.make_sound([[0]]))

    return audio