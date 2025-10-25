# Const.py

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
PLAYER_COLLIDER_SIZE = (46, 54) # [largura, altura] do collider
PLAYER_SPEED = 5 # Velocidade de movimento horizontal
PLAYER_ANIMATION_SPEED = 7 # Número de frames por imagem da animação (ex: 7 frames por imagem = 60/7 ≈ 8.5 FPS)

# --- Configurações de Câmera/Scroll ---
CAMERA_X_LIMIT = 400 # Distância do centro da tela para começar a rolar (player fica fixo)

# --- Configurações de Inimigo ---
ENEMY_SPEED = 2
ENEMY_ANIMATION_SPEED = 10
ENEMY_COLLIDER_SIZE = (30, 30)

# Raio de AGGREGAÇÃO
AGGRO_RANGE = 300

# --- Mapeamento do Mundo (Expandido para 40 tiles de largura) ---
GAME_MAP = [
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'K', ' ', ' ', 'P', 'G', 'H', 'J', 'F', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    ['S', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '1', '3', ' ', '1', '2', '2', '2', '3', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    ['3', 'B', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '1', '2', '3', ' ', '4', '5', '5', '5', '6', 'B', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    ['5', '3', '$', '$', '$', '$', '$', '$', '$', ' ', '7', '8', '9', ' ', '4', '5', '5', '5', '5', '3', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    ['5', '6', 'P', '$', 'O', 'O', 'K', 'P', ' ', ' ', ' ', ' ', ' ', 'N', '4', '5', '5', '5', '5', '6', 'M', ' ', 'P', 'P', 'K', 'O', 'K', 'K', 'E', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
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

# --- Caminhos dos Assets de Decoração ---
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
     'shell_left': './asset/Palm Tree Island/objects/shell_left.png'

# Adicione aqui todos os seus objetos estáticos
}

# --- Mapeamento de Nível para Decoração (ADICIONE CÓDIGOS) ---
# Use códigos que não sejam usados para tiles (Ex: 'T' para árvore, 'B' para arbusto)
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
    'N': 'shell_left'
    # Adicione aqui todos os códigos que você usará no mapa
}
# --- Mapeamento de Nível para ITENS (Certifique-se que o helm não está aqui!) ---
ITEM_MAP_CODES = {
    '$': 'coin',

}
ENTITY_ASSET_PATHS = {
    # Inimigos
    'E': './asset/enemies/Fierce Tooth/idle/Idle 01.png', # Placeholder
    # Itens
    'I': './asset/items/Coin/Gold Coin/01.png', # Coin Placeholder
    # Armadilhas
    'T': './asset/trap/spike_ball/Spiked Ball.png', # Spike Trap
}

# --- Configurações de Áudio ---
AUDIO_PATHS = {
    'bg': './asset/audio/bg.mp3', # Substitua pelo seu caminho real
    'jump': './asset/audio/jump.wav',   # Substitua pelo seu caminho real
    'coin': './asset/audio/coin.wav',
}