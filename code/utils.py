import pygame as pg
from code.Const import TILE_SIZE, TILE_ASSET_PATHS, SCREEN_WIDTH, SCREEN_HEIGHT, AUDIO_PATHS, DECORATION_ASSET_PATHS


def load_and_scale_image(path, size, flip=False):
    """Carrega, redimensiona e opcionalmente inverte uma imagem."""
    try:
        image = pg.image.load(path).convert_alpha()
        if flip:
            image = pg.transform.flip(image, True, False)
        return pg.transform.scale(image, size)
    except pg.error as e:
        print(f"Erro ao carregar imagem: {path}. Erro: {e}")
        return pg.Surface(size, pg.SRCALPHA)


def load_player_assets():
    """Carrega e organiza as animações do jogador por estado e direção."""
    base_path = './asset/Captain Clown Nose/Captain Clown Nose/with Sword/'
    player_size = (128, 80)

    animations = {
        'idle_right': [],
        'idle_left': [],
        'run_right': [],
        'run_left': [],
        'attack_right': [],
        'attack_left': [],
        'hit_right': [],
        'hit_left': [],
        'death_right': [],
        'death_left': []
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

    # ATTACK (De 01 a 02)
    for i in range(1, 3):
        path = f'{base_path}Attack 2/Attack 2 {i:02d}.png'
        img_right = load_and_scale_image(path, player_size)
        img_left = load_and_scale_image(path, player_size, flip=True)
        animations['attack_right'].append(img_right)
        animations['attack_left'].append(img_left)

    # HIT (De 01 a 03)
    for i in range(1, 4):
        path = f'{base_path}Hit Sword/Hit Sword {i:02d}.png'
        img_right = load_and_scale_image(path, player_size)
        img_left = load_and_scale_image(path, player_size, flip=True)
        animations['hit_right'].append(img_right)
        animations['hit_left'].append(img_left)

    # DEATH (De 01 a 03)
    for i in range(1, 4):
        path = f'{base_path}Dead Ground/Dead Ground {i:02d}.png'
        img_right = load_and_scale_image(path, player_size)
        img_left = load_and_scale_image(path, player_size, flip=True)
        animations['death_right'].append(img_right)
        animations['death_left'].append(img_left)

    return animations


def load_terrain_assets():
    """Carrega os assets de tiles de terreno."""
    terrain_images = {}
    for key, path in TILE_ASSET_PATHS.items():
        terrain_images[key] = load_and_scale_image(path, (TILE_SIZE, TILE_SIZE))
    return terrain_images


def load_background_assets():
    """Carrega os assets de fundo (parallax e animações de água)."""
    assets = {'background': load_and_scale_image('./asset/Palm Tree Island/Background/BG Image.png',
                                                 (SCREEN_WIDTH, SCREEN_HEIGHT)),
              'big_clouds': load_and_scale_image('./asset/Palm Tree Island/Background/Big Clouds.png', (896, 202)),
              'small_cloud_1': load_and_scale_image('./asset/Palm Tree Island/Background/Small Cloud 1.png', (148, 48)),
              'small_cloud_2': load_and_scale_image('./asset/Palm Tree Island/Background/Small Cloud 2.png', (266, 70)),
              'small_cloud_3': load_and_scale_image('./asset/Palm Tree Island/Background/Small Cloud 3.png', (280, 78))}

    # Animações da Água (Water Reflect)
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

        for i in range(1, 5):
            path = f'{base_path}{base_name} {i:02d}.png'
            assets[w_key].append(load_and_scale_image(path, size))

    return assets


def load_entity_assets(assets=None):
    """Carrega assets de inimigos, itens e armadilhas."""
    if assets is None:
        assets = {}

    # FIERCE TOOTH
    tooth_size = (64, 64)
    tooth_base_path = './asset/enemies/Fierce Tooth/'
    assets['tooth'] = {'idle': [], 'run': [], 'hit': [], 'death': [], 'attack': []}

    for i in range(1, 8):
        assets['tooth']['idle'].append(load_and_scale_image(f'{tooth_base_path}Idle/Idle {i:02d}.png', tooth_size))
    for i in range(1, 6):
        assets['tooth']['run'].append(load_and_scale_image(f'{tooth_base_path}Run/Run {i:02d}.png', tooth_size))
    for i in range(1, 5):
        assets['tooth']['attack'].append(load_and_scale_image(f'{tooth_base_path}Attack/Attack {i:02d}.png', tooth_size))
    for i in range(1, 4):
        assets['tooth']['hit'].append(load_and_scale_image(f'{tooth_base_path}Hit/Hit {i:02d}.png', tooth_size))
    for i in range(1, 4):
        assets['tooth']['death'].append(load_and_scale_image(f'{tooth_base_path}Dead Hit/Dead Hit {i:02d}.png', tooth_size))

    # SEASHELL
    seashell_size = (76, 46)
    seashell_base_path = './asset/enemies/seashell/'
    assets['seashell'] = {'idle': [], 'attack': []}

    # Carrega animações da Seashell
    for i in range(1, 2):
        assets['seashell']['idle'].append(load_and_scale_image(f'{seashell_base_path}Idle/idle {i:02d}.png', seashell_size))
    for i in range(1, 7):
        assets['seashell']['attack'].append(
            load_and_scale_image(f'{seashell_base_path}Attack/Attack {i:02d}.png', seashell_size))

    # COIN
    coin_size = (32, 32)
    assets['coin'] = []
    coin_base_path = './asset/items/coin/Gold Coin/'
    for i in range(1, 4):
        assets['coin'].append(load_and_scale_image(f'{coin_base_path}{i}.png', coin_size))

    # SPIKE BALL
    assets['spike_ball'] = load_and_scale_image('./asset/trap/spike_ball/Spiked Ball.png', (TILE_SIZE, TILE_SIZE))

    return assets


def load_audio():
    """Carrega os arquivos de áudio e inicializa o mixer."""
    pg.mixer.init()
    audio = {}
    try:
        audio['bg'] = AUDIO_PATHS['bg']
        audio['jump'] = pg.mixer.Sound(AUDIO_PATHS['jump'])
        audio['coin'] = pg.mixer.Sound(AUDIO_PATHS['coin'])
        audio['jump'].set_volume(0.5)
        audio['coin'].set_volume(0.8)

    except pg.error as e:
        print(f"Erro ao carregar áudio. Verifique os caminhos no Const.py. Erro: {e}")
        audio['jump'] = pg.mixer.Sound(pg.sndarray.make_sound([[0]]))
        audio['coin'] = pg.mixer.Sound(pg.sndarray.make_sound([[0]]))

    return audio


def load_decoration_assets():
    """Carrega os assets de objetos de decoração."""
    decoration_images = {}
    for key, path in DECORATION_ASSET_PATHS.items():
        try:
            image = pg.image.load(path).convert_alpha()
            decoration_images[key] = image
        except pg.error as e:
            print(f"Erro ao carregar asset de decoração: {path}. Erro: {e}")
            decoration_images[key] = pg.Surface((64, 64), pg.SRCALPHA)

    # Adiciona a animação do HELM
    helm_size = (64, 64)
    helm_base_path = './asset//Palm Tree Island/objects/Ship Helm/'
    decoration_images['helm'] = []

    for i in range(1, 6):
        path = f'{helm_base_path}{i}.png'
        decoration_images['helm'].append(load_and_scale_image(path, helm_size))

    return decoration_images