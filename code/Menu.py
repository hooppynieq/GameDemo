# Menu.py

import pygame as pg
from code.Const import SCREEN_SIZE, TITLE, WHITE, BLACK, FONT_NAME, FONT_SIZE


class Menu:
    def __init__(self, screen):
        self.screen = screen
        self.font = pg.font.SysFont(FONT_NAME, FONT_SIZE, bold=True)
        self.title_text = self.font.render(TITLE, True, WHITE)
        self.start_text = self.font.render("Pressione ESPAÇO para Começar", True, BLACK)
        self.quit_text = self.font.render("Pressione ESC para Sair", True, BLACK)
        self.clock = pg.time.Clock()

    def draw(self):
        """Desenha os elementos do menu."""
        self.screen.fill(WHITE)  # Fundo branco para o menu

        # Centraliza o título
        title_rect = self.title_text.get_rect(center=(SCREEN_SIZE[0] // 2, SCREEN_SIZE[1] // 2 - 100))
        self.screen.blit(self.title_text, title_rect)

        # Centraliza as opções
        start_rect = self.start_text.get_rect(center=(SCREEN_SIZE[0] // 2, SCREEN_SIZE[1] // 2))
        self.screen.blit(self.start_text, start_rect)

        quit_rect = self.quit_text.get_rect(center=(SCREEN_SIZE[0] // 2, SCREEN_SIZE[1] // 2 + 70))
        self.screen.blit(self.quit_text, quit_rect)

        pg.display.update()

    def run(self, key_event_key=None):
        """Executa o loop do menu. Retorna o estado ('MENU', 'GAME' ou 'QUIT')."""

        self.draw()

        if key_event_key == pg.K_SPACE:
            return 'GAME'  # Inicia o jogo

        if key_event_key == pg.K_ESCAPE:
            return 'QUIT'  # Sai do jogo

        return 'MENU'