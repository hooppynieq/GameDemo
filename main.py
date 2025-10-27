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
    # O jogo é inicializado fora do loop para manter os assets carregados e o estado
    game = Game(screen)

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
            # Captura a tecla pressionada APENAS no evento KEYDOWN para o menu e ações pontuais no jogo
            if event.type == pg.KEYDOWN:
                key_event_key = event.key

        # Se o evento de QUIT foi detectado, saímos imediatamente
        if not running:
            break

        # 2. Transição e Execução de Estados
        next_state = current_state

        if current_state == 'MENU':
            # O menu lida com o input do teclado e retorna 'GAME' ou 'QUIT'
            next_state = menu.run(key_event_key)

            # Se o menu retorna 'GAME', preparamos o jogo para iniciar na próxima iteração
            if next_state == 'GAME':
                # Reinicia o nível (necessário após voltar do menu)
                game._start_new_level()

        elif current_state == 'GAME':
            # O jogo lida com o input e retorna 'GAME', 'MENU' (se perder/ganhar) ou 'QUIT'

            # Passa as teclas pressionadas (para movimento contínuo) e a tecla do evento (para ações)
            next_state = game.run(keys_pressed, key_event_key)

        # 3. Gerenciamento do Estado
        if next_state == 'QUIT':
            running = False
        elif next_state != current_state:
            current_state = next_state

    # Finalização do Pygame
    pg.quit()


if __name__ == '__main__':
    # Nota: Assumi que você tem a constante 'SCREEN_SIZE' e as classes 'Game' e 'Menu'
    # disponíveis para importação conforme o código.
    main()