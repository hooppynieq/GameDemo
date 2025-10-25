# utils.py

import pygame as pg
from code.Const import TILE_SIZE, TILE_ASSET_PATHS, SCREEN_WIDTH, SCREEN_HEIGHT, AUDIO_PATHS, DECORATION_ASSET_PATHS


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
    """Carrega e organiza todos os assets do jogador (idle, run, attack, hit, death)."""
    base_path = './asset/Captain Clown Nose/Captain Clown Nose/with Sword/'
    player_size = (128, 80)

    animations = {
        'idle_right': [],
        'idle_left': [],
        'run_right': [],
        'run_left': [],
        'attack_right': [],  # NOVO: Ataque
        'attack_left': [],  # NOVO: Ataque
        'hit_right': [],  # NOVO: Recebendo Dano
        'hit_left': [],  # NOVO: Recebendo Dano
        'death_right': [],  # NOVO: Morte
        'death_left': []  # NOVO: Morte
    }

    # IDLE (De 01 a 04)
    for i in range(1, 5):
        path = f'{base_path}Idle/Idle {i:02d}.png'
        img_right = load_and_scale_image(path, player_size)
        img_left = load_and_scale_image(path, player_size, flip=True)
        animations['idle_right'].append(img_right)
        animations['idle_left'].append(img_left)

    # RUN (De 01 a 05)
    for i in range(1, 6):
        path = f'{base_path}Run/Run {i:02d}.png'
        img_right = load_and_scale_image(path, player_size)
        img_left = load_and_scale_image(path, player_size, flip=True)
        animations['run_right'].append(img_right)
        animations['run_left'].append(img_left)

    # NOVO: ATTACK (Ajuste o range conforme o número de frames do seu asset)
    for i in range(1, 3):  # Exemplo: 4 frames
        path = f'{base_path}Attack 2/Attack 2 {i:02d}.png'
        img_right = load_and_scale_image(path, player_size)
        img_left = load_and_scale_image(path, player_size, flip=True)
        animations['attack_right'].append(img_right)
        animations['attack_left'].append(img_left)

    # NOVO: HIT (Recebendo Dano)
    for i in range(1, 4):  # Exemplo: 2 frames
        path = f'{base_path}Hit Sword/Hit Sword {i:02d}.png'
        img_right = load_and_scale_image(path, player_size)
        img_left = load_and_scale_image(path, player_size, flip=True)
        animations['hit_right'].append(img_right)
        animations['hit_left'].append(img_left)

    # NOVO: DEATH (Morte)
    for i in range(1, 4):  # Exemplo: 5 frames
        path = f'{base_path}Dead Ground/Dead Ground {i:02d}.png'
        img_right = load_and_scale_image(path, player_size)
        img_left = load_and_scale_image(path, player_size, flip=True)
        animations['death_right'].append(img_right)
        animations['death_left'].append(img_left)

    return animations


def load_terrain_assets():
    """Carrega os assets do terreno."""
    terrain_images = {}
    for key, path in TILE_ASSET_PATHS.items():
        terrain_images[key] = load_and_scale_image(path, (TILE_SIZE, TILE_SIZE))
    return terrain_images


def load_background_assets():
    """Carrega os assets de fundo (BG, nuvens, água)."""
    assets = {'background': load_and_scale_image('./asset/Palm Tree Island/Background/BG Image.png',
                                                 (SCREEN_WIDTH, SCREEN_HEIGHT)),
              'big_clouds': load_and_scale_image('./asset/Palm Tree Island/Background/Big Clouds.png', (896, 202)),
              'small_cloud_1': load_and_scale_image('./asset/Palm Tree Island/Background/Small Cloud 1.png', (148, 48)),
              'small_cloud_2': load_and_scale_image('./asset/Palm Tree Island/Background/Small Cloud 2.png', (266, 70)),
              'small_cloud_3': load_and_scale_image('./asset/Palm Tree Island/Background/Small Cloud 3.png', (280, 78))}

    # Animações da Água
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
            path = f'{base_path}{base_name} {i:02d}.png'
            assets[w_key].append(load_and_scale_image(path, size))

    return assets


