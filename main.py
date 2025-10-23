# main.py

import pygame as pg

from code.Const import SCREEN_SIZE
from code.Game import Game
from code.Menu import Menu

# Inicialização global do Pygame
pg.init()
pg.font.init()


def main():
    """Função principal que gerencia o loop de estados do jogo."""

    # Configuração da tela
    screen = pg.display.set_mode(SCREEN_SIZE)

    # Instâncias de Menu e Game
    current_state = 'MENU'
    menu = Menu(screen)
    game = Game(screen)  # O jogo é inicializado fora do loop para manter os assets carregados

    running = True
    while running:

        # Variáveis de entrada resetadas a cada loop
        key_event_key = None
        mouse_input = pg.mouse.get_pressed()
        keys_pressed = pg.key.get_pressed()

        # 1. Tratamento de Eventos (Comum a todos os estados)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            if event.type == pg.KEYDOWN:
                key_event_key = event.key

        # 2. Transição de Estados
        next_state = current_state

        if current_state == 'MENU':
            next_state = menu.run(key_event_key)

        elif current_state == 'GAME':
            # O mouse_has_clicked do original foi removido/simplificado para manter o foco
            # na estrutura e lógica central do jogo

            # Passa as teclas pressionadas (para movimento contínuo) e a tecla do evento (para ações de pulo/escape)
            next_state = game.run(keys_pressed, key_event_key)

        if next_state == 'QUIT':
            running = False
        elif next_state != current_state:
            current_state = next_state

    # Finalização do Pygame
    pg.quit()


if __name__ == '__main__':
    main()