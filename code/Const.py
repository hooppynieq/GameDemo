# Const.py

# Dimensões da Tela
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 768
SCREEN_SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT)
TITLE = "Captain Clown Nose Game"
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

# Mapa (Apenas um bloco de dados)
GAME_MAP = [
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '1', '3', ' ', '1', '2', '2'],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '1', '2', '3', ' ', '7', '9', ' ', '4', '5', '5'],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '7', '8', '9', ' ', ' ', ' ', ' ', '4', '5', '5'],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '4', '5', '5'],
    ['2', '2', '2', '2', '2', '2', '2', '2', '2', '2', '2', '2', '2', '2', '2', '2', '2', '5', '5', '5']
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