def load_entity_assets(assets=None):
    if assets is None:
        assets = {}
    """Carrega assets de inimigos, itens e armadilhas."""

    tooth_size = (64, 64)
    tooth_base_path = './asset/enemies/Fierce Tooth/'

    # 1. ATUALIZADO: ESTRUTURA PARA SUPORTAR TODOS OS ESTADOS DE COMBATE DO INIMIGO
    assets['tooth'] = {'idle': [], 'run': [], 'hit': [], 'death': [], 'attack': []}

    # Carrega IDLE
    for i in range(1, 8):  # Assumindo frames 1 a 8 para Idle
        assets['tooth']['idle'].append(load_and_scale_image(f'{tooth_base_path}Idle/Idle {i:02d}.png', tooth_size))
    # path = f'{base_path}Idle/Idle {i:02d}.png'
    # Carrega RUN (perseguição)
    for i in range(1, 6):  # Assumindo frames 1 a 5 para Run (ou o que estiver disponível)
        assets['tooth']['run'].append(load_and_scale_image(f'{tooth_base_path}Run/Run {i:02d}.png', tooth_size))

        # NOVO: Attack
    for i in range(1, 5):  # Exemplo: 5 frames
        assets['tooth']['attack'].append(load_and_scale_image(f'{tooth_base_path}Attack/Attack {i:02d}.png', tooth_size))

        # NOVO: HIT (Recebendo Dano)
    for i in range(1, 4):  # Exemplo: 2 frames
        assets['tooth']['hit'].append(load_and_scale_image(f'{tooth_base_path}Hit/Hit {i:02d}.png', tooth_size))

        # NOVO: DEATH (Morte)
    for i in range(1, 4):  # Exemplo: 5 frames
        assets['tooth']['death'].append(load_and_scale_image(f'{tooth_base_path}Dead Hit/Dead Hit {i:02d}.png', tooth_size))

    # 2. Exemplo: Moeda
    coin_size = (32, 32)
    assets['coin'] = []
    coin_base_path = './asset/items/coin/Gold Coin/'
    for i in range(1, 5):
        assets['coin'].append(load_and_scale_image(f'{coin_base_path}{i}.png', coin_size))

    # 3. Exemplo: Espeto (Trap)
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
        # NOVO: Adicione sons de ataque, hit e morte aqui se tiver!

        # Define o volume para SFX (opcional)
        audio['jump'].set_volume(0.5)
        audio['coin'].set_volume(0.8)

    except pg.error as e:
        print(f"Erro ao carregar áudio. Verifique os caminhos no Const.py. Erro: {e}")
        # Cria objetos Sound vazios para evitar quebra
        audio['jump'] = pg.mixer.Sound(pg.sndarray.make_sound([[0]]))
        audio['coin'] = pg.mixer.Sound(pg.sndarray.make_sound([[0]]))

    return audio


def load_decoration_assets():
    """Carrega os assets de objetos de decoração (árvores, arbustos, pedras)."""
    decoration_images = {}
    for key, path in DECORATION_ASSET_PATHS.items():
        try:
            image = pg.image.load(path).convert_alpha()
            decoration_images[key] = image
        except pg.error as e:
            print(f"Erro ao carregar asset de decoração: {path}. Erro: {e}")
            decoration_images[key] = pg.Surface((64, 64), pg.SRCALPHA)

    # 2. NOVO: Adiciona a animação do HELM no dicionário de decorações
    helm_size = (64, 64)
    helm_base_path = './asset//Palm Tree Island/objects/Ship Helm/'
    decoration_images['helm'] = []  # Use a chave 'helm' para a lista de frames

    for i in range(1, 6):  # Carrega helm 1 a 5
        path = f'{helm_base_path}{i}.png'
        decoration_images['helm'].append(load_and_scale_image(path, helm_size))

    return decoration_images