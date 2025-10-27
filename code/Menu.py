import pygame as pg
from code.Const import SCREEN_SIZE, TITLE, WHITE, BLACK, FONT_NAME, FONT_SIZE


class Menu:
    def __init__(self, screen):
        self.screen = screen
        self.screen_width = SCREEN_SIZE[0]
        self.screen_height = SCREEN_SIZE[1]

        # Fontes
        pg.font.init()
        self.main_font = pg.font.SysFont(FONT_NAME, FONT_SIZE, bold=True)
        self.small_font = pg.font.SysFont(FONT_NAME, FONT_SIZE // 2, bold=False)

        # VARIÁVEIS DE NAVEGAÇÃO DO MENU
        self.menu_options = ["COMEÇAR O JOGO", "SAIR"]
        self.selected_option_index = 0
        self.option_spacing = self.main_font.get_height() + 10

        # Textos PRÉ-RENDERIZADOS
        self.title_text = self.main_font.render(TITLE, True, BLACK)

        # Textos de Controle
        self.controls_title_text = self.small_font.render("--- CONTROLES ---", True, BLACK)
        self.controls_move = self.small_font.render('Movimento: A (Esquerda) / D (Direita)', True, BLACK)
        self.controls_jump = self.small_font.render('Pular: ESPAÇO - Atacar: Z', True, BLACK)

        self.clock = pg.time.Clock()

    def draw(self):
        """Desenha os elementos do menu, incluindo as opções selecionáveis."""
        self.screen.fill(WHITE)
        center_x = self.screen_width // 2
        center_y = self.screen_height // 2

        # 1. Título do Jogo
        title_rect = self.title_text.get_rect(center=(center_x, center_y - 150))
        self.screen.blit(self.title_text, title_rect)

        # 2. Opções Selecionáveis
        option_y_start = center_y

        for index, option_text in enumerate(self.menu_options):
            # Cor: Amarelo para selecionado, Preto para não selecionado.
            color = (255, 255, 0) if index == self.selected_option_index else BLACK

            option_surface = self.main_font.render(option_text, True, color)

            option_rect = option_surface.get_rect(center=(center_x, option_y_start))
            self.screen.blit(option_surface, option_rect)

            option_y_start += self.option_spacing

        # 3. Instruções de Controle
        control_y_start = center_y + 160
        line_spacing = self.small_font.get_height() + 5

        controls_title_rect = self.controls_title_text.get_rect(center=(center_x, control_y_start))
        self.screen.blit(self.controls_title_text, controls_title_rect)

        current_y = control_y_start + line_spacing

        move_rect = self.controls_move.get_rect(center=(center_x, current_y))
        self.screen.blit(self.controls_move, move_rect)

        current_y += line_spacing

        jump_rect = self.controls_jump.get_rect(center=(center_x, current_y))
        self.screen.blit(self.controls_jump, jump_rect)

        pg.display.update()

    def run(self, key_event_key=None):
        """Executa o loop do menu. Lida com a navegação por setas e seleção por ENTER."""

        # Lógica de Navegação e Seleção
        if key_event_key is not None:

            # Navegação para cima
            if key_event_key == pg.K_UP:
                self.selected_option_index = (self.selected_option_index - 1) % len(self.menu_options)

            # Navegação para baixo
            elif key_event_key == pg.K_DOWN:
                self.selected_option_index = (self.selected_option_index + 1) % len(self.menu_options)

            # Seleção com ENTER
            elif key_event_key == pg.K_RETURN:
                selected_text = self.menu_options[self.selected_option_index]

                if selected_text == "COMEÇAR O JOGO":
                    return 'GAME'

                elif selected_text == "SAIR":
                    return 'QUIT'

            # Permite ESC para sair
            elif key_event_key == pg.K_ESCAPE:
                return 'QUIT'

        self.draw()
        return 'MENU'