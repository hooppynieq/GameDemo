import pygame as pg

from code.Const import SCREEN_SIZE
from code.Game import Game
from code.Menu import Menu

pg.init()
pg.font.init()


def main():
    screen = pg.display.set_mode(SCREEN_SIZE)
    current_state = 'MENU'
    menu = Menu(screen)
    game = Game(screen)

    running = True
    while running:
        key_event_key = None
        keys_pressed = pg.key.get_pressed()

        # Tratamento de Eventos (QUIT e KeyDown)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            # Captura a tecla pressionada no evento para menus/ações de toque
            if event.type == pg.KEYDOWN:
                key_event_key = event.key

        if not running:
            break

        next_state = current_state

        # Máquina de Estados do Jogo
        if current_state == 'MENU':
            next_state = menu.run(key_event_key)
            # Ao iniciar o jogo pelo menu, garante que o nível seja carregado
            if next_state == 'GAME':
                game._start_new_level()
        elif current_state == 'GAME':
            # Passa teclas pressionadas e evento de tecla
            next_state = game.run(keys_pressed, key_event_key)

        # Transição de Estados
        if next_state == 'QUIT':
            running = False
        elif next_state != current_state:
            current_state = next_state

    pg.quit()


if __name__ == '__main__':
    main()