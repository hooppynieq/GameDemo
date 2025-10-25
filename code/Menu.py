# Menu.py

import pygame as pg
from code.Const import SCREEN_SIZE, TITLE, WHITE, BLACK, FONT_NAME, FONT_SIZE


class Menu:
    def __init__(self, screen):
        self.screen = screen

        # Fontes
        pg.font.init()
        # Fonte principal para título/opções
        self.main_font = pg.font.SysFont(FONT_NAME, FONT_SIZE, bold=True)
        # Fonte menor para as instruções de controle
        self.small_font = pg.font.SysFont(FONT_NAME, FONT_SIZE // 2, bold=False)

        # Textos Principais
        self.title_text = self.main_font.render(TITLE, True,
                                                BLACK)  # Trocando para BLACK para melhor contraste no fundo WHITE
        self.start_text = self.main_font.render('Pressione ESPAÇO para Começar', True, BLACK)
        self.quit_text = self.main_font.render('Pressione ESC para Sair', True, BLACK)

        # NOVO: Textos de Controle
        self.controls_title_text = self.small_font.render("--- CONTROLES ---", True, BLACK)
        self.controls_move = self.small_font.render('Movimento: A (Esquerda) / D (Direita)', True, BLACK)
        self.controls_jump = self.small_font.render('Pular: ESPAÇO - Atacar: Z', True, BLACK)

        self.clock = pg.time.Clock()

    def draw(self):
        """Desenha os elementos do menu, incluindo as instruções de controle."""
        self.screen.fill(WHITE)  # Fundo branco para o menu
        center_x = SCREEN_SIZE[0] // 2
        center_y = SCREEN_SIZE[1] // 2

        # --- 1. Título do Jogo ---
        title_rect = self.title_text.get_rect(center=(center_x, center_y - 150))
        self.screen.blit(self.title_text, title_rect)

        # --- 2. Opções de Jogo ---
        start_rect = self.start_text.get_rect(center=(center_x, center_y))
        self.screen.blit(self.start_text, start_rect)

        quit_rect = self.quit_text.get_rect(center=(center_x, center_y + 70))
        self.screen.blit(self.quit_text, quit_rect)

        # --- 3. Instruções de Controle (Novas) ---
        control_y_start = center_y + 160
        line_spacing = self.small_font.get_height() + 5

        # Título dos Controles
        controls_title_rect = self.controls_title_text.get_rect(center=(center_x, control_y_start))
        self.screen.blit(self.controls_title_text, controls_title_rect)

        current_y = control_y_start + line_spacing

        # Instrução de Movimento
        move_rect = self.controls_move.get_rect(center=(center_x, current_y))
        self.screen.blit(self.controls_move, move_rect)

        current_y += line_spacing

        # Instrução de Pulo
        jump_rect = self.controls_jump.get_rect(center=(center_x, current_y))
        self.screen.blit(self.controls_jump, jump_rect)

        pg.display.update()

    def run(self, key_event_key=None):
        """Executa o loop do menu. Retorna o estado ('MENU', 'GAME' ou 'QUIT')."""

        self.draw()

        if key_event_key == pg.K_SPACE:
            return 'GAME'  # Inicia o jogo

        if key_event_key == pg.K_ESCAPE:
            return 'QUIT'  # Sai do jogo

        return 'MENU'