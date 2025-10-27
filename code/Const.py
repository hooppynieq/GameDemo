# Dimensões da Tela
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 768
SCREEN_SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT)
TITLE = 'Captain Clown Nose DEMO'
FPS = 60

# Cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE_DARK = (181, 181, 255)
PURPLE_LIGHT = (230, 230, 255)
GREEN = (0, 255, 0)
GREEN_LIGHT = (180, 255, 180)
BLUE = (0, 0, 255)

# Configurações do Jogo
TILE_SIZE = 64  # Tamanho de cada tile no mapa
GRAVITY = 1
FONT_NAME = "Courier New"
FONT_SIZE = 50

# Configurações do Jogador
PLAYER_JUMP_FORCE = -22
PLAYER_COLLIDER_SIZE = (46, 54)
PLAYER_SPEED = 5
PLAYER_ANIMATION_SPEED = 7

# Configurações de Câmera
CAMERA_X_LIMIT = 400

# Configurações de Inimigo
ENEMY_SPEED = 2
ENEMY_ANIMATION_SPEED = 10
ENEMY_COLLIDER_SIZE = (30, 30)

# Configurações de Item e Decoração
GENERIC_ANIMATION_SPEED = 10

# Raio de AGGREGAÇÃO
AGGRO_RANGE = 300

# Tipos de Entidades
ENEMY_TYPES = ['tooth', 'seashell']

# Mapeamento do Mundo
GAME_MAP = [
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'K', ' ', ' ', 'P', 'G', 'H', 'J', 'F', ' ', ' ', ' ', 'T', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    ['S', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '$', '1', '3', '$', '1', '2', '2', '2', '3', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    ['3', 'B', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '1', '2', '3', '$', '4', '5', '5', '5', '6', 'B', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    ['5', '3', '$', '$', '$', ' ', ' ', '$', '$', ' ', '7', '8', '9', '$', '4', '5', '5', '5', '5', '3', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    ['5', '6', 'P', '$', 'O', 'O', 'K', 'P', ' ', ' ', '$', '$', '$', 'N', '4', '5', '5', '5', '5', '6', 'V', ' ', 'P', 'P', 'K', 'O', 'K', 'K', 'G', 'G', 'J', 'J', 'P', 'P', 'K', 'O', 'P', ' ', 'O', 'P'],
    ['2', '2', '2', '2', '2', '2', '2', '2', '2', '2', '2', '2', '2', '2', '5', '5', '5', '5', '5', '5', '2', '2', '2', '2', '2', '2', '2', '2', '2', '2', '2', '2', '2', '2', '2', '2', '2', '2', '2', '2'],
]

# Mapeamento dos Tiles
TILE_ASSET_PATHS = {
    '1': './asset/Palm Tree Island/Terrain/ground_1.png',
    '2': './asset/Palm Tree Island/Terrain/ground_2.png',
    '3': './asset/Palm Tree Island/Terrain/ground_3.png',
    '4': './asset/Palm Tree Island/Terrain/ground_4.png',
    '5': './asset/Palm Tree Island/Terrain/ground_5.png',
    '6': './asset/Palm Tree Island/Terrain/ground_6.png',
    '7': './asset/Palm Tree Island/Terrain/ground_7.png',
    '8': './asset/Palm Tree Island/Terrain/ground_8.png',
    '9': './asset/Palm Tree Island/Terrain/ground_9.png',
}

# Caminhos dos Assets de Decoração
DECORATION_ASSET_PATHS = {
    'palm_tree_1': './asset/Palm Tree Island/objects/bg_palm_1.png',
    'palm_tree_2': './asset/Palm Tree Island/objects/bg_palm_left.png',
    'palm_tree_3': './asset/Palm Tree Island/objects/bg_palm_right.png',
    'palm_large': './asset/Palm Tree Island/objects/large_1.png',
    'palm_small': './asset/Palm Tree Island/objects/small_1.png',
    'floor_spikes': './asset/Palm Tree Island/objects/floor_spikes.png',
    'barrel_1': './asset/Palm Tree Island/objects/barrel.png',
    'barrel_2': './asset/Palm Tree Island/objects/bg_barrel.png',
    'barrel_3': './asset/Palm Tree Island/objects/bg_barrel_2.png',
    'flag': './asset/Palm Tree Island/objects/flag.png',
    'helm': './asset/Palm Tree Island/objects/Ship Helm/1.png',
    'shell': './asset/Palm Tree Island/objects/shell.png',
    'shell_left': './asset/Palm Tree Island/objects/shell_left.png',
    'spiked': './asset/trap/spike_ball/Spiked Ball.png'
}
# Mapeamento decorações
DECORATION_MAP_CODES = {
    'P': 'palm_tree_1',
    'U': 'palm_tree_2',
    'B': 'palm_tree_3',
    'O': 'palm_large',
    'K': 'palm_small',
    'F': 'flag',
    'H': 'helm',
    'G': 'barrel_1',
    'J': 'barrel_3',
    'S': 'floor_spikes',
    'M': 'shell',
    'N': 'shell_left',
    'T': 'spiked'
}

# Mapeamento Itens
ITEM_MAP_CODES = {
    '$': 'coin',

}
# Mapeamento de Inimigos
ENTITY_ASSET_PATHS = {
    # Inimigos
    'E': 'Fierce Tooth',
    'V': 'Seashell',
}

# Configurações de Áudio
AUDIO_PATHS = {
    'bg': './asset/audio/bg.mp3',
    'jump': './asset/audio/jump.wav',
    'coin': './asset/audio/coin.wav',
}